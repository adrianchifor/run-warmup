import os
import sys
import logging
import requestsgcp

from threading import Thread
from flask import Flask

PATH = os.getenv("PATH", "/")
TIMEOUT = int(os.getenv("TIMEOUT", 30))
SERVICES = [value for (key, value) in os.environ.items() if "_URL" in key]
if len(SERVICES) == 0:
    print("No services found. Use '<SERVICE NAME>_URL = <SERVICE URL>' env var syntax")
    sys.exit(1)

app = Flask(__name__)


@app.before_first_request
def setup_logging():
    gunicorn_logger = logging.getLogger("gunicorn.error")
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)


@app.route("/", methods=["POST"])
def handler():
    threads = []
    for service in SERVICES:
        t = Thread(target=http_get_service, args=(service,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    return "OK", 200


def http_get_service(url: str):
    try:
        r = requestsgcp.get(f"{url}{PATH}", timeout=TIMEOUT)
        app.logger.info(f"GET {url}{PATH}: response code {r.status_code}")
    except Exception as e:
        app.logger.error(f"GET {url}{PATH}: error {e}")
