from flask import Flask, render_template, request, redirect, url_for, flash, session, current_app, jsonify
from app import app, db
from app.forms import LoginForm
from app.API import send_verification_code
from app.models import User
import random
from app.funcs import user_finder, brand_finder, good_list_finder
from flask_login import login_user, current_user, login_required, logout_user




@app.route("/")
@app.route("/home")
def home():
    if current_user.is_authenticated:
        brands = brand_finder()
        goods_data = good_list_finder()  # ذخیره کردن goods_data_dict در جلسه
        return render_template('demo3.html', title="zagros", brands=brands, goods_data=goods_data)
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
                # session['goods_data'] = goods_data
                login_user(user)
                return redirect(url_for('home'))
            else:
                flash('نام کاربری یا رمز عبور اشتباه است  ', 'error')
        else:
            customer_data = user_finder(username)
            if customer_data:
                password = customer_data.password
                if password == form.password.data:
                    user = User(username=customer_data.username, password=password, shop_name=customer_data.shop_name)
                    db.session.add(user)
                    db.session.commit()
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


@app.route('/goods/<brand_name>', methods=['GET', 'POST'])
@login_required
def goods(brand_name):
    goods_data = good_list_finder()
    brands = brand_finder()
    return render_template("shop-banner-sidebar.html", goods_data=goods_data, brands=brands,
                           brand_name=brand_name)
