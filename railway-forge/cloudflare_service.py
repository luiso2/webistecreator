#!/usr/bin/env python3
"""HTTP supervisor used by Cloudflare Containers.

The existing forge is intentionally kept as the source of truth.  A worker
container runs ``main.main`` in a supervised background thread, while the cron
container exposes a non-blocking ``/run`` endpoint for ``cron.main``.  The
Cloudflare Worker is the only public caller; this server never receives direct
Internet traffic.
"""
from __future__ import annotations

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import os
import threading
import time
import traceback

import cron as discovery_cron
import main as forge


ROLE = os.environ.get("FORGE_ROLE", "worker").strip().lower()
PORT = int(os.environ.get("PORT", "8080"))
STARTED_AT = time.time()

_state_lock = threading.Lock()
_cron_lock = threading.Lock()
_worker_thread: threading.Thread | None = None
_cron_thread: threading.Thread | None = None
_state = {
    "worker_restarts": 0,
    "last_worker_error": None,
    "last_cron_started_at": None,
    "last_cron_finished_at": None,
    "last_cron_exit_code": None,
    "last_cron_error": None,
}


def _utc_timestamp() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def _run_worker_forever() -> None:
    while True:
        try:
            forge.main()
        except BaseException as exc:  # keep the container useful after a worker crash
            with _state_lock:
                _state["worker_restarts"] += 1
                _state["last_worker_error"] = f"{type(exc).__name__}: {exc}"[:300]
            print(json.dumps({
                "event": "forge_worker_crash",
                "error": _state["last_worker_error"],
                "trace": traceback.format_exc()[-1500:],
            }), flush=True)
            time.sleep(5)


def _start_worker() -> None:
    global _worker_thread
    if ROLE != "worker" or (_worker_thread and _worker_thread.is_alive()):
        return
    _worker_thread = threading.Thread(
        target=_run_worker_forever,
        name="siteforge-worker",
        daemon=True,
    )
    _worker_thread.start()


def _run_cron() -> None:
    with _cron_lock:
        with _state_lock:
            _state["last_cron_started_at"] = _utc_timestamp()
            _state["last_cron_error"] = None
        exit_code = 1
        try:
            exit_code = int(discovery_cron.main())
        except BaseException as exc:
            with _state_lock:
                _state["last_cron_error"] = f"{type(exc).__name__}: {exc}"[:300]
            print(json.dumps({
                "event": "discovery_cron_crash",
                "error": _state["last_cron_error"],
                "trace": traceback.format_exc()[-1500:],
            }), flush=True)
        finally:
            with _state_lock:
                _state["last_cron_exit_code"] = exit_code
                _state["last_cron_finished_at"] = _utc_timestamp()


def start_cron() -> bool:
    """Start one discovery run and reject overlapping invocations."""
    global _cron_thread
    if ROLE != "cron" or _cron_lock.locked() or (_cron_thread and _cron_thread.is_alive()):
        return False
    _cron_thread = threading.Thread(target=_run_cron, name="siteforge-cron", daemon=True)
    _cron_thread.start()
    return True


def health_snapshot() -> dict:
    with _state_lock:
        snapshot = dict(_state)
    return {
        "ok": True,
        "runtime": "cloudflare-container",
        "role": ROLE,
        "uptime_seconds": int(time.time() - STARTED_AT),
        "worker_alive": bool(_worker_thread and _worker_thread.is_alive()),
        "cron_running": _cron_lock.locked() or bool(_cron_thread and _cron_thread.is_alive()),
        **snapshot,
    }


class Handler(BaseHTTPRequestHandler):
    server_version = "siteforge-cloudflare/1"

    def _json(self, status: int, payload: dict) -> None:
        body = json.dumps(payload, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:  # noqa: N802 - BaseHTTPRequestHandler API
        if self.path.rstrip("/") in {"", "/health"}:
            self._json(200, health_snapshot())
            return
        self._json(404, {"ok": False, "error": "not_found"})

    def do_POST(self) -> None:  # noqa: N802 - BaseHTTPRequestHandler API
        path = self.path.rstrip("/")
        if path == "/wake":
            _start_worker()
            self._json(200, health_snapshot())
            return
        if path == "/run" and ROLE == "cron":
            accepted = start_cron()
            self._json(202 if accepted else 409, {
                **health_snapshot(),
                "accepted": accepted,
                "reason": None if accepted else "cron_already_running",
            })
            return
        self._json(404, {"ok": False, "error": "not_found"})

    def log_message(self, format_string: str, *args: object) -> None:
        print(json.dumps({
            "event": "container_http",
            "role": ROLE,
            "message": format_string % args,
        }), flush=True)


def serve() -> None:
    _start_worker()
    print(json.dumps({
        "event": "cloudflare_container_ready",
        "role": ROLE,
        "port": PORT,
    }), flush=True)
    ThreadingHTTPServer(("0.0.0.0", PORT), Handler).serve_forever()


if __name__ == "__main__":
    serve()
