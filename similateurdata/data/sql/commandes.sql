-- Table commandes
CREATE TABLE IF NOT EXISTS commandes (
    id SERIAL PRIMARY KEY,
    utilisateur_id INTEGER REFERENCES utilisateurs(id),
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    statut VARCHAR(50) DEFAULT 'en_cours',
    total DECIMAL(10,2) NOT NULL
);

INSERT INTO commandes (id, utilisateur_id, date, statut, total) 
VALUES (1, 17, '2025-01-28T21:21:12', 'annule', 1355.44);
INSERT INTO commandes (id, utilisateur_id, date, statut, total) 
VALUES (2, 73, '2025-04-04T15:01:59', 'expedie', 956.82);
INSERT INTO commandes (id, utilisateur_id, date, statut, total) 
VALUES (3, 33, '2025-08-18T02:14:31', 'livre', 377.19);
INSERT INTO commandes (id, utilisateur_id, date, statut, total) 
VALUES (4, 78, '2024-11-19T01:37:33', 'en_cours', 1566.69);
INSERT INTO commandes (id, utilisateur_id, date, statut, total) 
VALUES (5, 21, '2025-06-07T18:49:06', 'livre', 260.79);
INSERT INTO commandes (id, utilisateur_id, date, statut, total) 
VALUES (6, 4, '2024-09-25T14:32:03', 'livre', 1172.80);
INSERT INTO commandes (id, utilisateur_id, date, statut, total) 
VALUES (7, 49, '2025-06-03T15:13:22', 'annule', 1885.87);
INSERT INTO commandes (id, utilisateur_id, date, statut, total) 
VALUES (8, 26, '2024-12-30T17:18:46', 'en_cours', 1204.59);
INSERT INTO commandes (id, utilisateur_id, date, statut, total) 
VALUES (9, 81, '2025-06-30T13:21:58', 'expedie', 248.71);
INSERT INTO commandes (id, utilisateur_id, date, statut, total) 
VALUES (10, 99, '2025-03-02T00:29:55', 'livre', 1708.07);
INSERT INTO commandes (id, utilisateur_id, date, statut, total) 
VALUES (11, 77, '2024-11-01T18:31:53', 'en_cours', 1602.64);
INSERT INTO commandes (id, utilisateur_id, date, statut, total) 
VALUES (12, 73, '2025-03-04T06:01:46', 'en_cours', 727.05);
INSERT INTO commandes (id, utilisateur_id, date, statut, total) 
VALUES (13, 55, '2025-07-13T07:05:39', 'livre', 184.47);
INSERT INTO commandes (id, utilisateur_id, date, statut, total) 
VALUES (14, 83, '2025-08-10T18:28:31', 'livre', 74.67);
INSERT INTO commandes (id, utilisateur_id, date, statut, total) 
VALUES (15, 54, '2025-05-21T10:27:20', 'annule', 255.80);
INSERT INTO commandes (id, utilisateur_id, date, statut, total) 
VALUES (16, 47, '2025-05-26T13:58:50', 'annule', 1429.25);
INSERT INTO commandes (id, utilisateur_id, date, statut, total) 
VALUES (17, 56, '2025-04-07T09:50:21', 'expedie', 1480.90);
INSERT INTO commandes (id, utilisateur_id, date, statut, total) 
VALUES (18, 84, '2025-07-10T21:23:58', 'livre', 1251.03);
INSERT INTO commandes (id, utilisateur_id, date, statut, total) 
VALUES (19, 69, '2025-08-14T02:55:38', 'annule', 956.50);
INSERT INTO commandes (id, utilisateur_id, date, statut, total) 
VALUES (20, 94, '2024-10-02T15:49:15', 'livre', 678.49);
INSERT INTO commandes (id, utilisateur_id, date, statut, total) 
VALUES (21, 32, '2025-04-14T18:55:13', 'en_cours', 593.91);
INSERT INTO commandes (id, utilisateur_id, date, statut, total) 
VALUES (22, 58, '2025-05-03T01:12:38', 'expedie', 1513.43);
INSERT INTO commandes (id, utilisateur_id, date, statut, total) 
VALUES (23, 73, '2024-12-21T06:49:54', 'annule', 705.97);
INSERT INTO commandes (id, utilisateur_id, date, statut, total) 
VALUES (24, 64, '2024-09-10T03:17:31', 'livre', 404.59);
INSERT INTO commandes (id, utilisateur_id, date, statut, total) 
VALUES (25, 28, '2025-06-06T10:24:50', 'livre', 1605.77);
INSERT INTO commandes (id, utilisateur_id, date, statut, total) 
VALUES (26, 44, '2025-07-06T13:14:57', 'livre', 1766.62);
INSERT INTO commandes (id, utilisateur_id, date, statut, total) 
VALUES (27, 90, '2025-04-07T10:19:01', 'livre', 1133.79);
INSERT INTO commandes (id, utilisateur_id, date, statut, total) 
VALUES (28, 67, '2025-01-21T19:13:52', 'expedie', 216.95);
INSERT INTO commandes (id, utilisateur_id, date, statut, total) 
VALUES (29, 93, '2024-09-26T02:25:33', 'annule', 1002.73);
INSERT INTO commandes (id, utilisateur_id, date, statut, total) 
VALUES (30, 98, '2025-06-25T14:13:36', 'expedie', 1396.69);
INSERT INTO commandes (id, utilisateur_id, date, statut, total) 
VALUES (31, 83, '2024-09-17T08:12:03', 'annule', 923.94);
INSERT INTO commandes (id, utilisateur_id, date, statut, total) 
VALUES (32, 3, '2025-08-19T15:25:43', 'en_cours', 623.76);
INSERT INTO commandes (id, utilisateur_id, date, statut, total) 
VALUES (33, 52, '2025-06-22T00:17:11', 'expedie', 647.10);
INSERT INTO commandes (id, utilisateur_id, date, statut, total) 
VALUES (34, 75, '2025-01-03T11:42:03', 'livre', 972.86);
INSERT INTO commandes (id, utilisateur_id, date, statut, total) 
VALUES (35, 68, '2025-01-08T17:54:29', 'livre', 879.73);
INSERT INTO commandes (id, utilisateur_id, date, statut, total) 
VALUES (36, 96, '2025-08-03T07:13:26', 'livre', 736.03);
INSERT INTO commandes (id, utilisateur_id, date, statut, total) 
VALUES (37, 59, '2025-07-09T23:16:34', 'livre', 647.91);
INSERT INTO commandes (id, utilisateur_id, date, statut, total) 
VALUES (38, 30, '2025-02-11T06:58:26', 'en_cours', 1456.50);
INSERT INTO commandes (id, utilisateur_id, date, statut, total) 
VALUES (39, 41, '2025-02-04T09:13:38', 'en_cours', 1498.62);
INSERT INTO commandes (id, utilisateur_id, date, statut, total) 
VALUES (40, 98, '2025-08-22T21:29:07', 'expedie', 423.50);
INSERT INTO commandes (id, utilisateur_id, date, statut, total) 
VALUES (41, 95, '2025-07-29T15:44:08', 'annule', 589.17);
INSERT INTO commandes (id, utilisateur_id, date, statut, total) 
VALUES (42, 76, '2024-10-12T10:28:57', 'livre', 1962.00);
INSERT INTO commandes (id, utilisateur_id, date, statut, total) 
VALUES (43, 25, '2025-07-30T09:57:41', 'livre', 493.59);
INSERT INTO commandes (id, utilisateur_id, date, statut, total) 
VALUES (44, 23, '2025-06-21T19:31:09', 'livre', 77.59);
INSERT INTO commandes (id, utilisateur_id, date, statut, total) 
VALUES (45, 69, '2024-11-22T16:07:31', 'expedie', 584.91);
INSERT INTO commandes (id, utilisateur_id, date, statut, total) 
VALUES (46, 7, '2025-06-12T23:50:01', 'livre', 1409.96);
INSERT INTO commandes (id, utilisateur_id, date, statut, total) 
VALUES (47, 17, '2025-05-07T03:18:23', 'annule', 250.05);
INSERT INTO commandes (id, utilisateur_id, date, statut, total) 
VALUES (48, 2, '2025-07-22T12:40:26', 'livre', 965.32);
INSERT INTO commandes (id, utilisateur_id, date, statut, total) 
VALUES (49, 57, '2025-04-17T12:49:18', 'livre', 409.51);
INSERT INTO commandes (id, utilisateur_id, date, statut, total) 
VALUES (50, 7, '2025-08-22T06:38:18', 'livre', 1885.07);
INSERT INTO commandes (id, utilisateur_id, date, statut, total) 
VALUES (51, 62, '2024-08-31T01:32:23', 'en_cours', 1653.13);
INSERT INTO commandes (id, utilisateur_id, date, statut, total) 
VALUES (52, 52, '2025-04-29T19:13:10', 'annule', 194.46);
INSERT INTO commandes (id, utilisateur_id, date, statut, total) 
VALUES (53, 81, '2025-06-24T13:01:49', 'en_cours', 345.87);
INSERT INTO commandes (id, utilisateur_id, date, statut, total) 
VALUES (54, 73, '2025-04-29T03:26:06', 'livre', 216.10);
INSERT INTO commandes (id, utilisateur_id, date, statut, total) 
VALUES (55, 32, '2025-01-22T04:00:01', 'en_cours', 1138.24);
INSERT INTO commandes (id, utilisateur_id, date, statut, total) 
VALUES (56, 54, '2024-09-16T15:28:21', 'expedie', 1562.60);
INSERT INTO commandes (id, utilisateur_id, date, statut, total) 
VALUES (57, 49, '2024-12-22T23:45:02', 'annule', 1821.58);
INSERT INTO commandes (id, utilisateur_id, date, statut, total) 
VALUES (58, 39, '2025-03-18T06:34:14', 'annule', 645.49);
INSERT INTO commandes (id, utilisateur_id, date, statut, total) 
VALUES (59, 80, '2024-09-11T14:48:36', 'en_cours', 1238.78);
INSERT INTO commandes (id, utilisateur_id, date, statut, total) 
VALUES (60, 95, '2024-12-28T15:12:34', 'en_cours', 1897.80);
INSERT INTO commandes (id, utilisateur_id, date, statut, total) 
VALUES (61, 27, '2025-03-24T07:28:24', 'expedie', 566.06);
INSERT INTO commandes (id, utilisateur_id, date, statut, total) 
VALUES (62, 11, '2025-04-03T00:20:00', 'expedie', 517.74);
INSERT INTO commandes (id, utilisateur_id, date, statut, total) 
VALUES (63, 71, '2024-10-23T17:09:01', 'en_cours', 355.24);
INSERT INTO commandes (id, utilisateur_id, date, statut, total) 
VALUES (64, 53, '2024-12-31T13:15:18', 'annule', 1394.27);
INSERT INTO commandes (id, utilisateur_id, date, statut, total) 
VALUES (65, 61, '2025-03-09T17:41:09', 'livre', 113.65);
INSERT INTO commandes (id, utilisateur_id, date, statut, total) 
VALUES (66, 37, '2025-05-24T14:38:19', 'livre', 1420.83);
INSERT INTO commandes (id, utilisateur_id, date, statut, total) 
VALUES (67, 59, '2024-11-20T08:56:32', 'en_cours', 1390.40);
INSERT INTO commandes (id, utilisateur_id, date, statut, total) 
VALUES (68, 34, '2024-10-25T02:52:03', 'expedie', 879.02);
INSERT INTO commandes (id, utilisateur_id, date, statut, total) 
VALUES (69, 70, '2024-09-15T05:50:32', 'expedie', 1312.89);
INSERT INTO commandes (id, utilisateur_id, date, statut, total) 
VALUES (70, 35, '2025-05-15T05:41:56', 'expedie', 189.25);
INSERT INTO commandes (id, utilisateur_id, date, statut, total) 
VALUES (71, 22, '2025-06-06T17:46:12', 'livre', 1210.34);
INSERT INTO commandes (id, utilisateur_id, date, statut, total) 
VALUES (72, 73, '2025-01-26T04:53:44', 'livre', 906.35);
INSERT INTO commandes (id, utilisateur_id, date, statut, total) 
VALUES (73, 60, '2025-02-15T16:24:28', 'livre', 1414.48);
INSERT INTO commandes (id, utilisateur_id, date, statut, total) 
VALUES (74, 35, '2025-06-14T23:56:34', 'annule', 903.63);
INSERT INTO commandes (id, utilisateur_id, date, statut, total) 
VALUES (75, 77, '2025-04-14T17:59:51', 'en_cours', 1784.37);
INSERT INTO commandes (id, utilisateur_id, date, statut, total) 
VALUES (76, 95, '2025-04-07T00:43:38', 'livre', 1227.24);
INSERT INTO commandes (id, utilisateur_id, date, statut, total) 
VALUES (77, 4, '2025-03-10T15:22:55', 'en_cours', 496.40);
INSERT INTO commandes (id, utilisateur_id, date, statut, total) 
VALUES (78, 87, '2024-09-30T14:35:51', 'en_cours', 1999.17);
INSERT INTO commandes (id, utilisateur_id, date, statut, total) 
VALUES (79, 87, '2024-11-20T20:57:06', 'livre', 1173.68);
INSERT INTO commandes (id, utilisateur_id, date, statut, total) 
VALUES (80, 98, '2025-02-10T08:53:45', 'expedie', 967.48);
INSERT INTO commandes (id, utilisateur_id, date, statut, total) 
VALUES (81, 84, '2024-12-17T03:56:13', 'annule', 1836.34);
INSERT INTO commandes (id, utilisateur_id, date, statut, total) 
VALUES (82, 24, '2025-06-28T00:26:50', 'annule', 1287.83);
INSERT INTO commandes (id, utilisateur_id, date, statut, total) 
VALUES (83, 63, '2025-01-26T18:18:53', 'en_cours', 966.52);
INSERT INTO commandes (id, utilisateur_id, date, statut, total) 
VALUES (84, 53, '2024-10-23T02:32:21', 'livre', 676.06);
INSERT INTO commandes (id, utilisateur_id, date, statut, total) 
VALUES (85, 14, '2024-10-16T23:03:17', 'expedie', 693.12);
INSERT INTO commandes (id, utilisateur_id, date, statut, total) 
VALUES (86, 89, '2025-01-04T04:16:41', 'annule', 612.02);
INSERT INTO commandes (id, utilisateur_id, date, statut, total) 
VALUES (87, 52, '2024-09-27T16:20:23', 'en_cours', 936.91);
INSERT INTO commandes (id, utilisateur_id, date, statut, total) 
VALUES (88, 41, '2025-02-27T10:15:01', 'livre', 680.38);
INSERT INTO commandes (id, utilisateur_id, date, statut, total) 
VALUES (89, 99, '2025-04-05T13:10:33', 'annule', 1736.58);
INSERT INTO commandes (id, utilisateur_id, date, statut, total) 
VALUES (90, 1, '2025-06-12T01:48:11', 'annule', 855.83);
INSERT INTO commandes (id, utilisateur_id, date, statut, total) 
VALUES (91, 25, '2024-09-14T18:34:34', 'livre', 1264.14);
INSERT INTO commandes (id, utilisateur_id, date, statut, total) 
VALUES (92, 64, '2025-03-27T12:06:51', 'annule', 1531.98);
INSERT INTO commandes (id, utilisateur_id, date, statut, total) 
VALUES (93, 27, '2025-01-28T15:41:46', 'livre', 1120.98);
INSERT INTO commandes (id, utilisateur_id, date, statut, total) 
VALUES (94, 37, '2024-12-06T14:10:52', 'annule', 1767.65);
INSERT INTO commandes (id, utilisateur_id, date, statut, total) 
VALUES (95, 63, '2024-09-28T15:57:26', 'en_cours', 106.30);
INSERT INTO commandes (id, utilisateur_id, date, statut, total) 
VALUES (96, 81, '2025-01-28T09:30:17', 'expedie', 1434.08);
INSERT INTO commandes (id, utilisateur_id, date, statut, total) 
VALUES (97, 40, '2025-03-09T12:17:38', 'en_cours', 1126.89);
INSERT INTO commandes (id, utilisateur_id, date, statut, total) 
VALUES (98, 12, '2025-02-11T08:42:51', 'expedie', 1984.90);
INSERT INTO commandes (id, utilisateur_id, date, statut, total) 
VALUES (99, 15, '2025-06-23T03:32:11', 'annule', 1896.77);
INSERT INTO commandes (id, utilisateur_id, date, statut, total) 
VALUES (100, 83, '2025-05-24T15:35:17', 'expedie', 1021.83);
