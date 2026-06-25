# Deploying Brainiacs AI (StrangeCloud VM, nginx)

Self-hosted stack: PostgreSQL + FastAPI (`api`) + Next.js (`web`) in Docker Compose,
behind **host nginx** which terminates TLS and reverse-proxies the two domains. No
external LLM, no Google OAuth.

- `web` listens on `127.0.0.1:3000`, `api` on `127.0.0.1:8000` (reachable only via nginx).
- nginx: `APP_DOMAIN -> :3000`, `API_DOMAIN -> :8000` (config in `deploy/nginx/`).
- The api container self-bootstraps on start (`api/entrypoint.sh`): waits for the DB, runs
  Alembic migrations, loads course content if the DB is empty, then starts uvicorn.

---

## 1. One-time VM setup

Docker + nginx are already installed. As the deploy user (must be in the `docker` group):

```bash
# Clone to the path you set in the DEPLOY_PATH secret
sudo mkdir -p /app && sudo chown "$USER" /app
git clone https://github.com/izabayo7/brainiacs-ai.git /app/brainiacs-ai
cd /app/brainiacs-ai

# Environment
cp .env.deploy.example .env
echo "DB_PASSWORD=$(openssl rand -hex 16)"
echo "JWT_SECRET=$(openssl rand -hex 32)"
echo "NEXTAUTH_SECRET=$(openssl rand -hex 32)"
nano .env        # paste those 3 secrets; set APP_URL + API_URL to your https domains

# DNS: two A records -> the VM's public IP (run `curl -s ifconfig.me` to get it)
#   APP_DOMAIN  e.g. brainiacs.example.com
#   API_DOMAIN  e.g. api.brainiacs.example.com

# Bring up the app containers (db + api + web)
docker compose up -d --build
docker compose logs -f          # watch migrations + content load
```

### nginx + HTTPS
```bash
# Edit the domains in the config, then install it
sed -e 's/APP_DOMAIN/brainiacs.example.com/' -e 's/API_DOMAIN/api.brainiacs.example.com/' \
    deploy/nginx/brainiacs.conf.example | sudo tee /etc/nginx/sites-available/brainiacs
sudo ln -sf /etc/nginx/sites-available/brainiacs /etc/nginx/sites-enabled/brainiacs
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t && sudo systemctl reload nginx

# HTTPS certificates (Let's Encrypt) — needs DNS to already resolve to the VM
sudo apt-get install -y certbot python3-certbot-nginx
sudo certbot --nginx -d brainiacs.example.com -d api.brainiacs.example.com
```

Visit `https://APP_DOMAIN`, register an email/password account — done.

---

## 2. CI/CD — push-to-deploy (`.github/workflows/deploy.yml`)

Already wired. On every push / merged PR to `main`, the workflow SSHes into the VM and:
`cd $DEPLOY_PATH && git reset --hard origin/main && docker compose up -d --build`.
The api entrypoint re-runs migrations; nginx is unaffected (it just proxies the containers).

GitHub repo secrets it uses (Settings → Secrets and variables → Actions):

| Secret | Value |
|---|---|
| `DEPLOY_HOST` | VM host/IP |
| `DEPLOY_USER` | SSH user (in the `docker` group, owns `/app/brainiacs-ai`) |
| `DEPLOY_SSH_KEY` | the **private** deploy key |
| `DEPLOY_PATH` | `/app/brainiacs-ai` |
| `DEPLOY_PORT` | SSH port (optional, defaults 22) |

Trigger a run manually from the **Actions** tab (**Run workflow**). Your real `.env` is
gitignored, so deploys never overwrite it. If the repo is private, give the VM git read
access (a GitHub deploy key) so `git fetch` works.
