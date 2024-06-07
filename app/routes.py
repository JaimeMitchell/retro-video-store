from app import db
# from app.models.rental import Rental
from app.models.customer import Customer
# from app.models.video import Video
from flask import Blueprint,abort, make_response, request
from sqlalchemy import not_, and_

# INSTANTIATE BLUEPRINT FOR ROUTES
# rental_bp = Blueprint("rental", __name__, url_prefix="/rentals")
customer_bp = Blueprint("customer", __name__, url_prefix="/customers")
# video_bp = Blueprint("video", __name__, url_prefix="/videos")
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
@customer_bp.get("", strict_slashes=False)
def read_all_customers():
    customers = Customer.query.all()
    customer_response = [customer.to_dict() for customer in customers]
    return customer_response

# GET CUSTOMER BY ID
@customer_bp.get("/<int:id>", strict_slashes=False)
def get_one_customer(id):
    query = db.select(Customer).where(Customer.id == id)
    tast = db.session.scalar(query)
    customer = validate_model(Customer, id)
    return {"customer": customer.to_dict()}, 200


# GET ALL CUSTOMERS IN ASCENDING ORDER
@customer_bp.get("/ascending", strict_slashes=False) 
def read_all_customers_ascending():
    customers = Customer.query.order_by(Customer.id.asc()).all()
    customer_response = [customer.to_dict() for customer in customers]
    return customer_response


# # GET ALL RENTALS
# @rental_bp.get("", strict_slashes=False)
# def read_all_rentals():
#     rentals = Rental.query.all()
#     rental_response = [rental.to_dict() for rental in rentals]
#     return rental_response


# # GET RENTAL BY ID
# @rental_bp.get("/<int:id>", strict_slashes=False)
# def get_one_rental(id):

#     rental = validate_model(Rental, id)
#     return {"rental": rental.to_dict()}, 200

# #GET ALL RENTALS IN ASCENDING ORDER
# @rental_bp.get("/ascending", strict_slashes=False)
# def read_all_rentals_ascending():
#     rentals = Rental.query.order_by(Rental.id.asc()).all()
#     rental_response = [rental.to_dict() for rental in rentals]
#     return rental_response


# #GET ALL RENTAL HISTORY OF A CUSTOMER BY CUSTOMER_ID IN BUT IN ASC ORDER OF RENTAL ID TO CHECK "IS_RETURNED" IN LAST OBJECT IN JSON (DEF CAN BE A HELPER FUNCTION TO CHECK IS_RETURNED=TRUE FOR THIS CUSTOMER))
# @rental_bp.get("/customer/<int:customer_id>", strict_slashes=False)
# def get_rentals_by_customer_id(customer_id):
#     customer = validate_model(Customer, customer_id)
#     if not customer:
#         return {"message": "Customer not found"}, 404
#     rentals = Rental.query.filter_by(customer_id=customer_id).order_by(Rental.id.asc()).all()
#     if not rentals:
#         # Post a new customer with no history to check this.
#         return {"message": "No rental history found for this customer"}, 404
#     rental_response = [rental.to_dict() for rental in rentals]
#     return rental_response

# POST A NEW CUSTOMER (successfully shows in postman that customer is created but runs the error message "no rental history found for this customer")
#             'id': self.id,
#             'name': self.name,
#             'registered_at': self.registered_at,
#             'postal_code': self.postal_code,
#             'phone': self.phone}

@customer_bp.post("", strict_slashes=False)
def create_customer():
    data = request.get_json()

    try:
        id = data["id"]
        name = data["name"]
        registered_at = data["registered_at"]
        postal_code = data["postal_code"]
        phone = data["phone"]

    except KeyError:
        abort(make_response({"message": "Invalid request"}, 400))

    new_customer = Customer(id=id, name=name, registered_at=registered_at, postal_code=postal_code, phone=phone)
    db.session.add(new_customer)
    db.session.commit()

    return {"message": "Customer created successfully", "customer_id": new_customer.id}, 201


# # LIST OF AVAILABLE VideoS

# # My steps:

# # Look at the data.7 Videos can’t be rented based on the five customers that are renting them and/or charge_percent.

# # First seeded DB and then used SQL logic to get expected result.

# # SQL STATEMENT: "SELECT * FROM Video WHERE ID NOT IN (SELECT Video_id FROM rental WHERE is_returned = FALSE) AND charge_percent > 15;"

# # GET all Videos_id that are in rentals AND NOT is_returned = False

# # Read Doc from SQLalchemyfunction sqlalchemy.sql.expression.not_(clause: _ColumnExpressionArgument[_T]) → ColumnElement[_T]
# # Return a negation of the given clause, i.e. NOT(clause). 

# # Now search this query for the Video_id in the available Videos data, if it is not there, then return a message "The last Video is not available." if it is there, then return the user message "The last Video is available."

# # I can use the def as a helper function in the other routes to check if the Video is available for rent.

# @video_bp.get("/available/", strict_slashes=False)
# def read_available_Videos():
#     rental_subquery = Rental.query.filter(
#         Rental.Video_id == Video.id,
#         Rental.is_returned == False
#     ).exists()

