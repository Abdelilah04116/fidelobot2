-- Table paniers
CREATE TABLE IF NOT EXISTS paniers (
    id SERIAL PRIMARY KEY,
    utilisateur_id INTEGER REFERENCES utilisateurs(id),
    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO paniers (id, utilisateur_id, date_creation) 
VALUES (1, 95, '2025-08-03T04:37:18');
INSERT INTO paniers (id, utilisateur_id, date_creation) 
VALUES (2, 48, '2025-08-03T09:51:33');
INSERT INTO paniers (id, utilisateur_id, date_creation) 
VALUES (3, 17, '2025-08-20T05:02:20');
INSERT INTO paniers (id, utilisateur_id, date_creation) 
VALUES (4, 72, '2025-08-24T00:21:03');
INSERT INTO paniers (id, utilisateur_id, date_creation) 
VALUES (5, 8, '2025-08-06T11:32:12');
INSERT INTO paniers (id, utilisateur_id, date_creation) 
VALUES (6, 76, '2025-08-20T13:07:22');
INSERT INTO paniers (id, utilisateur_id, date_creation) 
VALUES (7, 72, '2025-08-16T01:18:12');
INSERT INTO paniers (id, utilisateur_id, date_creation) 
VALUES (8, 72, '2025-08-24T14:22:19');
INSERT INTO paniers (id, utilisateur_id, date_creation) 
VALUES (9, 43, '2025-08-06T09:11:45');
INSERT INTO paniers (id, utilisateur_id, date_creation) 
VALUES (10, 86, '2025-08-24T02:31:52');
INSERT INTO paniers (id, utilisateur_id, date_creation) 
VALUES (11, 16, '2025-08-26T18:24:42');
INSERT INTO paniers (id, utilisateur_id, date_creation) 
VALUES (12, 53, '2025-08-22T07:30:59');
INSERT INTO paniers (id, utilisateur_id, date_creation) 
VALUES (13, 46, '2025-08-08T19:37:14');
INSERT INTO paniers (id, utilisateur_id, date_creation) 
VALUES (14, 86, '2025-08-08T15:02:28');
INSERT INTO paniers (id, utilisateur_id, date_creation) 
VALUES (15, 97, '2025-07-31T08:11:41');
INSERT INTO paniers (id, utilisateur_id, date_creation) 
VALUES (16, 55, '2025-08-09T18:56:08');
INSERT INTO paniers (id, utilisateur_id, date_creation) 
VALUES (17, 93, '2025-08-17T17:47:11');
INSERT INTO paniers (id, utilisateur_id, date_creation) 
VALUES (18, 7, '2025-08-12T13:31:31');
INSERT INTO paniers (id, utilisateur_id, date_creation) 
VALUES (19, 37, '2025-08-24T19:50:00');
INSERT INTO paniers (id, utilisateur_id, date_creation) 
VALUES (20, 77, '2025-08-01T05:06:32');
INSERT INTO paniers (id, utilisateur_id, date_creation) 
VALUES (21, 40, '2025-08-02T07:49:49');
INSERT INTO paniers (id, utilisateur_id, date_creation) 
VALUES (22, 46, '2025-08-16T22:34:53');
INSERT INTO paniers (id, utilisateur_id, date_creation) 
VALUES (23, 14, '2025-08-17T10:11:03');
INSERT INTO paniers (id, utilisateur_id, date_creation) 
VALUES (24, 74, '2025-08-14T14:17:28');
INSERT INTO paniers (id, utilisateur_id, date_creation) 
VALUES (25, 65, '2025-08-13T18:31:54');
INSERT INTO paniers (id, utilisateur_id, date_creation) 
VALUES (26, 28, '2025-08-06T02:39:36');
INSERT INTO paniers (id, utilisateur_id, date_creation) 
VALUES (27, 20, '2025-08-12T10:24:39');
INSERT INTO paniers (id, utilisateur_id, date_creation) 
VALUES (28, 85, '2025-08-13T14:07:27');
INSERT INTO paniers (id, utilisateur_id, date_creation) 
VALUES (29, 62, '2025-08-25T16:38:26');
INSERT INTO paniers (id, utilisateur_id, date_creation) 
VALUES (30, 29, '2025-07-29T00:55:35');
INSERT INTO paniers (id, utilisateur_id, date_creation) 
VALUES (31, 14, '2025-08-11T15:51:47');
INSERT INTO paniers (id, utilisateur_id, date_creation) 
VALUES (32, 45, '2025-08-05T01:55:13');
INSERT INTO paniers (id, utilisateur_id, date_creation) 
VALUES (33, 72, '2025-08-13T20:10:21');
INSERT INTO paniers (id, utilisateur_id, date_creation) 
VALUES (34, 48, '2025-08-26T18:40:23');
INSERT INTO paniers (id, utilisateur_id, date_creation) 
VALUES (35, 15, '2025-08-18T07:56:08');
INSERT INTO paniers (id, utilisateur_id, date_creation) 
VALUES (36, 98, '2025-08-03T22:36:52');
INSERT INTO paniers (id, utilisateur_id, date_creation) 
VALUES (37, 36, '2025-08-18T05:54:02');
INSERT INTO paniers (id, utilisateur_id, date_creation) 
VALUES (38, 74, '2025-07-30T01:00:35');
INSERT INTO paniers (id, utilisateur_id, date_creation) 
VALUES (39, 29, '2025-08-08T04:45:31');
INSERT INTO paniers (id, utilisateur_id, date_creation) 
VALUES (40, 55, '2025-08-06T13:22:25');
INSERT INTO paniers (id, utilisateur_id, date_creation) 
VALUES (41, 72, '2025-08-15T00:15:23');
INSERT INTO paniers (id, utilisateur_id, date_creation) 
VALUES (42, 99, '2025-08-04T10:27:59');
INSERT INTO paniers (id, utilisateur_id, date_creation) 
VALUES (43, 80, '2025-08-01T00:42:16');
INSERT INTO paniers (id, utilisateur_id, date_creation) 
VALUES (44, 79, '2025-08-02T07:38:46');
INSERT INTO paniers (id, utilisateur_id, date_creation) 
VALUES (45, 87, '2025-07-30T12:15:54');
INSERT INTO paniers (id, utilisateur_id, date_creation) 
VALUES (46, 83, '2025-08-08T15:53:43');
INSERT INTO paniers (id, utilisateur_id, date_creation) 
VALUES (47, 72, '2025-08-04T00:46:47');
INSERT INTO paniers (id, utilisateur_id, date_creation) 
VALUES (48, 4, '2025-08-10T19:54:03');
INSERT INTO paniers (id, utilisateur_id, date_creation) 
VALUES (49, 78, '2025-07-28T12:43:26');
INSERT INTO paniers (id, utilisateur_id, date_creation) 
VALUES (50, 85, '2025-08-13T12:39:49');
INSERT INTO paniers (id, utilisateur_id, date_creation) 
VALUES (51, 89, '2025-08-02T06:22:18');
INSERT INTO paniers (id, utilisateur_id, date_creation) 
VALUES (52, 35, '2025-08-11T16:12:42');
INSERT INTO paniers (id, utilisateur_id, date_creation) 
VALUES (53, 4, '2025-08-18T17:05:00');
INSERT INTO paniers (id, utilisateur_id, date_creation) 
VALUES (54, 24, '2025-08-19T17:42:00');
INSERT INTO paniers (id, utilisateur_id, date_creation) 
VALUES (55, 35, '2025-07-28T23:13:37');
INSERT INTO paniers (id, utilisateur_id, date_creation) 
VALUES (56, 90, '2025-08-12T23:23:16');
INSERT INTO paniers (id, utilisateur_id, date_creation) 
VALUES (57, 98, '2025-08-07T00:14:14');
INSERT INTO paniers (id, utilisateur_id, date_creation) 
VALUES (58, 40, '2025-08-22T23:32:43');
INSERT INTO paniers (id, utilisateur_id, date_creation) 
VALUES (59, 44, '2025-08-07T03:34:34');
INSERT INTO paniers (id, utilisateur_id, date_creation) 
VALUES (60, 45, '2025-08-06T18:10:09');
INSERT INTO paniers (id, utilisateur_id, date_creation) 
VALUES (61, 1, '2025-08-23T09:21:14');
INSERT INTO paniers (id, utilisateur_id, date_creation) 
VALUES (62, 24, '2025-08-22T06:22:21');
INSERT INTO paniers (id, utilisateur_id, date_creation) 
VALUES (63, 19, '2025-08-09T10:04:55');
INSERT INTO paniers (id, utilisateur_id, date_creation) 
VALUES (64, 73, '2025-08-23T12:07:19');
INSERT INTO paniers (id, utilisateur_id, date_creation) 
VALUES (65, 85, '2025-08-20T07:29:24');
INSERT INTO paniers (id, utilisateur_id, date_creation) 
VALUES (66, 52, '2025-08-03T17:24:19');
INSERT INTO paniers (id, utilisateur_id, date_creation) 
VALUES (67, 9, '2025-07-28T18:08:52');
INSERT INTO paniers (id, utilisateur_id, date_creation) 
VALUES (68, 19, '2025-08-15T03:30:07');
INSERT INTO paniers (id, utilisateur_id, date_creation) 
VALUES (69, 95, '2025-08-25T03:58:24');
INSERT INTO paniers (id, utilisateur_id, date_creation) 
VALUES (70, 82, '2025-08-22T10:29:20');
INSERT INTO paniers (id, utilisateur_id, date_creation) 
VALUES (71, 4, '2025-07-29T23:23:01');
INSERT INTO paniers (id, utilisateur_id, date_creation) 
VALUES (72, 12, '2025-08-09T06:21:06');
INSERT INTO paniers (id, utilisateur_id, date_creation) 
VALUES (73, 96, '2025-08-05T03:09:37');
INSERT INTO paniers (id, utilisateur_id, date_creation) 
VALUES (74, 68, '2025-07-30T18:45:24');
INSERT INTO paniers (id, utilisateur_id, date_creation) 
VALUES (75, 28, '2025-08-10T15:37:24');
INSERT INTO paniers (id, utilisateur_id, date_creation) 
VALUES (76, 49, '2025-08-06T14:33:05');
INSERT INTO paniers (id, utilisateur_id, date_creation) 
VALUES (77, 54, '2025-08-26T20:42:17');
INSERT INTO paniers (id, utilisateur_id, date_creation) 
VALUES (78, 59, '2025-08-10T00:47:21');
INSERT INTO paniers (id, utilisateur_id, date_creation) 
VALUES (79, 44, '2025-07-30T10:34:20');
INSERT INTO paniers (id, utilisateur_id, date_creation) 
VALUES (80, 21, '2025-08-19T10:26:32');
INSERT INTO paniers (id, utilisateur_id, date_creation) 
VALUES (81, 48, '2025-07-28T06:26:01');
INSERT INTO paniers (id, utilisateur_id, date_creation) 
VALUES (82, 40, '2025-07-31T02:18:56');
INSERT INTO paniers (id, utilisateur_id, date_creation) 
VALUES (83, 93, '2025-08-15T17:31:40');
INSERT INTO paniers (id, utilisateur_id, date_creation) 
VALUES (84, 42, '2025-08-10T00:49:23');
INSERT INTO paniers (id, utilisateur_id, date_creation) 
VALUES (85, 100, '2025-08-14T08:24:33');
INSERT INTO paniers (id, utilisateur_id, date_creation) 
VALUES (86, 73, '2025-08-02T02:25:34');
INSERT INTO paniers (id, utilisateur_id, date_creation) 
VALUES (87, 77, '2025-07-28T18:57:05');
INSERT INTO paniers (id, utilisateur_id, date_creation) 
VALUES (88, 11, '2025-08-11T01:30:20');
INSERT INTO paniers (id, utilisateur_id, date_creation) 
VALUES (89, 7, '2025-08-15T15:03:20');
INSERT INTO paniers (id, utilisateur_id, date_creation) 
VALUES (90, 20, '2025-08-08T02:03:16');
INSERT INTO paniers (id, utilisateur_id, date_creation) 
VALUES (91, 21, '2025-08-15T08:16:21');
INSERT INTO paniers (id, utilisateur_id, date_creation) 
VALUES (92, 97, '2025-08-21T13:12:57');
INSERT INTO paniers (id, utilisateur_id, date_creation) 
VALUES (93, 80, '2025-08-01T16:46:13');
INSERT INTO paniers (id, utilisateur_id, date_creation) 
VALUES (94, 7, '2025-08-12T04:15:23');
INSERT INTO paniers (id, utilisateur_id, date_creation) 
VALUES (95, 87, '2025-08-20T09:23:45');
INSERT INTO paniers (id, utilisateur_id, date_creation) 
VALUES (96, 11, '2025-08-25T20:24:10');
INSERT INTO paniers (id, utilisateur_id, date_creation) 
VALUES (97, 35, '2025-08-22T16:02:11');
INSERT INTO paniers (id, utilisateur_id, date_creation) 
VALUES (98, 57, '2025-08-01T03:16:30');
INSERT INTO paniers (id, utilisateur_id, date_creation) 
VALUES (99, 85, '2025-08-05T21:54:56');
INSERT INTO paniers (id, utilisateur_id, date_creation) 
VALUES (100, 55, '2025-08-06T12:25:48');
