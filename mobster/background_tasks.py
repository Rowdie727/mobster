from time import sleep
from mobster import db
from mobster.models import User
from threading import Thread


def fill_health(user_id):
    user = User.query.get(user_id)
    user.stats.user_health_thread_running = True
    db.session.commit()
    print(f'{user.username} fill_health running!')
    sleep(20)
    while user.stats.user_current_health != user.stats.user_max_health:
        user.stats.user_current_health += 1
        db.session.commit()
        print('Changed comitted!')
        sleep(20)
    user.stats.user_health_thread_running = False
    db.session.commit()
    return 

def background_thread():
    print('Background_thread started')
    while True:
        sleep(2)
        for user in User.query.all():
            if user.stats.user_current_health < user.stats.user_max_health and user.stats.user_health_thread_running == False:
                health_thread = Thread(target=fill_health, args=[user.id])
                health_thread.daemon = True
                if not health_thread.is_alive():
                    health_thread.start()
                
