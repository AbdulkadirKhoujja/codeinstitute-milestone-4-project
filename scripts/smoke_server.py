"""Start Django or the Linux release WSGI server and verify a real HTTP response."""

import os
import socket
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request
from pathlib import Path


def main():
    if os.environ.get("DJANGO_ENV") != "development":
        raise SystemExit("Smoke testing requires explicit DJANGO_ENV=development.")
    root = Path(__file__).resolve().parent.parent
    with socket.socket() as listener:
        listener.bind(("127.0.0.1", 0))
        port = listener.getsockname()[1]
    with tempfile.TemporaryFile(mode="w+b") as log:
        command = [sys.executable, "manage.py", "runserver", f"127.0.0.1:{port}", "--noreload"]
        if "--gunicorn" in sys.argv:
            command = [
                sys.executable,
                "-m",
                "gunicorn",
                "config.wsgi:application",
                "--bind",
                f"127.0.0.1:{port}",
                "--workers",
                "2",
                "--threads",
                "2",
                "--timeout",
                "30",
            ]
        server = subprocess.Popen(
            command,
            cwd=root,
            stdout=log,
            stderr=subprocess.STDOUT,
            creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0,
        )
        try:
            deadline = time.monotonic() + 20
            # Loopback must not be routed through a configured external HTTP proxy.
            opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
            while time.monotonic() < deadline and server.poll() is None:
                try:
                    with opener.open(f"http://127.0.0.1:{port}/", timeout=2) as response:
                        body = response.read().decode("utf-8")
                        if response.status != 200 or "<h1>SkillSeat</h1>" not in body:
                            raise RuntimeError("Unexpected development server response.")
                        print("Real server smoke check: HTTP 200, SkillSeat home verified.")
                        return
                except urllib.error.URLError:
                    time.sleep(0.1)
            log.seek(0)
            raise RuntimeError(
                "Development server did not become ready:\n"
                + log.read().decode("utf-8", errors="replace")
            )
        finally:
            server.terminate()
            try:
                server.wait(timeout=5)
            except subprocess.TimeoutExpired:
                server.kill()
                server.wait(timeout=5)


if __name__ == "__main__":
    main()
