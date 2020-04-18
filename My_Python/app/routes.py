# -*- coding: utf-8 -*-
from flask import render_template, flash, url_for
from werkzeug.utils import redirect
from app import app
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User
from flask import request
from werkzeug.urls import url_parse
from app import db, login
import mysql.connector
from app.forms import LoginForm, RegistrationForm

mydata = mysql.connector.connect(
    host='localhost',
    user='root',
    passwd='1111',
    db='products'
)

mycursor = mydata.cursor()

categories = []
categories_hierarchy = {}
produc_hierarchy = {}


def load_products():
    mycursor.execute('SELECT * FROM product')
    prod = mycursor.fetchall()
    for prod_con in prod:
        arr_product_cont = prod_con
        prod_id = arr_product_cont[0]
        cat_id = arr_product_cont[1]
        name = arr_product_cont[2]
        title = arr_product_cont[3]
        meta_info = arr_product_cont[4]
        price = arr_product_cont[5]
        img = arr_product_cont[6]
        product = {
            'id': prod_id,
            'cat_id': cat_id,
            'name': name,
            'title': title,
            'meta_info': meta_info,
            'price': price,
            'img': img
        }
        products = produc_hierarchy.get(cat_id)
        if not products:
            products = []
            produc_hierarchy[cat_id] = products
        products.append(product)


def load_categories():
    mycursor.execute('SELECT * FROM category')
    categ = mycursor.fetchall()
    for category_content in categ:
        arr_cat_cont = category_content
        cat_id = arr_cat_cont[0]
        parent_id = arr_cat_cont[1]
        name = arr_cat_cont[2]
        img = arr_cat_cont[3]
        category = {
            'cat_id': cat_id,
            'parent_id': parent_id,
            'name': name,
            'img': img
        }
        if parent_id == -1:
            categories.append(category)
        else:
            sub_cat = categories_hierarchy.get(parent_id)
            if not sub_cat:
                sub_cat = []
                categories_hierarchy[parent_id] = sub_cat
            sub_cat.append(category)


load_categories()
load_products()


@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html', title='Главная', categories=categories, show=True)


@app.route('/categories/<parent_id>')
def sub_categories(parent_id):
    return render_template('index.html', categories=categories_hierarchy.get(int(parent_id)))


@app.route('/categories/<parent_id>/items')
def product(parent_id):
    form = LoginForm()
    return render_template('items.html', products=produc_hierarchy.get(int(parent_id)), form=form)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Вход на страницу', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, lastname=form.lastname.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html', user=user, posts=posts)


if __name__ == "__main__":
    app.run(port=4555, debug=True)
