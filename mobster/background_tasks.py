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

def fill_energy(user_id):
    user = User.query.get(user_id)
    user.stats.user_energy_thread_running = True
    db.session.commit()
    print(f'{user.username} fill_energy running!')
    sleep(20)
    while user.stats.user_current_energy != user.stats.user_max_energy:
        user.stats.user_current_energy += 1
        db.session.commit()
        print('Changed comitted!')
        sleep(20)
    user.stats.user_energy_thread_running = False
    db.session.commit()
    return 

def fill_stamina(user_id):
    user = User.query.get(user_id)
    user.stats.user_stamina_thread_running = True
    db.session.commit()
    print(f'{user.username} fill_stamina running!')
    sleep(20)
    while user.stats.user_current_stamina != user.stats.user_max_stamina:
        user.stats.user_current_stamina += 1
        db.session.commit()
        print('Changed comitted!')
        sleep(20)
    user.stats.user_stamina_thread_running = False
    db.session.commit()
    return 

def background_thread():
    print('Background_thread started')
    while True:
        sleep(2)
        for user in User.query.all():
            # Health regen
            if user.stats.user_current_health < user.stats.user_max_health and user.stats.user_health_thread_running == False:
                health_thread = Thread(target=fill_health, args=[user.id])
                health_thread.daemon = True
                if not health_thread.is_alive():
                    health_thread.start()
            # Energy regen
            if user.stats.user_current_energy < user.stats.user_max_energy and user.stats.user_energy_thread_running == False:
                energy_thread = Thread(target=fill_energy, args=[user.id])
                energy_thread.daemon = True
                if not energy_thread.is_alive():
                    energy_thread.start()
            # Stamina regen
            if user.stats.user_current_stamina < user.stats.user_max_stamina and user.stats.user_stamina_thread_running == False:
                stamina_thread = Thread(target=fill_stamina, args=[user.id])
                stamina_thread.daemon = True
                if not stamina_thread.is_alive():
                    stamina_thread.start()
                
