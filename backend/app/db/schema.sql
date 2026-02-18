-- PostgreSQL Schema for EcoTwin

CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email TEXT UNIQUE NOT NULL,
    hashed_password TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP WITH TIME ZONE
);

CREATE TABLE IF NOT EXISTS data_sources (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    source_type TEXT NOT NULL, -- 'Gmail', 'Plaid', 'Shelly', etc.
    access_token_encrypted TEXT,
    refresh_token_encrypted TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    last_synced_at TIMESTAMP WITH TIME ZONE
);

CREATE TABLE IF NOT EXISTS activity_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    activity_type TEXT NOT NULL,
    description TEXT,
    carbon_impact FLOAT NOT NULL,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    raw_data_json JSONB -- Anonymized snippet
);

-- Conceptual Graph Model (Neo4j)
/*
Nodes:
(u:User {id: '...'})
(a:Activity {type: 'Travel', carbon: 250})
(v:Vehicle {type: 'Sedan', emissions: 0.2})
(d:Device {name: 'Heating', power: 2.0})

Relationships:
(u)-[:PERFORMED {at: '...'}]->(a)
(a)-[:USED]->(v)
(u)-[:OWNS]->(v)
(u)-[:LIVES_IN]->(h:Home)
(h)-[:CONTAINS]->(d)
*/
