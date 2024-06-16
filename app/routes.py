from app import db
# from app.models.rental import Rental
from app.models.customer import Customer
from app.models.video import Video
# from app.models.rental import Rental
from flask import Blueprint,abort, make_response, request
from sqlalchemy import not_, and_
from datetime import datetime, timedelta

# INSTANTIATE BLUEPRINT FOR ROUTES
# rental_bp = Blueprint("rental", __name__, url_prefix="/rentals")
customer_bp = Blueprint("customer", __name__, url_prefix="/customers")
video_bp = Blueprint("video", __name__, url_prefix="/videos")
rental_bp = Blueprint("rental", __name__, url_prefix="/rentals")

# VALIDATE MODEL
def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except ValueError:
        abort(400, description=f"{cls.__name__} {model_id} invalid")

    # This is like SELECT * FROM table_name WHERE id=model_id
    query = db.select(cls).where(cls.id == model_id)
    model = db.session.scalar(query)

    if not model:
        abort(404, description=f"{cls.__name__} {model_id} can't be found")

    return model
#------------------------------------------------------------------------#
# CUSTOMER & VIDEO ROUTES WAVE 1
#------------------------------------------------------------------------#
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
    new_customer = Customer(id=id, name=name, registered_at=datetime.now(), postal_code=postal_code, phone=phone)
    
    db.session.add(new_customer)
    try:
        db.session.commit()
        return {"message": "Customer created successfully", "customer_id": new_customer.id}, 201
    except Exception as e:
        db.session.rollback()
        return {"message": "Failed to create customer", "error": str(e)}, 500
    
    

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
    # Old way but with New way version of validate_model
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
    try:
        db.session.commit()
        return {"message": "Video created successfully", "video_id": new_video.id}, 201
    except Exception as e:
        db.session.rollback()
        return {"message": "Failed to create video", "error": str(e)}, 500


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


#------------------------------------------------------------------------#
# RENTAL ROUTES WAVE 2
#------------------------------------------------------------------------#

'''POST /rentals/check-out
customer_id	integer	ID of the customer attempting to check out this video
video_id	integer	ID of the video to be checked out
'''
@rental_bp.route('/check-out', methods=['POST'])
def check_out():
    data = request.get_json()
    
    customer_id = data.get('customer_id')
    video_id = data.get('video_id')

    customer = Customer.query.get(customer_id)
    video = Video.query.get(video_id)

    if not customer:
        return {'error': 'Customer not found'}, 404

    if not video:
        return {'error': 'Video not found'}, 404

    # Calculate available inventory
    checked_out_count = Rental.query.filter_by(video_title=video.title, checked_in=False).count()
    available_inventory = video.total_inventory - checked_out_count

    if available_inventory <= 0:
        return {'error': 'No available inventory'}, 400

    # Create rental
    due_date = datetime.now() + timedelta(days=7)
    rental = Rental(
        customer_id=customer_id,
        video_id=video_id,
        video_title=video.title,
        due_date=due_date.strftime('%Y-%m-%d')
    )
    
    db.session.add(rental)
    db.session.commit()

    return {
        'customer_id': customer_id,
        'video_id': video_id,
        'due_date': due_date.strftime('%Y-%m-%d'),
        'videos_checked_out_count': Rental.query.filter_by(customer_id=customer_id, checked_in=False).count(),
        'available_inventory': available_inventory - 1
    }, 200


''' POST /rentals/check-in
Request Body Param	Type	Details
customer_id	integer	ID of the customer attempting to check out this video
video_id	integer	ID of the video to be checked out

'''

