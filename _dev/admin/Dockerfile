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

RUN useradd --create-home --uid 1000 --shell /usr/sbin/nologin appuser

COPY --from=builder /venv /venv
ENV PATH="/venv/bin:$PATH" \
    PYTHONUNBUFFERED=1

# /site is where docker-compose.yml bind-mounts the real repo working
# tree. Nothing is copied here at build time — see the note above.
RUN mkdir -p /site && chown appuser:appuser /site
WORKDIR /site/_dev/admin

USER appuser

# git needs a global identity to author commits, and needs this exact
# mount path trusted (bind mounts commonly cross UID/ownership boundaries,
# which git's safe.directory check otherwise refuses).
RUN git config --global --add safe.directory /site \
    && git config --global user.name "Tinkoder Admin GUI" \
    && git config --global user.email "admin-gui@tinkoder.local"

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
