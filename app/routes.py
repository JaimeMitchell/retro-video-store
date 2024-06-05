from app import db
from app.models.rental import Rental
from app.models.customer import Customer
from flask import Blueprint, jsonify, abort, make_response, request
from sqlalchemy import not_, and_

# INSTANTIATE BLUEPRINT FOR ROUTES
rental_bp = Blueprint("rental", __name__, url_prefix="/rentals")
customer_bp = Blueprint("customer", __name__, url_prefix="/customers")

# VALIDATE MODEL
def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response(
            {"message": f"{cls.__name__} {model_id} invalid"}, 400))

    # This is like SELECT * FROM table_name(cls param=Task)
    model = cls.query.get(model_id)

    if not model:
        abort(make_response(
            {"message": f"{cls.__name__} {model_id} can't be found"}, 404))

    return model

'''Required RESTful endpoints:

GET /customers
GET /customers/<id>
POST /customers
PUT /customers/<id>
DELETE /customers/<id>'''

# GET ALL CUSTOMERS
@customer_bp.route("", strict_slashes=False, methods=["GET"])
def read_all_customers():
    customers = Customer.query.all()
    customer_response = [customer.to_dict() for customer in customers]
    return jsonify(customer_response)

# GET CUSTOMER BY ID
@customer_bp.route("/<int:id>", strict_slashes=False, methods=["GET"])
def get_one_customer(id):

    customer = validate_model(Customer, id)
    return {"customer": customer.to_dict()}, 200


# GET ALL CUSTOMERS IN ASCENDING ORDER
@customer_bp.route("/ascending", strict_slashes=False, methods=["GET"]) 
def read_all_customers_ascending():
    customers = Customer.query.order_by(Customer.id.asc()).all()
    customer_response = [customer.to_dict() for customer in customers]
    return jsonify(customer_response)


# GET ALL RENTALS
@rental_bp.route("", strict_slashes=False, methods=["GET"])
def read_all_rentals():
    rentals = Rental.query.all()
    rental_response = [rental.to_dict() for rental in rentals]
    return jsonify(rental_response)


# GET RENTAL BY ID
@rental_bp.route("/<int:id>", strict_slashes=False, methods=["GET"])
def get_one_rental(id):

    rental = validate_model(Rental, id)
    return {"rental": rental.to_dict()}, 200

#GET ALL RENTALS IN ASCENDING ORDER
@rental_bp.route("/ascending", strict_slashes=False, methods=["GET"])
def read_all_rentals_ascending():
    rentals = Rental.query.order_by(Rental.id.asc()).all()
    rental_response = [rental.to_dict() for rental in rentals]
    return jsonify(rental_response)


#GET ALL RENTAL HISTORY OF A CUSTOMER BY CUSTOMER_ID IN BUT IN ASC ORDER OF RENTAL ID TO CHECK "IS_RETURNED" IN LAST OBJECT IN JSON (DEF CAN BE A HELPER FUNCTION TO CHECK IS_RETURNED=TRUE FOR THIS CUSTOMER))
@rental_bp.route("/customer/<int:customer_id>", strict_slashes=False, methods=["GET"])
def get_rentals_by_customer_id(customer_id):
    customer = validate_model(Customer, customer_id)
    if not customer:
        return jsonify({"message": "Customer not found"}), 404
    rentals = Rental.query.filter_by(customer_id=customer_id).order_by(Rental.id.asc()).all()
    if not rentals:
        # Post a new customer with no history to check this.
        return jsonify({"message": "No rental history found for this customer"}), 404
    rental_response = [rental.to_dict() for rental in rentals]
    return jsonify(rental_response)

# POST A NEW CUSTOMER (successfully shows in postman that customer is created but runs the error message "no rental history found for this customer")
@customer_bp.route("", strict_slashes=False, methods=["POST"])
def create_customer():
    data = request.get_json()

    try:
        id = data["id"]
        name = data["name"]
        email = data["email"]
        phone = data["phone"]
    except KeyError:
        abort(make_response({"message": "Invalid request"}, 400))

    new_customer = Customer(id=id, name=name, email=email, phone=phone)
    db.session.add(new_customer)
    db.session.commit()

    return jsonify({"message": "Customer created successfully", "customer_id": new_customer.id}), 201


# LIST OF AVAILABLE SCOOTERS

# My steps:

# Look at the data.7 scooters can’t be rented based on the five customers that are renting them and/or charge_percent.

# First seeded DB and then used SQL logic to get expected result.

# SQL STATEMENT: "SELECT * FROM scooter WHERE ID NOT IN (SELECT scooter_id FROM rental WHERE is_returned = FALSE) AND charge_percent > 15;"

# GET all scooters_id that are in rentals AND NOT is_returned = False

# Read Doc from SQLalchemyfunction sqlalchemy.sql.expression.not_(clause: _ColumnExpressionArgument[_T]) → ColumnElement[_T]
# Return a negation of the given clause, i.e. NOT(clause). 

# Now search this query for the scooter_id in the available scooters data, if it is not there, then return a message "The last scooter is not available." if it is there, then return the user message "The last scooter is available."

# I can use the def as a helper function in the other routes to check if the scooter is available for rent.

