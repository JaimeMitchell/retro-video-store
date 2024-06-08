from app import db
# from app.models.rental import Rental
from app.models.customer import Customer
from app.models.video import Video
# from app.models.rental import Rental
from flask import Blueprint,abort, make_response, request
from sqlalchemy import not_, and_
import datetime

# INSTANTIATE BLUEPRINT FOR ROUTES
# rental_bp = Blueprint("rental", __name__, url_prefix="/rentals")
customer_bp = Blueprint("customer", __name__, url_prefix="/customers")
video_bp = Blueprint("video", __name__, url_prefix="/videos")
# rental_bp = Blueprint("rental", __name__, url_prefix="/rentals")

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

@customer_bp.post("", strict_slashes=False)
def create_customer():
    # Get the data from the request
    data = request.get_json()
    # Get the name, postal_code, and phone from the data
    name = data["name"]
    postal_code = data["postal_code"]
    phone = data["phone"]
    
    # Get the last customer id from the database
    last_customer = Customer.query.order_by(Customer.id.desc()).first()
    if last_customer:
        id = last_customer.id + 1
    else:
        id = 1
    
    # Create a new customer with the generated id and current datetime
    new_customer = Customer(id=id, name=name, registered_at=datetime.datetime.now(), postal_code=postal_code, phone=phone)
    
    db.session.add(new_customer)
    db.session.commit()
    
    return {"message": "Customer created successfully", "customer_id": new_customer.id}, 201

# UPDATE CUSTOMER'S NAME, POSTAL_CODE, AND/OR PHONE BY ID but do not change position in database
@customer_bp.put("/<int:id>", strict_slashes=False)
def update_customer(id):
    customer = validate_model(Customer, id)
    data = request.get_json()
    if "name" in data:
        customer.name = data["name"]
    if "postal_code" in data:
        customer.postal_code = data["postal_code"]
    if "phone" in data:
        customer.phone = data["phone"]
    db.session.commit()
    return {"message": "Customer updated successfully"}, 200

# GET ALL CUSTOMERS
@customer_bp.get("", strict_slashes=False)
def read_all_customers():
    customers = Customer.query.all()
    customer_response = [customer.to_dict() for customer in customers]
    return customer_response

# GET CUSTOMER BY ID
@customer_bp.get("/<int:id>", strict_slashes=False)
def get_one_customer(id):
    # New way
    # query = db.select(Customer).where(Customer.id == id)
    # customer = db.session.scalar(query)
    # Old way
    customer = validate_model(Customer, id)
    return {"customer": customer.to_dict()}, 200


# GET ALL CUSTOMERS IN ASCENDING ORDER
@customer_bp.get("/ascending", strict_slashes=False) 
def read_all_customers_ascending():
    customers = Customer.query.order_by(Customer.id.asc()).all()
    customer_response = [customer.to_dict() for customer in customers]
    return customer_response

# DELETE CUSTOMER BY ID
@customer_bp.delete("/<int:id>", strict_slashes=False)
def delete_customer(id):
    customer = validate_model(Customer, id)
    db.session.delete(customer)
    db.session.commit()
    return {"message": "Customer deleted successfully"}, 200

'''title	string	The title of the video
release_date	datetime	Represents the date of the video's release
total_inventory	integer	The total quantity of this video in the store
'''
##CREATE A NEW Video WITH TITLE, RELEASE_DATE, AND TOTAL_INVENTORY
@video_bp.post("", strict_slashes=False)
def create_video():
    # Get the data from the request
    data = request.get_json()
    # Get the name, postal_code, and phone from the data
    title = data["title"]
    release_date= data["release_date"]
    total_inventory = data["total_inventory"]
    
    # Get the last video id from the database
    last_video = Video.query.order_by(Video.id.desc()).first()
    if last_video:
        id = last_video.id + 1
    else:
        id = 1
    # Get the last video total_inventory from the database based on the title and increment by 1.
    last_video = Video.query.filter_by(title=title).order_by(Video.total_inventory.desc()).first()
    if last_video:
        total_inventory = last_video.total_inventory + 1
    else:
        total_inventory = 1


    # Create a new customer with the generated id and current datetime
    new_video = Video(id=id, title=title, release_date=release_date, total_inventory=total_inventory)
    
    db.session.add(new_video)
    db.session.commit()
    return {"message": "Video created successfully", "video_id": new_video.id}, 201


# GET ALL VIDEOS
@video_bp.get("", strict_slashes=False)
def read_all_videos():
    videos = Video.query.all()
    video_response = [video.to_dict() for video in videos]
    return video_response


# GET VIDEO BY ID
@video_bp.get("/<int:id>", strict_slashes=False)
def get_one_video(id):

    video = validate_model(Video, id)
    return {"video": video.to_dict()}, 200

#GET ALL VIDEOS IN ASCENDING ORDER
@video_bp.get("/ascending", strict_slashes=False)
def read_all_rentals_ascending():
    videos = Video.query.order_by(Video.id.asc()).all()
    video_response = [video.to_dict() for video in videos]
    return video_response

# UPDATE VIDEO'S TITLE, RELEASE_DATE, AND/OR TOTAL_INVENTORY BY ID but do not change position in database
@video_bp.put("/<int:id>", strict_slashes=False)
def update_video(id):
    video = validate_model(Video, id)
    data = request.get_json()
    if "title" in data:
        video.title = data["title"]
    if "release_date" in data:
        video.release_date = data["release_date"]
    if "total_inventory" in data:
        video.total_inventory = data["total_inventory"]
    db.session.commit()
    return {"message": "Video updated successfully"}, 200


# DELETE VIDEO BY ID
@video_bp.delete("/<int:id>", strict_slashes=False)
def delete_video(id):
    video = validate_model(Video, id)
    db.session.delete(video)
    db.session.commit()
    return {"message": "Video deleted successfully"}, 200


#DELETE VIDEO BY TITLE
@video_bp.delete("/<string:title>", strict_slashes=False)
def delete_video_by_title(title):
    video = Video.query.filter_by(title=title).first()
    if not video:
        return {"message": "Video not found"}, 404
    db.session.delete(video)
    db.session.commit()
    return {"message": "Video deleted successfully"}, 200

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

# # LIST OF AVAILABLE Videos

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

