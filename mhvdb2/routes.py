from mhvdb2 import app
from mhvdb2.models import Entity
from flask import render_template, request, flash
import re
from datetime import date
from peewee import DoesNotExist
import json

from mhvdb2.resources import *


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup/', methods=['GET'])
def signup_get():
    return render_template('signup.html')

@app.route('/signup/', methods=['POST'])
def signup_post():
    name = request.form["name"].strip()
    email = request.form["email"].strip()
    phone = request.form["phone"].strip()

    (valid, flashes) = User.validate(name, email, phone)

    if not valid:
        for f in flashes:
            flash(f[0], f[1])

        return render_template('signup.html'), 400

    try:
        member = Entity.get(Entity.email == email)
        User.update(member, name, email, phone)
        flash("Thanks for renewing, your details have been updated!", "success")
    except DoesNotExist:
        User.create(name, email, phone)
        flash("Thanks for registering!", "success")

    return signup_get()

@app.route('/payments/', methods=['GET'])
def payments_get():
    return render_template('payments.html')

@app.route('/payments/', methods=['POST'])
def payments_post():
    amount = request.form["amount"].strip()
    email = request.form["email"].strip()
    method = request.form["method"].strip()
    type = request.form["type"].strip()
    notes = request.form["notes"].strip()
    reference = request.form["reference"].strip()

    (valid, flashes) = PaymentResource.validate(amount, email, method, type, notes, reference)

    entity = None
    try: 
        entity = Entity.get(Entity.email == email)
    except DoesNotExist: 
        flashes.append(("Sorry, you need to provide a valid member's email address.", 'danger'))
        valid = False

    if not valid:
        for f in flashes:
            flash(f[0], f[1])
            print("flashing ", f)
        return render_template('payments.html', amount=amount, email=email,
            method=method, type=type, notes=notes, reference=reference), 400

    PaymentResource.create(amount, entity, method, type, notes, reference)
    flash("Thank you!", "success")

    return payments_get()

@app.route('/admin/')
def admin():
    members = Entity.select().where(Entity.is_member)
    return render_template('admin.html', members=members)

