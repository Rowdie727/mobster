from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from mobster import db, login_manager, app
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(22), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    cash_on_hand = db.Column(db.Integer, default=0)
    cash_in_bank = db.Column(db.Integer, default=0)
    posts = db.relationship('Post', backref='author', lazy=True)
    items = db.relationship('User_Items', lazy=True)
    turf = db.relationship('User_Turf', lazy=True)
    stats = db.relationship('User_Stats', uselist=False)

    def __repr__(self):
        return f'User(username={self.username}, email={self.email}, image_file={self.image_file}, cash_on_hand={self.cash_on_hand}, cash_in_bank={self.cash_in_bank}, items={self.items}. stats={self.stats})'
        #return f'User(username={self.username})'

    def get_reset_token(self, expires_sec=1800):
        serializer = Serializer(app.config['SECRET_KEY'], expires_sec)
        return serializer.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        serializer = Serializer(app.config['SECRET_KEY'])
        try: 
            user_id = serializer.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)
    
    def add_item(self, _item, quantity):
        user = User.query.get(self.id)
        if user.items == []:
            user.items.append(User_Items(item=_item, item_quantity=quantity))
            db.session.commit()
        else:
            for item in user.items:
                if item.item.id == _item.id:
                    item.item_quantity += quantity
                    db.session.commit()
                    return 
            user.items.append(User_Items(item=_item, item_quantity=quantity))
            db.session.commit()

    def add_turf(self, _turf, quantity):
        user = User.query.get(self.id)
        if user.turf == []:
            user.turf.append(User_Turf(turf=_turf, turf_quantity=quantity))
            db.session.commit()
        else:
            for turf in user.turf:
                if turf.turf.id == _turf.id:
                    turf.turf_quantity += quantity 
                    db.session.commit()
                    return
            user.turf.append(User_Turf(turf=_turf, turf_quantity=quantity))
            db.session.commit()
            
    def sell_item(self, _item, quantity):
        user = User.query.get(self.id)
        for item in user.items:
            if item.item_id == _item.id:
                if item.item_quantity >= quantity:
                    item.item_quantity -= quantity
                    db.session.commit()
                    return True
        return False 

    def sell_turf(self, _turf, quantity):
        user = User.query.get(self.id)
        for turf in user.turf:
            if turf.turf_id == _turf.id:
                turf.turf_quantity -= quantity
                db.session.commit()
                return True
        return False
            
    def ready_to_level_up(self):
        if self.stats.user_experience >= self.stats.experience_to_level_up:
            return True
        return False
    
    def give_xp(self, xp):
        self.stats.user_experience += xp
        if self.ready_to_level_up():
            left_over_xp = self.stats.user_experience - self.stats.experience_to_level_up
            self.update_level()
            self.give_xp(left_over_xp)
        
    def update_level(self):
        self.stats.user_level += 1
        self.stats.user_experience = 0
        self.stats.experience_to_level_up += 100
            
    def heal_user(self, heal_by=50):
        if self.stats.user_current_health + heal_by > self.stats.user_max_health:
            self.stats.user_current_health = self.stats.user_max_health
        else:
            self.stats.user_current_health += heal_by
            
    def get_punched(self):
        if self.stats.user_current_health - 10 < 0:
            self.stats.user_current_health = 0
            return True
        else:
            self.stats.user_current_health -= 10
            return True
        
    def is_in_icu(self):
        if self.stats.user_in_icu == True:
            return True
        return False
            

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)    
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'Post(title={self.title}, date_posted={self.date_posted})'
    
    
class User_Items(db.Model):
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'), primary_key=True)
    item_id = db.Column(db.Integer(), db.ForeignKey('item.id'), primary_key=True)
    item = db.relationship('Item')
    item_quantity = db.Column(db.Integer())
    
    def __repr__(self):
        return f"User_Items(user_id ={self.user_id}, item_id={self.item_id}, item={self.item}, item_quantity={self.item_quantity})"


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(255))
    item_image = db.Column(db.String(20), nullable=False, default='default.jpg')
    item_type = db.Column(db.String(255))
    item_attack = db.Column(db.Integer)
    item_defense = db.Column(db.Integer)
    item_cost = db.Column(db.Integer)
    item_sell = db.Column(db.Integer)
    item_decay = db.Column(db.Integer)
    item_repair = db.Column(db.Integer)
    level_required = db.Column(db.Integer)
    
    def __repr__(self):
        return f'Item(id={self.id}, item_name={self.item_name}, item_image={self.item_image}, item_type={self.item_type}, item_attack={self.item_attack}, item_defense={self.item_defense}, item_cost={self.item_cost}, item_sell={self.item_sell}, item_decay={self.item_decay}, item_repair={self.item_repair}, level_required={self.level_required})'


