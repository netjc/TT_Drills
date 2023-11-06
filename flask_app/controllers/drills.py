from fileinput import filename
from flask_app import app
from flask import render_template, redirect, request, session, flash, url_for
from flask_app.models.drill import Drill
from flask_app.models.user import User


#Submit drill (from the new drill page)
@app.route('/drill', methods=['POST'])
def submit_drill():
    if 'user_id' not in session:
        flash('You must login to continue')
        return redirect('/')
    data = {
        "name":request.form['name'],
        "description":request.form['description'],
        "steps":request.form['steps'],
        "difficulty":request.form['difficulty'],
        "user_id":session['user_id']
    }
    if not Drill.validate_drill(request.form):
        return redirect('/drill/new')
    else:
        Drill.save(data)
        return redirect("/dashboard")

#Present one drill on page
@app.route('/drill/<int:id>')
def one_drill(id):
    if 'user_id' not in session:
        flash('You must login to continue')
        return redirect('/')
    user = User.get_one_by_id({"id":session['user_id']})
    data = {
        "id":id
    }
    drill = Drill.get_drill_w_creator(data)
    return render_template('show.html', drill=drill , user=user)

#Present create new drill page
@app.route('/drill/new')
def drill_form():
    if 'user_id' not in session:
        flash('You must login to continue')
        return redirect('/')
    user = User.get_one_by_id({"id":session['user_id']})
    return render_template('create.html', user=user)

#Present edit page for single drill
@app.route('/drill/<int:id>/edit')
def drill_edit(id):
    if 'user_id' not in session:
        flash('You must login to continue')
        return redirect('/')
    data = {
        "id":id
    }
    drill = Drill.get_drill_by_id(data)
    user = User.get_one_by_id({"id":session['user_id']})
    return render_template('edit.html',drill=drill, user=user)

#Update POST used in the edit page
@app.route('/drill/update', methods=['POST'])
def drill_update():
    if 'user_id' not in session:
        flash('You must login to continue')
        return redirect('/')
    data = {
        "id":request.form['id'],
        "name":request.form['name'],
        "description":request.form['description'],
        "steps":request.form['steps'],
        "difficulty":request.form['difficulty']
    }
    id = request.form['id']
    if not Drill.validate_drill(request.form):
        return redirect(f'/drill/{id}/edit')
    else:
        Drill.update(data)
        return redirect("/dashboard")

#Delete drill (from the dashboard)
@app.route("/drill/<int:id>/delete")
def delete_drill(id):
    if 'user_id' not in session:
        flash('You must login to continue')
        return redirect('/')
    data = {
        "id":id
    }
    Drill.delete(data)
    return redirect('/dashboard')