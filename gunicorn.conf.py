import multiprocessing
import os

# Basic dynamic settings with sane defaults
bind = os.getenv("GUNICORN_BIND", "0.0.0.0:5000")
workers = int(os.getenv("GUNICORN_WORKERS", (multiprocessing.cpu_count() * 2) + 1))
threads = int(os.getenv("GUNICORN_THREADS", "2"))
worker_class = os.getenv("GUNICORN_WORKER_CLASS", "sync")
keepalive = int(os.getenv("GUNICORN_KEEPALIVE", "30"))
accesslog = os.getenv("GUNICORN_ACCESSLOG", "-")  # '-' => stdout
errorlog = os.getenv("GUNICORN_ERRORLOG", "-")
loglevel = os.getenv("GUNICORN_LOG_LEVEL", "info")
proc_name = os.getenv("GUNICORN_PROC_NAME", "auth_service")
preload_app = os.getenv("GUNICORN_PRELOAD", "true").lower() == "true"
max_requests = int(os.getenv("GUNICORN_MAX_REQUESTS", "0")) or None
max_requests_jitter = int(os.getenv("GUNICORN_MAX_REQUESTS_JITTER", "0")) or 0

# Timeout configuration
# (allow overriding for slow startup if migrations/etc.)
timeout = int(os.getenv("GUNICORN_TIMEOUT", "30"))

# Graceful reload in dev (only if explicitly enabled)
reload = os.getenv("GUNICORN_RELOAD", "false").lower() == "true"

# Forwarded headers (if behind reverse proxy)
forwarded_allow_ips = os.getenv("GUNICORN_FORWARDED_ALLOW_IPS", "*")

# TLS (optional) — can be enabled if cert paths provided
keyfile = os.getenv("GUNICORN_KEYFILE") or None
certfile = os.getenv("GUNICORN_CERTFILE") or None

# Optional: health hook example

def when_ready(server):  # pragma: no cover - side-effect logging
    server.log.info("Gunicorn is ready. Workers: %s", len(server.WORKERS))


def post_fork(server, worker):  # pragma: no cover
    # Access server to avoid linter 'unused' complaint
    _ = server
    worker.log.info("Worker spawned (pid: %s)", worker.pid)


def pre_fork(server, worker):  # pragma: no cover
    # Access worker to avoid linter 'unused' complaint
    _ = worker
    server.log.debug("About to fork worker")


def worker_int(worker):  # pragma: no cover
    worker.log.warning("Worker received INT signal")


def worker_abort(worker):  # pragma: no cover
    worker.log.warning("Worker received SIGABRT signal")
