from flask import render_template,redirect,session,request, flash
from flask_app import app
from flask_app.models import user
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from flask import flash

@app.route('/')
def index():
    print('you reached / route')
    return render_template('log_reg.html')

@app.route('/register',methods=['POST'])
def register():
    print("you've reached register route")
    if not user.User.validate_register(request.form):
        return redirect('/')
    data = {
        "first_name" : request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password'])
    }
    id = user.User.save(data)
    session['user_id'] = id

    return redirect('/shows')


@app.route('/login',methods=['POST'])
def login():
    print('youve reached login route')
    valid_user = user.User.get_email(request.form)
    if not valid_user:
        flash("Invalid Credentials","login")
        return redirect('/')
    if not bcrypt.check_password_hash(valid_user.password, request.form['password']):
        flash("Invalid Password","login")
        return redirect('/')
    session['user_id'] = valid_user.id
    return redirect('/shows')

@app.route('/logout')
def logout():
    print('log out route')
    session.clear()
    return redirect('/')


