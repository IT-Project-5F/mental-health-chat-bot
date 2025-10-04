from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from database_config import get_db
from models import (
    Organisation, Service, Campus, ServiceCampus, Region,
    Cost, DeliveryMethod, LevelOfCare, ReferralPathway,
    ServiceType, TargetPopulation, WorkforceType
)
from .Schemas import ServiceCreate, ServiceUpdate, ServiceResponse

router = APIRouter()


def build_service_response(service_campus, db: Session) -> ServiceResponse:
    """Helper function to build the service response with all related data"""
    service = db.query(Service).filter(Service.service_key == service_campus.service_key).first()
    campus = db.query(Campus).filter(Campus.campus_key == service_campus.campus_key).first()
    organisation = None
    if service:
        organisation = db.query(Organisation).filter(
            Organisation.organisation_key == service.organisation_key
        ).first()

    service_campus_key = service_campus.service_campus_key

    cost = db.query(Cost).filter(Cost.service_campus_key == service_campus_key).first()
    delivery = db.query(DeliveryMethod).filter(
        DeliveryMethod.service_campus_key == service_campus_key
    ).first()
    level_care = db.query(LevelOfCare).filter(
        LevelOfCare.service_campus_key == service_campus_key
    ).first()
    referral = db.query(ReferralPathway).filter(
        ReferralPathway.service_campus_key == service_campus_key
    ).first()
    svc_type = db.query(ServiceType).filter(
        ServiceType.service_campus_key == service_campus_key
    ).first()
    target = db.query(TargetPopulation).filter(
        TargetPopulation.service_campus_key == service_campus_key
    ).first()
    workforce = db.query(WorkforceType).filter(
        WorkforceType.service_campus_key == service_campus_key
    ).first()

    return ServiceResponse(
        service_campus_key=service_campus.service_campus_key,
        organisation_name=organisation.organisation_name if organisation else None,
        campus_name=campus.campus_name if campus else None,
        service_name=service.service_name if service else None,
        region_name=None,  # TODO: Add region lookup through ServiceRegion
        email=service_campus.email,
        phone=service_campus.phone,
        website=service_campus.website,
        notes=service_campus.notes,
        expected_wait_time=service_campus.expected_wait_time,
        opening_hours_24_7=service_campus.op_hours_24_7,
        opening_hours_standard=service_campus.op_hours_standard,
        opening_hours_extended=service_campus.op_hours_extended,
        op_hours_extended_details=service_campus.op_hours_extended_details,
        address=service_campus.address,
        suburb=service_campus.suburb,
        state=service_campus.state,
        postcode=service_campus.postcode,
        cost=cost.cost if cost else None,
        delivery_method=delivery.delivery_method if delivery else None,
        level_of_care=level_care.level_of_care if level_care else None,
        referral_pathway=referral.referral_pathway if referral else None,
        service_type=svc_type.service_type if svc_type else None,
        target_population=target.target_population if target else None,
        workforce_type=workforce.workforce_type if workforce else None
    )


@router.get("/search", response_model=List[ServiceResponse])
def search_services(q: str = Query(None, description="Search term for service name"), db: Session = Depends(get_db)):
    """Search for services by name (partial match) - returns all matching services"""
    query = db.query(ServiceCampus).join(Service)

    if q:
        # Case-insensitive partial match
        query = query.filter(Service.service_name.ilike(f"%{q}%"))

    results = query.all()

    response = []
    for service_campus in results:
        response.append(build_service_response(service_campus, db))

    return response


@router.get("/by-name/{service_name}", response_model=List[ServiceResponse])
def get_services_by_name(service_name: str, db: Session = Depends(get_db)):
    """Get all services with the exact name - returns list since there can be multiple"""
    services = db.query(Service).filter(Service.service_name == service_name).all()

    if not services:
        raise HTTPException(status_code=404, detail=f"No services found with name '{service_name}'")

    response = []
    for service in services:
        service_campuses = db.query(ServiceCampus).filter(
            ServiceCampus.service_key == service.service_key
        ).all()

        for service_campus in service_campuses:
            response.append(build_service_response(service_campus, db))

    return response


@router.get("/{service_campus_key}", response_model=ServiceResponse)
def get_service_by_key(service_campus_key: UUID, db: Session = Depends(get_db)):
    """Get a specific service by its unique service_campus_key"""
    service_campus = db.query(ServiceCampus).filter(
        ServiceCampus.service_campus_key == service_campus_key
    ).first()

    if not service_campus:
        raise HTTPException(status_code=404, detail="Service not found")

    return build_service_response(service_campus, db)


