from flask_app import app
from flask import render_template, redirect, request, session,flash
from flask_app.models.user import User
from flask_app.models.drill import Drill
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/register', methods=['POST'])
def register():
    if request.form['password'] != request.form['conf_password']:
        flash('Passwords do not match. Please confirm and try again.')
        return redirect('/')
    data = {"email": request.form['email']}
    user_in_db = User.get_one_by_email(data)
    term =  request.form.get('terms')
    print (term)
    if user_in_db:
        flash("Email has already been registered")
        return redirect('/')
    if term != 'term':
        flash("You must agree to Terms of Service")
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)
    data = {
        "first_name": request.form['first_name'],
        "last_name" : request.form['last_name'],
        "email" : request.form['email'],
        "password" : pw_hash,
    }
    if not User.validate_user(request.form):
        return redirect('/')
    else:
        user_id = User.save(data)
        session['user_id'] = user_id
        return redirect("/dashboard")

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('You must login to continue')
        return redirect('/')
    user = User.get_one_by_id({"id":session['user_id']})
    drills = Drill.get_drills_w_creator()
    return render_template('dashboard.html', user=user, drills=drills)

@app.route('/drills/easy')
def easydrills():
    if 'user_id' not in session:
        flash('You must login to continue')
        return redirect('/')
    user = User.get_one_by_id({"id":session['user_id']})
    drills = Drill.get_drills_w_creator_easy()
    dif = "Easy"
    return render_template('dashboard.html', user=user, drills=drills, dif=dif)

@app.route('/drills/medium')
def mediumdrills():
    if 'user_id' not in session:
        flash('You must login to continue')
        return redirect('/')
    user = User.get_one_by_id({"id":session['user_id']})
    drills = Drill.get_drills_w_creator_medium()
    dif = "Medium"
    return render_template('dashboard.html', user=user, drills=drills, dif=dif)

@app.route('/drills/hard')
def harddrills():
    if 'user_id' not in session:
        flash('You must login to continue')
        return redirect('/')
    user = User.get_one_by_id({"id":session['user_id']})
    drills = Drill.get_drills_w_creator_hard()
    dif = "Hard"
    return render_template('dashboard.html', user=user, drills=drills, dif=dif)

@app.route('/login', methods=['POST'])
def login():
    data = {"email": request.form['email']}
    user_in_db = User.get_one_by_email(data)
    if not user_in_db:
        flash("Invalid Email/Password")
        return redirect('/')
    if not bcrypt.check_password_hash(user_in_db.password,request.form['password']):
        flash("Invalid Email/Password")
        return redirect('/')
    session['user_id'] = user_in_db.id
    return redirect('/dashboard')
    
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')