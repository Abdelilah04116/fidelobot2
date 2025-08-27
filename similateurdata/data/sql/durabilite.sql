-- Table durabilite
CREATE TABLE IF NOT EXISTS durabilite (
    id SERIAL PRIMARY KEY,
    produit_id INTEGER REFERENCES produits(id),
    label_ecologique VARCHAR(100),
    certification VARCHAR(100)
);

INSERT INTO durabilite (id, produit_id, label_ecologique, certification) 
VALUES (1, 4, 'EPEAT Silver', 'Cert-7044');
INSERT INTO durabilite (id, produit_id, label_ecologique, certification) 
VALUES (2, 60, 'FSC', 'Cert-3126');
INSERT INTO durabilite (id, produit_id, label_ecologique, certification) 
VALUES (3, 79, 'Energy Star', 'Cert-2077');
INSERT INTO durabilite (id, produit_id, label_ecologique, certification) 
VALUES (4, 40, 'RoHS', 'Cert-8842');
INSERT INTO durabilite (id, produit_id, label_ecologique, certification) 
VALUES (5, 68, 'RoHS', 'Cert-7708');
INSERT INTO durabilite (id, produit_id, label_ecologique, certification) 
VALUES (6, 74, 'Energy Star', 'Cert-3053');
INSERT INTO durabilite (id, produit_id, label_ecologique, certification) 
VALUES (7, 41, 'TCO Certified', 'Cert-2215');
INSERT INTO durabilite (id, produit_id, label_ecologique, certification) 
VALUES (8, 58, 'RoHS', 'Cert-9476');
INSERT INTO durabilite (id, produit_id, label_ecologique, certification) 
VALUES (9, 45, 'EPEAT Gold', 'Cert-3981');
INSERT INTO durabilite (id, produit_id, label_ecologique, certification) 
VALUES (10, 99, 'EPEAT Gold', 'Cert-8088');
INSERT INTO durabilite (id, produit_id, label_ecologique, certification) 
VALUES (11, 65, 'Energy Star', 'Cert-3034');
INSERT INTO durabilite (id, produit_id, label_ecologique, certification) 
VALUES (12, 67, 'EPEAT Gold', 'Cert-5982');
INSERT INTO durabilite (id, produit_id, label_ecologique, certification) 
VALUES (13, 22, 'EPEAT Gold', 'Cert-6286');
INSERT INTO durabilite (id, produit_id, label_ecologique, certification) 
VALUES (14, 91, 'EPEAT Gold', 'Cert-6669');
INSERT INTO durabilite (id, produit_id, label_ecologique, certification) 
VALUES (15, 67, 'EPEAT Silver', 'Cert-2292');
INSERT INTO durabilite (id, produit_id, label_ecologique, certification) 
VALUES (16, 33, 'EPEAT Gold', 'Cert-5496');
INSERT INTO durabilite (id, produit_id, label_ecologique, certification) 
VALUES (17, 17, 'TCO Certified', 'Cert-5961');
INSERT INTO durabilite (id, produit_id, label_ecologique, certification) 
VALUES (18, 79, 'FSC', 'Cert-2530');
INSERT INTO durabilite (id, produit_id, label_ecologique, certification) 
VALUES (19, 65, 'TCO Certified', 'Cert-3762');
INSERT INTO durabilite (id, produit_id, label_ecologique, certification) 
VALUES (20, 76, 'FSC', 'Cert-3526');
INSERT INTO durabilite (id, produit_id, label_ecologique, certification) 
VALUES (21, 22, 'TCO Certified', 'Cert-6531');
INSERT INTO durabilite (id, produit_id, label_ecologique, certification) 
VALUES (22, 73, 'Energy Star', 'Cert-1464');
INSERT INTO durabilite (id, produit_id, label_ecologique, certification) 
VALUES (23, 11, 'Energy Star', 'Cert-5336');
INSERT INTO durabilite (id, produit_id, label_ecologique, certification) 
VALUES (24, 84, 'EPEAT Gold', 'Cert-7825');
INSERT INTO durabilite (id, produit_id, label_ecologique, certification) 
VALUES (25, 80, 'TCO Certified', 'Cert-1496');
INSERT INTO durabilite (id, produit_id, label_ecologique, certification) 
VALUES (26, 64, 'TCO Certified', 'Cert-9938');
INSERT INTO durabilite (id, produit_id, label_ecologique, certification) 
VALUES (27, 38, 'TCO Certified', 'Cert-5949');
INSERT INTO durabilite (id, produit_id, label_ecologique, certification) 
VALUES (28, 62, 'EPEAT Gold', 'Cert-7653');
INSERT INTO durabilite (id, produit_id, label_ecologique, certification) 
VALUES (29, 39, 'RoHS', 'Cert-2195');
INSERT INTO durabilite (id, produit_id, label_ecologique, certification) 
VALUES (30, 89, 'Energy Star', 'Cert-3589');
INSERT INTO durabilite (id, produit_id, label_ecologique, certification) 
VALUES (31, 57, 'RoHS', 'Cert-8933');
INSERT INTO durabilite (id, produit_id, label_ecologique, certification) 
VALUES (32, 60, 'EPEAT Gold', 'Cert-6573');
INSERT INTO durabilite (id, produit_id, label_ecologique, certification) 
VALUES (33, 78, 'EPEAT Gold', 'Cert-6121');
INSERT INTO durabilite (id, produit_id, label_ecologique, certification) 
VALUES (34, 92, 'EPEAT Silver', 'Cert-6658');
INSERT INTO durabilite (id, produit_id, label_ecologique, certification) 
VALUES (35, 52, 'EPEAT Gold', 'Cert-7070');
INSERT INTO durabilite (id, produit_id, label_ecologique, certification) 
VALUES (36, 66, 'FSC', 'Cert-2739');
INSERT INTO durabilite (id, produit_id, label_ecologique, certification) 
VALUES (37, 41, 'EPEAT Gold', 'Cert-8642');
INSERT INTO durabilite (id, produit_id, label_ecologique, certification) 
VALUES (38, 16, 'EPEAT Silver', 'Cert-8366');
INSERT INTO durabilite (id, produit_id, label_ecologique, certification) 
VALUES (39, 32, 'EPEAT Gold', 'Cert-2586');
INSERT INTO durabilite (id, produit_id, label_ecologique, certification) 
VALUES (40, 7, 'EPEAT Silver', 'Cert-7293');
INSERT INTO durabilite (id, produit_id, label_ecologique, certification) 
VALUES (41, 79, 'RoHS', 'Cert-5067');
INSERT INTO durabilite (id, produit_id, label_ecologique, certification) 
VALUES (42, 21, 'EPEAT Silver', 'Cert-6123');
INSERT INTO durabilite (id, produit_id, label_ecologique, certification) 
VALUES (43, 25, 'EPEAT Gold', 'Cert-9163');
INSERT INTO durabilite (id, produit_id, label_ecologique, certification) 
VALUES (44, 66, 'RoHS', 'Cert-9171');
INSERT INTO durabilite (id, produit_id, label_ecologique, certification) 
VALUES (45, 40, 'RoHS', 'Cert-1379');
INSERT INTO durabilite (id, produit_id, label_ecologique, certification) 
VALUES (46, 12, 'RoHS', 'Cert-9281');
INSERT INTO durabilite (id, produit_id, label_ecologique, certification) 
VALUES (47, 59, 'EPEAT Gold', 'Cert-4524');
INSERT INTO durabilite (id, produit_id, label_ecologique, certification) 
VALUES (48, 75, 'EPEAT Silver', 'Cert-1797');
INSERT INTO durabilite (id, produit_id, label_ecologique, certification) 
VALUES (49, 7, 'EPEAT Silver', 'Cert-9108');
INSERT INTO durabilite (id, produit_id, label_ecologique, certification) 
VALUES (50, 77, 'TCO Certified', 'Cert-8710');
INSERT INTO durabilite (id, produit_id, label_ecologique, certification) 
VALUES (51, 37, 'FSC', 'Cert-1133');
INSERT INTO durabilite (id, produit_id, label_ecologique, certification) 
VALUES (52, 14, 'RoHS', 'Cert-3194');
INSERT INTO durabilite (id, produit_id, label_ecologique, certification) 
VALUES (53, 34, 'TCO Certified', 'Cert-6992');
INSERT INTO durabilite (id, produit_id, label_ecologique, certification) 
VALUES (54, 98, 'RoHS', 'Cert-6995');
INSERT INTO durabilite (id, produit_id, label_ecologique, certification) 
VALUES (55, 6, 'RoHS', 'Cert-1838');
INSERT INTO durabilite (id, produit_id, label_ecologique, certification) 
VALUES (56, 73, 'FSC', 'Cert-4189');
INSERT INTO durabilite (id, produit_id, label_ecologique, certification) 
VALUES (57, 47, 'FSC', 'Cert-5728');
INSERT INTO durabilite (id, produit_id, label_ecologique, certification) 
VALUES (58, 10, 'RoHS', 'Cert-9261');
INSERT INTO durabilite (id, produit_id, label_ecologique, certification) 
VALUES (59, 58, 'FSC', 'Cert-5582');
INSERT INTO durabilite (id, produit_id, label_ecologique, certification) 
VALUES (60, 80, 'TCO Certified', 'Cert-2946');
INSERT INTO durabilite (id, produit_id, label_ecologique, certification) 
VALUES (61, 17, 'Energy Star', 'Cert-7453');
INSERT INTO durabilite (id, produit_id, label_ecologique, certification) 
VALUES (62, 48, 'EPEAT Silver', 'Cert-6990');
INSERT INTO durabilite (id, produit_id, label_ecologique, certification) 
VALUES (63, 97, 'EPEAT Gold', 'Cert-4261');
INSERT INTO durabilite (id, produit_id, label_ecologique, certification) 
VALUES (64, 78, 'FSC', 'Cert-7576');
INSERT INTO durabilite (id, produit_id, label_ecologique, certification) 
VALUES (65, 65, 'Energy Star', 'Cert-1742');
INSERT INTO durabilite (id, produit_id, label_ecologique, certification) 
VALUES (66, 5, 'EPEAT Gold', 'Cert-6456');
INSERT INTO durabilite (id, produit_id, label_ecologique, certification) 
VALUES (67, 61, 'FSC', 'Cert-8487');
INSERT INTO durabilite (id, produit_id, label_ecologique, certification) 
VALUES (68, 20, 'FSC', 'Cert-9446');
INSERT INTO durabilite (id, produit_id, label_ecologique, certification) 
VALUES (69, 18, 'EPEAT Silver', 'Cert-6218');
INSERT INTO durabilite (id, produit_id, label_ecologique, certification) 
VALUES (70, 21, 'RoHS', 'Cert-5902');
INSERT INTO durabilite (id, produit_id, label_ecologique, certification) 
VALUES (71, 76, 'EPEAT Silver', 'Cert-9311');
INSERT INTO durabilite (id, produit_id, label_ecologique, certification) 
VALUES (72, 66, 'FSC', 'Cert-9025');
INSERT INTO durabilite (id, produit_id, label_ecologique, certification) 
VALUES (73, 91, 'FSC', 'Cert-5911');
INSERT INTO durabilite (id, produit_id, label_ecologique, certification) 
VALUES (74, 61, 'Energy Star', 'Cert-7035');
INSERT INTO durabilite (id, produit_id, label_ecologique, certification) 
VALUES (75, 43, 'TCO Certified', 'Cert-2795');
INSERT INTO durabilite (id, produit_id, label_ecologique, certification) 
VALUES (76, 54, 'FSC', 'Cert-6040');
INSERT INTO durabilite (id, produit_id, label_ecologique, certification) 
VALUES (77, 93, 'TCO Certified', 'Cert-1436');
INSERT INTO durabilite (id, produit_id, label_ecologique, certification) 
VALUES (78, 77, 'RoHS', 'Cert-5350');
INSERT INTO durabilite (id, produit_id, label_ecologique, certification) 
VALUES (79, 84, 'FSC', 'Cert-4728');
INSERT INTO durabilite (id, produit_id, label_ecologique, certification) 
VALUES (80, 93, 'Energy Star', 'Cert-8871');
INSERT INTO durabilite (id, produit_id, label_ecologique, certification) 
VALUES (81, 22, 'FSC', 'Cert-7229');
INSERT INTO durabilite (id, produit_id, label_ecologique, certification) 
VALUES (82, 19, 'TCO Certified', 'Cert-4968');
INSERT INTO durabilite (id, produit_id, label_ecologique, certification) 
VALUES (83, 5, 'FSC', 'Cert-2800');
INSERT INTO durabilite (id, produit_id, label_ecologique, certification) 
VALUES (84, 25, 'Energy Star', 'Cert-8225');
INSERT INTO durabilite (id, produit_id, label_ecologique, certification) 
VALUES (85, 41, 'RoHS', 'Cert-3481');
INSERT INTO durabilite (id, produit_id, label_ecologique, certification) 
VALUES (86, 53, 'TCO Certified', 'Cert-4340');
INSERT INTO durabilite (id, produit_id, label_ecologique, certification) 
VALUES (87, 53, 'FSC', 'Cert-8726');
INSERT INTO durabilite (id, produit_id, label_ecologique, certification) 
VALUES (88, 95, 'TCO Certified', 'Cert-2020');
INSERT INTO durabilite (id, produit_id, label_ecologique, certification) 
VALUES (89, 91, 'EPEAT Gold', 'Cert-9498');
INSERT INTO durabilite (id, produit_id, label_ecologique, certification) 
VALUES (90, 27, 'FSC', 'Cert-6325');
INSERT INTO durabilite (id, produit_id, label_ecologique, certification) 
VALUES (91, 85, 'RoHS', 'Cert-9609');
INSERT INTO durabilite (id, produit_id, label_ecologique, certification) 
VALUES (92, 49, 'EPEAT Silver', 'Cert-3837');
INSERT INTO durabilite (id, produit_id, label_ecologique, certification) 
VALUES (93, 59, 'FSC', 'Cert-6608');
INSERT INTO durabilite (id, produit_id, label_ecologique, certification) 
VALUES (94, 70, 'EPEAT Silver', 'Cert-5331');
INSERT INTO durabilite (id, produit_id, label_ecologique, certification) 
VALUES (95, 79, 'RoHS', 'Cert-4150');
INSERT INTO durabilite (id, produit_id, label_ecologique, certification) 
VALUES (96, 32, 'EPEAT Silver', 'Cert-5890');
INSERT INTO durabilite (id, produit_id, label_ecologique, certification) 
VALUES (97, 29, 'EPEAT Silver', 'Cert-5735');
INSERT INTO durabilite (id, produit_id, label_ecologique, certification) 
VALUES (98, 91, 'EPEAT Gold', 'Cert-9011');
INSERT INTO durabilite (id, produit_id, label_ecologique, certification) 
VALUES (99, 41, 'RoHS', 'Cert-6714');
INSERT INTO durabilite (id, produit_id, label_ecologique, certification) 
VALUES (100, 72, 'TCO Certified', 'Cert-5480');
