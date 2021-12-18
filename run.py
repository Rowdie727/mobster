from mobster import app, thread
from threading import Thread
from mobster.background_tasks import background_thread

if __name__ == '__main__':
    thread = Thread(target=background_thread)
    thread.daemon = True
    thread.start()
    app.run(debug=True)
    

