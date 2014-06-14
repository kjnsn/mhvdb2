from mhvdb2 import app
from mhvdb2.models import Entity, Payment
from flask import render_template, request, flash
import re
from datetime import date, datetime
from peewee import DoesNotExist

class Resource:
    pass

class User(Resource):
    @staticmethod
    def validate(name, email, phone):
        flashes = []
        valid = True
        if not name:
            flashes.append(("Sorry, you need to provide a name.", 'danger'))
            valid = False
        if not phone:
            flashes.append(("Sorry, you need to provide a phone number.", 'danger'))
            valid = False
        if not re.match("[^@\s]+@[^@\s]+", email):
            flashes.append(("Sorry, you need to provide an email address.", 'danger'))
            valid = False

        if valid:
            return (True, flashes)
        else:
            return (False, flashes)

    @staticmethod
    def create(name, email, phone):
        member = Entity()
        member.is_member = True
        member.joined_date = date.today()
        member.name = name
        member.email = email
        member.phone = phone
        member.agreement_date = date.today()

        return member.save()

    @staticmethod
    def update(member, name, email, phone):
        member.name = name
        member.email = email
        member.phone = phone
        member.agreement_date = date.today()

        return member.save()

class PaymentResource(Resource):
    @staticmethod
    def validate(amount, email, method, type, notes, reference):
        valid = True
        flashes = []

        if not amount or not amount.isdigit() or int(amount) <=0:
            flashes.append(("Sorry, you need to provide a valid amount.", 'danger'))
            valid = False
        if not re.match("[^@\s]+@[^@\s]+", email):
            flashes.append(("Sorry, you need to provide a valid email address.", 'danger'))
            valid = False
        if not type or not type.isdigit() or int(type) > 2:
            flashes.append(("Sorry, you need to provide a valid payment type.", 'danger'))
            valid = False
        if not method or not method.isdigit() or int(method) > 2:
            flashes.append(("Sorry, you need to provide a valid payment method.", 'danger'))
            valid = False
        if not reference:
            flashes.append(("Sorry, you need to provide a reference.", 'danger'))
            valid = False

        if valid:
            return (True, flashes)
        else:
            return (False, flashes)

    @staticmethod
    def create(amount, entity, method, type, notes, reference):
        # Cajole the post data into integers
        amount = int(amount)
        type = int(type)
        method = int(method)

        # Create payment
        payment = Payment()
        payment.time = datetime.now()
        payment.entity = entity
        payment.amount = amount
        payment.source = method
        payment.is_donation = type != 0
        payment.notes = notes
        if method == 0: # Bank transfer
            payment.bank_reference = reference
        payment.pending = True
        payment.save()
