# Recovery Checklist — Getting zeddstudy.dev Back Up

Living doc. Check things off, add notes, reorder as you learn more. Superseded facts from `DEPLOYMENT_NOTES.md` are called out below rather than deleted from that file — leaving it as historical record.

## RESOLVED (2026-07-19)

Site is back up — `curl -I https://zeddstudy.dev/-/health` and `/` both return `200`.

Two stacked issues, fixed in order:
1. **Billing** — instead of waiting on the Google Billing Support case, the user opened a brand-new billing account (`01F077-DBAE8D-961DBA`, "Portfolio Site") and it was linked directly to the project: `gcloud beta billing projects link portfoliosite-468605 --billing-account=01F077-DBAE8D-961DBA`. `billingEnabled` flipped to `true` immediately.
2. **Cloud SQL password mismatch (newly surfaced, unrelated to billing)** — once billing was fixed, requests started failing with a *different* error: `password authentication failed for user "gun_sounds_user"`. The `db-password` Secret Manager secret had a version 4 (created 2026-07-18, during the outage) whose value didn't even meet Cloud SQL's password complexity rules — it was corrupted/invalid. Fixed by generating a new strong password, setting it directly on the `gun_sounds_user` Cloud SQL user, and pushing it as secret version 5 so `latest` (which Cloud Run's `DB_PASSWORD` env var already pointed to) is valid and in sync again.
3. Cleaned up: deleted the old, separately-broken `gun-sounds` Cloud Run service (superseded by `gun-sounds-app`, which is what traffic actually routes to).

Old root-cause section below is kept for historical record.

## ROOT CAUSE FOUND (2026-07-16)

**The billing account behind `portfoliosite-468605` is closed.** Confirmed via:
```
gcloud beta billing projects describe portfoliosite-468605
  → billingEnabled: false

gcloud beta billing accounts describe 01F280-8444E5-D5B572
  → open: false
```
Cloud Run logs for `gun-sounds-app` show the actual error on every cold start:
```
ERROR  The request failed because billing is disabled for this project.
```
This is why requests intermittently "worked" (INFO-only log lines) and other times failed — Cloud Run was serving from a still-warm instance when it worked, and hitting the billing check on cold starts/autoscaling events, which fail outright.

**Everything else investigated below (Cloudflare DNS, SSL/TLS mode, Cloud Run service health, domain mapping) is confirmed correctly configured and was never the problem.** Don't re-investigate those unless this fix doesn't resolve it.

- [x] **Add a valid payment method.** Done — new primary card added to `01F280-8444E5-D5B572`.
- [x] **Check for an unpaid balance blocking reopen.** Checked via Transactions page — current balance is **$0.00** (May's $38.62 balance was successfully charged June 1, 2026). Not a money-owed problem. One anomaly noted: balance grew instead of clearing between March ($52.37) and April ($160.57) 2026, suggesting a declined charge attempt around then — resolved by June regardless, not worth chasing further unless support asks.
- [ ] **"Reopen billing account" button still not appearing** on Account Management page, despite: $0 balance, valid card attached, account type `Direct` (self-serve, not invoiced), and admin permissions confirmed (Billing Account Administrator role visible). Self-service is exhausted — this needs a Google Billing Support case.
- [ ] **Open a Billing Support case**: [console.cloud.google.com/support](https://console.cloud.google.com/support) → select project `portfoliosite-468605` → **Billing support** → live chat or phone → Create case. Free for all users regardless of support plan; needs Project Owner/Editor on the project (should already have this as account owner). Mention: billing account `01F280-8444E5-D5B572` closed, $0 balance, valid payment method attached, Reopen option never appears.
- [ ] **Confirm it's linked back to the project**: `gcloud beta billing projects describe portfoliosite-468605` should show `billingEnabled: true`.
- [ ] **Re-test**: `curl -I https://zeddstudy.dev/-/health` should return `200`.

## How we got there (verified 2026-07-16)

- [x] **Local dev** — works. `./dev.sh` serves the app at `http://127.0.0.1:8000/` via SQLite, no issues.
- [x] **GCP access** — personal account `ellifian@gmail.com` authenticated via `gcloud auth login`, confirmed access to `portfoliosite-468605`.
- [x] **Cloud Run service `gun-sounds-app`** — deployment-level config is healthy (`Ready=True` since 2026-03-03). Real-time requests fail due to billing, not this.
- [x] **Domain mapping** — `zeddstudy.dev` → `gun-sounds-app`, `Ready=True`, `CertificateProvisioned=True`, `DomainRoutable=True`. Confirmed fine.
- [x] **Cloudflare DNS records** — all 4 A + 4 AAAA records match exactly what Google's domain mapping requires (`216.239.32/34/36/38.21` etc). Confirmed fine via Cloudflare API.
- [x] **Cloudflare SSL/TLS mode** — `full`. Confirmed fine via Cloudflare API (this was the earlier top suspect — ruled out).
- [x] **Bypassed Cloudflare entirely** (`curl --resolve zeddstudy.dev:443:216.239.32.21 ...`) and still got errors straight from Google's frontend (500 on `/-/health`, 503 on `/`) — this is what proved the problem was on Google's side, not Cloudflare's, and led to checking Cloud Run logs → billing error.

**Correction to `DEPLOYMENT_NOTES.md`:** the March notes called the `216.239.x.x` DNS records "wrong Google Sites IPs." They're actually correct/required for a Cloud Run domain mapping — don't repoint DNS away from them.

## Other loose ends (not urgent — billing is the blocker)

- [x] **Uncommitted edit in `cloud_build_deploy.sh`**: `SERVICE_NAME` changed `gun-sounds` → `gun-sounds-app`. Matches reality (that's the correct/current service) — committed 2026-07-19.
- [x] **Old `gun-sounds` Cloud Run service** (pre-rename) is separately broken — "container failed to start" — but isn't what traffic routes to. Deleted 2026-07-19.
- [ ] **Decide Cloud Run vs MIG, for real.** Compute Engine has never been enabled on `portfoliosite-468605`, so the MIG path (`deploy/gunicorn.service`, `deploy/startup-script.sh`) was never actually provisioned. Recommend shelving it.
- [ ] **Cloudflare API token**: `CLOUDFLARE_API_TOKEN` now lives in `~/.bashrc` (above the interactive-shell guard, so non-interactive shells/scripts can `source` it). Scoped to the zeddstudy.dev zone only.
- [ ] **The abandoned Billing Support case** — never opened, since the user linked a new billing account instead. The old closed billing account (`01F280-8444E5-D5B572`) and its case are now moot; nothing to follow up on unless the new account also has issues.
- [ ] Consider archiving/annotating `DEPLOYMENT_NOTES.md` — its Cloudflare DNS diagnosis (March 2026) was wrong and already corrected in this file; worth a pointer note rather than leaving it as the only place someone looks first.

## Priority order

All resolved as of 2026-07-19 — see "RESOLVED" section at the top. Remaining items above are non-urgent cleanup.

## Notes
-