class User_Stats(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_level = db.Column(db.Integer, nullable=False, default=1)
    user_current_health = db.Column(db.Integer, default=100)
    user_max_health = db.Column(db.Integer, default=100)
    user_in_icu = db.Column(db.Boolean, default=False)
    user_health_thread_running = db.Column(db.Boolean, default=False)
    user_current_energy = db.Column(db.Integer, default=10)
    user_max_energy = db.Column(db.Integer, default=10)
    user_energy_thread_running = db.Column(db.Boolean, default=False)
    user_current_stamina = db.Column(db.Integer, default=10)
    user_max_stamina = db.Column(db.Integer, default=10)
    user_stamina_thread_running = db.Column(db.Boolean, default=False)
    user_experience = db.Column(db.Integer, nullable=False, default=0)
    user_total_income = db.Column(db.Integer, default=0)
    user_current_mission_id = db.Column(db.Integer, default=1)
    user_current_mission_stage = db.Column(db.Integer, default=1)
    user_on_hitlist = db.Column(db.Boolean, default=False)
    user_current_bounty = db.Column(db.Integer, default=0)
    experience_to_level_up = db.Column(db.Integer, nullable=False, default=100)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def __repr__(self):
        return f"User_Stats(user_level = {self.user_level}, user_experience = {self.user_experience}, experience_to_level_up = {self.experience_to_level_up}, user_current_health = {self.user_current_health}, user_max_health = {self.user_max_health}, user_in_icu = {self.user_in_icu}"
    

class User_Turf(db.Model):
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'), primary_key=True)
    turf_id = db.Column(db.Integer(), db.ForeignKey('turf.id'), primary_key=True)
    turf = db.relationship('Turf')
    turf_quantity = db.Column(db.Integer())

    def __repr__(self):
        return f"User_Turf(user_id ={self.user_id}, turf_id={self.turf_id}, turf={self.turf}, turf_quantity={self.turf_quantity})"


class Turf(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    turf_name = db.Column(db.String(255))
    turf_image = db.Column(db.String(20), default='default.jpg')
    turf_cost = db.Column(db.Integer)
    turf_sell = db.Column(db.Integer)
    turf_income = db.Column(db.Integer)
    level_required = db.Column(db.Integer)

    def __repr__(self):
        return f"Turf(turf_name={self.turf_name}, turf_cost={self.turf_cost}, turf_sell={self.turf_sell}, turf_income={self.turf_income}, level_required={self.level_required}"

class Missions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mission_region = db.Column(db.String(128), nullable=False)
    mission_name = db.Column(db.String(128), nullable=False, unique=True)
    mission_image = db.Column(db.String(128), nullable=False, default='default.jpg')
    mission_tier = db.Column(db.String(24), nullable=False)
    mission_required_mastery = db.Column(db.Integer, nullable=False)
    mission_required_energy = db.Column(db.Integer, nullable=False)
    mission_required_item_id = db.Column(db.Integer, nullable=False)
    mission_required_mobc = db.Column(db.Integer, nullable=False)
    mission_reward_min_xp = db.Column(db.Integer, nullable=False)
    mission_reward_max_xp = db.Column(db.Integer, nullable=False)
    mission_reward_min_cash = db.Column(db.Integer, nullable=False)
    mission_reward_max_cash = db.Column(db.Integer, nullable=False)
    mission_reward_skill_points = db.Column(db.Integer, nullable=False)
    mission_reward_mobc = db.Column(db.Integer, nullable=False)
    mission_reward_item_id = db.Column(db.Integer, nullable=False)
    mission_reward_turf_id = db.Column(db.Integer, nullable=False)
    mission_mastery_reward_min_xp = db.Column(db.Integer, nullable=False)
    mission_mastery_reward_max_xp = db.Column(db.Integer, nullable=False)
    mission_mastery_reward_min_cash = db.Column(db.Integer, nullable=False)
    mission_mastery_reward_max_cash = db.Column(db.Integer, nullable=False)
    mission_mastery_reward_skill_points = db.Column(db.Integer, nullable=False)
    mission_mastery_reward_mobc = db.Column(db.Integer, nullable=False)
    mission_mastery_reward_item_id = db.Column(db.Integer, nullable=False)
    mission_mastery_reward_turf_id = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Mission(id={self.id}, name={self.mission_name})"