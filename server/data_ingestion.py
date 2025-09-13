import pandas as pd
import ast
from sqlalchemy.orm import Session
from database_config import engine, SessionLocal
from models import *


def insert_data(csv_path='mental_health_services_nwmphn_dataset.csv'):
    df = pd.read_csv(csv_path)
    df["index"] = range(1, len(df) + 1)

    session = SessionLocal()
    try:
        # Initialize dictionaries to cache existing records
        organisations = {}
        campuses = {}
        services = {}
        regions = {}
        costs = {}
        delivery_methods = {}
        referral_pathways = {}
        level_of_cares = {}
        service_types = {}
        target_populations = {}
        workforce_types = {}

        for _, row in df.iterrows():
            # Handle Organisation
            org_name = row['organisation_name']
            if org_name not in organisations:
                org = session.query(Organisation).filter_by(organisation_name=org_name).first()
                if not org:
                    org = Organisation(organisation_name=org_name)
                    session.add(org)
                    session.flush()
                organisations[org_name] = org.organisation_key
            org_key = organisations[org_name]

            # Handle Campus
            campus_name = row['campus_name']
            campus_key_name = f"{campus_name}_{org_key}"
            if campus_key_name not in campuses:
                campus = session.query(Campus).filter_by(
                    campus_name=campus_name,
                    organisation_key=org_key
                ).first()
                if not campus:
                    campus = Campus(
                        campus_name=campus_name,
                        organisation_key=org_key
                    )
                    session.add(campus)
                    session.flush()
                campuses[campus_key_name] = campus.campus_key
            campus_key = campuses[campus_key_name]

            # Handle Service
            service_name = row['service_name']
            service_key_name = f"{service_name}_{org_key}"
            if service_key_name not in services:
                service = session.query(Service).filter_by(
                    service_name=service_name,
                    organisation_key=org_key
                ).first()
                if not service:
                    service = Service(
                        service_name=service_name,
                        organisation_key=org_key
                    )
                    session.add(service)
                    session.flush()
                services[service_key_name] = service.service_key
            service_key = services[service_key_name]

            # Handle Region
            region_name = row.get('region_name')
            region_key = None
            if pd.notna(region_name) and region_name:
                if region_name not in regions:
                    region = session.query(Region).filter_by(region_name=region_name).first()
                    if not region:
                        region = Region(region_name=region_name)
                        session.add(region)
                        session.flush()
                    regions[region_name] = region.region_key
                region_key = regions[region_name]

            # Create ServiceCampus record
            service_campus = ServiceCampus(
                service_key=service_key,
                campus_key=campus_key,
                email=row.get('email') if pd.notna(row.get('email')) else None,
                phone=row.get('phone') if pd.notna(row.get('phone')) else None,
                website=row.get('website') if pd.notna(row.get('website')) else None,
                notes=row.get('notes') if pd.notna(row.get('notes')) else None,
                expected_wait_time=row.get('expected_wait_time') if pd.notna(row.get('expected_wait_time')) else None,
                op_hours_24_7=row.get('opening_hours_24_7') == "Yes" if pd.notna(row.get('opening_hours_24_7')) else False,
                op_hours_standard=row.get('opening_hours_standard') == "Yes" if pd.notna(row.get('opening_hours_standard')) else False,
                op_hours_extended=row.get('opening_hours_extended') == "Yes" if pd.notna(row.get('opening_hours_extended')) else False,
                op_hours_extended_details=row.get('op_hours_extended_details') if pd.notna(row.get('op_hours_extended_details')) else None,
                address=row.get('address') if pd.notna(row.get('address')) else None,
                suburb=row.get('suburb') if pd.notna(row.get('suburb')) else None,
                state=row.get('state') if pd.notna(row.get('state')) else None,
                postcode=row.get('postcode') if pd.notna(row.get('postcode')) else None
            )
            session.add(service_campus)
            session.flush()
            sc_key = service_campus.service_campus_key

            # Initialize foreign key variables
            cost_pk = None
            delivery_method_pk = None
            referral_pathway_pk = None
            level_of_care_pk = None
            service_type_pk = None
            target_population_pk = None
            workforce_type_pk = None

            # Handle Cost
            if pd.notna(row.get('cost')) and row.get('cost'):
                cost_value = row['cost']
                cost_key = f"{cost_value}_{sc_key}"
                if cost_key not in costs:
                    cost = session.query(Cost).filter_by(
                        cost=cost_value,
                        service_campus_key=sc_key
                    ).first()
                    if not cost:
                        cost = Cost(service_campus_key=sc_key, cost=cost_value)
                        session.add(cost)
                        session.flush()
                    costs[cost_key] = cost.cost_key
                cost_pk = costs[cost_key]

            # Handle DeliveryMethod
            if pd.notna(row.get('delivery_method')) and row.get('delivery_method'):
                delivery_value = row['delivery_method']
                delivery_key = f"{delivery_value}_{sc_key}"
                if delivery_key not in delivery_methods:
                    delivery_method = session.query(DeliveryMethod).filter_by(
                        delivery_method=delivery_value,
                        service_campus_key=sc_key
                    ).first()
                    if not delivery_method:
                        delivery_method = DeliveryMethod(
                            service_campus_key=sc_key,
                            delivery_method=delivery_value
                        )
                        session.add(delivery_method)
                        session.flush()
                    delivery_methods[delivery_key] = delivery_method.delivery_method_key
                delivery_method_pk = delivery_methods[delivery_key]

            # Handle LevelOfCare
            if pd.notna(row.get('level_of_care')) and row.get('level_of_care'):
                level_value = row['level_of_care']
                level_key = f"{level_value}_{sc_key}"
                if level_key not in level_of_cares:
                    level_of_care = session.query(LevelOfCare).filter_by(
                        level_of_care=level_value,
                        service_campus_key=sc_key
                    ).first()
                    if not level_of_care:
                        level_of_care = LevelOfCare(
                            service_campus_key=sc_key,
                            level_of_care=level_value
                        )
                        session.add(level_of_care)
                        session.flush()
                    level_of_cares[level_key] = level_of_care.level_of_care_key
                level_of_care_pk = level_of_cares[level_key]

            # Handle ReferralPathway
            if pd.notna(row.get('referral_pathway')) and row.get('referral_pathway'):
                referral_value = row['referral_pathway']
                referral_key = f"{referral_value}_{sc_key}"
                if referral_key not in referral_pathways:
                    referral_pathway = session.query(ReferralPathway).filter_by(
                        referral_pathway=referral_value,
                        service_campus_key=sc_key
                    ).first()
                    if not referral_pathway:
                        referral_pathway = ReferralPathway(
                            service_campus_key=sc_key,
                            referral_pathway=referral_value
                        )
                        session.add(referral_pathway)
                        session.flush()
                    referral_pathways[referral_key] = referral_pathway.referral_pathway_key
                referral_pathway_pk = referral_pathways[referral_key]

            # Handle ServiceType
            if pd.notna(row.get('service_type')) and row.get('service_type'):
                service_type_value = row['service_type']
                service_type_key_name = f"{service_type_value}_{sc_key}"
                if service_type_key_name not in service_types:
                    service_type = session.query(ServiceType).filter_by(
                        service_type=service_type_value,
                        service_campus_key=sc_key
                    ).first()
                    if not service_type:
                        service_type = ServiceType(
                            service_campus_key=sc_key,
                            service_type=service_type_value
                        )
                        session.add(service_type)
                        session.flush()
                    service_types[service_type_key_name] = service_type.service_type_key
                service_type_pk = service_types[service_type_key_name]

            # Handle TargetPopulation
            if pd.notna(row.get('target_population')) and row.get('target_population'):
                target_value = row['target_population']
                target_key = f"{target_value}_{sc_key}"
                if target_key not in target_populations:
                    target_population = session.query(TargetPopulation).filter_by(
                        target_population=target_value,
                        service_campus_key=sc_key
                    ).first()
                    if not target_population:
                        target_population = TargetPopulation(
                            service_campus_key=sc_key,
                            target_population=target_value
                        )
                        session.add(target_population)
                        session.flush()
                    target_populations[target_key] = target_population.target_population_key
                target_population_pk = target_populations[target_key]

            # Handle WorkforceType
            if pd.notna(row.get('workforce_type')) and row.get('workforce_type'):
                workforce_value = row['workforce_type']
                workforce_key = f"{workforce_value}_{sc_key}"
                if workforce_key not in workforce_types:
                    workforce_type = session.query(WorkforceType).filter_by(
                        workforce_type=workforce_value,
                        service_campus_key=sc_key
                    ).first()
                    if not workforce_type:
                        workforce_type = WorkforceType(
                            service_campus_key=sc_key,
                            workforce_type=workforce_value
                        )
                        session.add(workforce_type)
                        session.flush()
                    workforce_types[workforce_key] = workforce_type.workforce_type_key
                workforce_type_pk = workforce_types[workforce_key]

            # Create RawRecordStorage record
            raw_record = RawRecordStorage(
                csv_record_index=row['index'],
                organisation_key=org_key,
                campus_service_key=sc_key,
                region_key=region_key,
                cost_key=cost_pk,
                delivery_method_key=delivery_method_pk,
                level_of_care_key=level_of_care_pk,
                referral_pathway_key=referral_pathway_pk,
                service_type_key=service_type_pk,
                target_population_key=target_population_pk,
                workforce_type_key=workforce_type_pk
            )
            session.add(raw_record)

        session.commit()
        print("Data insertion completed successfully!")

    except Exception as e:
        session.rollback()
        print(f"Error inserting CSV: {e}")
        raise
    finally:
        session.close()


