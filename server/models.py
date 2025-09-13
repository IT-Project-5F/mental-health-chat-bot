import uuid
from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from pgvector.sqlalchemy import Vector

Base = declarative_base()


class EmbeddingStorage(Base):
    __tablename__ = "embedding_table"
    embedding_record_key = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    record_key           = Column(UUID(as_uuid=True), ForeignKey("raw_record_storage.raw_record_storage_key"), nullable=False)
    token                = Column(Integer)
    embedding            = Column(Vector(1536))


class RawRecordStorage(Base):
    __tablename__ = "raw_record_storage"

    raw_record_storage_key = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    csv_record_index       = Column(Integer, unique=True, nullable=False)
    organisation_key       = Column(UUID(as_uuid=True), ForeignKey("organisation.organisation_key"), nullable=False)
    campus_service_key     = Column(UUID(as_uuid=True), ForeignKey("service_campus.service_campus_key"), nullable=False)
    region_key             = Column(UUID(as_uuid=True), ForeignKey("region.region_key"), nullable=True)
    cost_key               = Column(UUID(as_uuid=True), ForeignKey("cost.cost_key"), nullable=True)
    delivery_method_key    = Column(UUID(as_uuid=True), ForeignKey("delivery_method.delivery_method_key"), nullable=True)
    level_of_care_key      = Column(UUID(as_uuid=True), ForeignKey("level_of_care.level_of_care_key"), nullable=True)
    referral_pathway_key   = Column(UUID(as_uuid=True), ForeignKey("referral_pathway.referral_pathway_key"), nullable=True)
    service_type_key       = Column(UUID(as_uuid=True), ForeignKey("service_type.service_type_key"), nullable=True)
    target_population_key  = Column(UUID(as_uuid=True), ForeignKey("target_population.target_population_key"), nullable=True)
    workforce_type_key     = Column(UUID(as_uuid=True), ForeignKey("workforce_type.workforce_type_key"), nullable=True)


class Organisation(Base):
    __tablename__ = "organisation"

    organisation_key  = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organisation_name = Column(String, nullable=False)


class Service(Base):
    __tablename__ = "service"

    service_key       = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organisation_key  = Column(UUID(as_uuid=True), ForeignKey("organisation.organisation_key"), nullable=False)
    service_name      = Column(String, nullable=False)


class Campus(Base):
    __tablename__ = "campus"

    campus_key        = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organisation_key  = Column(UUID(as_uuid=True), ForeignKey("organisation.organisation_key"), nullable=False)
    campus_name       = Column(String, nullable=False)


class ServiceCampus(Base):
    __tablename__ = "service_campus"

    service_campus_key         = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    service_key                = Column(UUID(as_uuid=True), ForeignKey("service.service_key"), nullable=False)
    campus_key                 = Column(UUID(as_uuid=True), ForeignKey("campus.campus_key"), nullable=False)
    email                      = Column(String)
    phone                      = Column(String)
    website                    = Column(String)
    notes                      = Column(String)
    expected_wait_time          = Column(String)
    op_hours_24_7               = Column(Boolean)
    op_hours_standard           = Column(Boolean)
    op_hours_extended           = Column(Boolean)
    op_hours_extended_details   = Column(String)
    address                     = Column(String)
    suburb                      = Column(String)
    state                       = Column(String)
    postcode                    = Column(String)
    eligibility_and_description = Column(String)


class TargetPopulation(Base):
    __tablename__ = "target_population"

    target_population_key = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    service_campus_key    = Column(UUID(as_uuid=True), ForeignKey("service_campus.service_campus_key"), nullable=False)
    target_population     = Column(String)


class LevelOfCare(Base):
    __tablename__ = "level_of_care"

    level_of_care_key  = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    service_campus_key = Column(UUID(as_uuid=True), ForeignKey("service_campus.service_campus_key"), nullable=False)
    level_of_care_num  = Column(Integer)
    level_of_care      = Column(String)


class ServiceType(Base):
    __tablename__ = "service_type"

    service_type_key   = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    service_campus_key = Column(UUID(as_uuid=True), ForeignKey("service_campus.service_campus_key"), nullable=False)
    service_type_num   = Column(Integer)
    service_type       = Column(String)


class Cost(Base):
    __tablename__ = "cost"

    cost_key           = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    service_campus_key = Column(UUID(as_uuid=True), ForeignKey("service_campus.service_campus_key"), nullable=False)
    cost               = Column(String, nullable=False)


class ReferralPathway(Base):
    __tablename__ = "referral_pathway"

    referral_pathway_key = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    service_campus_key   = Column(UUID(as_uuid=True), ForeignKey("service_campus.service_campus_key"), nullable=False)
    referral_pathway     = Column(String, nullable=False)


class WorkforceType(Base):
    __tablename__ = "workforce_type"

    workforce_type_key  = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    service_campus_key  = Column(UUID(as_uuid=True), ForeignKey("service_campus.service_campus_key"), nullable=False)
    workforce_type      = Column(String, nullable=False)


class DeliveryMethod(Base):
    __tablename__ = "delivery_method"

    delivery_method_key  = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    service_campus_key   = Column(UUID(as_uuid=True), ForeignKey("service_campus.service_campus_key"), nullable=False)
    delivery_method      = Column(String, nullable=False)


class Postcode(Base):
    __tablename__ = "postcode"

    postcode_key = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    region_key   = Column(UUID(as_uuid=True), ForeignKey("region.region_key"), nullable=False)
    postcode     = Column(String, nullable=False)


class ServiceRegion(Base):
    __tablename__ = "service_region"

    service_campus_key = Column(UUID(as_uuid=True), ForeignKey("service_campus.service_campus_key"), primary_key=True)
    region_key         = Column(UUID(as_uuid=True), ForeignKey("region.region_key"), primary_key=True)


class Region(Base):
    __tablename__ = "region"

    region_key  = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    region_name = Column(String, nullable=False)