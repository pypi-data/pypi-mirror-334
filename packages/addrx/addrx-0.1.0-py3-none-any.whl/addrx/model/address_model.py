from pydantic import BaseModel
from typing import Optional


class Address(BaseModel):
    """Base model to parse query response from libpostal into different address classes."""

    house: Optional[str] = None
    category: Optional[str] = None
    near: Optional[str] = None
    house_number: Optional[str] = None
    road: Optional[str] = None
    unit: Optional[str] = None
    level: Optional[str] = None
    entrance: Optional[str] = None
    po_box: Optional[str] = None
    postcode: Optional[str] = None
    suburb: Optional[str] = None
    city_district: Optional[str] = None
    city: Optional[str] = None
    island: Optional[str] = None
    state_district: Optional[str] = None
    state: Optional[str] = None
    country_region: Optional[str] = None
    country: Optional[str] = None
    world_region: Optional[str] = None

    def __init__(self, exclude_fields: list = None, **data):
        """Overwrite the speCific field values with None"""

        if isinstance(exclude_fields, list):
            for each in exclude_fields:
                data.pop(each, None)
        super().__init__(**data)
