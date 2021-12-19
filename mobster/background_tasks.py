from time import sleep
from mobster import db
from mobster.models import User
from threading import Thread

def fill_health(user_id, wait_in_secs):
    user = User.query.get(user_id)
    print(f'{user.username} fill_health running!')
    sleep(wait_in_secs)
    user.stats.user_current_health = user.stats.user_max_health
    db.session.commit()
    print('***************************')
    print('Changed comitted!')
    return

def background_thread():
    while True:
        sleep(5)
        for user in User.query.all():
            if user.stats.user_current_health < user.stats.user_max_health:
                wait_time = ((user.stats.user_max_health - user.stats.user_current_health) * 12)
                #print(f'{user.username}, {user.stats.user_current_health}, {user.stats.user_max_health}')
                health_thread = Thread(target=fill_health, args=[user.id, wait_time])
                health_thread.daemon = True
                health_thread.start()
