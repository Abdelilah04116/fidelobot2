-- Table panier_produits
CREATE TABLE IF NOT EXISTS panier_produits (
    id SERIAL PRIMARY KEY,
    panier_id INTEGER REFERENCES paniers(id),
    produit_id INTEGER REFERENCES produits(id),
    quantite INTEGER DEFAULT 1
);

INSERT INTO panier_produits (id, panier_id, produit_id, quantite) 
VALUES (1, 63, 78, 2);
INSERT INTO panier_produits (id, panier_id, produit_id, quantite) 
VALUES (2, 54, 35, 1);
INSERT INTO panier_produits (id, panier_id, produit_id, quantite) 
VALUES (3, 97, 66, 1);
INSERT INTO panier_produits (id, panier_id, produit_id, quantite) 
VALUES (4, 45, 56, 1);
INSERT INTO panier_produits (id, panier_id, produit_id, quantite) 
VALUES (5, 37, 87, 3);
INSERT INTO panier_produits (id, panier_id, produit_id, quantite) 
VALUES (6, 76, 63, 3);
INSERT INTO panier_produits (id, panier_id, produit_id, quantite) 
VALUES (7, 86, 40, 1);
INSERT INTO panier_produits (id, panier_id, produit_id, quantite) 
VALUES (8, 29, 51, 3);
INSERT INTO panier_produits (id, panier_id, produit_id, quantite) 
VALUES (9, 8, 1, 1);
INSERT INTO panier_produits (id, panier_id, produit_id, quantite) 
VALUES (10, 39, 28, 1);
INSERT INTO panier_produits (id, panier_id, produit_id, quantite) 
VALUES (11, 98, 33, 2);
INSERT INTO panier_produits (id, panier_id, produit_id, quantite) 
VALUES (12, 42, 16, 1);
INSERT INTO panier_produits (id, panier_id, produit_id, quantite) 
VALUES (13, 64, 96, 2);
INSERT INTO panier_produits (id, panier_id, produit_id, quantite) 
VALUES (14, 23, 17, 2);
INSERT INTO panier_produits (id, panier_id, produit_id, quantite) 
VALUES (15, 69, 91, 1);
INSERT INTO panier_produits (id, panier_id, produit_id, quantite) 
VALUES (16, 65, 72, 3);
INSERT INTO panier_produits (id, panier_id, produit_id, quantite) 
VALUES (17, 46, 10, 2);
INSERT INTO panier_produits (id, panier_id, produit_id, quantite) 
VALUES (18, 95, 6, 2);
INSERT INTO panier_produits (id, panier_id, produit_id, quantite) 
VALUES (19, 3, 59, 1);
INSERT INTO panier_produits (id, panier_id, produit_id, quantite) 
VALUES (20, 41, 74, 2);
INSERT INTO panier_produits (id, panier_id, produit_id, quantite) 
VALUES (21, 74, 52, 3);
INSERT INTO panier_produits (id, panier_id, produit_id, quantite) 
VALUES (22, 82, 54, 2);
INSERT INTO panier_produits (id, panier_id, produit_id, quantite) 
VALUES (23, 15, 52, 1);
INSERT INTO panier_produits (id, panier_id, produit_id, quantite) 
VALUES (24, 42, 22, 3);
INSERT INTO panier_produits (id, panier_id, produit_id, quantite) 
VALUES (25, 59, 89, 2);
INSERT INTO panier_produits (id, panier_id, produit_id, quantite) 
VALUES (26, 12, 56, 1);
INSERT INTO panier_produits (id, panier_id, produit_id, quantite) 
VALUES (27, 32, 56, 3);
INSERT INTO panier_produits (id, panier_id, produit_id, quantite) 
VALUES (28, 52, 68, 1);
INSERT INTO panier_produits (id, panier_id, produit_id, quantite) 
VALUES (29, 51, 40, 3);
INSERT INTO panier_produits (id, panier_id, produit_id, quantite) 
VALUES (30, 44, 29, 2);
INSERT INTO panier_produits (id, panier_id, produit_id, quantite) 
VALUES (31, 100, 22, 1);
INSERT INTO panier_produits (id, panier_id, produit_id, quantite) 
VALUES (32, 66, 82, 1);
INSERT INTO panier_produits (id, panier_id, produit_id, quantite) 
VALUES (33, 68, 66, 1);
INSERT INTO panier_produits (id, panier_id, produit_id, quantite) 
VALUES (34, 100, 45, 2);
INSERT INTO panier_produits (id, panier_id, produit_id, quantite) 
VALUES (35, 94, 83, 1);
INSERT INTO panier_produits (id, panier_id, produit_id, quantite) 
VALUES (36, 31, 14, 1);
INSERT INTO panier_produits (id, panier_id, produit_id, quantite) 
VALUES (37, 33, 26, 1);
INSERT INTO panier_produits (id, panier_id, produit_id, quantite) 
VALUES (38, 78, 20, 3);
INSERT INTO panier_produits (id, panier_id, produit_id, quantite) 
VALUES (39, 10, 23, 3);
INSERT INTO panier_produits (id, panier_id, produit_id, quantite) 
VALUES (40, 64, 60, 3);
INSERT INTO panier_produits (id, panier_id, produit_id, quantite) 
VALUES (41, 98, 75, 2);
INSERT INTO panier_produits (id, panier_id, produit_id, quantite) 
VALUES (42, 88, 73, 3);
INSERT INTO panier_produits (id, panier_id, produit_id, quantite) 
VALUES (43, 82, 80, 2);
INSERT INTO panier_produits (id, panier_id, produit_id, quantite) 
VALUES (44, 81, 41, 1);
INSERT INTO panier_produits (id, panier_id, produit_id, quantite) 
VALUES (45, 57, 9, 2);
INSERT INTO panier_produits (id, panier_id, produit_id, quantite) 
VALUES (46, 57, 81, 2);
INSERT INTO panier_produits (id, panier_id, produit_id, quantite) 
VALUES (47, 36, 76, 1);
INSERT INTO panier_produits (id, panier_id, produit_id, quantite) 
VALUES (48, 46, 65, 1);
INSERT INTO panier_produits (id, panier_id, produit_id, quantite) 
VALUES (49, 40, 60, 2);
INSERT INTO panier_produits (id, panier_id, produit_id, quantite) 
VALUES (50, 5, 8, 2);
INSERT INTO panier_produits (id, panier_id, produit_id, quantite) 
VALUES (51, 37, 10, 3);
INSERT INTO panier_produits (id, panier_id, produit_id, quantite) 
VALUES (52, 12, 79, 3);
INSERT INTO panier_produits (id, panier_id, produit_id, quantite) 
VALUES (53, 65, 50, 2);
INSERT INTO panier_produits (id, panier_id, produit_id, quantite) 
VALUES (54, 75, 71, 3);
INSERT INTO panier_produits (id, panier_id, produit_id, quantite) 
VALUES (55, 6, 58, 3);
INSERT INTO panier_produits (id, panier_id, produit_id, quantite) 
VALUES (56, 84, 25, 2);
INSERT INTO panier_produits (id, panier_id, produit_id, quantite) 
VALUES (57, 78, 61, 3);
INSERT INTO panier_produits (id, panier_id, produit_id, quantite) 
VALUES (58, 20, 8, 2);
INSERT INTO panier_produits (id, panier_id, produit_id, quantite) 
VALUES (59, 14, 44, 3);
INSERT INTO panier_produits (id, panier_id, produit_id, quantite) 
VALUES (60, 11, 65, 3);
INSERT INTO panier_produits (id, panier_id, produit_id, quantite) 
VALUES (61, 23, 6, 1);
INSERT INTO panier_produits (id, panier_id, produit_id, quantite) 
VALUES (62, 91, 57, 2);
INSERT INTO panier_produits (id, panier_id, produit_id, quantite) 
VALUES (63, 68, 67, 3);
INSERT INTO panier_produits (id, panier_id, produit_id, quantite) 
VALUES (64, 21, 47, 2);
INSERT INTO panier_produits (id, panier_id, produit_id, quantite) 
VALUES (65, 37, 50, 2);
INSERT INTO panier_produits (id, panier_id, produit_id, quantite) 
VALUES (66, 100, 44, 3);
INSERT INTO panier_produits (id, panier_id, produit_id, quantite) 
VALUES (67, 77, 7, 3);
INSERT INTO panier_produits (id, panier_id, produit_id, quantite) 
VALUES (68, 83, 43, 1);
INSERT INTO panier_produits (id, panier_id, produit_id, quantite) 
VALUES (69, 43, 13, 3);
INSERT INTO panier_produits (id, panier_id, produit_id, quantite) 
VALUES (70, 87, 50, 2);
INSERT INTO panier_produits (id, panier_id, produit_id, quantite) 
VALUES (71, 33, 93, 3);
INSERT INTO panier_produits (id, panier_id, produit_id, quantite) 
VALUES (72, 78, 20, 2);
INSERT INTO panier_produits (id, panier_id, produit_id, quantite) 
VALUES (73, 11, 75, 3);
INSERT INTO panier_produits (id, panier_id, produit_id, quantite) 
VALUES (74, 19, 45, 2);
INSERT INTO panier_produits (id, panier_id, produit_id, quantite) 
VALUES (75, 84, 90, 3);
INSERT INTO panier_produits (id, panier_id, produit_id, quantite) 
VALUES (76, 51, 17, 3);
INSERT INTO panier_produits (id, panier_id, produit_id, quantite) 
VALUES (77, 91, 11, 2);
INSERT INTO panier_produits (id, panier_id, produit_id, quantite) 
VALUES (78, 72, 49, 3);
INSERT INTO panier_produits (id, panier_id, produit_id, quantite) 
VALUES (79, 43, 17, 3);
INSERT INTO panier_produits (id, panier_id, produit_id, quantite) 
VALUES (80, 90, 95, 3);
INSERT INTO panier_produits (id, panier_id, produit_id, quantite) 
VALUES (81, 68, 12, 3);
INSERT INTO panier_produits (id, panier_id, produit_id, quantite) 
VALUES (82, 86, 55, 3);
INSERT INTO panier_produits (id, panier_id, produit_id, quantite) 
VALUES (83, 47, 3, 2);
INSERT INTO panier_produits (id, panier_id, produit_id, quantite) 
VALUES (84, 40, 24, 1);
INSERT INTO panier_produits (id, panier_id, produit_id, quantite) 
VALUES (85, 44, 99, 2);
INSERT INTO panier_produits (id, panier_id, produit_id, quantite) 
VALUES (86, 25, 29, 1);
INSERT INTO panier_produits (id, panier_id, produit_id, quantite) 
VALUES (87, 20, 10, 2);
INSERT INTO panier_produits (id, panier_id, produit_id, quantite) 
VALUES (88, 13, 65, 3);
INSERT INTO panier_produits (id, panier_id, produit_id, quantite) 
VALUES (89, 95, 68, 1);
INSERT INTO panier_produits (id, panier_id, produit_id, quantite) 
VALUES (90, 85, 44, 3);
INSERT INTO panier_produits (id, panier_id, produit_id, quantite) 
VALUES (91, 17, 77, 2);
INSERT INTO panier_produits (id, panier_id, produit_id, quantite) 
VALUES (92, 20, 21, 1);
INSERT INTO panier_produits (id, panier_id, produit_id, quantite) 
VALUES (93, 89, 99, 3);
INSERT INTO panier_produits (id, panier_id, produit_id, quantite) 
VALUES (94, 22, 93, 2);
INSERT INTO panier_produits (id, panier_id, produit_id, quantite) 
VALUES (95, 6, 53, 2);
INSERT INTO panier_produits (id, panier_id, produit_id, quantite) 
VALUES (96, 87, 93, 1);
INSERT INTO panier_produits (id, panier_id, produit_id, quantite) 
VALUES (97, 57, 79, 2);
INSERT INTO panier_produits (id, panier_id, produit_id, quantite) 
VALUES (98, 97, 96, 2);
INSERT INTO panier_produits (id, panier_id, produit_id, quantite) 
VALUES (99, 30, 69, 1);
INSERT INTO panier_produits (id, panier_id, produit_id, quantite) 
VALUES (100, 40, 61, 1);
