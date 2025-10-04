from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class ServiceBase(BaseModel):
    organisation_name: Optional[str] = None
    campus_name: Optional[str] = None
    service_name: Optional[str] = None
    region_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    website: Optional[str] = None
    notes: Optional[str] = None
    expected_wait_time: Optional[str] = None
    opening_hours_24_7: Optional[bool] = None
    opening_hours_standard: Optional[bool] = None
    opening_hours_extended: Optional[bool] = None
    op_hours_extended_details: Optional[str] = None
    address: Optional[str] = None
    suburb: Optional[str] = None
    state: Optional[str] = None
    postcode: Optional[str] = None
    cost: Optional[str] = None
    delivery_method: Optional[str] = None
    level_of_care: Optional[str] = None
    referral_pathway: Optional[str] = None
    service_type: Optional[str] = None
    target_population: Optional[str] = None
    workforce_type: Optional[str] = None

class ServiceCreate(ServiceBase):
    pass

class ServiceUpdate(ServiceBase):
    pass

class ServiceResponse(ServiceBase):
    service_campus_key: UUID

    class Config:
        from_attributes = True