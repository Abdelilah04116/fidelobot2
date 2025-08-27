-- Table produits
CREATE TABLE IF NOT EXISTS produits (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(200) NOT NULL,
    prix DECIMAL(10,2) NOT NULL,
    stock INTEGER DEFAULT 0,
    categorie_id INTEGER REFERENCES categories(id),
    description_courte TEXT,
    caracteristiques_structurees JSONB
);

INSERT INTO produits (id, nom, prix, stock, categorie_id, description_courte, caracteristiques_structurees) 
VALUES (1, 'ThinkPad X1 Carbon - Violet orchidée moyen', 1524, 377, 2, 'Laptop professionnel ultra-léger, certifié MIL-STD', '{"processeur": "Intel i7", "ram": "16GB", "stockage": "512GB SSD"}');
INSERT INTO produits (id, nom, prix, stock, categorie_id, description_courte, caracteristiques_structurees) 
VALUES (2, 'HP Spectre x360', 1243, 16, 2, 'Laptop convertible 2-en-1 avec écran tactile OLED', '{"processeur": "Intel i7", "ram": "16GB", "stockage": "512GB SSD"}');
INSERT INTO produits (id, nom, prix, stock, categorie_id, description_courte, caracteristiques_structurees) 
VALUES (3, 'Samsung Galaxy S24', 957, 287, 1, 'Smartphone Android avec écran Dynamic AMOLED 6.2 pouces, processeur Snapdragon 8 Gen 3', '{"ecran": "6.2 pouces", "stockage": "256GB", "appareil_photo": "50MP"}');
INSERT INTO produits (id, nom, prix, stock, categorie_id, description_courte, caracteristiques_structurees) 
VALUES (4, 'Traore SARL Composants P Max', 2922, 112, 4, 'Qualité plusieurs suite bataille. An bête dehors observer miser prière.', '{"couleur": "Beige citron soie", "poids": "1216g", "garantie": "2 ans"}');
INSERT INTO produits (id, nom, prix, stock, categorie_id, description_courte, caracteristiques_structurees) 
VALUES (5, 'Verdier Accessoire Max', 2463, 388, 8, 'Peu religion voici. Soirée fidèle idée science clef.
Plaisir premier police autour partie. Propre coeur feuille voisin passé mille politique. Découvrir an enfoncer distance.', '{"couleur": "Blanc menthe", "poids": "669g", "garantie": "1 ans"}');
INSERT INTO produits (id, nom, prix, stock, categorie_id, description_courte, caracteristiques_structurees) 
VALUES (6, 'Samsung Galaxy Tab S9 - Beige papaye', 791, 490, 3, 'Tablette Android premium avec S Pen inclus', '{"ecran": "11 pouces", "stockage": "256GB", "connectivite": "Wi-Fi"}');
INSERT INTO produits (id, nom, prix, stock, categorie_id, description_courte, caracteristiques_structurees) 
VALUES (7, 'Grégoire Teixeira SA Audi Pro', 468, 49, 6, 'Pareil respirer gloire attitude. Nouveau intelligence dessus mettre trente poids.
Raison regarder étage école cinq absence professeur. Vide recommencer livrer briller paraître.', '{"couleur": "Rose", "poids": "289g", "garantie": "2 ans"}');
INSERT INTO produits (id, nom, prix, stock, categorie_id, description_courte, caracteristiques_structurees) 
VALUES (8, 'Rodriguez Delmas S.A.R.L. Audi Elite', 1458, 413, 6, 'Malade oeuvre véritable tourner rapport. Preuve fort plante faux surveiller.', '{"couleur": "Saumon", "poids": "1336g", "garantie": "2 ans"}');
INSERT INTO produits (id, nom, prix, stock, categorie_id, description_courte, caracteristiques_structurees) 
VALUES (9, 'Pereira et Fils Smartphone Ultra', 2246, 40, 1, 'Fumer société article perdre pays atteindre. Réussir brusquement contraire mariage changement connaissance. Désormais toit heure situation mer arracher y.
Tôt sérieux combat jour.', '{"couleur": "Brun ros\u00e9", "poids": "355g", "garantie": "2 ans"}');
INSERT INTO produits (id, nom, prix, stock, categorie_id, description_courte, caracteristiques_structurees) 
VALUES (10, 'Collet Carpentier SA Périphérique Elite', 2583, 295, 5, 'Quitter assez neuf lier. Ciel veiller avis conseil nourrir pluie demain. Trembler monter naître appartement.
Personne moitié engager digne plaisir enfermer. Forcer plante eh engager ramener.', '{"couleur": "Rose", "poids": "1913g", "garantie": "2 ans"}');
INSERT INTO produits (id, nom, prix, stock, categorie_id, description_courte, caracteristiques_structurees) 
VALUES (11, 'Lemaître Jacquet S.A. Composants P Ultra', 237, 395, 4, 'Or voile perdu accord rouge. Tout bouche soudain discours subir. Chose drame creuser été porter seulement lire.
Beaux goutte doucement. Espace certainement violent.', '{"couleur": "Ivoire", "poids": "1454g", "garantie": "1 ans"}');
INSERT INTO produits (id, nom, prix, stock, categorie_id, description_courte, caracteristiques_structurees) 
VALUES (12, 'Lacroix Périphérique Max', 1003, 194, 5, 'Renoncer sourire frère pain choisir tout. Village roche soulever air.
Réveiller soi roche disposer représenter brûler. Silence d''autres rose. Étranger ruine somme d''autres petit fort doute.', '{"couleur": "Orange fonc\u00e9", "poids": "1874g", "garantie": "1 ans"}');
INSERT INTO produits (id, nom, prix, stock, categorie_id, description_courte, caracteristiques_structurees) 
VALUES (13, 'Keychron K8', -28, 107, 5, 'Clavier mécanique sans fil compact', '{"switches": "Cherry MX", "connectivite": "Bluetooth + USB"}');
INSERT INTO produits (id, nom, prix, stock, categorie_id, description_courte, caracteristiques_structurees) 
VALUES (14, 'Nicolas S.A.S. Périphérique Ultra', 2849, 311, 5, 'Haïr vivant campagne surveiller content approcher. Abattre ton masse prix que plan. Groupe trouver titre papier phrase céder.
En front franc écrire centre geste travers. Ou élément mener à.', '{"couleur": "Jaune clair", "poids": "1427g", "garantie": "1 ans"}');
INSERT INTO produits (id, nom, prix, stock, categorie_id, description_courte, caracteristiques_structurees) 
VALUES (15, 'iPad Pro 12.9"', 1082, 138, 3, 'Tablette professionnelle avec puce M2, écran Liquid Retina XDR', '{"ecran": "12.9 pouces", "stockage": "256GB", "connectivite": "Wi-Fi + 5G"}');
INSERT INTO produits (id, nom, prix, stock, categorie_id, description_courte, caracteristiques_structurees) 
VALUES (16, 'NVIDIA RTX 4080', 1116, 412, 4, 'Carte graphique haut de gamme pour gaming et création', '{"memoire": "16GB GDDR6X", "architecture": "Ada Lovelace"}');
INSERT INTO produits (id, nom, prix, stock, categorie_id, description_courte, caracteristiques_structurees) 
VALUES (17, 'Morin Audi Max', 1693, 108, 6, 'Rideau chef après vivant oncle. Île soutenir moyen prison.
Fortune chef porter suivant simple sous rencontrer. Composer valeur lune arracher désirer. Imaginer rêve placer voir.', '{"couleur": "Rose brumeux", "poids": "648g", "garantie": "1 ans"}');
INSERT INTO produits (id, nom, prix, stock, categorie_id, description_courte, caracteristiques_structurees) 
VALUES (18, 'Cordier Audi Plus', 920, 202, 6, 'Gauche coûter geste tandis que nerveux pourtant signe. Fier accepter étroit rapide si un genre. Réunir sur juge donner jour flamme plaine.', '{"couleur": "Bleu alice", "poids": "1442g", "garantie": "2 ans"}');
INSERT INTO produits (id, nom, prix, stock, categorie_id, description_courte, caracteristiques_structurees) 
VALUES (19, 'Faure Accessoire Ultra', 635, 126, 8, 'Arrivée un de aussitôt vaincre appartement amuser.
Secret paix demi inutile calmer. Inquiétude devenir falloir oeil ventre.
Vérité brûler ajouter énergie. Forêt prier avant posséder pareil bon.', '{"couleur": "Blanc menthe", "poids": "642g", "garantie": "1 ans"}');
INSERT INTO produits (id, nom, prix, stock, categorie_id, description_courte, caracteristiques_structurees) 
VALUES (20, 'Neveu Périphérique Max', 1804, 204, 5, 'Puisque verre dix rire. Remercier inquiétude saluer nord entourer dès train. Soulever dernier inquiétude on feuille.
Seuil confiance crise retour étage souhaiter préférer.', '{"couleur": "Bleu de minuit", "poids": "1938g", "garantie": "3 ans"}');
INSERT INTO produits (id, nom, prix, stock, categorie_id, description_courte, caracteristiques_structurees) 
VALUES (21, 'Lamy Audi Elite', 948, 252, 6, 'Premier doigt dessus casser contre carte. Type posséder contraire quarante doucement nom recherche. Droit bois conversation décider condamner adresser marche dormir.', '{"couleur": "Bleu clair", "poids": "383g", "garantie": "3 ans"}');
INSERT INTO produits (id, nom, prix, stock, categorie_id, description_courte, caracteristiques_structurees) 
VALUES (22, 'Leblanc Laptop Max', 499, 81, 2, 'Traverser jaune sac fou autrement.', '{"couleur": "Corail clair", "poids": "413g", "garantie": "3 ans"}');
INSERT INTO produits (id, nom, prix, stock, categorie_id, description_courte, caracteristiques_structurees) 
VALUES (23, 'Lejeune S.A.R.L. Gamin Elite', 2492, 195, 7, 'Ancien durer droit silencieux autour. Tombe représenter par peu tracer. Calmer de chemise discuter chanter attaquer.', '{"couleur": "Gris clair", "poids": "230g", "garantie": "2 ans"}');
INSERT INTO produits (id, nom, prix, stock, categorie_id, description_courte, caracteristiques_structurees) 
VALUES (24, 'Verdier Accessoire Pro', 2217, 440, 8, 'Lutte hésiter douleur vrai haine rompre vêtement. Étouffer espace plaisir signifier épaule pourquoi durer.', '{"couleur": "Chocolat", "poids": "614g", "garantie": "3 ans"}');
INSERT INTO produits (id, nom, prix, stock, categorie_id, description_courte, caracteristiques_structurees) 
VALUES (25, 'iPhone 15 Pro', 1348, 384, 1, 'Smartphone haut de gamme avec puce A17 Pro, écran Super Retina XDR 6.1 pouces, triple caméra 48MP', '{"ecran": "6.1 pouces", "stockage": "128GB", "appareil_photo": "48MP"}');
INSERT INTO produits (id, nom, prix, stock, categorie_id, description_courte, caracteristiques_structurees) 
VALUES (26, 'Hervé Navarro et Fils Périphérique Ultra', 1443, 222, 5, 'Vieil oiseau dent. Endormir admettre froid de.
Trop paysan choisir toute éclairer près gauche. Visage dernier mériter fille toi loi souffrance.', '{"couleur": "Bleu toile", "poids": "328g", "garantie": "2 ans"}');
INSERT INTO produits (id, nom, prix, stock, categorie_id, description_courte, caracteristiques_structurees) 
VALUES (27, 'Surface Pro 9', 1347, 497, 3, 'Tablette Windows 2-en-1 avec clavier détachable', '{"ecran": "13 pouces", "stockage": "256GB", "connectivite": "Wi-Fi"}');
INSERT INTO produits (id, nom, prix, stock, categorie_id, description_courte, caracteristiques_structurees) 
VALUES (28, 'iPad Pro 12.9"', 1444, 430, 3, 'Tablette professionnelle avec puce M2, écran Liquid Retina XDR', '{"ecran": "12.9 pouces", "stockage": "256GB", "connectivite": "Wi-Fi + 5G"}');
INSERT INTO produits (id, nom, prix, stock, categorie_id, description_courte, caracteristiques_structurees) 
VALUES (29, 'AMD Ryzen 9 7950X', 775, 472, 4, 'Processeur 16 cœurs haute performance', '{"coeurs": "16", "frequence": "4.5 GHz"}');
INSERT INTO produits (id, nom, prix, stock, categorie_id, description_courte, caracteristiques_structurees) 
VALUES (30, 'OnePlus 12 - Pourpre', 608, 185, 1, 'Smartphone haute performance avec charge rapide 100W', '{"ecran": "6.82 pouces", "stockage": "256GB", "appareil_photo": "50MP"}');
INSERT INTO produits (id, nom, prix, stock, categorie_id, description_courte, caracteristiques_structurees) 
VALUES (31, 'Logitech MX Master 3S', 358, 40, 5, 'Souris ergonomique sans fil pour professionnels', '{"connectivite": "Bluetooth + USB", "autonomie": "70 jours"}');
INSERT INTO produits (id, nom, prix, stock, categorie_id, description_courte, caracteristiques_structurees) 
VALUES (32, 'Tanguy Laptop Ultra', 333, 392, 2, 'Mesure mêler île entier consulter pouvoir. Fil sien fumée énorme interrompre tenir figure. Lendemain annoncer lien nombre.
Boire tempête affirmer charger somme victime. Intéresser vêtement est pour.', '{"couleur": "Prune", "poids": "1657g", "garantie": "3 ans"}');
INSERT INTO produits (id, nom, prix, stock, categorie_id, description_courte, caracteristiques_structurees) 
VALUES (33, 'Samsung Galaxy Tab S9', 1133, 135, 3, 'Tablette Android premium avec S Pen inclus', '{"ecran": "11 pouces", "stockage": "256GB", "connectivite": "Wi-Fi"}');
INSERT INTO produits (id, nom, prix, stock, categorie_id, description_courte, caracteristiques_structurees) 
VALUES (34, 'Hebert S.A. Gamin Plus', 917, 353, 7, 'Entrée asseoir exister.
Derrière fusil point condition. Avenir somme page déposer. Charge impossible deux devant accrocher revoir table plutôt.', '{"couleur": "Vert printemps moyen", "poids": "1204g", "garantie": "3 ans"}');
INSERT INTO produits (id, nom, prix, stock, categorie_id, description_courte, caracteristiques_structurees) 
VALUES (35, 'Bruneau Composants P Plus', 1684, 191, 4, 'Vin perte dormir. Soin rencontre vieillard tempête question savoir taille.
Réveiller danger content dessiner rapport regard point chaise. Taille pays en hauteur.', '{"couleur": "Miellat", "poids": "1475g", "garantie": "3 ans"}');
INSERT INTO produits (id, nom, prix, stock, categorie_id, description_courte, caracteristiques_structurees) 
VALUES (36, 'Delaunay SA Accessoire Plus', 2169, 126, 8, 'Il plein plante neuf. Brûler déjà air sourire miser terminer. Paysan partie inquiéter précis pencher.
Après annoncer voyager campagne. Souvenir chair ignorer plan quelque.', '{"couleur": "Blanc Lin", "poids": "1024g", "garantie": "1 ans"}');
INSERT INTO produits (id, nom, prix, stock, categorie_id, description_courte, caracteristiques_structurees) 
VALUES (37, 'NVIDIA RTX 4080', 1300, 301, 4, 'Carte graphique haut de gamme pour gaming et création', '{"memoire": "16GB GDDR6X", "architecture": "Ada Lovelace"}');
INSERT INTO produits (id, nom, prix, stock, categorie_id, description_courte, caracteristiques_structurees) 
VALUES (38, 'NVIDIA RTX 4080 - Vert océan foncé', 1116, 16, 4, 'Carte graphique haut de gamme pour gaming et création', '{"memoire": "16GB GDDR6X", "architecture": "Ada Lovelace"}');
INSERT INTO produits (id, nom, prix, stock, categorie_id, description_courte, caracteristiques_structurees) 
VALUES (39, 'Aubert Audi Pro', 340, 142, 6, 'Peur passion nu aider. Dernier celui mois aussitôt réel coûter. Rôle dehors remercier réserver nouveau.
Voile matin retourner bureau. Certes existence réserver.', '{"couleur": "Jaune vert", "poids": "1152g", "garantie": "1 ans"}');
INSERT INTO produits (id, nom, prix, stock, categorie_id, description_courte, caracteristiques_structurees) 
VALUES (40, 'Godard Accessoire Elite', 927, 370, 8, 'Lisser gris ressembler calmer père soudain mesure. Gris souvent garçon sang fort.
Grain pierre femme chien toit auquel. Bête blanc quart rocher.', '{"couleur": "Violet orchid\u00e9e", "poids": "1204g", "garantie": "1 ans"}');
INSERT INTO produits (id, nom, prix, stock, categorie_id, description_courte, caracteristiques_structurees) 
VALUES (41, 'Berthelot Accessoire Plus', 1045, 413, 8, 'Mouvement rien sentier vieux rouler. Plonger militaire oiseau personne pourquoi amener donner reconnaître.', '{"couleur": "Corail clair", "poids": "1706g", "garantie": "2 ans"}');
INSERT INTO produits (id, nom, prix, stock, categorie_id, description_courte, caracteristiques_structurees) 
VALUES (42, 'Parent SA Gamin Plus', 829, 337, 7, 'Jour hésiter donner rappeler calme gris. Poche note mal en dans. As courir troisième refuser réduire eaux cas lettre.', '{"couleur": "Vert marin clair", "poids": "293g", "garantie": "1 ans"}');
INSERT INTO produits (id, nom, prix, stock, categorie_id, description_courte, caracteristiques_structurees) 
VALUES (43, 'Blanc Gamin Ultra', 1501, 239, 7, 'Habitude fou avec sombre queue. Escalier commander long calme long.', '{"couleur": "Brun kaki", "poids": "967g", "garantie": "2 ans"}');
INSERT INTO produits (id, nom, prix, stock, categorie_id, description_courte, caracteristiques_structurees) 
VALUES (44, 'iPhone 15 Pro', 1030, 173, 1, 'Smartphone haut de gamme avec puce A17 Pro, écran Super Retina XDR 6.1 pouces, triple caméra 48MP', '{"ecran": "6.1 pouces", "stockage": "128GB", "appareil_photo": "48MP"}');
INSERT INTO produits (id, nom, prix, stock, categorie_id, description_courte, caracteristiques_structurees) 
VALUES (45, 'Dell XPS 13', 1373, 216, 2, 'Ultrabook premium avec processeur Intel Core i7, écran InfinityEdge', '{"processeur": "Intel i7", "ram": "16GB", "stockage": "1TB SSD"}');
INSERT INTO produits (id, nom, prix, stock, categorie_id, description_courte, caracteristiques_structurees) 
VALUES (46, 'iPad Pro 12.9"', 1446, 226, 3, 'Tablette professionnelle avec puce M2, écran Liquid Retina XDR', '{"ecran": "12.9 pouces", "stockage": "256GB", "connectivite": "Wi-Fi + 5G"}');
INSERT INTO produits (id, nom, prix, stock, categorie_id, description_courte, caracteristiques_structurees) 
VALUES (47, 'HP Spectre x360 - Terre de Sienne', 1627, 47, 2, 'Laptop convertible 2-en-1 avec écran tactile OLED', '{"processeur": "Intel i7", "ram": "16GB", "stockage": "512GB SSD"}');
INSERT INTO produits (id, nom, prix, stock, categorie_id, description_courte, caracteristiques_structurees) 
VALUES (48, 'Samsung 990 PRO - Blanc dentelle', 245, 205, 4, 'SSD NVMe ultra-rapide 2TB', '{"capacite": "2TB", "interface": "PCIe 4.0"}');
INSERT INTO produits (id, nom, prix, stock, categorie_id, description_courte, caracteristiques_structurees) 
VALUES (49, 'iPhone 15 Pro - Citron vert', 1198, 401, 1, 'Smartphone haut de gamme avec puce A17 Pro, écran Super Retina XDR 6.1 pouces, triple caméra 48MP', '{"ecran": "6.1 pouces", "stockage": "128GB", "appareil_photo": "48MP"}');
INSERT INTO produits (id, nom, prix, stock, categorie_id, description_courte, caracteristiques_structurees) 
VALUES (50, 'Ruiz S.A.R.L. Accessoire Ultra', 1218, 490, 8, 'Falloir dur pauvre ville.
Notre fin nature usage quart appartenir tellement mort. Entier jamais cheval attention bouche.', '{"couleur": "Pourpre", "poids": "966g", "garantie": "3 ans"}');
INSERT INTO produits (id, nom, prix, stock, categorie_id, description_courte, caracteristiques_structurees) 
VALUES (51, 'Faure Accessoire Elite', 684, 111, 8, 'Encore personnage peur cercle président barbe. Ferme respecter rôle plaisir santé quart pont.
Pays goutte expression extraordinaire. Type état réflexion contraire. Choix écrire réserver livrer.', '{"couleur": "Aigue-marine moyen", "poids": "488g", "garantie": "2 ans"}');
INSERT INTO produits (id, nom, prix, stock, categorie_id, description_courte, caracteristiques_structurees) 
VALUES (52, 'Xiaomi 14', 480, 29, 1, 'Smartphone avec caméra Leica, écran LTPO OLED', '{"ecran": "6.36 pouces", "stockage": "256GB", "appareil_photo": "50MP"}');
INSERT INTO produits (id, nom, prix, stock, categorie_id, description_courte, caracteristiques_structurees) 
VALUES (53, 'Xiaomi 14', 919, 80, 1, 'Smartphone avec caméra Leica, écran LTPO OLED', '{"ecran": "6.36 pouces", "stockage": "256GB", "appareil_photo": "50MP"}');
INSERT INTO produits (id, nom, prix, stock, categorie_id, description_courte, caracteristiques_structurees) 
VALUES (54, 'Lecoq Smartphone Plus', 378, 35, 1, 'Malade vers rouge rêve champ désormais passer. Mien bonheur sentiment seuil droite recueillir. Hors loup sauvage beaux tempête.', '{"couleur": "Bleu p\u00e9trole", "poids": "1843g", "garantie": "1 ans"}');
INSERT INTO produits (id, nom, prix, stock, categorie_id, description_courte, caracteristiques_structurees) 
VALUES (55, 'Dell XPS 13 - Turquoise', 1305, 455, 2, 'Ultrabook premium avec processeur Intel Core i7, écran InfinityEdge', '{"processeur": "Intel i7", "ram": "16GB", "stockage": "1TB SSD"}');
INSERT INTO produits (id, nom, prix, stock, categorie_id, description_courte, caracteristiques_structurees) 
VALUES (56, 'NVIDIA RTX 4080 - Gris mat', 1316, 336, 4, 'Carte graphique haut de gamme pour gaming et création', '{"memoire": "16GB GDDR6X", "architecture": "Ada Lovelace"}');
INSERT INTO produits (id, nom, prix, stock, categorie_id, description_courte, caracteristiques_structurees) 
VALUES (57, 'Moreau SARL Audi Max', 1118, 366, 6, 'Travers oiseau goût remonter demeurer causer demi. Immense ça tant nouveau âgé lui depuis charge.', '{"couleur": "Rose", "poids": "518g", "garantie": "3 ans"}');
INSERT INTO produits (id, nom, prix, stock, categorie_id, description_courte, caracteristiques_structurees) 
VALUES (58, 'Guillot Audi Pro', 1027, 67, 6, 'Cesser étude est patron sauvage politique. Parole rocher attitude remonter immobile école approcher. Soutenir enfoncer encore fort rose. Détruire rapide continuer exemple rentrer soir erreur.', '{"couleur": "Saumon clair", "poids": "643g", "garantie": "2 ans"}');
INSERT INTO produits (id, nom, prix, stock, categorie_id, description_courte, caracteristiques_structurees) 
VALUES (59, 'Logitech MX Master 3S', -87, 288, 5, 'Souris ergonomique sans fil pour professionnels', '{"connectivite": "Bluetooth + USB", "autonomie": "70 jours"}');
INSERT INTO produits (id, nom, prix, stock, categorie_id, description_courte, caracteristiques_structurees) 
VALUES (60, 'Dell XPS 13 - Beige citron soie', 1358, 477, 2, 'Ultrabook premium avec processeur Intel Core i7, écran InfinityEdge', '{"processeur": "Intel i7", "ram": "16GB", "stockage": "1TB SSD"}');
INSERT INTO produits (id, nom, prix, stock, categorie_id, description_courte, caracteristiques_structurees) 
VALUES (61, 'Henry Audi Pro', 331, 189, 6, 'Employer obtenir grâce position être. Prononcer temps oser. Dormir violent trou avance pas face.
Chaque offrir renverser. Celui demande payer.', '{"couleur": "Violet fonc\u00e9", "poids": "1900g", "garantie": "1 ans"}');
INSERT INTO produits (id, nom, prix, stock, categorie_id, description_courte, caracteristiques_structurees) 
VALUES (62, 'Dell UltraSharp U2723QE', 759, 413, 5, 'Moniteur 4K 27 pouces pour professionnels', '{"resolution": "4K", "taille": "27 pouces"}');
INSERT INTO produits (id, nom, prix, stock, categorie_id, description_courte, caracteristiques_structurees) 
VALUES (63, 'Xiaomi 14', 602, 53, 1, 'Smartphone avec caméra Leica, écran LTPO OLED', '{"ecran": "6.36 pouces", "stockage": "256GB", "appareil_photo": "50MP"}');
INSERT INTO produits (id, nom, prix, stock, categorie_id, description_courte, caracteristiques_structurees) 
VALUES (64, 'iPad Pro 12.9"', 1379, 139, 3, 'Tablette professionnelle avec puce M2, écran Liquid Retina XDR', '{"ecran": "12.9 pouces", "stockage": "256GB", "connectivite": "Wi-Fi + 5G"}');
INSERT INTO produits (id, nom, prix, stock, categorie_id, description_courte, caracteristiques_structurees) 
VALUES (65, 'Dell UltraSharp U2723QE - Orange foncé', 574, 324, 5, 'Moniteur 4K 27 pouces pour professionnels', '{"resolution": "4K", "taille": "27 pouces"}');
INSERT INTO produits (id, nom, prix, stock, categorie_id, description_courte, caracteristiques_structurees) 
VALUES (66, 'Keychron K8', 352, 26, 5, 'Clavier mécanique sans fil compact', '{"switches": "Cherry MX", "connectivite": "Bluetooth + USB"}');
INSERT INTO produits (id, nom, prix, stock, categorie_id, description_courte, caracteristiques_structurees) 
VALUES (67, 'ThinkPad X1 Carbon - Orange', 1421, 394, 2, 'Laptop professionnel ultra-léger, certifié MIL-STD', '{"processeur": "Intel i7", "ram": "16GB", "stockage": "512GB SSD"}');
INSERT INTO produits (id, nom, prix, stock, categorie_id, description_courte, caracteristiques_structurees) 
VALUES (68, 'Samsung Galaxy Tab S9', 731, 282, 3, 'Tablette Android premium avec S Pen inclus', '{"ecran": "11 pouces", "stockage": "256GB", "connectivite": "Wi-Fi"}');
INSERT INTO produits (id, nom, prix, stock, categorie_id, description_courte, caracteristiques_structurees) 
VALUES (69, 'Benoit Gamin Elite', 2347, 38, 7, 'Couleur chair autrement commun preuve vrai robe. Plaindre presque mer écarter eh ciel.
Loi cause coup chance résoudre aller. Mort instinct vite certain sourire aujourd''hui fort.', '{"couleur": "Amande", "poids": "119g", "garantie": "1 ans"}');
INSERT INTO produits (id, nom, prix, stock, categorie_id, description_courte, caracteristiques_structurees) 
VALUES (70, 'Samsung Galaxy Tab S9', 947, 220, 3, 'Tablette Android premium avec S Pen inclus', '{"ecran": "11 pouces", "stockage": "256GB", "connectivite": "Wi-Fi"}');
INSERT INTO produits (id, nom, prix, stock, categorie_id, description_courte, caracteristiques_structurees) 
VALUES (71, 'Samsung Galaxy Tab S9', 1109, 497, 3, 'Tablette Android premium avec S Pen inclus', '{"ecran": "11 pouces", "stockage": "256GB", "connectivite": "Wi-Fi"}');
INSERT INTO produits (id, nom, prix, stock, categorie_id, description_courte, caracteristiques_structurees) 
VALUES (72, 'Paul Smartphone Plus', 910, 341, 1, 'Côte vague dormir par oser. Lien comme trembler choisir.', '{"couleur": "Jaune dor\u00e9 fonc\u00e9", "poids": "1496g", "garantie": "1 ans"}');
INSERT INTO produits (id, nom, prix, stock, categorie_id, description_courte, caracteristiques_structurees) 
VALUES (73, 'HP Spectre x360', 1651, 498, 2, 'Laptop convertible 2-en-1 avec écran tactile OLED', '{"processeur": "Intel i7", "ram": "16GB", "stockage": "512GB SSD"}');
INSERT INTO produits (id, nom, prix, stock, categorie_id, description_courte, caracteristiques_structurees) 
VALUES (74, 'Alexandre Tablette Max', 1019, 499, 3, 'Mode ensemble installer distance désigner blanc écarter. Soi genou vent tache roman tracer. Content cinquante voyager instant souffrance lettre.', '{"couleur": "Blanc floral", "poids": "1870g", "garantie": "1 ans"}');
INSERT INTO produits (id, nom, prix, stock, categorie_id, description_courte, caracteristiques_structurees) 
VALUES (75, 'Roux Tablette Elite', 151, 473, 3, 'Extraordinaire durer fine huit mentir. Poids caresser vieux fond résultat et travail rappeler. Observer foule appartement apparaître prévenir.', '{"couleur": "Gris gainsboro (Etain)", "poids": "467g", "garantie": "3 ans"}');
INSERT INTO produits (id, nom, prix, stock, categorie_id, description_courte, caracteristiques_structurees) 
VALUES (76, 'Aubry Audi Elite', 1736, 442, 6, 'Produire nerveux commencer parfaitement page. Chemin point an troubler bureau agir. Genre gagner courir libre oncle intérieur.
Lutte miser vue je. Enfant compagnie tendre etc événement relation.', '{"couleur": "Vert printemps moyen", "poids": "1742g", "garantie": "3 ans"}');
INSERT INTO produits (id, nom, prix, stock, categorie_id, description_courte, caracteristiques_structurees) 
VALUES (77, 'NVIDIA RTX 4080', 1194, 439, 4, 'Carte graphique haut de gamme pour gaming et création', '{"memoire": "16GB GDDR6X", "architecture": "Ada Lovelace"}');
INSERT INTO produits (id, nom, prix, stock, categorie_id, description_courte, caracteristiques_structurees) 
VALUES (78, 'Barre Accessoire Max', 961, 179, 8, 'Durant prévoir étoile. Personnage quinze croiser sans doigt mode.
Brusquement que dent arrêter. Debout dehors bois épaule interroger point chaleur.', '{"couleur": "Blanc", "poids": "508g", "garantie": "2 ans"}');
INSERT INTO produits (id, nom, prix, stock, categorie_id, description_courte, caracteristiques_structurees) 
VALUES (79, 'Costa Périphérique Max', 982, 337, 5, 'Accrocher monsieur briser. Droite voisin mêler le travail seuil.
Contre cacher clef importance devoir. Adresser essayer écraser pleurer. Complètement sien sûr sang lui.', '{"couleur": "Orange", "poids": "556g", "garantie": "1 ans"}');
INSERT INTO produits (id, nom, prix, stock, categorie_id, description_courte, caracteristiques_structurees) 
VALUES (80, 'Corsair Vengeance DDR5 - Blanc menthe', 541, 395, 4, 'Mémoire RAM haute performance 32GB', '{"capacite": "32GB", "frequence": "5600MHz"}');
INSERT INTO produits (id, nom, prix, stock, categorie_id, description_courte, caracteristiques_structurees) 
VALUES (81, 'Dell UltraSharp U2723QE', 603, 431, 5, 'Moniteur 4K 27 pouces pour professionnels', '{"resolution": "4K", "taille": "27 pouces"}');
INSERT INTO produits (id, nom, prix, stock, categorie_id, description_courte, caracteristiques_structurees) 
VALUES (82, 'Bonnet Martineau SA Audi Ultra', 163, 91, 6, 'François lien supérieur prendre. Posséder pas traverser fait dans.
Chien quitter oeil gauche mensonge intérieur marier. Recommencer poids nouveau représenter maître.', '{"couleur": "Jaune", "poids": "336g", "garantie": "2 ans"}');
INSERT INTO produits (id, nom, prix, stock, categorie_id, description_courte, caracteristiques_structurees) 
VALUES (83, 'Dell UltraSharp U2723QE', 621, 402, 5, 'Moniteur 4K 27 pouces pour professionnels', '{"resolution": "4K", "taille": "27 pouces"}');
INSERT INTO produits (id, nom, prix, stock, categorie_id, description_courte, caracteristiques_structurees) 
VALUES (84, 'Delaunay SARL Audi Pro', 1837, 59, 6, 'Autre goutte précipiter me atteindre sujet voie interroger. Front règle réfléchir vingt pays.', '{"couleur": "Bleu azur", "poids": "1341g", "garantie": "3 ans"}');
INSERT INTO produits (id, nom, prix, stock, categorie_id, description_courte, caracteristiques_structurees) 
VALUES (85, 'Rolland Gamin Max', 2411, 22, 7, 'Choix consulter sonner réfléchir ancien petit. Réfléchir sourire affirmer court bon anglais nu prendre. Derrière approcher haut.', '{"couleur": "Rouge", "poids": "489g", "garantie": "2 ans"}');
INSERT INTO produits (id, nom, prix, stock, categorie_id, description_courte, caracteristiques_structurees) 
VALUES (86, 'Berthelot Gamin Ultra', 56, 351, 7, 'Trembler planche reposer énorme gauche cher.
Rapidement inutile serrer élément. Riche terme moi verser. Malheur fixer devant épaule avenir hôtel fatiguer.', '{"couleur": "Rouge fonc\u00e9", "poids": "1164g", "garantie": "3 ans"}');
INSERT INTO produits (id, nom, prix, stock, categorie_id, description_courte, caracteristiques_structurees) 
VALUES (87, 'NVIDIA RTX 4080', 1484, 169, 4, 'Carte graphique haut de gamme pour gaming et création', '{"memoire": "16GB GDDR6X", "architecture": "Ada Lovelace"}');
INSERT INTO produits (id, nom, prix, stock, categorie_id, description_courte, caracteristiques_structurees) 
VALUES (88, 'Dupuis Audi Elite', 2767, 368, 6, 'Fier marche expérience dimanche lorsque. Installer révéler profiter recommencer ensuite courage enfance. Moi danser chat.', '{"couleur": "Vert marin clair", "poids": "1836g", "garantie": "1 ans"}');
INSERT INTO produits (id, nom, prix, stock, categorie_id, description_courte, caracteristiques_structurees) 
VALUES (89, 'Dell UltraSharp U2723QE', 608, 356, 5, 'Moniteur 4K 27 pouces pour professionnels', '{"resolution": "4K", "taille": "27 pouces"}');
INSERT INTO produits (id, nom, prix, stock, categorie_id, description_courte, caracteristiques_structurees) 
VALUES (90, 'Logitech MX Master 3S', 124, 194, 5, 'Souris ergonomique sans fil pour professionnels', '{"connectivite": "Bluetooth + USB", "autonomie": "70 jours"}');
INSERT INTO produits (id, nom, prix, stock, categorie_id, description_courte, caracteristiques_structurees) 
VALUES (91, 'Samsung Galaxy Tab S9', 856, 0, 3, 'Tablette Android premium avec S Pen inclus', '{"ecran": "11 pouces", "stockage": "256GB", "connectivite": "Wi-Fi"}');
INSERT INTO produits (id, nom, prix, stock, categorie_id, description_courte, caracteristiques_structurees) 
VALUES (92, 'Keychron K8', 291, 335, 5, 'Clavier mécanique sans fil compact', '{"switches": "Cherry MX", "connectivite": "Bluetooth + USB"}');
INSERT INTO produits (id, nom, prix, stock, categorie_id, description_courte, caracteristiques_structurees) 
VALUES (93, 'Peron Benard S.A. Audi Max', 1954, 345, 6, 'Connaître subir voiture vaincre mais secret autrement. Réduire fusil semaine. Aussi cheval dame image atteindre.', '{"couleur": "Jaune bl\u00e9", "poids": "1004g", "garantie": "2 ans"}');
INSERT INTO produits (id, nom, prix, stock, categorie_id, description_courte, caracteristiques_structurees) 
VALUES (94, 'AMD Ryzen 9 7950X - Amande', 836, 263, 4, 'Processeur 16 cœurs haute performance', '{"coeurs": "16", "frequence": "4.5 GHz"}');
INSERT INTO produits (id, nom, prix, stock, categorie_id, description_courte, caracteristiques_structurees) 
VALUES (95, 'Pottier Audi Pro', 432, 344, 6, 'François fermer jamais partout.
Lever habitant répondre moment. Supérieur tête décrire table.', '{"couleur": "Kaki", "poids": "1776g", "garantie": "1 ans"}');
INSERT INTO produits (id, nom, prix, stock, categorie_id, description_courte, caracteristiques_structurees) 
VALUES (96, 'Logitech MX Master 3S - Vert forêt', -16, 125, 5, 'Souris ergonomique sans fil pour professionnels', '{"connectivite": "Bluetooth + USB", "autonomie": "70 jours"}');
INSERT INTO produits (id, nom, prix, stock, categorie_id, description_courte, caracteristiques_structurees) 
VALUES (97, 'Lagarde Ramos SA Accessoire Elite', 2553, 233, 8, 'Blanc dehors avant. Règle user forêt religion ami donner volonté justice. Mettre fenêtre conseil nez fidèle relation.
Preuve avouer choisir prétendre parti. Engager briller accent en expliquer dix.', '{"couleur": "Jaune vert", "poids": "1840g", "garantie": "1 ans"}');
INSERT INTO produits (id, nom, prix, stock, categorie_id, description_courte, caracteristiques_structurees) 
VALUES (98, 'Richard Gamin Plus', 2629, 367, 7, 'Rendre projet ministre volonté depuis madame. Comme divers distinguer chat combien double. Joli avant dessus désert par.', '{"couleur": "Brun", "poids": "1278g", "garantie": "1 ans"}');
INSERT INTO produits (id, nom, prix, stock, categorie_id, description_courte, caracteristiques_structurees) 
VALUES (99, 'Normand Lecoq S.A.S. Gamin Pro', 2074, 75, 7, 'Haut échapper pour route retenir. Plein chance éloigner détail choisir goût. Autrement voix jeter fou lit tirer.', '{"couleur": "Bleu moyen", "poids": "918g", "garantie": "1 ans"}');
INSERT INTO produits (id, nom, prix, stock, categorie_id, description_courte, caracteristiques_structurees) 
VALUES (100, 'Cohen Besson S.A.R.L. Smartphone Ultra', 486, 112, 1, 'Cheval vraiment joie écraser tirer bas sauver. Étrange été répondre madame. Jambe haut poussière ensemble eh robe. Ailleurs été brusquement réunir.', '{"couleur": "Beige", "poids": "1694g", "garantie": "2 ans"}');
