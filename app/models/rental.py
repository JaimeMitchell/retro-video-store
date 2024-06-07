# from app import db
# from sqlalchemy.orm import Mapped, mapped_column, relationship
# from sqlalchemy import ForeignKey
# import datetime
# from typing import Optional

# class Rental(db.Model):
   
#     customer_id: Mapped[int] = mapped_column(primary_key=True)
#     video_id: Mapped[int] = mapped_column(ForeignKey('video.video.id'), primary_key=True) # This is a foreign key to the video table (id column)
#     video: Mapped[Optional['Video']] = relationship('Video', back_populates='rentals') # This is a relationship to the video table
#     due_date: Mapped[Optional[datetime.datetime]]
#     videos_checked_out_count: Mapped[int]
#     available_inventory: Mapped[int]


# #  This is a method that returns a dictionary of the object
#     def to_dict(self):
#         return {
#             'customer_id': self.customer_id,
#             'video_id': self.video_id,
#             'due_date': self.due_date,
#             'videos_checked_out_count': self.videos_checked_out_count,
#             'available_inventory': self.available_inventory}
    
# # This is a class method that takes a dictionary and returns a new instance of the class
#     @classmethod
#     def to_object(cls, data_dict):
#         return cls(
#             customer_id=data_dict["customer_id"],
#             video_id=data_dict["video_id"],
#             due_date=data_dict["due_date"],
#             videos_checked_out_count=data_dict["videos_checked_out_count"],
#             available_inventory=data_dict["available_inventory"]
#         )