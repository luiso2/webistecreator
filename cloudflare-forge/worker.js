import { Container, getContainer } from "@cloudflare/containers";
import { env } from "cloudflare:workers";

const FORGE_INSTANCE_COUNT = 4;
const CONTAINER_ORIGIN = "http://container";

function containerEnv(role) {
  return {
    FORGE_ROLE: role,
    FORGE_RUNTIME: "cloudflare-container",
    PANEL_URL: env.PANEL_URL,
    DEMOS_URL: env.DEMOS_URL,
    GH_REPO: env.GH_REPO,
    GITHUB_TOKEN: env.GITHUB_TOKEN,
    PANEL_KEY: env.PANEL_KEY,
    SITEFORGE_PUBLISH_KEY: env.SITEFORGE_PUBLISH_KEY,
    GITHUB_BACKUP_ENABLED: "false",
    POLL_SECONDS: env.POLL_SECONDS,
    FORGE_DEADLINE_SECONDS: env.FORGE_DEADLINE_SECONDS,
    DISCOVERY_BUILD_WORKERS: env.DISCOVERY_BUILD_WORKERS,
    DISCOVERY_TARGET: env.DISCOVERY_TARGET,
    DISCOVERY_CANDIDATES: env.DISCOVERY_CANDIDATES,
    CRON_MAX_BUILDS: env.CRON_MAX_BUILDS,
    DISCOVERY_ROTATION_MINUTES: env.DISCOVERY_ROTATION_MINUTES,
    DISCOVERY_QUERIES: env.DISCOVERY_QUERIES,
  };
}

export class SiteforgeForgeContainer extends Container {
  defaultPort = 8080;
  requiredPorts = [8080];
  sleepAfter = "10m";
  enableInternet = true;
  entrypoint = ["python3", "cloudflare_service.py"];
  pingEndpoint = "http://localhost:8080/health";
  envVars = containerEnv("worker");

  onStart() {
    console.log(JSON.stringify({ event: "forge_container_started", instance: this.ctx.id.toString() }));
  }

  onError(error) {
    console.error(JSON.stringify({ event: "forge_container_error", error: String(error) }));
  }
}

export class SiteforgeCronContainer extends Container {
  defaultPort = 8080;
  requiredPorts = [8080];
  sleepAfter = "2m";
  enableInternet = true;
  entrypoint = ["python3", "cloudflare_service.py"];
  pingEndpoint = "http://localhost:8080/health";
  envVars = containerEnv("cron");

  onStart() {
    console.log(JSON.stringify({ event: "cron_container_started", instance: this.ctx.id.toString() }));
  }

  onError(error) {
    console.error(JSON.stringify({ event: "cron_container_error", error: String(error) }));
  }
}

function json(payload, status = 200) {
  return Response.json(payload, {
    status,
    headers: { "Cache-Control": "no-store" },
  });
}

async function secretsMatch(received, expected) {
  if (!received || !expected) return false;
  const encoder = new TextEncoder();
  const [left, right] = await Promise.all([
    crypto.subtle.digest("SHA-256", encoder.encode(received)),
    crypto.subtle.digest("SHA-256", encoder.encode(expected)),
  ]);
  const a = new Uint8Array(left);
  const b = new Uint8Array(right);
  let difference = a.length ^ b.length;
  for (let index = 0; index < Math.max(a.length, b.length); index += 1) {
    difference |= (a[index] ?? 0) ^ (b[index] ?? 0);
  }
  return difference === 0;
}

async function authorized(request, workerEnv) {
  const authorization = request.headers.get("Authorization") || "";
  const bearer = authorization.startsWith("Bearer ") ? authorization.slice(7) : "";
  const legacy = request.headers.get("x-siteforge-key") || "";
  return secretsMatch(bearer || legacy, workerEnv.SITEFORGE_PUBLISH_KEY);
}

async function callContainer(namespace, name, path, method = "GET") {
  const container = getContainer(namespace, name);
  const startedAt = Date.now();
  try {
    const response = await container.fetch(new Request(`${CONTAINER_ORIGIN}${path}`, { method }));
    const body = await response.json().catch(() => ({ ok: false, error: "invalid_container_response" }));
    return {
      name,
      status: response.status,
      duration_ms: Date.now() - startedAt,
      ...body,
    };
  } catch (error) {
    console.error(JSON.stringify({ event: "container_call_failed", name, path, error: String(error) }));
    return {
      ok: false,
      name,
      status: 503,
      duration_ms: Date.now() - startedAt,
      error: String(error),
    };
  }
}

async function wakeForge(workerEnv) {
  const results = await Promise.all(
    Array.from({ length: FORGE_INSTANCE_COUNT }, (_, index) =>
      callContainer(workerEnv.FORGE_CONTAINERS, `forge-${index}`, "/wake", "POST"),
    ),
  );
  console.log(JSON.stringify({ event: "forge_wake", healthy: results.filter((item) => item.ok).length }));
  return results;
}

async function runDiscovery(workerEnv) {
  const result = await callContainer(workerEnv.CRON_CONTAINER, "discovery", "/run", "POST");
  console.log(JSON.stringify({ event: "discovery_trigger", result }));
  return result;
}

export default {
  async fetch(request, workerEnv) {
    const url = new URL(request.url);
    if (request.method === "GET" && url.pathname === "/health") {
      return json({
        ok: true,
        runtime: "cloudflare",
        forge_instances: FORGE_INSTANCE_COUNT,
        discovery_schedule: "*/5 * * * *",
      });
    }

    if (url.pathname.startsWith("/admin/") && !(await authorized(request, workerEnv))) {
      return json({ ok: false, error: "unauthorized" }, 401);
    }

    if (request.method === "POST" && url.pathname === "/admin/wake") {
      const results = await wakeForge(workerEnv);
      return json({ ok: results.some((item) => item.ok), results }, results.some((item) => item.ok) ? 200 : 503);
    }

    if (request.method === "GET" && url.pathname === "/admin/status") {
      const workers = await Promise.all(
        Array.from({ length: FORGE_INSTANCE_COUNT }, (_, index) =>
          callContainer(workerEnv.FORGE_CONTAINERS, `forge-${index}`, "/health"),
        ),
      );
      const cron = await callContainer(workerEnv.CRON_CONTAINER, "discovery", "/health");
      return json({ ok: workers.every((item) => item.ok) && cron.ok, workers, cron });
    }

    if (request.method === "POST" && url.pathname === "/admin/discover") {
      const result = await runDiscovery(workerEnv);
      return json({ ok: result.status === 202 || result.status === 409, result }, result.status === 202 || result.status === 409 ? 202 : 503);
    }

    return json({ ok: false, error: "not_found" }, 404);
  },

  async scheduled(controller, workerEnv, ctx) {
    if (controller.cron === "*/5 * * * *") {
      ctx.waitUntil(runDiscovery(workerEnv));
      return;
    }
    ctx.waitUntil(wakeForge(workerEnv));
  },
};
