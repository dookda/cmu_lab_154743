CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS postgis_raster;
CREATE EXTENSION IF NOT EXISTS postgis_topology;

CREATE SCHEMA IF NOT EXISTS workshop AUTHORIZATION CURRENT_USER;
SET search_path TO workshop, public;

DROP TABLE IF EXISTS poi CASCADE;
CREATE TABLE poi (
    id   BIGSERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    category TEXT,
    geom GEOMETRY(Point, 4326) NOT NULL,
    CONSTRAINT poi_geom_valid CHECK (ST_IsValid(geom))
);
CREATE INDEX poi_gix ON poi USING GIST (geom);

DROP TABLE IF EXISTS districts CASCADE;
CREATE TABLE districts (
    id   BIGSERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    geom GEOMETRY(MultiPolygon, 4326) NOT NULL,
    CONSTRAINT districts_geom_valid CHECK (ST_IsValid(geom))
);
CREATE INDEX districts_gix ON districts USING GIST (geom);

INSERT INTO poi (name, category, geom) VALUES
('Cafe A', 'cafe', ST_SetSRID(ST_Point(98.9800, 18.7900), 4326)),
('Clinic B', 'clinic', ST_SetSRID(ST_Point(98.9850, 18.7925), 4326));

INSERT INTO districts (name, geom) VALUES
('Demo District', ST_Multi(
    ST_SetSRID(
        ST_GeomFromText('POLYGON((98.975 18.785, 98.995 18.785, 98.995 18.800, 98.975 18.800, 98.975 18.785))'), 4326
    )
));