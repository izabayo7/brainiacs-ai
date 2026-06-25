# Deploying Brainiacs AI (StrangeCloud VM)

The stack is fully self-hosted: PostgreSQL + FastAPI (api) + Next.js (web) + Caddy
(auto-HTTPS reverse proxy), all via Docker Compose. No external LLM, no Google OAuth.

The api container self-bootstraps on start (`api/entrypoint.sh`): waits for the DB, runs
Alembic migrations, loads the course content if the DB is empty, then starts uvicorn.

---

## 1. One-time VM setup (do this once, manually)

On a fresh StrangeCloud VM (Ubuntu):

```bash
# Docker + compose plugin + git
curl -fsSL https://get.docker.com | sh
sudo apt-get install -y git
# (log out/in so your user is in the docker group, or use sudo)

# Clone the repo
git clone https://github.com/izabayo7/brainiacs-ai.git
cd brainiacs-ai

# Configure environment
cp .env.deploy.example .env
nano .env        # fill in domains + generate strong secrets (openssl rand -hex 32)

# Point DNS: two A records -> the VM's public IP
#   APP_DOMAIN  (e.g. brainiacs.example.com)
#   API_DOMAIN  (e.g. api.brainiacs.example.com)

# First launch (Caddy gets HTTPS certs automatically once DNS resolves)
docker compose up -d --build
docker compose logs -f api      # watch migrations + content load
```

Visit `https://APP_DOMAIN` — register an account (email/password) and you're in.

---

## 2. CI/CD — push-to-deploy (`.github/workflows/deploy.yml`)

Once the VM is running, every push / merged PR to `main` auto-redeploys it.

**a. Create a deploy SSH key (on your laptop):**
```bash
ssh-keygen -t ed25519 -f brainiacs_deploy -N ""      # makes brainiacs_deploy (private) + .pub
ssh-copy-id -i brainiacs_deploy.pub <user>@<vm-host> # add the PUBLIC key to the VM
```

**b. Add GitHub repo secrets** (Settings → Secrets and variables → Actions → New secret):

| Secret | Value |
|---|---|
| `DEPLOY_HOST` | the VM's host/IP (or `API_DOMAIN`) |
| `DEPLOY_USER` | the SSH username on the VM |
| `DEPLOY_SSH_KEY` | contents of the **private** key file `brainiacs_deploy` (paste the whole file) |
| `DEPLOY_PATH` | absolute path to the repo on the VM, e.g. `/home/<user>/brainiacs-ai` |
| `DEPLOY_PORT` | SSH port (optional — defaults to 22) |

> The private key only ever lives in your machine + the GitHub secret. Never commit it.

**c. That's it.** Push to `main` → the workflow SSHes in, `git reset --hard origin/main`,
`docker compose up -d --build`. Your real `.env` on the VM is gitignored, so deploys never
touch your secrets. Watch runs in the repo's **Actions** tab; trigger one manually with
**Run workflow** (workflow_dispatch).

> If the repo is private, give the VM git read access (a GitHub deploy key) so `git fetch` works.
