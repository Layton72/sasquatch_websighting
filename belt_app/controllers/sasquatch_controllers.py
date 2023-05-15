from belt_app import app
from flask import render_template, redirect, request, session, flash, get_flashed_messages
from belt_app.models.users import Users
from belt_app.models.sightings import Sighting
from belt_app.models.skeptics import Skeptic

@app.route('/sasquatch')
def dashboard():
    if "logged_in" not in session:
        return redirect ('/sasquatch/login')
    
    user = Users.get_one_by_id(session["logged_in"])
    sightings = Sighting.get_all_with_user()
    for sighting in sightings:
        sighting.skeptics = len(Skeptic.get_all_skeptics(sighting.id))
    return render_template('dashboard.html', user=user, sightings=sightings)

@app.route('/sasquatch/report')
def report():
    if "logged_in" not in session:
        return redirect ('/sasquatch/login')
    user = Users.get_one_by_id(session["logged_in"])
    if "errors" in session and session["errors"] == True:
        location  = session.pop("location", None)
        description= session.pop("description", None)
        date = session.pop("date", None)
        num_sas = session.pop("num_sas", None)
        session["errors"] = False
        return render_template('report_sighting.html', user=user, location=location, description=description, date=date, num_sas=num_sas)
    return render_template('report_sighting.html', user=user)

@app.route('/sasquatch/report/process', methods=['POST'])
def report_process():
    if not Sighting.validate_sighting(request.form):
        session["errors"] = True
        session["location"]= request.form["location"]
        session["description"]= request.form["description"]
        session["date"]= request.form["date"]
        session["num_sas"]= request.form["num_sas"]
        return redirect("/sasquatch/report")

    data = {
        "location": request.form["location"],
        "description": request.form["description"],
        "date": request.form["date"],
        "num_sas": request.form["num_sas"],
        "user_id": session["logged_in"]
    }
    Sighting.save(data)
    return redirect('/sasquatch')

@app.route('/sasquatch/view/<int:sighting_id>')
def view_sighting(sighting_id):
    if "logged_in" not in session:
        return redirect ('/sasquatch/login')
    data = {
        "id": sighting_id
    }
    sighting = Sighting.get_one(data)
    user = Users.get_one_by_id(session["logged_in"])
    skeptics_objects = Skeptic.get_all_skeptics(sighting_id)
    skeptics = []
    for skeptic in skeptics_objects:
        skeptics.append(skeptic.user_id)
    return render_template('view_sighting.html', sighting=sighting, user=user, skeptics_objects=skeptics_objects, skeptics=skeptics)

@app.route('/sasquatch/edit/<int:sighting_id>')
def edit_sasquatch(sighting_id):
    
    if "logged_in" not in session:
        return redirect ('/sasquatch')
    
    data = {
        "id": sighting_id
    }
    name = Users.get_one_by_id(session["logged_in"]).first_name
    sighting = Sighting.get_one(data)

    if "errors" in session and session["errors"] == True:
        sighting.location = session.pop("location", None)
        sighting.description = session.pop("description", None)
        sighting.date = session.pop("date", None)
        sighting.num_sas = session.pop("num_sas", None)
        session["errors"] = False
        return render_template('edit_sighting.html', sighting=sighting, name=name)
    
    return render_template('edit_sighting.html', sighting=sighting, name=name)

@app.route('/sasquatch/edit/<int:sighting_id>/process', methods=['POST'])
def edit_sighting_process(sighting_id):
    if not Sighting.validate_sighting(request.form):
        session["errors"] = True
        session["location"]= request.form["location"]
        session["description"]= request.form["description"]
        session["date"]= request.form["date"]
        session["num_sas"]= request.form["num_sas"]
        return redirect(f"/sasquatch/edit/{sighting_id}")

    data = {
        "location": request.form["location"],
        "description": request.form["description"],
        "date": request.form["date"],
        "num_sas": request.form["num_sas"],
        "id": sighting_id
    }
    Sighting.update(data)
    return redirect('/sasquatch')

@app.route('/sasquatch/delete/<int:sighting_id>')
def delete_recipe(sighting_id):
    data = {"id": sighting_id}
    Sighting.delete(data)
    return redirect('/sasquatch')