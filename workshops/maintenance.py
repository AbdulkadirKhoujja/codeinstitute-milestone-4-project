"""Run idempotent maintenance inside an existing, awake web worker."""

import logging
from io import StringIO
from threading import Event, Thread

from django.core.management import call_command
from django.db import connections

logger = logging.getLogger("skillseat.maintenance")


def run_expiry(stop, interval=60, log=None):
    log = log or logger
    while not stop.is_set():
        output = StringIO()
        try:
            call_command("expire_bookings", stdout=output, stderr=output)
            log.info(
                "Scheduled hold expiry completed: %s", output.getvalue().strip().replace("\n", " ")
            )
        except Exception:
            # Retry on the next tick without leaking provider/connection details.
            log.error("Scheduled hold expiry failed; will retry on the next tick.")
        finally:
            # This thread has no Django request lifecycle to close its connections.
            connections.close_all()
        if stop.wait(interval):
            break


def start_expiry(worker):
    worker.hold_expiry_stop = Event()
    worker.hold_expiry_thread = Thread(
        target=run_expiry,
        args=(worker.hold_expiry_stop,),
        kwargs={"log": worker.log},
        name="skillseat-hold-expiry",
        daemon=True,
    )
    worker.hold_expiry_thread.start()


def stop_expiry(worker):
    if hasattr(worker, "hold_expiry_stop"):
        worker.hold_expiry_stop.set()
        worker.hold_expiry_thread.join(timeout=5)
