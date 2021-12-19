def post_worker_init(worker):
    from mobster import start_threads
    start_threads()
