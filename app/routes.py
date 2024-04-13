from flask import Flask, render_template, request, redirect, url_for, flash, session, current_app, jsonify
from app import app, db
from app.forms import LoginForm
from app.API import send_verification_code
from app.models import User, Order
import random
from app.funcs import user_finder, brand_finder, good_list_finder, good_finder_by_id, create_order, preview_order
from flask_login import login_user, current_user, login_required, logout_user
import json




@app.route("/")
@app.route("/home")
def home():
    if current_user.is_authenticated:
        brands = brand_finder()
        # goods_data = good_list_finder()  # ذخیره کردن goods_data_dict در جلسه
        return render_template('demo3.html', title="zagros", brands=brands)
    else:
        # اگر کاربر لاگین نکرده باشد، به صفحه لاگین هدایت کنید
        return redirect(url_for('login'))


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        user = User.query.filter_by(username=username).first()
        if user is not None:
            password = user.password
            if password == form.password.data:
                # goods_data = good_list_finder()
                session['customer'] = user.customer_id
                login_user(user)
                return redirect(url_for('home'))
            else:
                flash('نام کاربری یا رمز عبور اشتباه است  ', 'error')
        else:
            customer_data = user_finder(username)
            if customer_data:
                password = customer_data.password
                customer_id = customer_data.customer_id
                if password == form.password.data:
                    user = User(username=customer_data.username, password=password, shop_name=customer_data.shop_name,
                                customer_id=customer_id)
                    db.session.add(user)
                    db.session.commit()
                    session['customer'] = user.customer_id
                    # goods_data = good_list_finder()
                    # session['goods_data'] = goods_data
                    login_user(user)
                    next_page = request.args.get('next')
                    return redirect(next_page if next_page else 'home')
            else:
                flash('نام کاربری یا رمز عبور اشتباه است  ', 'danger')
    return render_template("login.html", title="Login", form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('با موفقیت خارج شدید', 'success')
    return redirect(url_for('home'))


@app.route('/loading')
def loading():
    return render_template("loader.html", title="Loading")


@app.route('/goods/', methods=['GET', 'POST'])
@login_required
def goods():
    goods_data = good_list_finder()
    brands = brand_finder()
    return render_template("shop-banner-sidebar.html", goods_data=goods_data, brands=brands)


@app.route('/product/<product_id>', methods=['GET', 'POST'])
@login_required
def product(product_id):
    brands = brand_finder()
    good = good_finder_by_id(product_id)
    return render_template('product-default.html', title="Product", brands=brands, good=good)


@app.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    price = request.form['code']
    return price


@app.route('/add-to-cart', methods=['POST'])
@login_required
def add_to_cart():
    data = request.json
    product_id = data['productCode']
    product_name = data['productName']
    product_price = data['productPrice']
    quantity = data['productQuantity']
    cart_item = {
        'product_id': product_id,
        'product_name': product_name,
        'product_price': product_price,
        'quantity': quantity,
    }
    if 'cart' not in session:
        session['cart'] = []
    for item in session['cart']:
        if item['product_id'] == product_id:
            return jsonify({'error': 'این محصول'}), 400
    session['cart'].append(cart_item)
    session.modified = True  # اطمینان حاصل کنید که تغییرات در session ذخیره شده‌اند
    return jsonify(session['cart'])


@app.route('/remove-from-cart', methods=['POST'])
@login_required
def remove_from_cart():
    product_id = request.form['product_id']
    # اطلاعات سبد خرید را از جلسه بخوانید
    if 'cart' not in session:
        return jsonify([])
    # محصول مورد نظر را از سبد خرید حذف کنید
    session['cart'] = [item for item in session['cart'] if item['product_id'] != product_id]
    return jsonify(session['cart'])


@app.route('/clear_cart')
@login_required
def clear_cart():
    brands = brand_finder()
    # سبد خرید را از جلسه پاک کنید
    session.pop('cart', None)
    return render_template('cart.html', title="سبد خرید", brands=brands)


@app.route('/cart')
@login_required
def cart():
    brands = brand_finder()
    # اطلاعات سبد خرید را از جلسه بخوانید
    if 'cart' not in session:
        return render_template('cart.html', title="سبد خرید", brands=brands)

    # داده‌های سبد خرید را به عنوان آرگومان به تابع render_template ارسال کنید
    return render_template('cart.html', shop_cart=session['cart'], title="سبد خرید", brands=brands)


@app.route('/accept')
@login_required
def accept():
    response_dict = create_order(session['cart'], session['customer'])
    order_id = response_dict['ReturnData'][0]['ExtraInfo1']
    for item in session['cart']:
        order = Order(customer_id=session['customer'], order_id=order_id, quantity=item['quantity'],
                      price=item['product_price'], goods_id=item['product_id'], goods_name=item['product_name'])
        db.session.add(order)
        db.session.commit()
    flash(response_dict['ReturnData'][0]['ResultMessage'], category='success')
    session['orderId'] = order_id
    session.pop('cart', None)
    return redirect(url_for('cart'))


@app.route('/discount')
@login_required
def discount():
    order_id = session.get('orderId')  # دریافت مقدار کلید orderId از دیکشنری session
    if order_id is not None:
        orders = Order.query.filter_by(order_id=order_id)
        response = preview_order(orders, session['customer'])
        response_dict = json.loads(response)
        flash(response, category='success')
        session.pop('orderId', None)
        return render_template('discount.html', response=response_dict)
    else:
        flash('سفارشی وجود ندارد', category='danger')
    return redirect(url_for('cart'))