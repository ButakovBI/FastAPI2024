FROM python:3.12-slim

RUN mkdir /fastapi_app

WORKDIR /fastapi_app

COPY requirements.txt .

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev \
    && useradd -m appuser \
    && pip install --no-cache-dir -r requirements.txt; \
    rm -rf /var/lib/apt/lists/*;  \
    chmod 755 /usr/bin/chsh; \
    chmod 755 /usr/bin/gpasswd; \
    chmod 755 /usr/bin/su; \
    chmod 755 /usr/bin/newgrp; \
    chmod 755 /usr/bin/umount; \
    chmod 755 /usr/bin/passwd; \
    chmod 755 /usr/sbin/unix_chkpwd; \
    chmod 755 /usr/bin/chfn; \
    chmod 755 /usr/bin/expiry; \
    chmod 755 /usr/bin/chage; \
    chmod 755 /usr/bin/mount

COPY . .

RUN chmod a+x docker/*.sh && chown -R appuser:appuser /fastapi_app

USER appuser

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s \
  CMD curl --fail http://localhost:8000/health || exit 1
