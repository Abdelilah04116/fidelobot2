-- Table categories
CREATE TABLE IF NOT EXISTS categories (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(100) NOT NULL UNIQUE
);

INSERT INTO categories (id, nom) VALUES (1, 'Smartphones');
INSERT INTO categories (id, nom) VALUES (2, 'Laptops');
INSERT INTO categories (id, nom) VALUES (3, 'Tablettes');
INSERT INTO categories (id, nom) VALUES (4, 'Composants PC');
INSERT INTO categories (id, nom) VALUES (5, 'Périphériques');
INSERT INTO categories (id, nom) VALUES (6, 'Audio');
INSERT INTO categories (id, nom) VALUES (7, 'Gaming');
INSERT INTO categories (id, nom) VALUES (8, 'Accessoires');
