CREATE TABLE IF NOT EXISTS products (
    id VARCHAR(26) PRIMARY KEY,
    name VARCHAR(200) UNIQUE NOT NULL,
    description TEXT NULL,
    price NUMERIC(10, 2) NOT NULL,
    quantity INTEGER NOT NULL,
    active BOOLEAN NOT NULL DEFAULT TRUE,

    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NULL
);

CREATE INDEX IF NOT EXISTS products_name_idx ON products (name);