@router.post("/", response_model=ServiceResponse)
def create_service_record(service_data: ServiceCreate, db: Session = Depends(get_db)):
    """Create a new service record - returns the new record with service_campus_key"""
    try:
        # Check/Create Organisation
        organisation = None
        if service_data.organisation_name:
            organisation = db.query(Organisation).filter(
                Organisation.organisation_name == service_data.organisation_name
            ).first()
            if not organisation:
                organisation = Organisation(organisation_name=service_data.organisation_name)
                db.add(organisation)
                db.flush()

        # Check/Create Service
        service = None
        if service_data.service_name and organisation:
            service = db.query(Service).filter(
                Service.service_name == service_data.service_name,
                Service.organisation_key == organisation.organisation_key
            ).first()
            if not service:
                service = Service(
                    service_name=service_data.service_name,
                    organisation_key=organisation.organisation_key
                )
                db.add(service)
                db.flush()

        # Check/Create Campus
        campus = None
        if service_data.campus_name and organisation:
            campus = db.query(Campus).filter(
                Campus.campus_name == service_data.campus_name,
                Campus.organisation_key == organisation.organisation_key
            ).first()
            if not campus:
                campus = Campus(
                    campus_name=service_data.campus_name,
                    organisation_key=organisation.organisation_key
                )
                db.add(campus)
                db.flush()

        # Create ServiceCampus - this will generate a new unique service_campus_key
        service_campus = ServiceCampus(
            service_key=service.service_key if service else None,
            campus_key=campus.campus_key if campus else None,
            email=service_data.email,
            phone=service_data.phone,
            website=service_data.website,
            notes=service_data.notes,
            expected_wait_time=service_data.expected_wait_time,
            op_hours_24_7=service_data.opening_hours_24_7,
            op_hours_standard=service_data.opening_hours_standard,
            op_hours_extended=service_data.opening_hours_extended,
            op_hours_extended_details=service_data.op_hours_extended_details,
            address=service_data.address,
            suburb=service_data.suburb,
            state=service_data.state,
            postcode=service_data.postcode
        )
        db.add(service_campus)
        db.flush()

        # Add related entities
        if service_data.region_name:
            region = db.query(Region).filter(Region.region_name == service_data.region_name).first()
            if not region:
                region = Region(region_name=service_data.region_name)
                db.add(region)
                db.flush()

        if service_data.cost:
            cost = Cost(
                service_campus_key=service_campus.service_campus_key,
                cost=service_data.cost
            )
            db.add(cost)

        if service_data.delivery_method:
            delivery = DeliveryMethod(
                service_campus_key=service_campus.service_campus_key,
                delivery_method=service_data.delivery_method
            )
            db.add(delivery)

        if service_data.level_of_care:
            level_care = LevelOfCare(
                service_campus_key=service_campus.service_campus_key,
                level_of_care=service_data.level_of_care
            )
            db.add(level_care)

        if service_data.referral_pathway:
            referral = ReferralPathway(
                service_campus_key=service_campus.service_campus_key,
                referral_pathway=service_data.referral_pathway
            )
            db.add(referral)

        if service_data.service_type:
            svc_type = ServiceType(
                service_campus_key=service_campus.service_campus_key,
                service_type=service_data.service_type
            )
            db.add(svc_type)

        if service_data.target_population:
            target = TargetPopulation(
                service_campus_key=service_campus.service_campus_key,
                target_population=service_data.target_population
            )
            db.add(target)

        if service_data.workforce_type:
            workforce = WorkforceType(
                service_campus_key=service_campus.service_campus_key,
                workforce_type=service_data.workforce_type
            )
            db.add(workforce)

        db.commit()

        # Return the created service with all fields including the new service_campus_key
        return build_service_response(service_campus, db)

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{service_campus_key}", response_model=ServiceResponse)
def update_service_record(
    service_campus_key: UUID,
    service_data: ServiceUpdate,
    db: Session = Depends(get_db)
):
    """Update a specific service by its unique service_campus_key"""
    service_campus = db.query(ServiceCampus).filter(
        ServiceCampus.service_campus_key == service_campus_key
    ).first()

    if not service_campus:
        raise HTTPException(status_code=404, detail="Service not found")

    try:
        # Update organisation/service/campus if provided
        if service_data.organisation_name or service_data.service_name or service_data.campus_name:
            service = db.query(Service).filter(Service.service_key == service_campus.service_key).first()
            campus = db.query(Campus).filter(Campus.campus_key == service_campus.campus_key).first()

            if service_data.organisation_name:
                organisation = db.query(Organisation).filter(
                    Organisation.organisation_name == service_data.organisation_name
                ).first()
                if not organisation:
                    organisation = Organisation(organisation_name=service_data.organisation_name)
                    db.add(organisation)
                    db.flush()

                # Update service and campus organisation keys if needed
                if service:
                    service.organisation_key = organisation.organisation_key
                if campus:
                    campus.organisation_key = organisation.organisation_key

            if service_data.service_name:
                if service:
                    service.service_name = service_data.service_name

            if service_data.campus_name:
                if campus:
                    campus.campus_name = service_data.campus_name

        # Update ServiceCampus fields
        update_fields = {
            'email': service_data.email,
            'phone': service_data.phone,
            'website': service_data.website,
            'notes': service_data.notes,
            'expected_wait_time': service_data.expected_wait_time,
            'op_hours_24_7': service_data.opening_hours_24_7,
            'op_hours_standard': service_data.opening_hours_standard,
            'op_hours_extended': service_data.opening_hours_extended,
            'op_hours_extended_details': service_data.op_hours_extended_details,
            'address': service_data.address,
            'suburb': service_data.suburb,
            'state': service_data.state,
            'postcode': service_data.postcode
        }

        for field, value in update_fields.items():
            if value is not None:
                setattr(service_campus, field, value)

        # Update or create related entities
        if service_data.cost is not None:
            cost = db.query(Cost).filter(Cost.service_campus_key == service_campus_key).first()
            if cost:
                cost.cost = service_data.cost
            else:
                cost = Cost(service_campus_key=service_campus_key, cost=service_data.cost)
                db.add(cost)

        if service_data.delivery_method is not None:
            delivery = db.query(DeliveryMethod).filter(
                DeliveryMethod.service_campus_key == service_campus_key
            ).first()
            if delivery:
                delivery.delivery_method = service_data.delivery_method
            else:
                delivery = DeliveryMethod(
                    service_campus_key=service_campus_key,
                    delivery_method=service_data.delivery_method
                )
                db.add(delivery)

        if service_data.level_of_care is not None:
            level_care = db.query(LevelOfCare).filter(
                LevelOfCare.service_campus_key == service_campus_key
            ).first()
            if level_care:
                level_care.level_of_care = service_data.level_of_care
            else:
                level_care = LevelOfCare(
                    service_campus_key=service_campus_key,
                    level_of_care=service_data.level_of_care
                )
                db.add(level_care)

        if service_data.referral_pathway is not None:
            referral = db.query(ReferralPathway).filter(
                ReferralPathway.service_campus_key == service_campus_key
            ).first()
            if referral:
                referral.referral_pathway = service_data.referral_pathway
            else:
                referral = ReferralPathway(
                    service_campus_key=service_campus_key,
                    referral_pathway=service_data.referral_pathway
                )
                db.add(referral)

        if service_data.service_type is not None:
            svc_type = db.query(ServiceType).filter(
                ServiceType.service_campus_key == service_campus_key
            ).first()
            if svc_type:
                svc_type.service_type = service_data.service_type
            else:
                svc_type = ServiceType(
                    service_campus_key=service_campus_key,
                    service_type=service_data.service_type
                )
                db.add(svc_type)

        if service_data.target_population is not None:
            target = db.query(TargetPopulation).filter(
                TargetPopulation.service_campus_key == service_campus_key
            ).first()
            if target:
                target.target_population = service_data.target_population
            else:
                target = TargetPopulation(
                    service_campus_key=service_campus_key,
                    target_population=service_data.target_population
                )
                db.add(target)

        if service_data.workforce_type is not None:
            workforce = db.query(WorkforceType).filter(
                WorkforceType.service_campus_key == service_campus_key
            ).first()
            if workforce:
                workforce.workforce_type = service_data.workforce_type
            else:
                workforce = WorkforceType(
                    service_campus_key=service_campus_key,
                    workforce_type=service_data.workforce_type
                )
                db.add(workforce)

        db.commit()

        return build_service_response(service_campus, db)

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{service_campus_key}")
def delete_service_record(service_campus_key: UUID, db: Session = Depends(get_db)):
    """Delete a specific service by its unique service_campus_key"""
    service_campus = db.query(ServiceCampus).filter(
        ServiceCampus.service_campus_key == service_campus_key
    ).first()

    if not service_campus:
        raise HTTPException(status_code=404, detail="Service not found")

    try:
        # Delete related records first
        db.query(Cost).filter(Cost.service_campus_key == service_campus_key).delete()
        db.query(DeliveryMethod).filter(DeliveryMethod.service_campus_key == service_campus_key).delete()
        db.query(LevelOfCare).filter(LevelOfCare.service_campus_key == service_campus_key).delete()
        db.query(ReferralPathway).filter(ReferralPathway.service_campus_key == service_campus_key).delete()
        db.query(ServiceType).filter(ServiceType.service_campus_key == service_campus_key).delete()
        db.query(TargetPopulation).filter(TargetPopulation.service_campus_key == service_campus_key).delete()
        db.query(WorkforceType).filter(WorkforceType.service_campus_key == service_campus_key).delete()

        # Delete the service campus record
        db.delete(service_campus)
        db.commit()

        return {"message": "Service record deleted successfully"}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))