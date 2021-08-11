"""This is the amenity class"""
import models.base_model as mb
import os
import sqlalchemy as s
import sqlalchemy.orm as orm


class Amenity(mb.BaseModel, mb.Base):
    """This is the class for Amenity
    Attributes:
        name: input name
    """
    __tablename__ = 'amenities'
    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        name = s.Column(
            s.String(128),
            nullable=False
        )
        place_amenities = orm.relationship(
            "Place",
            secondary="place_amenity",
            back_populates="amenities"
        )
    else:
        name = ""
