# Phase 2 - Docker and Containers (Days 13-18)

**Goal:** understand what a container really is, build small and secure images, run
multi-container apps with Compose, and push images to a registry.

**Setup:** Docker Engine on Ubuntu (`curl -fsSL https://get.docker.com | sh`, then
`sudo usermod -aG docker $USER`) or Docker Desktop with WSL2.

---

## Day-by-day plan

### Day 13 - Containers vs VMs, running containers
- **Learn:** container = isolated process using Linux namespaces + cgroups, sharing the host kernel. Image vs container, registries, layers.
- **Do:** `docker run`, `ps`, `logs`, `exec -it`, `stop`, `rm`, `images`, `pull`, `inspect`, flags `-d -p -e --name --rm`.
- **Lab:** run `nginx`, publish port 8080, `exec` into it and edit the page, then show the change is lost when the container is recreated (this motivates volumes).
- **Done when:** you can explain to a non-technical friend why a container is not a VM.
- **Server link:** compare containers with VMs: a full OS per VM vs a shared kernel, density and isolation trade-offs.

### Day 14 - Images and Dockerfiles
- **Learn:** `FROM`, `RUN`, `COPY`, `WORKDIR`, `ENV`, `EXPOSE`, `CMD` vs `ENTRYPOINT`, layers and the build cache, `.dockerignore`.
- **Lab:** write a Dockerfile for the Phase 1 `log_analyzer.py`. Build it, run it with a mounted log file, rebuild after a tiny code change and watch the cache.
- **Done when:** you can predict which layers rebuild after a change.

### Day 15 - Optimise and secure images
- **Learn:** multi-stage builds, slim/alpine bases, non-root users, pinning versions, no secrets in images, vulnerability scanning (Trivy).
- **Lab:** open `labs/bad.Dockerfile` and list every problem. Then read `app/Dockerfile`. Compare image sizes with `docker images`. Scan both with `trivy image`.
- **Done when:** your list matches the answers below.

### Day 16 - Volumes and networking
- **Learn:** bind mounts vs named volumes, data persistence, bridge networks, container DNS by name, port publishing.
- **Lab:** run Redis with a named volume, write a key, delete the container, start a new one with the same volume, read the key. Then create a user-defined network and `ping` one container from another by name.
- **Done when:** you can explain why `localhost` inside a container is not your laptop.

### Day 17 - Docker Compose
- **Learn:** services, networks, volumes, `depends_on` with health checks, environment variables, `.env` files, profiles.
- **Lab:** read `docker-compose.yml` fully. Run `docker compose up --build`, open http://localhost:8080 repeatedly and watch the counter. `docker compose down` then `up` again: does the count survive? Why?
- **Done when:** you understand why Redis is on a separate `backend` network.

### Day 18 - Registries + capstone: three-tier app
- **Learn:** tagging, `docker login`, pushing to GHCR / Docker Hub / ACR / ECR, image tags that are immutable (commit SHA) vs `latest`.
- **Lab:** tag and push `app` to `ghcr.io/<you>/visit-counter:v1`. Add a second app replica behind nginx and prove load balancing (the `host` field changes). Break Redis on purpose and observe `/ready` and the 503.
- **Capstone deliverable:** this repo with a working Compose stack, a README with a diagram, and CI green.

---

## Answers: what is wrong with `labs/bad.Dockerfile`?
1. `ubuntu:latest` is unpinned and large; use a pinned slim image.
2. Separate `RUN apt-get update` and `install` layers: stale cache bug, and no `--no-install-recommends` or cleanup.
3. Installs `vim` and `git` that production never needs (bigger, more attack surface).
4. `COPY . /app` before installing dependencies: any code change invalidates the dependency layer.
5. Dependencies not pinned or listed in `requirements.txt`.
6. Secret (`SECRET_KEY`) baked into the image, visible in `docker history`.
7. Exposes port 22 (SSH is not needed in a container).
8. Runs as root.
9. Shell-form `CMD` (no signal handling) and runs the Flask dev server instead of gunicorn.
10. No `HEALTHCHECK`, no `.dockerignore`.

## Cheat sheet
```bash
docker ps -a                     # containers (running and stopped)
docker logs -f <name>            # follow logs
docker exec -it <name> sh        # shell inside
docker inspect <name>            # everything about it (IP, mounts, env)
docker stats                     # live CPU / memory
docker system df                 # disk used by images, containers, volumes
docker system prune              # clean up (careful)
docker compose up -d --build     # start the stack
docker compose logs -f app       # logs for one service
docker compose ps                # service health
```

## Troubleshooting checklist
- Container exits immediately: `docker logs`, check `CMD`, run with `-it ... sh` to explore.
- Cannot reach the app: right port published (`-p host:container`)? app listening on `0.0.0.0` and not `127.0.0.1`?
- "Connection refused" between containers: same network? using service name, not `localhost`?
- Image is huge: multi-stage build, slim base, `.dockerignore`, fewer layers that add files.

## Check yourself
1. Namespaces vs cgroups: what does each do?
2. `CMD` vs `ENTRYPOINT`?
3. Why copy `requirements.txt` before the rest of the code?
4. Bind mount vs named volume: when do you use which?
5. What does `depends_on` guarantee and what does it not?
6. How do containers on the same Compose network find each other?
7. Why is running as root in a container still risky?
