# syntax=docker/dockerfile:1
#
# Deployment image for the tinkoder-site admin GUI. Unlike a typical app
# image, this one does NOT bake in app/templates/static — SITE_ROOT
# (app/pages.py) is computed as `Path(__file__).resolve().parents[3]`,
# i.e. the app must physically live at <site-root>/_dev/admin/app/ for
# that math to work. So the runtime image only bakes the venv; the actual
# site repo (this repo, including _dev/admin/ itself) is bind-mounted at
# /site by docker-compose.yml, which is also what lets Publish commit/push
# against a real git working tree instead of a throwaway copy.
#
# git is installed in the runtime stage because app/git_ops.py shells out
# to the `git` binary for status/log/commit/push/checkout.

FROM python:3.12-slim AS builder

COPY --from=ghcr.io/astral-sh/uv:0.5.29 /uv /uvx /usr/local/bin/

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PROJECT_ENVIRONMENT=/venv

WORKDIR /build

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-install-project --no-dev

FROM python:3.12-slim AS runtime

RUN apt-get update \
    && apt-get install -y --no-install-recommends git \
    && rm -rf /var/lib/apt/lists/*

# This UID must match the owner of the site repo on whatever host runs
# this container (bind mounts preserve numeric ownership across the
# container boundary, and NFS/host filesystems commonly don't start
# numbering at 1000) — set via build arg, not hardcoded, since it's
# host-specific. A mismatched UID leaves the app able to read the site
# files but not write/commit to them.
ARG APP_UID=1000
RUN useradd --create-home --uid ${APP_UID} --shell /usr/sbin/nologin appuser

COPY --from=builder /venv /venv
ENV PATH="/venv/bin:$PATH" \
    PYTHONUNBUFFERED=1

# /site is where docker-compose.yml bind-mounts the real repo working
# tree. Nothing is copied here at build time — see the note above.
RUN mkdir -p /site && chown appuser:appuser /site
WORKDIR /site/_dev/admin

# GitHub's published SSH host keys, pinned here rather than trusted from
# a build-time `ssh-keyscan` — this is what makes StrictHostKeyChecking
# meaningful for the deploy key set up below (docker-compose.yml mounts
# the actual private key at /home/appuser/.ssh/deploy_key at runtime;
# it's a secret and never baked into the image).
RUN mkdir -p /home/appuser/.ssh && chmod 700 /home/appuser/.ssh \
    && { \
        echo 'github.com ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIOMqqnkVzrm0SdG6UOoqKLsabgH5C9okWi0dh2l9GKJl'; \
        echo 'github.com ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQCj7ndNxQowgcQnjshcLrqPEiiphnt+VTTvDP6mHBL9j1aNUkY4Ue1gvwnGLVlOhGeYrnZaMgRK6+PKCUXaDbC7qtbW8gIkhL7aGCsOr/C56SJMy/BCZfxd1nWzAOxSDPgVsmerOBYfNqltV9/hWCqBywINIR+5dIg6JTJ72pcEpEjcYgXkE2YEFXV1JHnsKgbLWNlhScqb2UmyRkQyytRLtL+38TGxkxCflmO+5Z8CSSNY7GidjMIZ7Q4zMjA2n1nGrlTDkzwDCsw+wqFPGQA179cnfGWOWRVruj16z6XyvxvjJwbz0wQZ75XK5tKSb7FNyeIEs4TT4jk+S4dhPeAUC5y+bDYirYgM4GC7uEnztnZyaVWQ7B381AK4Qdrwt51ZqExKbQpTUNn+EjqoTwvqNj4kqx5QUCI0ThS/YkOxJCXmPUWZbhjpCg56i+2aB6CmK2JGhn57K5mj0MNdBXA4/WnwH6XoPWJzK5Nyu2zB3nAZp+S5hpQs+p1vN1/wsjk='; \
        echo 'github.com ecdsa-sha2-nistp256 AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAIbmlzdHAyNTYAAABBBEmKSENjQEezOmxkZMy7opKgwFB9nkt5YRrYMjNuG5N87uRgg6CLrbo5wAdT/y6v0mKV0U2w0WZ2YB/++Tpockg='; \
    } > /home/appuser/.ssh/known_hosts \
    && printf 'Host github.com\n  IdentityFile /home/appuser/.ssh/deploy_key\n  IdentitiesOnly yes\n  StrictHostKeyChecking yes\n' > /home/appuser/.ssh/config \
    && chmod 600 /home/appuser/.ssh/known_hosts /home/appuser/.ssh/config \
    && chown -R appuser:appuser /home/appuser/.ssh

USER appuser

# git needs a global identity to author commits, and needs this exact
# mount path trusted (bind mounts commonly cross UID/ownership boundaries,
# which git's safe.directory check otherwise refuses).
RUN git config --global --add safe.directory /site \
    && git config --global user.name "Tinkoder Admin GUI" \
    && git config --global user.email "admin-gui@tinkoder.local" \
    && git config --global core.sshCommand "ssh -F /home/appuser/.ssh/config"

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
