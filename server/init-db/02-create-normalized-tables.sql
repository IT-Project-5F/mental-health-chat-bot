-- Create Organisation table
CREATE TABLE IF NOT EXISTS organisation (
    organisation_key UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organisation_name VARCHAR(255) NOT NULL
);

-- Create Region table
CREATE TABLE IF NOT EXISTS region (
    region_key UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    region_name VARCHAR(255) NOT NULL
);

-- Create Service table
CREATE TABLE IF NOT EXISTS service (
    service_key UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organisation_key UUID NOT NULL REFERENCES organisation(organisation_key),
    service_name VARCHAR(255) NOT NULL
);

-- Create Campus table
CREATE TABLE IF NOT EXISTS campus (
    campus_key UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organisation_key UUID NOT NULL REFERENCES organisation(organisation_key),
    campus_name VARCHAR(255) NOT NULL
);

-- Create ServiceCampus junction table
CREATE TABLE IF NOT EXISTS service_campus (
    service_campus_key UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    service_key UUID NOT NULL REFERENCES service(service_key),
    campus_key UUID NOT NULL REFERENCES campus(campus_key),
    email VARCHAR(255),
    phone VARCHAR(255),
    website TEXT,
    notes TEXT,
    expected_wait_time VARCHAR(255),
    op_hours_24_7 BOOLEAN DEFAULT FALSE,
    op_hours_standard BOOLEAN DEFAULT FALSE,
    op_hours_extended BOOLEAN DEFAULT FALSE,
    op_hours_extended_details TEXT,
    address TEXT,
    suburb VARCHAR(255),
    state VARCHAR(50),
    postcode VARCHAR(10),
    eligibility_and_description TEXT
);

-- Create lookup tables
CREATE TABLE IF NOT EXISTS target_population (
    target_population_key UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    service_campus_key UUID NOT NULL REFERENCES service_campus(service_campus_key),
    target_population VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS level_of_care (
    level_of_care_key UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    service_campus_key UUID NOT NULL REFERENCES service_campus(service_campus_key),
    level_of_care_num INTEGER,
    level_of_care VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS service_type (
    service_type_key UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    service_campus_key UUID NOT NULL REFERENCES service_campus(service_campus_key),
    service_type_num INTEGER,
    service_type VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS cost (
    cost_key UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    service_campus_key UUID NOT NULL REFERENCES service_campus(service_campus_key),
    cost VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS referral_pathway (
    referral_pathway_key UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    service_campus_key UUID NOT NULL REFERENCES service_campus(service_campus_key),
    referral_pathway VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS workforce_type (
    workforce_type_key UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    service_campus_key UUID NOT NULL REFERENCES service_campus(service_campus_key),
    workforce_type VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS delivery_method (
    delivery_method_key UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    service_campus_key UUID NOT NULL REFERENCES service_campus(service_campus_key),
    delivery_method VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS postcode (
    postcode_key UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    region_key UUID NOT NULL REFERENCES region(region_key),
    postcode VARCHAR(10) NOT NULL
);

-- Create ServiceRegion junction table
CREATE TABLE IF NOT EXISTS service_region (
    service_campus_key UUID NOT NULL REFERENCES service_campus(service_campus_key),
    region_key UUID NOT NULL REFERENCES region(region_key),
    PRIMARY KEY (service_campus_key, region_key)
);

-- Create RawRecordStorage table
CREATE TABLE IF NOT EXISTS raw_record_storage (
    raw_record_storage_key UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    csv_record_index INTEGER UNIQUE NOT NULL,
    organisation_key UUID NOT NULL REFERENCES organisation(organisation_key),
    campus_service_key UUID NOT NULL REFERENCES service_campus(service_campus_key),
    region_key UUID REFERENCES region(region_key),
    cost_key UUID REFERENCES cost(cost_key),
    delivery_method_key UUID REFERENCES delivery_method(delivery_method_key),
    level_of_care_key UUID REFERENCES level_of_care(level_of_care_key),
    referral_pathway_key UUID REFERENCES referral_pathway(referral_pathway_key),
    service_type_key UUID REFERENCES service_type(service_type_key),
    target_population_key UUID REFERENCES target_population(target_population_key),
    workforce_type_key UUID REFERENCES workforce_type(workforce_type_key)
);

-- Create EmbeddingStorage table
CREATE TABLE IF NOT EXISTS embedding_table (
    embedding_record_key UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    record_key UUID NOT NULL REFERENCES raw_record_storage(raw_record_storage_key),
    token INTEGER,
    embedding vector(1536)
);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_organisation_name ON organisation(organisation_name);
CREATE INDEX IF NOT EXISTS idx_service_org ON service(organisation_key);
CREATE INDEX IF NOT EXISTS idx_campus_org ON campus(organisation_key);
CREATE INDEX IF NOT EXISTS idx_service_campus_service ON service_campus(service_key);
CREATE INDEX IF NOT EXISTS idx_service_campus_campus ON service_campus(campus_key);
CREATE INDEX IF NOT EXISTS idx_raw_record_csv_index ON raw_record_storage(csv_record_index);
CREATE INDEX IF NOT EXISTS idx_embedding_record ON embedding_table(record_key);

-- Vector similarity search index (create after data insertion)
-- CREATE INDEX IF NOT EXISTS embedding_idx ON embedding_table USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);
