# Siteforge Forge on Cloudflare

This Worker replaces both Railway services without rewriting the proven Python
pipeline:

- `SiteforgeForgeContainer`: four named container instances polling the panel
  every 10 seconds and publishing atomic bundles to R2.
- `SiteforgeCronContainer`: one isolated instance that discovers prospects every
  five minutes and rejects overlapping runs.
- Worker Cron Triggers keep the forge instances available and start discovery.
- `/health` is public and contains no business or secret data.
- `/admin/status`, `/admin/wake`, and `/admin/discover` require
  `Authorization: Bearer <SITEFORGE_PUBLISH_KEY>`.

Secrets are Worker Secrets and must never be committed:

```sh
npx wrangler secret put GITHUB_TOKEN -c cloudflare-forge/wrangler.jsonc
npx wrangler secret put PANEL_KEY -c cloudflare-forge/wrangler.jsonc
npx wrangler secret put SITEFORGE_PUBLISH_KEY -c cloudflare-forge/wrangler.jsonc
```

Safe cutover sequence:

1. Deploy and add the three secrets.
2. Wake the four workers and validate `/admin/status`.
3. Run one discovery cycle and confirm the panel queue changes normally.
4. Pause Railway only after the Cloudflare containers are healthy.

Rollback is immediate: resume the two Railway services. The panel claim endpoint
is atomic, so a short overlap during cutover cannot build the same queue item twice.
