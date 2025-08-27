-- Table commande_produits
CREATE TABLE IF NOT EXISTS commande_produits (
    id SERIAL PRIMARY KEY,
    commande_id INTEGER REFERENCES commandes(id),
    produit_id INTEGER REFERENCES produits(id),
    quantite INTEGER DEFAULT 1,
    prix_unitaire DECIMAL(10,2) NOT NULL
);

INSERT INTO commande_produits (id, commande_id, produit_id, quantite, prix_unitaire) 
VALUES (1, 92, 38, 5, 1072.85);
INSERT INTO commande_produits (id, commande_id, produit_id, quantite, prix_unitaire) 
VALUES (2, 54, 62, 4, 403.41);
INSERT INTO commande_produits (id, commande_id, produit_id, quantite, prix_unitaire) 
VALUES (3, 71, 19, 4, 326.39);
INSERT INTO commande_produits (id, commande_id, produit_id, quantite, prix_unitaire) 
VALUES (4, 77, 66, 2, 1302.84);
INSERT INTO commande_produits (id, commande_id, produit_id, quantite, prix_unitaire) 
VALUES (5, 36, 99, 4, 542.82);
INSERT INTO commande_produits (id, commande_id, produit_id, quantite, prix_unitaire) 
VALUES (6, 65, 35, 1, 460.12);
INSERT INTO commande_produits (id, commande_id, produit_id, quantite, prix_unitaire) 
VALUES (7, 39, 76, 5, 1498.41);
INSERT INTO commande_produits (id, commande_id, produit_id, quantite, prix_unitaire) 
VALUES (8, 63, 20, 4, 830.94);
INSERT INTO commande_produits (id, commande_id, produit_id, quantite, prix_unitaire) 
VALUES (9, 45, 43, 5, 1156.17);
INSERT INTO commande_produits (id, commande_id, produit_id, quantite, prix_unitaire) 
VALUES (10, 49, 59, 3, 1310.92);
INSERT INTO commande_produits (id, commande_id, produit_id, quantite, prix_unitaire) 
VALUES (11, 90, 31, 5, 605.31);
INSERT INTO commande_produits (id, commande_id, produit_id, quantite, prix_unitaire) 
VALUES (12, 100, 53, 1, 511.36);
INSERT INTO commande_produits (id, commande_id, produit_id, quantite, prix_unitaire) 
VALUES (13, 61, 91, 4, 609.81);
INSERT INTO commande_produits (id, commande_id, produit_id, quantite, prix_unitaire) 
VALUES (14, 85, 84, 2, 768.23);
INSERT INTO commande_produits (id, commande_id, produit_id, quantite, prix_unitaire) 
VALUES (15, 5, 17, 5, 1449.76);
INSERT INTO commande_produits (id, commande_id, produit_id, quantite, prix_unitaire) 
VALUES (16, 43, 13, 4, 194.58);
INSERT INTO commande_produits (id, commande_id, produit_id, quantite, prix_unitaire) 
VALUES (17, 59, 2, 2, 644.47);
INSERT INTO commande_produits (id, commande_id, produit_id, quantite, prix_unitaire) 
VALUES (18, 84, 20, 1, 730.76);
INSERT INTO commande_produits (id, commande_id, produit_id, quantite, prix_unitaire) 
VALUES (19, 34, 44, 5, 1054.42);
INSERT INTO commande_produits (id, commande_id, produit_id, quantite, prix_unitaire) 
VALUES (20, 84, 11, 3, 1285.89);
INSERT INTO commande_produits (id, commande_id, produit_id, quantite, prix_unitaire) 
VALUES (21, 69, 49, 3, 958.86);
INSERT INTO commande_produits (id, commande_id, produit_id, quantite, prix_unitaire) 
VALUES (22, 98, 63, 5, 102.05);
INSERT INTO commande_produits (id, commande_id, produit_id, quantite, prix_unitaire) 
VALUES (23, 9, 31, 3, 1496.27);
INSERT INTO commande_produits (id, commande_id, produit_id, quantite, prix_unitaire) 
VALUES (24, 96, 12, 4, 1468.59);
INSERT INTO commande_produits (id, commande_id, produit_id, quantite, prix_unitaire) 
VALUES (25, 98, 82, 1, 693.33);
INSERT INTO commande_produits (id, commande_id, produit_id, quantite, prix_unitaire) 
VALUES (26, 89, 39, 1, 116.69);
INSERT INTO commande_produits (id, commande_id, produit_id, quantite, prix_unitaire) 
VALUES (27, 8, 38, 3, 593.52);
INSERT INTO commande_produits (id, commande_id, produit_id, quantite, prix_unitaire) 
VALUES (28, 19, 32, 5, 647.48);
INSERT INTO commande_produits (id, commande_id, produit_id, quantite, prix_unitaire) 
VALUES (29, 88, 24, 2, 303.85);
INSERT INTO commande_produits (id, commande_id, produit_id, quantite, prix_unitaire) 
VALUES (30, 79, 49, 5, 1040.55);
INSERT INTO commande_produits (id, commande_id, produit_id, quantite, prix_unitaire) 
VALUES (31, 64, 75, 2, 386.67);
INSERT INTO commande_produits (id, commande_id, produit_id, quantite, prix_unitaire) 
VALUES (32, 82, 33, 4, 420.22);
INSERT INTO commande_produits (id, commande_id, produit_id, quantite, prix_unitaire) 
VALUES (33, 2, 60, 3, 1032.54);
INSERT INTO commande_produits (id, commande_id, produit_id, quantite, prix_unitaire) 
VALUES (34, 21, 10, 4, 1420.59);
INSERT INTO commande_produits (id, commande_id, produit_id, quantite, prix_unitaire) 
VALUES (35, 76, 39, 4, 1050.95);
INSERT INTO commande_produits (id, commande_id, produit_id, quantite, prix_unitaire) 
VALUES (36, 59, 39, 2, 1499.09);
INSERT INTO commande_produits (id, commande_id, produit_id, quantite, prix_unitaire) 
VALUES (37, 62, 14, 2, 602.98);
INSERT INTO commande_produits (id, commande_id, produit_id, quantite, prix_unitaire) 
VALUES (38, 46, 74, 3, 1489.40);
INSERT INTO commande_produits (id, commande_id, produit_id, quantite, prix_unitaire) 
VALUES (39, 38, 3, 4, 448.00);
INSERT INTO commande_produits (id, commande_id, produit_id, quantite, prix_unitaire) 
VALUES (40, 73, 88, 1, 1370.39);
INSERT INTO commande_produits (id, commande_id, produit_id, quantite, prix_unitaire) 
VALUES (41, 96, 64, 3, 1174.82);
INSERT INTO commande_produits (id, commande_id, produit_id, quantite, prix_unitaire) 
VALUES (42, 30, 78, 3, 367.56);
INSERT INTO commande_produits (id, commande_id, produit_id, quantite, prix_unitaire) 
VALUES (43, 25, 80, 3, 1032.76);
INSERT INTO commande_produits (id, commande_id, produit_id, quantite, prix_unitaire) 
VALUES (44, 93, 99, 2, 960.96);
INSERT INTO commande_produits (id, commande_id, produit_id, quantite, prix_unitaire) 
VALUES (45, 81, 83, 1, 497.95);
INSERT INTO commande_produits (id, commande_id, produit_id, quantite, prix_unitaire) 
VALUES (46, 57, 5, 5, 579.05);
INSERT INTO commande_produits (id, commande_id, produit_id, quantite, prix_unitaire) 
VALUES (47, 17, 12, 3, 523.74);
INSERT INTO commande_produits (id, commande_id, produit_id, quantite, prix_unitaire) 
VALUES (48, 54, 23, 2, 241.63);
INSERT INTO commande_produits (id, commande_id, produit_id, quantite, prix_unitaire) 
VALUES (49, 70, 47, 5, 777.60);
INSERT INTO commande_produits (id, commande_id, produit_id, quantite, prix_unitaire) 
VALUES (50, 35, 22, 3, 1375.37);
INSERT INTO commande_produits (id, commande_id, produit_id, quantite, prix_unitaire) 
VALUES (51, 62, 38, 3, 1216.14);
INSERT INTO commande_produits (id, commande_id, produit_id, quantite, prix_unitaire) 
VALUES (52, 60, 10, 2, 1143.52);
INSERT INTO commande_produits (id, commande_id, produit_id, quantite, prix_unitaire) 
VALUES (53, 29, 87, 4, 1452.54);
INSERT INTO commande_produits (id, commande_id, produit_id, quantite, prix_unitaire) 
VALUES (54, 72, 47, 1, 1196.49);
INSERT INTO commande_produits (id, commande_id, produit_id, quantite, prix_unitaire) 
VALUES (55, 2, 34, 5, 229.20);
INSERT INTO commande_produits (id, commande_id, produit_id, quantite, prix_unitaire) 
VALUES (56, 48, 87, 3, 897.61);
INSERT INTO commande_produits (id, commande_id, produit_id, quantite, prix_unitaire) 
VALUES (57, 82, 48, 1, 1028.51);
INSERT INTO commande_produits (id, commande_id, produit_id, quantite, prix_unitaire) 
VALUES (58, 61, 4, 5, 1332.14);
INSERT INTO commande_produits (id, commande_id, produit_id, quantite, prix_unitaire) 
VALUES (59, 72, 42, 5, 370.98);
INSERT INTO commande_produits (id, commande_id, produit_id, quantite, prix_unitaire) 
VALUES (60, 9, 82, 4, 1368.61);
INSERT INTO commande_produits (id, commande_id, produit_id, quantite, prix_unitaire) 
VALUES (61, 39, 84, 4, 219.18);
INSERT INTO commande_produits (id, commande_id, produit_id, quantite, prix_unitaire) 
VALUES (62, 6, 5, 3, 1494.09);
INSERT INTO commande_produits (id, commande_id, produit_id, quantite, prix_unitaire) 
VALUES (63, 15, 13, 2, 1336.53);
INSERT INTO commande_produits (id, commande_id, produit_id, quantite, prix_unitaire) 
VALUES (64, 18, 50, 4, 587.97);
INSERT INTO commande_produits (id, commande_id, produit_id, quantite, prix_unitaire) 
VALUES (65, 96, 90, 5, 657.73);
INSERT INTO commande_produits (id, commande_id, produit_id, quantite, prix_unitaire) 
VALUES (66, 96, 94, 2, 1333.85);
INSERT INTO commande_produits (id, commande_id, produit_id, quantite, prix_unitaire) 
VALUES (67, 84, 13, 4, 942.70);
INSERT INTO commande_produits (id, commande_id, produit_id, quantite, prix_unitaire) 
VALUES (68, 36, 5, 3, 365.04);
INSERT INTO commande_produits (id, commande_id, produit_id, quantite, prix_unitaire) 
VALUES (69, 57, 31, 3, 194.06);
INSERT INTO commande_produits (id, commande_id, produit_id, quantite, prix_unitaire) 
VALUES (70, 88, 48, 5, 1357.46);
INSERT INTO commande_produits (id, commande_id, produit_id, quantite, prix_unitaire) 
VALUES (71, 83, 46, 1, 627.30);
INSERT INTO commande_produits (id, commande_id, produit_id, quantite, prix_unitaire) 
VALUES (72, 25, 16, 4, 182.93);
INSERT INTO commande_produits (id, commande_id, produit_id, quantite, prix_unitaire) 
VALUES (73, 28, 83, 5, 1458.09);
INSERT INTO commande_produits (id, commande_id, produit_id, quantite, prix_unitaire) 
VALUES (74, 7, 43, 2, 1483.79);
INSERT INTO commande_produits (id, commande_id, produit_id, quantite, prix_unitaire) 
VALUES (75, 73, 27, 1, 1253.24);
INSERT INTO commande_produits (id, commande_id, produit_id, quantite, prix_unitaire) 
VALUES (76, 71, 27, 5, 363.13);
INSERT INTO commande_produits (id, commande_id, produit_id, quantite, prix_unitaire) 
VALUES (77, 30, 43, 2, 1193.53);
INSERT INTO commande_produits (id, commande_id, produit_id, quantite, prix_unitaire) 
VALUES (78, 77, 1, 3, 1294.69);
INSERT INTO commande_produits (id, commande_id, produit_id, quantite, prix_unitaire) 
VALUES (79, 19, 17, 5, 413.45);
INSERT INTO commande_produits (id, commande_id, produit_id, quantite, prix_unitaire) 
VALUES (80, 23, 15, 1, 241.11);
INSERT INTO commande_produits (id, commande_id, produit_id, quantite, prix_unitaire) 
VALUES (81, 46, 31, 5, 519.47);
INSERT INTO commande_produits (id, commande_id, produit_id, quantite, prix_unitaire) 
VALUES (82, 23, 34, 1, 233.80);
INSERT INTO commande_produits (id, commande_id, produit_id, quantite, prix_unitaire) 
VALUES (83, 54, 68, 1, 1131.21);
INSERT INTO commande_produits (id, commande_id, produit_id, quantite, prix_unitaire) 
VALUES (84, 61, 58, 3, 794.20);
INSERT INTO commande_produits (id, commande_id, produit_id, quantite, prix_unitaire) 
VALUES (85, 14, 58, 5, 371.25);
INSERT INTO commande_produits (id, commande_id, produit_id, quantite, prix_unitaire) 
VALUES (86, 79, 6, 5, 487.36);
INSERT INTO commande_produits (id, commande_id, produit_id, quantite, prix_unitaire) 
VALUES (87, 83, 4, 1, 1497.95);
INSERT INTO commande_produits (id, commande_id, produit_id, quantite, prix_unitaire) 
VALUES (88, 52, 55, 1, 760.89);
INSERT INTO commande_produits (id, commande_id, produit_id, quantite, prix_unitaire) 
VALUES (89, 57, 10, 1, 517.06);
INSERT INTO commande_produits (id, commande_id, produit_id, quantite, prix_unitaire) 
VALUES (90, 19, 9, 2, 448.77);
INSERT INTO commande_produits (id, commande_id, produit_id, quantite, prix_unitaire) 
VALUES (91, 82, 75, 5, 1082.62);
INSERT INTO commande_produits (id, commande_id, produit_id, quantite, prix_unitaire) 
VALUES (92, 49, 77, 5, 477.60);
INSERT INTO commande_produits (id, commande_id, produit_id, quantite, prix_unitaire) 
VALUES (93, 65, 78, 4, 193.81);
INSERT INTO commande_produits (id, commande_id, produit_id, quantite, prix_unitaire) 
VALUES (94, 90, 15, 5, 1095.22);
INSERT INTO commande_produits (id, commande_id, produit_id, quantite, prix_unitaire) 
VALUES (95, 28, 56, 4, 1337.73);
INSERT INTO commande_produits (id, commande_id, produit_id, quantite, prix_unitaire) 
VALUES (96, 53, 44, 4, 628.16);
INSERT INTO commande_produits (id, commande_id, produit_id, quantite, prix_unitaire) 
VALUES (97, 94, 13, 3, 668.81);
INSERT INTO commande_produits (id, commande_id, produit_id, quantite, prix_unitaire) 
VALUES (98, 86, 33, 3, 1432.71);
INSERT INTO commande_produits (id, commande_id, produit_id, quantite, prix_unitaire) 
VALUES (99, 88, 61, 1, 182.28);
INSERT INTO commande_produits (id, commande_id, produit_id, quantite, prix_unitaire) 
VALUES (100, 11, 12, 4, 190.02);
