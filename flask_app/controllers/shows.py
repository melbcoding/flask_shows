from flask import render_template,redirect,session,request, flash
from flask_app import app
from flask_app.models import user, show


@app.route('/shows')
def show_dash():
    if 'user_id' not in session:
        return redirect('/')
    data ={
        'id': session['user_id']
    }
    logged_user= user.User.get_by_id(data)
    all_shows= show.Show.get_all_shows()    
    return render_template("dashboard.html", logged_user=logged_user, all_shows=all_shows)    

@app.route('/shows/<int:id>')
def view_one(id):
    if 'user_id' not in session:
        return redirect('/')
    data={
        'id':id
    }
    return render_template('view_one.html', one_show=show.Show.get_one(data))

@app.route('/shows/new')
def create_show():
    if 'user_id' not in session:
        return redirect('/')
    return render_template('create_one.html')

@app.route('/shows/create', methods=['POST'])
def insert_show():
    if 'user_id' not in session:
        return redirect('/')
    if not show.Show.validate_new(request.form):
        return redirect('/shows/new')
    data= {
        "added_by_id": session['user_id'],
        "title": request.form['title'],
        "network": request.form['network'],
        "release_date": request.form['release_date'],
        "description": request.form['description'],
    }
    show.Show.save(data)
    return redirect('/shows')

@app.route('/shows/edit/<int:id>')
def edit_show(id):
    if 'user_id' not in session:
        return redirect('/')
    data={
        'id':id
    }
    return render_template('edit_one.html', one_show=show.Show.get_one(data))

@app.route('/shows/update/<int:id>', methods=['POST'])
def update_show(id):
    if 'user_id' not in session:
        return redirect('/')
    if not show.Show.validate_update(request.form):
        return redirect(f'/shows/edit/{id}')
    data= {
        'id': id,
        "title": request.form['title'],
        "network": request.form['network'],
        "release_date": request.form['release_date'],
        "description": request.form['description'],
    }
    show.Show.update(data)
    return redirect('/shows')

@app.route('/shows/like/<int:id>')
def like(id):
    if 'user_id' not in session:
        return redirect('/')
    data={
        "user_id": session['user_id'],
        "show_id": id
    }
    show.Show.like(data)
    return redirect('/shows')

@app.route('/shows/unlike/<int:id>')
def unlike(id):
    if 'user_id' not in session:
        return redirect('/')
    data={
        "user_id": session['user_id'],
        "show_id": id
    }
    show.Show.unlike(data)
    return redirect('/shows')

    
@app.route('/shows/delete/<int:id>')
def delete(id):
    if 'user_id' not in session:
        return redirect('/')
    data={'id':id}
    show.Show.delete(data)
    return redirect('/shows')