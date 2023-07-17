from flask import render_template,redirect,session,request,flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.pizza import Pizza
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    if 'logged_in' in session:
        if session['logged_in'] == True:
            return redirect('/home')
    else:
        return render_template('index.html')


@app.route('/home')
def home():
    if not 'logged_in' in session:
        return redirect('/')
    if not 'order_count' in session:
        session['order_count'] = 0
    order_count = session['order_count']
    data = { 'id': session['user_id'],}
    user = User.user_logged_in(data)
    return render_template('home.html', user=user, order_count=order_count)

@app.route('/register', methods=['POST'])
def register():
    if request.form['password'] != request.form['confirm_password']:
        flash('Passwords do not match!', 'register')
        return redirect('/')
    if not User.user_vald(request.form):
        return redirect('/')
    if User.unique_email(request.form['email']) == True:
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        'first_name' : request.form['first_name'],
        'last_name' : request.form['last_name'],
        'email' : request.form['email'],
        'address' : request.form['address'],
        'city' : request.form['city'],
        'state' : request.form['state'],
        'password' : pw_hash
    }
    new_user = User.create_user(data)
    print(new_user)
    session['user_id'] = new_user
    session['logged_in'] = True
    return redirect('/home')

@app.route('/login_page')
def login_page():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    data = { 'email': request.form['email'] }
    user_in_db = User.find_user(data)
    print(user_in_db)
    if not user_in_db:
        flash('Invalid Email/Password', 'login')
        return redirect('/login_page')
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash('Invalid Email/Password', 'login')
        return redirect('/login_page')
    session['user_id'] = user_in_db.id
    session['logged_in'] = True
    return redirect('/home')

@app.route('/order')
def order():
    if not 'logged_in' in session:
        return redirect('/')
    if not 'order_count' in session:
        session['order_count'] = 0
    order_count = session['order_count']
    data = { 'id': session['user_id'],}
    user = User.user_logged_in(data)
    return render_template('order.html', user=user, order_count=order_count)

@app.route('/order/submit', methods=['POST'])
def order_submit():
    if not 'logged_in' in session:
        return redirect('/')
    session['order_count'] += 1
    print(request.form)
    data = {
        'method': request.form['method'],
        'size': request.form['size'],
        'crust': request.form['crust'],
        'qty': request.form['qty'],
        'cheese': request.form['cheese'],
        'pepperoni': request.form['pepperoni'],
        'mushroom' : request.form['mushroom'],
        'sausage': request.form['sausage'],
        'onion' : request.form['onion'],
        'user_id': request.form['user_id']
    }
    new_pizza = Pizza.create_pizza(data)
    print(new_pizza)
    return redirect('/cart')

@app.route('/cart')
def cart():
    if not 'logged_in' in session:
        return redirect('/')
    if not 'order_count' in session:
        session['order_count'] = 0
    order_count = session['order_count']
    data = { 'id': session['user_id'],}
    user = User.user_logged_in(data)
    return render_template('cart.html', order_count=order_count, user=user)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')