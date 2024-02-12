from app import db, login_manager
import datetime
from flask_login import UserMixin



@login_manager.user_loader
def load_user(user_id):
    return User.query.get((user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(30), nullable=False)
    shop_name = db.Column(db.String(30), nullable=False)
    # registered_on = db.Column(db.DateTime, default=datetime.datetime.now)

    def __init__(self, username, password, shop_name):
        self.username = username
        self.password = password
        self.shop_name = shop_name
        # self.registered_on = datetime.datetime.now()

    def __repr__(self):
        return '<User {0}>'.format(self.username)


class Brand(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)
    picture = db.Column(db.String(255))

    def __init__(self, name, picture):
        self.name = name
        self.picture = picture

    def __repr__(self):
        return '<Brand: {0}>'.format(self.name)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    goods_ref = db.Column(db.Integer)
    goods_code = db.Column(db.String)
    goods_name = db.Column(db.String)
    stock_dc_ref = db.Column(db.Integer)
    stock_dc_code = db.Column(db.String)
    stock_dc_name = db.Column(db.String)
    is_batch = db.Column(db.Integer)
    carton_type = db.Column(db.Float)
    on_hand_qty = db.Column(db.Float)
    order_point = db.Column(db.Integer)
    location = db.Column(db.String)
    sale_price = db.Column(db.Float)
    brand_name = db.Column(db.String)
    picture = db.Column(db.String(255))
    created_at = db.Column(db.DateTime)

    def __repr__(self):
        return f"<Product(id={self.id}, goods_name='{self.goods_name}', sale_price={self.sale_price})>"

