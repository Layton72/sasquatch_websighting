from belt_app import app
from flask import render_template, redirect, request, session, flash, get_flashed_messages
from belt_app.models.users import Users
from belt_app.models.sightings import Sighting
from belt_app.models.skeptics import Skeptic


@app.route('/sasquatch/view/add_skeptic/<int:sighting_id>')
def add_skeptic(sighting_id):
    data = {
        "user_id": session["logged_in"],
        "sighting_id": sighting_id
    }

    Skeptic.save(data)
    return redirect(f"/sasquatch/view/{sighting_id}")

@app.route('/sasquatch/view/delete_skeptic/<int:sighting_id>')
def delete_skeptic(sighting_id):
    data = {
        "user_id": session["logged_in"],
        "sighting_id": sighting_id
    }

    Skeptic.delete(data)
    return redirect(f"/sasquatch/view/{sighting_id}")