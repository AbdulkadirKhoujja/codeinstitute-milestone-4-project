"""Start maintenance only after Django is initialized in each forked worker."""


def post_worker_init(worker):
    from workshops.maintenance import start_expiry

    start_expiry(worker)


def worker_exit(server, worker):
    from workshops.maintenance import stop_expiry

    stop_expiry(worker)
