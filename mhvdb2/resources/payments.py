from mhvdb2.models import Payment, Entity
import re
from datetime import datetime
from peewee import DoesNotExist


def validate(amount, email, method, type, notes, reference):
    errors = []

    if not amount or not re.match("^[0-9]*(\.[0-9]{2}|\.[0-9]|)$", amount):
        errors.append("Sorry, you need to provide a valid amount.")
    if not re.match("[^@\s]+@[^@\s]+", email):
        errors.append("Sorry, you need to provide a valid email address.")
    else:  # Valid email, so check that they're a member
        try:
            Entity.get(Entity.email == email)
        except DoesNotExist:
            errors.append("Sorry, you need to provide a valid member's email address.")
    if not type or not type.isdigit() or int(type) > 2:
        errors.append("Sorry, you need to provide a valid payment type.")
    if not method or not method.isdigit() or int(method) > 2:
        errors.append("Sorry, you need to provide a valid payment method.")
    if not reference:
        errors.append("Sorry, you need to provide a reference.")

    return errors


def create(amount, email, method, type, notes, reference):

    # Create payment
    payment = Payment()
    payment.time = datetime.now()
    payment.entity = Entity.get(Entity.email == email)
    payment.amount = amount
    payment.source = method
    payment.is_donation = type != 0
    payment.notes = notes
    if method == 0:  # Bank transfer
        payment.bank_reference = reference
    payment.pending = True
    payment.save()
