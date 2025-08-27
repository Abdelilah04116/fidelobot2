-- Table utilisateurs
CREATE TABLE IF NOT EXISTS utilisateurs (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    mot_de_passe VARCHAR(255) NOT NULL,
    consentement_rgpd BOOLEAN DEFAULT FALSE
);

INSERT INTO utilisateurs (id, nom, email, mot_de_passe, consentement_rgpd) 
VALUES (1, 'Guillaume de Verdier', 'regnierjulien@example.com', 'eaaff2b8af2372daa820da1d467c45a876f58f7fd4855cd7244c02dac039cf59', True);
INSERT INTO utilisateurs (id, nom, email, mot_de_passe, consentement_rgpd) 
VALUES (2, 'Célina Dupuis', 'gabriel25@example.net', '1a78ade8fbf6ed90503e58e61a13e34f9ab9cc22616e8b150e969cf8bbbd0807', False);
INSERT INTO utilisateurs (id, nom, email, mot_de_passe, consentement_rgpd) 
VALUES (3, 'Joseph Petit', 'mdufour@example.com', 'afb08556dd5e75e9923657e00012c0c8ee17ea7463288dfc181023538a6b0648', True);
INSERT INTO utilisateurs (id, nom, email, mot_de_passe, consentement_rgpd) 
VALUES (4, 'Dominique Marie', 'royerphilippine@example.net', 'b47187b144a95234b207c9a73d971694c43154f046be2a992efefd26df0c6ddc', True);
INSERT INTO utilisateurs (id, nom, email, mot_de_passe, consentement_rgpd) 
VALUES (5, 'Pénélope Gaillard', 'sabineleclerc@example.org', '816964c2b4580deadfa961e9abc2adcd367b3fb233b81912ed880d1a0b39ad6e', True);
INSERT INTO utilisateurs (id, nom, email, mot_de_passe, consentement_rgpd) 
VALUES (6, 'Gérard Rodrigues', 'veronique36@example.com', '4d76d89078dd22542249e16412bb349c747f2ee430b536532174ec58e68c6381', False);
INSERT INTO utilisateurs (id, nom, email, mot_de_passe, consentement_rgpd) 
VALUES (7, 'Michel Bousquet', 'claude18@example.com', 'ba62656fe2c6d8135c681c8dad0fdf466b97a63ef60fe9d86f77d75e78cd2214', True);
INSERT INTO utilisateurs (id, nom, email, mot_de_passe, consentement_rgpd) 
VALUES (8, 'Susanne Martin', 'srenaud@example.org', 'e11b8c19d655fc8ae79f625bb526d591556ca92bceb83d2141046ff2a1fca235', False);
INSERT INTO utilisateurs (id, nom, email, mot_de_passe, consentement_rgpd) 
VALUES (9, 'Christophe Allain', 'dianebazin@example.com', '8b1209b263435d0d6b240d30f16fef5a58a9aeee419a41fb319a906e138cbbcc', False);
INSERT INTO utilisateurs (id, nom, email, mot_de_passe, consentement_rgpd) 
VALUES (10, 'Adrienne-Danielle Besnard', 'michelle32@example.com', '82b92b5989429658b068182494ff8184ccda6952d48daa37890038f9009f43b8', False);
INSERT INTO utilisateurs (id, nom, email, mot_de_passe, consentement_rgpd) 
VALUES (11, 'Dominique de la Letellier', 'pcollet@example.org', 'f8e49f2a64c9083e33f633768ffa6aa3bf605773b743780fe8551ee4d18d275c', False);
INSERT INTO utilisateurs (id, nom, email, mot_de_passe, consentement_rgpd) 
VALUES (12, 'Théodore Mercier', 'charlesmartin@example.org', '236acc88b218b6a4e717cc40142e62348a2d2a82302e9c5352ab8834103c1850', False);
INSERT INTO utilisateurs (id, nom, email, mot_de_passe, consentement_rgpd) 
VALUES (13, 'Anouk Ruiz', 'pchauveau@example.org', 'dd3e0379bc15c322707e2e9e11e94f178f00950d96c87dbd2d2e33847549e3f4', True);
INSERT INTO utilisateurs (id, nom, email, mot_de_passe, consentement_rgpd) 
VALUES (14, 'Grégoire Peron', 'piresantoine@example.com', 'c6cf49d8f2a00f203b57b37a129f67c6a1052db7acdb6c662fd75a02cd8c2db7', False);
INSERT INTO utilisateurs (id, nom, email, mot_de_passe, consentement_rgpd) 
VALUES (15, 'Alphonse Richard', 'benjamingeorges@example.com', '40e6fd53b0cff4c4e07657411f5153d258609c8102e022495757ffda518254d3', False);
INSERT INTO utilisateurs (id, nom, email, mot_de_passe, consentement_rgpd) 
VALUES (16, 'Amélie du Muller', 'xcarre@example.com', '2ddb65faebc711c19583ac027c8583c3ea6b5adadf8781e0f1620794051704b5', False);
INSERT INTO utilisateurs (id, nom, email, mot_de_passe, consentement_rgpd) 
VALUES (17, 'Alexandrie Rey', 'luce05@example.org', 'f3c09561e4836b7b079978ecbc7a8bb25ac5c52543e0433339f346da63b6a542', True);
INSERT INTO utilisateurs (id, nom, email, mot_de_passe, consentement_rgpd) 
VALUES (18, 'Stéphane Gauthier', 'luciecarlier@example.org', '93c717866c30e266af71c9728743870c934dbccc5a9c5cac8415e13d60d2074d', False);
INSERT INTO utilisateurs (id, nom, email, mot_de_passe, consentement_rgpd) 
VALUES (19, 'Bernard Gaillard', 'uturpin@example.com', '99572f8a98bd1c15d6b9e38e8afc9fe040af781b77b5a22c37f2f027977ab905', False);
INSERT INTO utilisateurs (id, nom, email, mot_de_passe, consentement_rgpd) 
VALUES (20, 'Nicole Blanchet', 'labbetheophile@example.com', 'af33326c0f79dabba7211ff2d70ea30c2f835d0b7ee631884c1faa08cc3eb25a', True);
INSERT INTO utilisateurs (id, nom, email, mot_de_passe, consentement_rgpd) 
VALUES (21, 'Josette-Astrid Simon', 'philippemadeleine@example.com', '0ab5fc672cc78f50dd5f2896df40b47dcf49044d79f859f02a187688840877fe', False);
INSERT INTO utilisateurs (id, nom, email, mot_de_passe, consentement_rgpd) 
VALUES (22, 'Jacqueline Jourdan Le Didier', 'edias@example.org', '51a0ec0ca3f771e68c6a01250f016068e39b3ac26e0afc56d0ed0c7a13f93d4f', False);
INSERT INTO utilisateurs (id, nom, email, mot_de_passe, consentement_rgpd) 
VALUES (23, 'Nath Dupuy', 'andrejulien@example.net', '28070c52f7059be04361791d83bd8114a16ffc0af86f936c88e8db7d1f7c59fe', True);
INSERT INTO utilisateurs (id, nom, email, mot_de_passe, consentement_rgpd) 
VALUES (24, 'Diane Schmitt', 'jeanneprevost@example.net', '0d884fa37077285466206a722cc1f8e51465b1ddfb4c53b0873124f564b54df2', False);
INSERT INTO utilisateurs (id, nom, email, mot_de_passe, consentement_rgpd) 
VALUES (25, 'Alain Laine-Martel', 'remylaetitia@example.org', 'cfe43e6f51eeab493a904f465a042f70d92b01424c633a5039cc23858c601610', True);
INSERT INTO utilisateurs (id, nom, email, mot_de_passe, consentement_rgpd) 
VALUES (26, 'Madeleine Breton', 'huguesfoucher@example.com', 'a239caa20f62f152cba1e0c061ed8437b029c518dd70151bebbfa8cac8120dbc', False);
INSERT INTO utilisateurs (id, nom, email, mot_de_passe, consentement_rgpd) 
VALUES (27, 'Alexandria-Édith Marion', 'suzanne93@example.net', 'a316e54836749037066ef184439c4bf4a98875c467e9d906fe96e032724fb9be', False);
INSERT INTO utilisateurs (id, nom, email, mot_de_passe, consentement_rgpd) 
VALUES (28, 'Joséphine Nicolas', 'rousseaualice@example.com', 'f7f48206fa9008a2344e792f1f43d24b18b9dffc303e7511e16099acb47cdac3', False);
INSERT INTO utilisateurs (id, nom, email, mot_de_passe, consentement_rgpd) 
VALUES (29, 'Jean Picard', 'urenard@example.org', 'ea352b6ad7306daac206d82cd38cfd1112e2a0a89efb68c588542c7a153792a1', True);
INSERT INTO utilisateurs (id, nom, email, mot_de_passe, consentement_rgpd) 
VALUES (30, 'André Carlier', 'dbrunet@example.com', '46241cc4b79c140c1c27e014280659e99ceb432d6a811d13699369e06219c6d2', True);
INSERT INTO utilisateurs (id, nom, email, mot_de_passe, consentement_rgpd) 
VALUES (31, 'Éléonore Lemaître', 'llemaitre@example.com', '5c3e2fe098c78d19aceb70cf8a01932fb40f23e4003d518daccc692e1e11102d', True);
INSERT INTO utilisateurs (id, nom, email, mot_de_passe, consentement_rgpd) 
VALUES (32, 'Paulette du Baudry', 'christelleribeiro@example.org', '771aed50951b1339d51125f89cd8f1829fcb17db35b402e6c4bddcae6b5bd215', True);
INSERT INTO utilisateurs (id, nom, email, mot_de_passe, consentement_rgpd) 
VALUES (33, 'Émilie Techer', 'victoirevalentin@example.com', '9f05fda12fe6d8f4f39ceb8bde760406392fb06ac23a75f3ad1419df31da51fc', False);
INSERT INTO utilisateurs (id, nom, email, mot_de_passe, consentement_rgpd) 
VALUES (34, 'Marie Bouchet-Aubry', 'fbegue@example.net', 'd487b07839ab5acbf3cd5e3e695fcadb34b5c4183c2f66ec951ced21a3fe1591', True);
INSERT INTO utilisateurs (id, nom, email, mot_de_passe, consentement_rgpd) 
VALUES (35, 'Gabriel Lucas', 'noemi75@example.com', '9fe8970308da8edc97fcc7d49e0bdc6f71aa81206602e75b2ba4bec19dd360d1', True);
INSERT INTO utilisateurs (id, nom, email, mot_de_passe, consentement_rgpd) 
VALUES (36, 'Emmanuel Olivier', 'virginieboyer@example.org', '21d81fc17d7b4e406ef574178bf2a4148f47cbcabe0365355b359d29bf64752a', True);
INSERT INTO utilisateurs (id, nom, email, mot_de_passe, consentement_rgpd) 
VALUES (37, 'Corinne Poirier', 'jacquetantoine@example.com', 'c32a3d16b48cd1605a40f44e2380d7b2461ffe7fc2bc3e51982ff63849c7a577', False);
INSERT INTO utilisateurs (id, nom, email, mot_de_passe, consentement_rgpd) 
VALUES (38, 'Thibaut-Honoré Mendès', 'audrey65@example.com', '75c0f9120e78eff319357a57eb4059a29be1a19c7e2a862b25f1dfc77b5717ae', False);
INSERT INTO utilisateurs (id, nom, email, mot_de_passe, consentement_rgpd) 
VALUES (39, 'Timothée-Isaac Baron', 'marcelle43@example.org', '8a876a3697071cfb1406be9388df49a19641a92a8993c13efc6d1faeeb916f76', False);
INSERT INTO utilisateurs (id, nom, email, mot_de_passe, consentement_rgpd) 
VALUES (40, 'Zacharie Joubert-Diaz', 'wleconte@example.net', 'f5f79ddcc0af3860a050c8d5999856fb7abf52557ff849fa37eb3296a6aba9b7', False);
INSERT INTO utilisateurs (id, nom, email, mot_de_passe, consentement_rgpd) 
VALUES (41, 'Michelle Bertin', 'celina17@example.org', '7e2db18e592b473ce3f6c48e7d228c9f6c88c9c3c24ca1490c60634350e85b4c', False);
INSERT INTO utilisateurs (id, nom, email, mot_de_passe, consentement_rgpd) 
VALUES (42, 'Édith Merle', 'coulonxavier@example.net', '9ebdaafe4e333f1ec84c3d0d0b7f5363598ca6c3423e4cde95c9336fc8f89c02', True);
INSERT INTO utilisateurs (id, nom, email, mot_de_passe, consentement_rgpd) 
VALUES (43, 'Julien de Lebrun', 'alfredlabbe@example.org', '9faac8d24b11622c23f99e0768b4a832b72268b6001649b9be890bb311c52dd5', True);
INSERT INTO utilisateurs (id, nom, email, mot_de_passe, consentement_rgpd) 
VALUES (44, 'Victoire Pelletier', 'jacquesantoine@example.org', '9b0a7c3d007c8842a5278e5907b68fbd2147e428b45f6b6c359485ad2438949c', False);
INSERT INTO utilisateurs (id, nom, email, mot_de_passe, consentement_rgpd) 
VALUES (45, 'Monique Denis', 'christelle23@example.net', 'f344e561659d5af7ca0cf5be9264602971cfb8a458d61a2bc01ace0d1b725de6', False);
INSERT INTO utilisateurs (id, nom, email, mot_de_passe, consentement_rgpd) 
VALUES (46, 'Gilles de la Pelletier', 'kcollet@example.org', '470eaaf7201dc5c2a82bc9ebd2af70387480aa4c1a1fb93cc5f664faf3250ce6', True);
INSERT INTO utilisateurs (id, nom, email, mot_de_passe, consentement_rgpd) 
VALUES (47, 'Gilles Barthelemy de Roussel', 'augustincharpentier@example.com', '78b55cd747e4bd473a316dbd1bc3ea0454bb892388c3459364f5115f128fa98b', False);
INSERT INTO utilisateurs (id, nom, email, mot_de_passe, consentement_rgpd) 
VALUES (48, 'Susanne Maillard', 'eblot@example.com', 'ce97bd8e0f0673238e7d153ccf151a4363bbbebda9f0e06a8b73d05628995b83', False);
INSERT INTO utilisateurs (id, nom, email, mot_de_passe, consentement_rgpd) 
VALUES (49, 'Véronique Marie', 'cbesnard@example.org', '8ca740b3e4805c72652211857fc785c550a18ac52ae60a058a8b6eece1e5d1a1', True);
INSERT INTO utilisateurs (id, nom, email, mot_de_passe, consentement_rgpd) 
VALUES (50, 'Clémence Pascal', 'duboislucy@example.org', 'cca3860af9e892d3fd8ec2fafcff37b7d429e4846d8998935f7d191d9a38c5fc', False);
INSERT INTO utilisateurs (id, nom, email, mot_de_passe, consentement_rgpd) 
VALUES (51, 'Paul Vallet', 'henryanne@example.com', '4d26020b94fb7ae7becdcd1f13d82ac491ba6d26589b41d07a2598a1b0dc5574', False);
INSERT INTO utilisateurs (id, nom, email, mot_de_passe, consentement_rgpd) 
VALUES (52, 'Thérèse Auger Le Auger', 'gnoel@example.net', '36d0761241be783bee509225f395dddac9946d3e9d0e8feaeb7e9283a59ffd33', False);
INSERT INTO utilisateurs (id, nom, email, mot_de_passe, consentement_rgpd) 
VALUES (53, 'Charles du Fabre', 'taubert@example.com', '30b808a69215ea339166fae89e2bf2af4ca3694b9f8ec78cdce415e3f08001a7', False);
INSERT INTO utilisateurs (id, nom, email, mot_de_passe, consentement_rgpd) 
VALUES (54, 'Stéphane Giraud', 'francoischevallier@example.net', 'ad458a3ad10e694249f9a7a062f40b7f12d97659585993f10c096c8e79e09c17', True);
INSERT INTO utilisateurs (id, nom, email, mot_de_passe, consentement_rgpd) 
VALUES (55, 'Gabrielle Bourgeois-Lacroix', 'marianne52@example.net', '8ff1311873ec9d651bdc577fa9117277d9892eda2859aa8976e0787a2bafacbe', False);
INSERT INTO utilisateurs (id, nom, email, mot_de_passe, consentement_rgpd) 
VALUES (56, 'Alexandre Weber', 'bernardleconte@example.org', 'a34d3fd7d6d614f4a9d54fdc67a202834a2c2b79d6bddc7aca513d6c098d54d2', True);
INSERT INTO utilisateurs (id, nom, email, mot_de_passe, consentement_rgpd) 
VALUES (57, 'Laurent Chevallier', 'upottier@example.net', '99aae36ed436388392f90cfb49dacb39cf4d1a7a2d0cc07e835604e854ccbe98', False);
INSERT INTO utilisateurs (id, nom, email, mot_de_passe, consentement_rgpd) 
VALUES (58, 'Éric Giraud', 'hoareauaugustin@example.com', '5d825eaab6977c33b0646aea505c2442cd7481c897836a69cc6ad86c2b4e7f23', False);
INSERT INTO utilisateurs (id, nom, email, mot_de_passe, consentement_rgpd) 
VALUES (59, 'Arnaude Neveu', 'edith32@example.net', 'f3cee9c8e4dec8ddef878ad16b8f1c0ae6b0e7cedaef3a0aa28f638c580b943c', False);
INSERT INTO utilisateurs (id, nom, email, mot_de_passe, consentement_rgpd) 
VALUES (60, 'Isabelle Clerc', 'augustinnormand@example.com', 'a173cbc5b79cc8a31a279206588e8d28d29d753cc4338a7d675e01345c9884f6', True);
INSERT INTO utilisateurs (id, nom, email, mot_de_passe, consentement_rgpd) 
VALUES (61, 'François Leconte', 'mariannelamy@example.org', '57bbea223a6ac4e106f04092c4d740391bb56d748e4a15767982f1fe8e95db9c', False);
INSERT INTO utilisateurs (id, nom, email, mot_de_passe, consentement_rgpd) 
VALUES (62, 'Lucas-Léon Lebreton', 'ulesage@example.org', 'ff1adedc2ed258670a22a2f58ad85b191bf91ba51ed2bd6a184101fb0431150a', False);
INSERT INTO utilisateurs (id, nom, email, mot_de_passe, consentement_rgpd) 
VALUES (63, 'Alix Reynaud', 'elisabethvasseur@example.org', '9837e108dace02daf89f0e7b1540e67f80a63fa5c22304c5f51517659c2bfee5', False);
INSERT INTO utilisateurs (id, nom, email, mot_de_passe, consentement_rgpd) 
VALUES (64, 'Sébastien Godard', 'jtanguy@example.org', '3b4b03139af6603532b00852c38b207681e7ceeb0e98ec122b4103b9f3743789', True);
INSERT INTO utilisateurs (id, nom, email, mot_de_passe, consentement_rgpd) 
VALUES (65, 'Arnaude Charpentier-Leconte', 'deschampseugene@example.org', 'a71939b8c9075cc8dd5685084945c4cd392cac73e5558ba0a927a40ca5e5ad42', False);
INSERT INTO utilisateurs (id, nom, email, mot_de_passe, consentement_rgpd) 
VALUES (66, 'Adrien Bouvier', 'simonelouis@example.net', 'c17282ac8c2a323dd492f70e3b6c65755f49ccf71e75c44b7e267bbb4698f774', True);
INSERT INTO utilisateurs (id, nom, email, mot_de_passe, consentement_rgpd) 
VALUES (67, 'Auguste Moreau', 'blinines@example.com', '6f3df3f97db2a626db0cec3a04a75fa67a5947b60f861fa7b8195bbec7ec33cf', True);
INSERT INTO utilisateurs (id, nom, email, mot_de_passe, consentement_rgpd) 
VALUES (68, 'Adrienne de la Bonneau', 'oliviebuisson@example.org', '2ad6ca072a851258f1b672580d763db05cd870e5310d789b5689b805406dad82', False);
INSERT INTO utilisateurs (id, nom, email, mot_de_passe, consentement_rgpd) 
VALUES (69, 'Sylvie De Sousa', 'fourniermanon@example.com', '4687a29515248b13dfb646b8010d9a7d15e50463886f96a1d892bf80e6215449', True);
INSERT INTO utilisateurs (id, nom, email, mot_de_passe, consentement_rgpd) 
VALUES (70, 'Véronique Leduc', 'charrierguillaume@example.com', '655d24a1efe0d9e80fe197e294933183fcfc5e380921c94cd5225b821d8d006b', True);
INSERT INTO utilisateurs (id, nom, email, mot_de_passe, consentement_rgpd) 
VALUES (71, 'Aimée Berger', 'rodriguezhenriette@example.net', 'c90ca9d25ce83ce3da22b0d4824db206b32561886c2f6fda363ebe89eb0018e1', False);
INSERT INTO utilisateurs (id, nom, email, mot_de_passe, consentement_rgpd) 
VALUES (72, 'Sylvie Leduc de la Vasseur', 'jbrunel@example.net', '1800400f2d5857fc1b69314dbec2bddfb87e740a913d5d4d22afa8f5db86d4f6', True);
INSERT INTO utilisateurs (id, nom, email, mot_de_passe, consentement_rgpd) 
VALUES (73, 'Emmanuel Ollivier', 'rossiconstance@example.org', '20d3444bd210822936e58f56ac774a1298d8243fb71cb14836668a7d9171c330', False);
INSERT INTO utilisateurs (id, nom, email, mot_de_passe, consentement_rgpd) 
VALUES (74, 'Capucine-Pauline Lucas', 'christiane31@example.com', '2ca5eb48533f5abddb990784e3d7cb5baf422f8ff5cb6b92ef30dd588c684508', True);
INSERT INTO utilisateurs (id, nom, email, mot_de_passe, consentement_rgpd) 
VALUES (75, 'René-Marcel Moreno', 'juliette46@example.org', '863acb6723ab6ebf725f89b889182f4f159d6a2c43588cfbd46b846c93ed2585', True);
INSERT INTO utilisateurs (id, nom, email, mot_de_passe, consentement_rgpd) 
VALUES (76, 'Pierre du Maillot', 'renardamelie@example.net', '5099be486aca96ce7b252feb4ac09a4832c837eaacd78dda2b3357a0c0d21a82', False);
INSERT INTO utilisateurs (id, nom, email, mot_de_passe, consentement_rgpd) 
VALUES (77, 'Adrienne Renaud', 'leon09@example.net', '189b8380ae9717cc7c7f34960b2ae52241566425a449e9db4f3b49499cc92527', False);
INSERT INTO utilisateurs (id, nom, email, mot_de_passe, consentement_rgpd) 
VALUES (78, 'Marine Perrot-Baron', 'julieleclercq@example.com', '4881cc13d69653cb9b6adb73f35a3ccd2eae1dfc04f2b38a39766ad08119a4cc', False);
INSERT INTO utilisateurs (id, nom, email, mot_de_passe, consentement_rgpd) 
VALUES (79, 'Jacqueline Boulay', 'philippine77@example.net', '88bb2133fc6574a3f8bdcfd920af6822d61c520687d6f3518a5d84ce4e07e369', True);
INSERT INTO utilisateurs (id, nom, email, mot_de_passe, consentement_rgpd) 
VALUES (80, 'Astrid Lenoir', 'christellebouvier@example.com', '08672e125c9a841f7b075be518e7423340f16d2e7ac2f862c17b5264bd788f72', False);
INSERT INTO utilisateurs (id, nom, email, mot_de_passe, consentement_rgpd) 
VALUES (81, 'Augustin Labbé', 'abonneau@example.net', '149e2ea9e2f2c3f5d4adb241849f7a08293c1942ffd85c840d3f460f3e0d9da3', False);
INSERT INTO utilisateurs (id, nom, email, mot_de_passe, consentement_rgpd) 
VALUES (82, 'Alexandria Gaudin', 'anais27@example.org', 'ffd738a19cb19b6b061c87777a304eb9974e61480dd5b0f6db689a60a65c3d41', False);
INSERT INTO utilisateurs (id, nom, email, mot_de_passe, consentement_rgpd) 
VALUES (83, 'Françoise Humbert', 'aimee64@example.com', '8bf96ccf00593da6779f60bb5a2256eb2a523e092bc3f694174020d82af6cbce', False);
INSERT INTO utilisateurs (id, nom, email, mot_de_passe, consentement_rgpd) 
VALUES (84, 'Thomas Blondel', 'simone74@example.com', 'b31497a215cfe89f00c7fcbbe0e8540975568de8b5f8b8b06620870f59d422b7', False);
INSERT INTO utilisateurs (id, nom, email, mot_de_passe, consentement_rgpd) 
VALUES (85, 'Jérôme Potier', 'hortensebruneau@example.net', '29077b4a948f3d1b0a279bce5bf6592a881fef8a948569e0aa89f1546999db4b', False);
INSERT INTO utilisateurs (id, nom, email, mot_de_passe, consentement_rgpd) 
VALUES (86, 'Édouard Le Goff', 'thomasprevost@example.net', '32e005410a290906e467c7811be157acab558d1729d7b2af3909d1a23fcf3847', False);
INSERT INTO utilisateurs (id, nom, email, mot_de_passe, consentement_rgpd) 
VALUES (87, 'Caroline Gauthier', 'reynaudemmanuelle@example.org', 'f6e3da4fba294d6354e48f9ce10bbadcf0dc320741c63450d05ccb6779ab0ff5', True);
INSERT INTO utilisateurs (id, nom, email, mot_de_passe, consentement_rgpd) 
VALUES (88, 'Thérèse Bigot', 'emmanuelle72@example.net', '692b0132e03ee93b671feb0c07aee4b511ea3b467905477881efb7441d823a2b', False);
INSERT INTO utilisateurs (id, nom, email, mot_de_passe, consentement_rgpd) 
VALUES (89, 'Aimé Martin de la Barre', 'charlotte80@example.net', '5a6a19f5572ee5f0fa9f156ef75415f90ef1bf5f32c8b44c17192a65a08adfe3', True);
INSERT INTO utilisateurs (id, nom, email, mot_de_passe, consentement_rgpd) 
VALUES (90, 'Isabelle Blondel', 'roland84@example.com', '794774472a9538eb1e2e4a8f9395520d8bf87e4e9a7c5fb6dbf318fa23b8e9a4', True);
INSERT INTO utilisateurs (id, nom, email, mot_de_passe, consentement_rgpd) 
VALUES (91, 'Gabriel Robin', 'alexandreteixeira@example.org', '0cfb8eb1e5bd33e10cf706f9a3033b9a46cbe400f58724c6f8c058bb04305d5d', False);
INSERT INTO utilisateurs (id, nom, email, mot_de_passe, consentement_rgpd) 
VALUES (92, 'Agathe Rivière', 'alicepires@example.com', '48519aae5ae4e372e89480a5658d02f2ccde9677f3c630a7fc2cea8615988e36', True);
INSERT INTO utilisateurs (id, nom, email, mot_de_passe, consentement_rgpd) 
VALUES (93, 'Eugène Alves de Martineau', 'frederichuet@example.net', 'b27f994d851c8794c9753e90812f7c8191956c8d66f9e92d7159d644dcfd4172', True);
INSERT INTO utilisateurs (id, nom, email, mot_de_passe, consentement_rgpd) 
VALUES (94, 'Maggie Thierry de Lopez', 'madeleine28@example.org', '65cd9f32a00c341a77abb61ea410292350070c3e32fcdadff019d947cd390003', True);
INSERT INTO utilisateurs (id, nom, email, mot_de_passe, consentement_rgpd) 
VALUES (95, 'Éléonore-Marine Breton', 'mparis@example.net', 'a0e3cf0c35d7f605728879a401e8bebff4bc91424cb4b07c4f26ca29f176d75b', True);
INSERT INTO utilisateurs (id, nom, email, mot_de_passe, consentement_rgpd) 
VALUES (96, 'Nath Aubert-Hardy', 'jgosselin@example.org', 'eb72237a418fc942827558fd7882bc2b29c4bee2b60e3549b026adc86de13d60', True);
INSERT INTO utilisateurs (id, nom, email, mot_de_passe, consentement_rgpd) 
VALUES (97, 'Joséphine Girard Le Louis', 'richardmarc@example.net', '6dc47a900ffe5015e4a166e009dc5937a11498154ade636d2b1cbab6cf861b86', True);
INSERT INTO utilisateurs (id, nom, email, mot_de_passe, consentement_rgpd) 
VALUES (98, 'Benoît Pages', 'elisabethcollin@example.org', '217ad41a132d978af5af0a32c1e26c8127e634e3e7de583877f459015ad81a63', True);
INSERT INTO utilisateurs (id, nom, email, mot_de_passe, consentement_rgpd) 
VALUES (99, 'Maggie de la Joubert', 'ubenard@example.net', 'dfbc55d724281635a26c9dda9db06880137fe82e0cc9cdb8ff48f21ba9a0ed6a', True);
INSERT INTO utilisateurs (id, nom, email, mot_de_passe, consentement_rgpd) 
VALUES (100, 'Raymond Dufour', 'aime43@example.org', 'f7f533ef18469a4d3cf7dc0de287d844fef8602f2d20b712dfcd4076f98987de', True);