#     available_Videos = Video.query.filter(
#         not_(rental_subquery),
#         Video.charge_percent > 15
#     ).all()

#     available_Videos_data = [Video.to_dict() for Video in available_Videos]
#     print(len(available_Videos_data))
#     return available_Videos_data

# # Now search this query for the Video_id in the available Videos data, if it is not there, then return a message "The last Video is not available." 

# #if it is there, then return the user message "The last Video is available."

# @video_bp.get("/check-Video/<int:Video_id>", strict_slashes=False)
# def check_Video_availability(Video_id):
#     # Validate if the Video exists
#     Video = Video.query.get(Video_id)
#     if not Video:
#         return {"message": "Video not found"}, 404

#     # Check if the Video is currently being rented
#     active_rental = Rental.query.filter(
#         Rental.Video_id == Video_id,
#         Rental.is_returned == False
#     ).scalar()

#     if active_rental:
#         return {"message": "The Video is being rented"}, 400

#     # Check if the Video's charge percent is greater than 15
#     if Video.charge_percent <= 15:
#         return {"message": "The Video has to be charged"}, 400

#     return {"message": "The Video is available! :)"},{"Video": Video.to_dict()}, 200


# # RENT A Video:

# # STEPS:
# # 1. Looks at Data and sees that 5 customers are renting, I can use this to check query results.

# # 2. Helper function: query all Rental<customer_id> in ascending order, if the last record (is_returned=True) go to Video check, else return message "You can only have one active rental."

# # 3. Give feedback message "You can only have one active rental."

# # 4. Helper function: query all Rental<Video_id> in ascending order, if the last record (is_returned=True) POST a new rental 

# # 5. Give feedback message "The last Video is not available."

# # 6. (REMEMBER id needs to be created in ascending order for other route logic to work! same with return route!)

# # 7. I found that I ran into problems with .scalar, so I used .first() instead because it returns the first result of the query or None if there are no results which didn't give me any errors when i created a new customer with no history! i'm bummed though that it didn't seem to work in helper functions but im running out of time and will refactor later!

# # 8. I also learned that i dont need to increment the id in rentals. This could cause duplicates if simultaneous requests are made and may have also given me some trouble within postman that set me back an hour.

# @rental_bp.post("/rent/customer/<int:customer_id>/Video/<int:Video_id>", strict_slashes=False)
# def rent_Video(customer_id, Video_id):
#     # Validate if the customer exists
#     customer = Customer.query.get(customer_id)
#     if not customer:
#         return {"message": "Customer not found"}, 404
#     # Validate if the Video exists
#     Video = Video.query.get(Video_id)
#     if not Video:
#         return {"message": "Video not found"}, 404
    
#     # Check if the Video is currently being rented
#     active_rental = Rental.query.filter(
#         Rental.Video_id == Video_id,
#         Rental.is_returned == False
#     ).first()

#     if active_rental:
#         return {"message": "The Video is being rented"}, 400

#     # Check if the Video's charge percent is greater than 15
#     if Video.charge_percent <= 15:
#         return {"message": "The Video has to be charged"}, 400

#     # Check if the customer already has an active rental
#     active_rental_customer = Rental.query.filter(
#         Rental.customer_id == customer_id,
#         Rental.is_returned == False
#     ).first()

#     if active_rental_customer:
#         return {"message": "You can only have one active rental"}, 400

#     # Create a new rental
#     new_rental = Rental(customer_id=customer_id, Video_id=Video_id, is_returned=False)
#     db.session.add(new_rental)
#     db.session.commit()
#     return {"message": "Rental created successfully"}, 200

#     return {"message": "Rental created successfully"}, 200


# # RETURN A Video
# #Steps:
# # 1.  I have most of the logic from above I can reuse. If I had time I'd refactor everything into a function, and then from there refactor into a class. Please forgive me! I'm still wet behind the ears so can't be DRY! ;P
# # 2. A customer should only be able to return a Video if they are currently renting a Video.
# # 3. A customer should only be able to return a Video if the Video is not already returned.
# # 4. Since I'm almost outta time, I'm goint to streamline this and only enter a customer id because I imagine the customer will only be shown their own Video to return. I can just check if is_returned is false, then I can post from there and change is_returned to true. Finito.

# @rental_bp.post("/return/customer/<int:customer_id>", strict_slashes=False)
# def return_Video(customer_id):
#     # Validate if the customer exists
#     customer = Customer.query.get(customer_id)
#     if not customer:
#         return {"message": "Customer not found"}, 404
    
#     # Check if the customer already has an active rental
#     active_rental_customer = Rental.query.filter(
#         Rental.customer_id == customer_id,
#         Rental.is_returned == False
#     ).first()

#     if active_rental_customer:

#         # Update is_returned to True
#         active_rental_customer.is_returned = True

#         # Create a new rental
#         Video_id = active_rental_customer.Video_id

#         new_rental = Rental(customer_id=active_rental_customer.customer_id, Video_id=Video_id, is_returned=True)
#         db.session.add(new_rental)
#         db.session.commit()

#         return {"message": "Rental returned successfully"}, 200
#     else:
#         return {"message": "You can only return a Video if you are currently renting a Video"}, 400