def insert_embeddings(embedding_csv_path='mental_health_embedding.csv'):
    df = pd.read_csv(embedding_csv_path)

    with Session(engine) as session:
        for _, row in df.iterrows():
            csv_record_index = row.get('index')

            # Find the corresponding raw record
            csv_raw_record = session.query(RawRecordStorage).filter_by(
                csv_record_index=csv_record_index
            ).first()

            if not csv_raw_record:
                print(f"Warning: No RawRecordStorage found for index {csv_record_index}")
                continue

            # Parse embedding vector
            if isinstance(row['embeddings'], str):
                try:
                    embedding_vector = ast.literal_eval(row['embeddings'])
                except (ValueError, SyntaxError) as e:
                    print(f"Error parsing embedding for index {csv_record_index}: {e}")
                    continue
            else:
                embedding_vector = row['embeddings']

            # Create embedding record
            insert_embedding = EmbeddingStorage(
                record_key=csv_raw_record.raw_record_storage_key,
                token=row['token_len'],
                embedding=embedding_vector
            )
            session.add(insert_embedding)

        try:
            session.commit()
            print("Embedding insertion completed successfully!")
        except Exception as e:
            session.rollback()
            print(f"Error inserting embeddings: {e}")
            raise


def create_embedding_index():
    with Session(engine) as session:
        try:
            session.execute(text("CREATE INDEX IF NOT EXISTS embedding_idx ON embedding_table USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);"))
            session.execute(text("ANALYZE embedding_table;"))
            session.commit()
            print("Index creation completed successfully!")
        except Exception as e:
            session.rollback()
            print(f"Error creating index: {e}")
            raise


if __name__ == "__main__":
    # Create all tables
    Base.metadata.create_all(bind=engine)

    # Insert data
    insert_data()
    insert_embeddings()
    create_embedding_index()