@scooter_bp.route("/available/", strict_slashes=False, methods=["GET"])
def read_available_scooters():
    rental_subquery = Rental.query.filter(
        Rental.scooter_id == Scooter.id,
        Rental.is_returned == False
    ).exists()

    available_scooters = Scooter.query.filter(
        not_(rental_subquery),
        Scooter.charge_percent > 15
    ).all()

    available_scooters_data = [scooter.to_dict() for scooter in available_scooters]
    print(len(available_scooters_data))
    return jsonify(available_scooters_data)

# Now search this query for the scooter_id in the available scooters data, if it is not there, then return a message "The last scooter is not available." 

#if it is there, then return the user message "The last scooter is available."

@scooter_bp.route("/check-scooter/<int:scooter_id>", strict_slashes=False, methods=["GET"])
def check_scooter_availability(scooter_id):
    # Validate if the scooter exists
    scooter = Scooter.query.get(scooter_id)
    if not scooter:
        return jsonify({"message": "Scooter not found"}), 404

    # Check if the scooter is currently being rented
    active_rental = Rental.query.filter(
        Rental.scooter_id == scooter_id,
        Rental.is_returned == False
    ).scalar()

    if active_rental:
        return jsonify({"message": "The scooter is being rented"}), 400

    # Check if the scooter's charge percent is greater than 15
    if scooter.charge_percent <= 15:
        return jsonify({"message": "The scooter has to be charged"}), 400

    return jsonify({"message": "The scooter is available! :)"},{"scooter": scooter.to_dict()}), 200


# RENT A SCOOTER:

# STEPS:
# 1. Looks at Data and sees that 5 customers are renting, I can use this to check query results.

# 2. Helper function: query all Rental<customer_id> in ascending order, if the last record (is_returned=True) go to scooter check, else return message "You can only have one active rental."

# 3. Give feedback message "You can only have one active rental."

# 4. Helper function: query all Rental<scooter_id> in ascending order, if the last record (is_returned=True) POST a new rental 

# 5. Give feedback message "The last scooter is not available."

# 6. (REMEMBER id needs to be created in ascending order for other route logic to work! same with return route!)

# 7. I found that I ran into problems with .scalar, so I used .first() instead because it returns the first result of the query or None if there are no results which didn't give me any errors when i created a new customer with no history! i'm bummed though that it didn't seem to work in helper functions but im running out of time and will refactor later!

# 8. I also learned that i dont need to increment the id in rentals. This could cause duplicates if simultaneous requests are made and may have also given me some trouble within postman that set me back an hour.

@rental_bp.route("/rent/customer/<int:customer_id>/scooter/<int:scooter_id>", strict_slashes=False, methods=["POST"])
def rent_scooter(customer_id, scooter_id):
    # Validate if the customer exists
    customer = Customer.query.get(customer_id)
    if not customer:
        return jsonify({"message": "Customer not found"}), 404
    # Validate if the scooter exists
    scooter = Scooter.query.get(scooter_id)
    if not scooter:
        return jsonify({"message": "Scooter not found"}), 404
    
    # Check if the scooter is currently being rented
    active_rental = Rental.query.filter(
        Rental.scooter_id == scooter_id,
        Rental.is_returned == False
    ).first()

    if active_rental:
        return jsonify({"message": "The scooter is being rented"}), 400

    # Check if the scooter's charge percent is greater than 15
    if scooter.charge_percent <= 15:
        return jsonify({"message": "The scooter has to be charged"}), 400

    # Check if the customer already has an active rental
    active_rental_customer = Rental.query.filter(
        Rental.customer_id == customer_id,
        Rental.is_returned == False
    ).first()

    if active_rental_customer:
        return jsonify({"message": "You can only have one active rental"}), 400

    # Create a new rental
    new_rental = Rental(customer_id=customer_id, scooter_id=scooter_id, is_returned=False)
    db.session.add(new_rental)
    db.session.commit()

    return jsonify({"message": "Rental created successfully"}), 200


# RETURN A SCOOTER
#Steps:
# 1.  I have most of the logic from above I can reuse. If I had time I'd refactor everything into a function, and then from there refactor into a class. Please forgive me! I'm still wet behind the ears so can't be DRY! ;P
# 2. A customer should only be able to return a scooter if they are currently renting a scooter.
# 3. A customer should only be able to return a scooter if the scooter is not already returned.
# 4. Since I'm almost outta time, I'm goint to streamline this and only enter a customer id because I imagine the customer will only be shown their own scooter to return. I can just check if is_returned is false, then I can post from there and change is_returned to true. Finito.

@rental_bp.route("/return/customer/<int:customer_id>", strict_slashes=False, methods=["POST"])
def return_scooter(customer_id):
    # Validate if the customer exists
    customer = Customer.query.get(customer_id)
    if not customer:
        return jsonify({"message": "Customer not found"}), 404
    
    # Check if the customer already has an active rental
    active_rental_customer = Rental.query.filter(
        Rental.customer_id == customer_id,
        Rental.is_returned == False
    ).first()

    if active_rental_customer:

        # Update is_returned to True
        active_rental_customer.is_returned = True

        # Create a new rental
        scooter_id = active_rental_customer.scooter_id

        new_rental = Rental(customer_id=active_rental_customer.customer_id, scooter_id=scooter_id, is_returned=True)
        db.session.add(new_rental)
        db.session.commit()

        return jsonify({"message": "Rental returned successfully"}), 200
    else:
        return jsonify({"message": "You can only return a scooter if you are currently renting a scooter"}), 400

