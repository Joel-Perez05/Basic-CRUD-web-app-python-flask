from flask import render_template, redirect, session, request, flash

from flask_app import app

from flask_app.models import user, anime

from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route('/reviews/new')
def reviews_new():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id': session['user_id']
    }
    return render_template('create.html', user=user.User.get_by_user_id(data))

@app.route('/review/create', methods=['POST'])
def create_review():
    if 'user_id' not in session:
        return redirect('/logout')
    if not anime.Anime.validate_anime(request.form):
        return redirect('/reviews/new')
    data = {
        'name': request.form['name'],
        'review': request.form['review'],
        'rating': int(request.form['rating']),
        'watch_date': request.form['watch_date'],
        'user_id': session['user_id']
    }
    anime.Anime.save(data)
    return redirect('/dashboard')

@app.route('/review/edit/<int:id>')
def edit_review(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id': id
    }
    user_data = {
        'id': session['user_id']
    }
    return render_template('edit.html', user=user.User.get_by_user_id(user_data), anime=anime.Anime.get_by_anime_id(data))

@app.route('/review/edit', methods=['POST'])
def update_review():
    if 'user_id' not in session:
        return redirect('/logout')
    if not anime.Anime.validate_anime(request.form):
        return redirect('/dashboard')
    data = {
        'name': request.form['name'],
        'review': request.form['review'],
        'rating': int(request.form['rating']),
        'watch_date': request.form['watch_date'],
        'id': request.form['id']
    }
    anime.Anime.update(data)
    return redirect('/dashboard')

@app.route('/review/delete/<int:id>')
def delete_review(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id': id
    }
    anime.Anime.delete(data)
    return redirect('/dashboard')

@app.route('/review/<int:id>')
def view_review(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data= {
        'id': id
    }
    user_data = {
        'id': session['user_id']
    }
    return render_template('reviews.html', user=user.User.get_by_user_id(user_data), anime=anime.Anime.get_by_anime_id(data))