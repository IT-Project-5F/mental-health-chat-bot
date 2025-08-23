-- Create MentalHealthRawData table
CREATE TABLE IF NOT EXISTS MentalHealthRawData (
  id SERIAL PRIMARY KEY,
  organisation_name TEXT,
  campus_name TEXT,
  service_name TEXT,
  region_name TEXT,
  email VARCHAR(255),
  phone VARCHAR(255),
  website TEXT,
  notes TEXT,
  expected_wait_time TEXT,
  opening_hours_24_7 BOOL,
  opening_hours_standard BOOL,
  opening_hours_extended BOOL,
  op_hours_extended_details TEXT,
  address TEXT,
  suburb TEXT,
  state TEXT,
  postcode VARCHAR(10),
  cost TEXT,
  delivery_method TEXT,
  level_of_care TEXT,
  referral_pathway TEXT,
  service_type TEXT,
  target_population TEXT,
  work_force_type TEXT
);

-- Create MentalHealthEmbeddings table
CREATE TABLE IF NOT EXISTS MentalHealthEmbeddings (
  id SERIAL PRIMARY KEY,
  record_index INTEGER,
  tokens INTEGER,
  embedding vector(1536)
);

-- Create index for vector similarity search
CREATE INDEX IF NOT EXISTS embedding_idx ON MentalHealthEmbeddings USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);