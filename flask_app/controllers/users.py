from flask import render_template, redirect, session, request, flash

from flask_app import app

from flask_app.models import user, anime

from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('log_and_reg.html')

@app.route('/register', methods=['POST'])
def register():
    if not user.User.validate_registration(request.form):
        return redirect('/')
    
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': bcrypt.generate_password_hash(request.form['password'])
    }
    
    user_id = user.User.save(data)
    session['user_id'] = user_id
    
    return redirect ('/dashboard')
    
@app.route('/login', methods=['POST'])
def login():
    users = user.User.get_by_email(request.form)
    
    if not users:
        flash('Invalid Email or Password.', 'login')
        return redirect('/')
    if not bcrypt.check_password_hash(users.password, request.form['password']):
        flash('Invalid Email or Password.', 'login')
        return redirect('/')
    
    session['user_id'] = users.id
    
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id': session['user_id']
    }
    return render_template('dashboard.html', user=user.User.get_by_user_id(data), animes=anime.Anime.get_all_animes())

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')