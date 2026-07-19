# Deployment Notes — Health Check & Infrastructure Fix

**Date:** March 3, 2026  
**Problem:** Site returning HTTP 429 via Cloudflare; GCP backend showing 0% healthy.

---

## Root Causes Identified

1. **No `/healthz` endpoint existed** — GCP health check probe had nothing to hit.
2. **`SECURE_SSL_REDIRECT = True` in prod settings** — Django was 301-redirecting the plain HTTP health check probes to HTTPS. GCP probes don't follow redirects, so they saw a 301 (not 200) and marked instances unhealthy.
3. **`RUNNING_IN_CLOUD_RUN=true` hardcoded in `entrypoint.sh`** — This flag was always set, even on Compute Engine VMs, potentially triggering wrong settings behavior.
4. **Cloudflare DNS pointing to Google Sites IPs** (`216.239.32.21/34.21/36.21/38.21`) instead of the actual Load Balancer or VM external IP.

---

## Changes Completed

### 1. Added `/healthz` health check endpoint
**File:** `mysite/urls.py`
- Added `healthz()` view returning `HTTP 200 "ok"` (plain text).
- Registered at two paths:
  - `/healthz` — for MIG/Compute Engine health checks (note: intercepted by Google Frontend on Cloud Run)
  - `/-/health` — alternative that works everywhere including Cloud Run

### 2. Disabled `SECURE_SSL_REDIRECT` in prod
**File:** `mysite/settings/prod.py`
- Changed `SECURE_SSL_REDIRECT = True` → `SECURE_SSL_REDIRECT = False`
- GCP health probes use plain HTTP on port 8080; they need a 200, not a 301 redirect.
- Cloudflare or the GCP LB enforces HTTPS for real user traffic anyway.

### 3. Smart environment detection in entrypoint
**File:** `entrypoint.sh`
- Replaced hardcoded `RUNNING_IN_CLOUD_RUN=true` with auto-detection using `$K_SERVICE` (set automatically by Cloud Run).
- On Compute Engine / MIG, `RUNNING_IN_CLOUD_RUN` is now correctly set to `false`.

### 4. Created systemd service + MIG startup script
**Files:** `deploy/gunicorn.service`, `deploy/startup-script.sh`
- `gunicorn.service` — systemd unit to run Gunicorn on port 8080, auto-restart on failure.
- `startup-script.sh` — instance template startup script that clones code, installs deps, runs migrations, and enables the systemd service.
- **Note:** `REPO_URL` in `startup-script.sh` needs to be updated to your actual repo URL.

### 5. Deployed to Cloud Run
- Two successful deploys to Cloud Run (revisions `00056-djf` and `00057-rpx`).
- Verified `/-/health` returns HTTP 200 on Cloud Run.
- Verified `/healthz` is intercepted by Google Frontend on Cloud Run (returns Google-branded 404) — this is expected and only affects Cloud Run, not MIG.

---

## What Still Needs To Be Done

### A. Fix Cloudflare DNS (CRITICAL)
Your Cloudflare DNS A records point to Google Sites IPs, not your origin:
```
Current (wrong):  216.239.32.21, 216.239.34.21, 216.239.36.21, 216.239.38.21
```
These need to point to your **Load Balancer's external IP** (or VM external IP if no LB).

**To find your LB IP:**
```bash
gcloud compute forwarding-rules list --format="table(name, IPAddress, target)"
```

**To find VM external IP (if no LB):**
```bash
gcloud compute instances list --format="table(name, EXTERNAL_IP)"
```

Update the Cloudflare A record for `zeddstudy.dev` to the correct IP.  
**While debugging:** Set Cloudflare proxy to **DNS-only** (grey cloud) to bypass Cloudflare caching/WAF.

### B. Wire startup script into MIG instance template
Update `REPO_URL` in `deploy/startup-script.sh`, then:
```bash
gcloud compute instance-templates create hunt-template \
  --metadata-from-file=startup-script=deploy/startup-script.sh \
  --machine-type=e2-small \
  --tags=http-server \
  --image-family=debian-12 \
  --image-project=debian-cloud \
  --region=us-west1

# Then update MIG to use the new template:
gcloud compute instance-groups managed set-instance-template YOUR_MIG_NAME \
  --template=hunt-template \
  --zone=us-west1-b

# Rolling restart to pick up new template:
gcloud compute instance-groups managed rolling-action restart YOUR_MIG_NAME \
  --zone=us-west1-b
```

### C. Verify health checks from inside a VM
SSH into a MIG instance and run:
```bash
# Check Gunicorn is listening
sudo ss -lntp | grep :8080

# Test health endpoint locally
curl -i http://localhost:8080/healthz

# Check systemd service
sudo systemctl status gunicorn

# View logs if something is wrong
sudo journalctl -u gunicorn -f
```

### D. ALLOWED_HOSTS consideration
If GCP health probes send requests with the VM's internal IP as the `Host` header, you may need to add it to `ALLOWED_HOSTS` in `mysite/settings/prod.py`. For debugging, you can temporarily use `"*"`.

### E. Decide Cloud Run vs MIG
You currently have both:
- **Cloud Run** — working, deployed, health check works via `/-/health`
- **MIG** — startup script and systemd service created but not yet wired in

If you're moving to MIG, the Cloud Run health check path (`/-/health`) is just a bonus. The MIG health check at `/healthz:8080` will work directly since there's no Google Frontend intercepting.

---

## Key Files Reference
| File | Purpose |
|---|---|
| `mysite/urls.py` | `/healthz` and `/-/health` endpoints |
| `mysite/settings/prod.py` | Prod settings (SSL redirect disabled) |
| `entrypoint.sh` | Docker/Cloud Run entrypoint |
| `deploy/gunicorn.service` | systemd unit for Gunicorn on VMs |
| `deploy/startup-script.sh` | MIG instance startup script |
| `cloud_build_deploy.sh` | Cloud Run build & deploy script |

## GCP Health Check Config (unchanged)
- Name: `hc-1`
- Protocol: HTTP, Port: 8080, Path: `/healthz`
- Interval: 10s, Timeout: 5s
- Healthy/Unhealthy threshold: 1
