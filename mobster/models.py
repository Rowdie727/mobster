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

    def __repr__(self):
        return f'User(username={self.username}, email={self.email}, image_file={self.image_file}, cash_on_hand={self.cash_on_hand}, cash_in_bank={self.cash_in_bank}, items={self.items})'
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
            
    def sell_item(self, _item, quantity):
        user = User.query.get(self.id)
        for item in user.items:
            if item.item_id == _item.id:
                if item.item_quantity >= quantity:
                    item.item_quantity -= quantity
                    db.session.commit()
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
        return f'Item(id={self.id}, item_name={self.item_name})'
