-- Table tickets_service_client
CREATE TABLE IF NOT EXISTS tickets_service_client (
    id SERIAL PRIMARY KEY,
    utilisateur_id INTEGER REFERENCES utilisateurs(id),
    sujet VARCHAR(200) NOT NULL,
    description TEXT,
    statut VARCHAR(50) DEFAULT 'ouvert'
);

INSERT INTO tickets_service_client (id, utilisateur_id, sujet, description, statut) 
VALUES (1, 48, 'Modification de commande', 'Minute prêter appartement toile émotion juste quelqu''un. Étoile étroit paraître. Voyager vingt double attention devoir.
Triste trouver debout. Sûr personne battre figurer veiller or. Port général mot grain énergie oeil hors certes.', 'ferme');
INSERT INTO tickets_service_client (id, utilisateur_id, sujet, description, statut) 
VALUES (2, 60, 'Problème de paiement', 'Connaître secrétaire chasser ami. Souffrir garde fumer heure tracer sujet. Chez construire certes aller voie.
Oeil or nouveau défendre aller. Portier jambe lien odeur. Connaissance fixe inutile coin début front. Ton tuer d''autres.', 'resolu');
INSERT INTO tickets_service_client (id, utilisateur_id, sujet, description, statut) 
VALUES (3, 100, 'Demande de remboursement', 'Or quel notre maison sorte reprendre. Brusquement imaginer soudain soudain descendre marquer vivant. Million lumière parmi.
Échapper former émotion sang impossible.
Ordre article l''un chanter sauter. Beaucoup lèvre condamner neuf sujet même fonction. Humain conclure nombreux prêter cour il.', 'ferme');
INSERT INTO tickets_service_client (id, utilisateur_id, sujet, description, statut) 
VALUES (4, 21, 'Problème de paiement', 'Approcher commencer espoir somme social clef. Conclure prêter gens en. Eau conduire surprendre veiller absolu réfléchir acte.
Mêler accepter source demeurer noire jamais fuir. Objet accompagner soumettre douleur. Million salle armée chemin perdre année si placer.', 'en_cours');
INSERT INTO tickets_service_client (id, utilisateur_id, sujet, description, statut) 
VALUES (5, 78, 'Produit défectueux', 'Créer crainte assurer mort violence malgré battre. Tracer voie dur oiseau engager maître vous événement. Oser lentement protéger lettre.
Dehors écarter convenir caractère inquiétude retirer quant à couvrir. Y garde espèce minute pas achever couper drame.', 'resolu');
INSERT INTO tickets_service_client (id, utilisateur_id, sujet, description, statut) 
VALUES (6, 7, 'Modification de commande', 'Retomber payer jeune parcourir suite marier espérer. Toujours aspect madame mois poche mieux. Craindre pont retrouver.
Vêtir douze amuser vivant. Marcher colon oeil considérer capable répandre en signifier. Doigt bas sou.', 'ferme');
INSERT INTO tickets_service_client (id, utilisateur_id, sujet, description, statut) 
VALUES (7, 48, 'Support technique', 'Plusieurs cesse projet important prévenir main absolument. Porte notre bataille.
Bord réflexion queue. Musique énergie suite. Coup du marchand relever planche donc.
Calmer valoir ministre bonheur meilleur. Énorme chant préparer droit derrière autour ordre.', 'ouvert');
INSERT INTO tickets_service_client (id, utilisateur_id, sujet, description, statut) 
VALUES (8, 92, 'Problème de paiement', 'Certes rôle théâtre intelligence image politique presser. Intérêt trou charger supporter devoir face connaissance. Résistance source idée amour inviter être.
Dresser étrange moyen livrer. Rouge retirer entretenir pencher respirer marchand. Nombreux demi dernier cinquante joie aujourd''hui.', 'ouvert');
INSERT INTO tickets_service_client (id, utilisateur_id, sujet, description, statut) 
VALUES (9, 37, 'Problème de livraison', 'Nuage pont nouveau rue. Le petit beaucoup rouge souvenir taille. Rare peu idée.
Ou honneur course sou eh rester. Terrible traiter printemps terme voiture.', 'en_cours');
INSERT INTO tickets_service_client (id, utilisateur_id, sujet, description, statut) 
VALUES (10, 35, 'Demande de remboursement', 'Choisir vraiment plaisir chacun autour affirmer. Personne vieux chair chaleur riche simple suivre. Tout papier il gouvernement rue fin début grâce.
Leur public prêter divers tôt muet anglais.
Joindre fait nature venir avis prouver mal.', 'en_cours');
INSERT INTO tickets_service_client (id, utilisateur_id, sujet, description, statut) 
VALUES (11, 56, 'Problème de livraison', 'Puisque glace veiller retourner eau animal toit. Prononcer moins attendre interrompre comme. Personnage éclairer quant à.
Joue cent avant répéter détacher.
Dos deviner que occasion témoin. Peser famille complètement repas. Joue retrouver six été barbe. Nous sac secours rang.', 'en_cours');
INSERT INTO tickets_service_client (id, utilisateur_id, sujet, description, statut) 
VALUES (12, 58, 'Question sur la garantie', 'Poche venir poitrine appartenir terreur parvenir. On pensée donc docteur réveiller devant. Foi religion race puissance noire corde essuyer posséder.
Menacer plein sauver acte blanc bouche. Être promener détacher anglais ouvrir assez notre.', 'ouvert');
INSERT INTO tickets_service_client (id, utilisateur_id, sujet, description, statut) 
VALUES (13, 54, 'Problème de livraison', 'Toile doucement grand taille regretter entraîner classe. Douceur attirer flamme voyager.
Compter autant violence coup fonction. Brûler mauvais groupe oreille briller herbe dieu.
Auteur propos remplir agir.', 'ferme');
INSERT INTO tickets_service_client (id, utilisateur_id, sujet, description, statut) 
VALUES (14, 65, 'Question sur la garantie', 'Monde traîner exister point. As vrai paysan faible si étage. Recherche eaux courage mien verser petit égal.
Parler expérience bas partager. Changement convenir problème nord jusque. Respirer paupière lever vérité.', 'en_cours');
INSERT INTO tickets_service_client (id, utilisateur_id, sujet, description, statut) 
VALUES (15, 50, 'Problème de livraison', 'Perdre intérieur terrible après préférer certain comment. Tandis Que ruine blanc.
Sec au rouge calme. Retrouver dans revoir grain rocher vision poche entrée. Même entier vérité croire après compagnie attitude. Chant garder pousser midi haut.', 'resolu');
INSERT INTO tickets_service_client (id, utilisateur_id, sujet, description, statut) 
VALUES (16, 29, 'Problème de livraison', 'Salut élever genre million contraire voilà ville ouvrage. Livrer inquiéter parce que craindre arriver cacher cher.
Composer plaisir apprendre pauvre droite habiter espèce. Apprendre quatre ton composer reposer jouer campagne. Produire nord entretenir coucher plusieurs.', 'resolu');
INSERT INTO tickets_service_client (id, utilisateur_id, sujet, description, statut) 
VALUES (17, 13, 'Problème de paiement', 'Douze ça inspirer genou. Dangereux écraser ci rester un tant. Victime siège bas signe jusque voyage nommer.
Affaire grand sommet désigner habitant. Suffire non chemise mourir accent. Appartement intérieur regarder.
Manier jeter retour sable ici dépasser.', 'resolu');
INSERT INTO tickets_service_client (id, utilisateur_id, sujet, description, statut) 
VALUES (18, 19, 'Produit défectueux', 'Inquiéter parti simple autorité suivre escalier ancien grâce. Pouvoir or moyen coûter politique. Souhaiter pur as troisième plonger souvent ça faible.
Faible complètement mince. Minute religion champ espérer. Calme je travailler nature vaste créer question. Ensuite sur lieu goût article.', 'ouvert');
INSERT INTO tickets_service_client (id, utilisateur_id, sujet, description, statut) 
VALUES (19, 37, 'Problème de paiement', 'Valeur avant colère cabinet chemin. Sonner madame pareil éclater.
Inutile geste quant à aider. Attitude sommeil dehors trou pauvre. Naître permettre reprendre jour pitié manger.', 'ferme');
INSERT INTO tickets_service_client (id, utilisateur_id, sujet, description, statut) 
VALUES (20, 90, 'Problème de paiement', 'Demeurer appel engager celui. Famille cours présent pitié vin.
Horizon vif marche cause air tout. Trou toujours chute victime.
Éprouver près inutile eaux triste visage mourir. Retrouver propre toile et. Public système chance mériter.
Frais sein homme. Envelopper oh corps mal.', 'en_cours');
INSERT INTO tickets_service_client (id, utilisateur_id, sujet, description, statut) 
VALUES (21, 98, 'Modification de commande', 'Fine acte étendue en hiver miser. Proposer hier volonté revenir durer. Propre garde sec nuage charger embrasser.
Aujourd''Hui veille rapporter beau fruit tenter. Complet impression monsieur terme couler savoir. Midi appeler saluer se emmener.', 'ferme');
INSERT INTO tickets_service_client (id, utilisateur_id, sujet, description, statut) 
VALUES (22, 58, 'Support technique', 'Parent jamais pourquoi carte lorsque. Âge différent naturellement chat impossible pourquoi exiger. Donc gens tendre.
Eaux malheur trait. Conversation parent réduire nuit combien entourer engager. Doigt pouvoir extraordinaire marcher étroit.', 'ouvert');
INSERT INTO tickets_service_client (id, utilisateur_id, sujet, description, statut) 
VALUES (23, 11, 'Problème de livraison', 'Position un sentiment prêter premier révéler général terrain. Route tombe jeu endroit. Chance hésiter voile maintenant victime comment.
Quelqu''Un caresser cercle. Porter emporter créer visible.
Avec remercier rassurer apporter. Ancien petit note intention. Apprendre elle acheter blanc ce.', 'resolu');
INSERT INTO tickets_service_client (id, utilisateur_id, sujet, description, statut) 
VALUES (24, 28, 'Problème de paiement', 'Seuil inviter pouvoir conscience plein briser se. Gouvernement lourd froid recommencer enfermer installer.
Lendemain expression durer professeur. Environ campagne droit obéir. Porte sein début froid voici.', 'en_cours');
INSERT INTO tickets_service_client (id, utilisateur_id, sujet, description, statut) 
VALUES (25, 71, 'Modification de commande', 'Face couler couleur sembler. Ce secret promener doute prévenir naturellement.
Exécuter place tuer voile longtemps chef. Bruit dessiner lettre parent chacun boire arriver.
Poche vie fil poésie chien palais billet. Peu machine large installer.', 'ferme');
INSERT INTO tickets_service_client (id, utilisateur_id, sujet, description, statut) 
VALUES (26, 15, 'Problème de paiement', 'Petit rendre sourire coin gros énergie flamme. Montagne justice midi matière.
Moi chute aspect diriger nommer fête plusieurs. Ensuite âme appuyer seconde étranger. Allumer suffire étaler blanc étendue exiger être peu.', 'resolu');
INSERT INTO tickets_service_client (id, utilisateur_id, sujet, description, statut) 
VALUES (27, 31, 'Question sur la garantie', 'Ah intéresser aile engager montrer. Mot rire bois pluie esprit lier. Combat également vêtir couper partir vieux.
Croiser discussion effet mourir revoir par valeur. Bien essayer auquel rêve inviter créer retenir pénétrer.', 'ouvert');
INSERT INTO tickets_service_client (id, utilisateur_id, sujet, description, statut) 
VALUES (28, 7, 'Produit défectueux', 'Tranquille marchand oser règle habitant. Prononcer attaquer coup inconnu dépasser qui réfléchir. Fuir simple temps parti sentiment disposer.
Devenir obliger frapper calme. Alors retomber endormir jouer vol.
Cour donc amener. Perte composer seulement véritable jour. As supposer enfant.', 'ferme');
INSERT INTO tickets_service_client (id, utilisateur_id, sujet, description, statut) 
VALUES (29, 82, 'Problème de paiement', 'Toute main santé tu tout détacher sourire. Nul religion enfant savoir quand. Traîner d''abord briser croix dormir.
Social aspect marché précieux calme. Goutte poitrine ventre souffrance traiter extraordinaire prière. Aide vers oeil selon peur.
Détail fin passage précis taille.', 'ferme');
INSERT INTO tickets_service_client (id, utilisateur_id, sujet, description, statut) 
VALUES (30, 9, 'Problème de livraison', 'Parole souffrance réflexion frapper anglais soirée. Intérieur gagner sein principe sortir ruine saison.
Auprès glace protéger menacer envelopper pourtant reconnaître. Parler respect chair fou.', 'ferme');
INSERT INTO tickets_service_client (id, utilisateur_id, sujet, description, statut) 
VALUES (31, 77, 'Support technique', 'Parcourir tapis vieux couche préférer comme foule grave. Cher valeur commencement monde adresser. Habitude tirer ignorer plein caresser prévenir contenter.
Qui figurer groupe coûter cuisine. Prononcer contenir condition respirer amener.', 'ouvert');
INSERT INTO tickets_service_client (id, utilisateur_id, sujet, description, statut) 
VALUES (32, 81, 'Support technique', 'Preuve présenter qualité devenir bientôt. Arrivée tout intérieur événement. Travailler verser nuage quitter après détruire ouvrir éloigner.
Cerveau suite appel condamner commencement larme. Soudain certes enlever manger chanter capable. Vingt leur vieillard.', 'en_cours');
INSERT INTO tickets_service_client (id, utilisateur_id, sujet, description, statut) 
VALUES (33, 92, 'Produit défectueux', 'Contenir article confondre. Difficile présence haïr vous toucher appartenir exemple. Jouer larme sentiment soit ce bête soldat.
Raconter saint moindre phrase. Nerveux vide mal morceau gauche.
Regarder plusieurs souvenir ajouter point. Fonder nombreux type seconde.', 'resolu');
INSERT INTO tickets_service_client (id, utilisateur_id, sujet, description, statut) 
VALUES (34, 55, 'Problème de livraison', 'Crier armée pauvre entraîner. Quelque mémoire observer besoin. Compter vérité soir beau seulement.
Rendre droite rang perdu casser justice. Pur toi taire occasion exister billet.', 'resolu');
INSERT INTO tickets_service_client (id, utilisateur_id, sujet, description, statut) 
VALUES (35, 31, 'Support technique', 'Intelligence avenir rêve élément vivant. Selon maintenant écraser argent avant.
Bruit grâce bien peu montagne détruire devant.
Afin De quatre inconnu repousser semblable après gauche. Enfant profondément rassurer hôtel rire.', 'ferme');
INSERT INTO tickets_service_client (id, utilisateur_id, sujet, description, statut) 
VALUES (36, 24, 'Modification de commande', 'Posséder ventre plonger revoir battre chaîne. Cabinet afin de victime silence crainte. Pencher haine parce que résister. Bas regretter chemin glisser capable.
Véritable intérieur simple neuf couper monter. Arrêter accord parler preuve violent sérieux.', 'ouvert');
INSERT INTO tickets_service_client (id, utilisateur_id, sujet, description, statut) 
VALUES (37, 68, 'Question sur la garantie', 'Sourd profond flot général. Retenir réunir sens palais dresser race. Cercle couler oeil bon gauche votre embrasser.
Arbre agent souhaiter exemple cinq sans sujet. Rideau essuyer calme.
Mode journal votre réponse. Regretter mille supposer.', 'ouvert');
INSERT INTO tickets_service_client (id, utilisateur_id, sujet, description, statut) 
VALUES (38, 68, 'Support technique', 'Route ce cour vêtir règle accompagner. État lire bas fauteuil rappeler exposer pierre. Rapide malheur reprendre chambre.
Terrible sur un lumière pointe trésor. Chasser accuser riche trésor barbe enfin. Habitant fonction annoncer toile.', 'ouvert');
INSERT INTO tickets_service_client (id, utilisateur_id, sujet, description, statut) 
VALUES (39, 50, 'Problème de paiement', 'Homme cours membre réserver pensée pouvoir. Remettre souhaiter barbe marier flot prix.
Voler droite besoin mesure magnifique rare circonstance. Succès matin dieu.
Voilà but attaquer faux parcourir éviter. Rare trembler hors.', 'ferme');
INSERT INTO tickets_service_client (id, utilisateur_id, sujet, description, statut) 
VALUES (40, 6, 'Modification de commande', 'Bleu prétendre santé avouer attention spectacle jambe. Avec plusieurs franc mine rencontrer sommeil neuf. Voyager poser trou public général coeur.
Joue immobile vert loup. Caractère crise inutile qui triste falloir un. Seulement but famille eaux maintenant caractère émotion femme.', 'ferme');
INSERT INTO tickets_service_client (id, utilisateur_id, sujet, description, statut) 
VALUES (41, 48, 'Question sur la garantie', 'Jeune en ici essuyer fermer science.
Recommencer ligne imposer hôtel. Chemise proposer beau par papier fixe système. Mauvais valeur succès pur pays soirée. Mort retenir présent.
Pauvre bas user médecin. Vaincre magnifique raison. Sûr cas trait condamner agir reprendre dès.', 'ouvert');
INSERT INTO tickets_service_client (id, utilisateur_id, sujet, description, statut) 
VALUES (42, 46, 'Problème de paiement', 'Allumer assurer flot ensemble. Suivant devoir trembler surveiller arrière départ. Nez larme ramener fin camarade atteindre inquiétude froid.
Froid déjà soutenir. Mien nez bon recueillir pénétrer. Émotion frère bande partir.
Faux voici répandre marier. Vendre mieux appeler rôle vendre pain.', 'ouvert');
INSERT INTO tickets_service_client (id, utilisateur_id, sujet, description, statut) 
VALUES (43, 45, 'Produit défectueux', 'Après quart moindre élément force. Sauvage promener y souffler. On vaincre énorme pointe etc.
Donner peur entier creuser vaste envoyer tenter. Paysage abattre jambe table.
Milieu poussière juger fonction avoir sortir. Masse suite rose histoire.', 'ouvert');
INSERT INTO tickets_service_client (id, utilisateur_id, sujet, description, statut) 
VALUES (44, 99, 'Support technique', 'Quelque rayon poids président continuer.
Embrasser printemps delà le extraordinaire douze tandis que présent. Accomplir vivant pas ça douceur. Le mesure petit moment pointe moitié aucun. Queue centre trace siège.', 'resolu');
INSERT INTO tickets_service_client (id, utilisateur_id, sujet, description, statut) 
VALUES (45, 18, 'Problème de livraison', 'Cause lune lendemain l''une apprendre. Arbre terrible marchand engager fois. Avouer mort ajouter quant à vin goutte.
Côté épais attirer paraître alors. Rire nord parce que espèce dessiner bruit.
Savoir sac lutter demander autre obéir. Réduire paraître naître bas atteindre anglais.', 'resolu');
INSERT INTO tickets_service_client (id, utilisateur_id, sujet, description, statut) 
VALUES (46, 70, 'Question sur la garantie', 'Ouvrir établir tranquille repas ignorer environ contre bord. Preuve nord sein tandis que celui loin examiner jeune. Histoire dernier retomber atteindre endroit haine veille rapidement.
Sous remettre chef en été falloir accord ni. Assez livre sec silence.', 'en_cours');
INSERT INTO tickets_service_client (id, utilisateur_id, sujet, description, statut) 
VALUES (47, 100, 'Modification de commande', 'Jeune regarder rond rien fer. Connaître voiture extraordinaire autrefois ami camarade.
Corde nez réfléchir approcher ami couche. Danger dire compagnon sept.
Côte composer dimanche bon. Feu représenter ça trait.', 'ferme');
INSERT INTO tickets_service_client (id, utilisateur_id, sujet, description, statut) 
VALUES (48, 90, 'Demande de remboursement', 'Poursuivre ennemi grave partout titre recueillir. Contenir mari résister environ arriver retenir son seuil. Soutenir crainte avouer intérieur pièce aucun loi ramasser.', 'en_cours');
INSERT INTO tickets_service_client (id, utilisateur_id, sujet, description, statut) 
VALUES (49, 18, 'Problème de livraison', 'Chacun bande hier étroit. Appel lors esprit humain guerre fait lettre donner. Condamner déjà payer.
Écouter libre mémoire avec. Tôt bleu autour apercevoir couleur. Pluie désormais question regarder sentiment.', 'ferme');
INSERT INTO tickets_service_client (id, utilisateur_id, sujet, description, statut) 
VALUES (50, 5, 'Question sur la garantie', 'Décider profond créer déjà noir métier. Profiter impossible respecter enfance construire regretter pouvoir.
Hôtel mince femme musique cependant trésor. Lever peser éviter.
Grâce rang recueillir posséder eh noir. Reposer toile chiffre un épaule parfois obtenir.', 'en_cours');
INSERT INTO tickets_service_client (id, utilisateur_id, sujet, description, statut) 
VALUES (51, 6, 'Problème de paiement', 'Voisin cercle genou quelque. User soir certain course guère presque. Cinquante moyen encore courage prince importance couper.
Au fort rien maître témoin souffrance importer. Apparence beauté pays tête étoile semaine respirer.', 'en_cours');
INSERT INTO tickets_service_client (id, utilisateur_id, sujet, description, statut) 
VALUES (52, 6, 'Question sur la garantie', 'Voyage avant branche réflexion. Fuir colère couvrir appuyer allumer passage. Figure queue sien forêt acheter calmer terre.
Joue aussi mener depuis tu changer ruine. Commencer agent bois écouter. Que comme planche achever donner hauteur compter.
Curieux poussière second rocher passer prince sûr.', 'resolu');
INSERT INTO tickets_service_client (id, utilisateur_id, sujet, description, statut) 
VALUES (53, 66, 'Demande de remboursement', 'Approcher lorsque rose entourer. Content coûter me travail casser croiser exemple compagnie.
Acte croire dangereux personne doute paquet. Auquel dame élever. Lever voix prêter respect toile monter détacher bien.', 'ferme');
INSERT INTO tickets_service_client (id, utilisateur_id, sujet, description, statut) 
VALUES (54, 33, 'Problème de livraison', 'Quant À rassurer page attaquer femme. Cour fer passion demi promener.
Chacun ennemi reprendre apparence respecter garder. Raison découvrir puis été course. Tapis pierre désir.
Sommet magnifique connaissance parfois aucun là unique arrivée. Transformer cela compagnie mensonge.', 'en_cours');
INSERT INTO tickets_service_client (id, utilisateur_id, sujet, description, statut) 
VALUES (55, 37, 'Question sur la garantie', 'Type expérience fête intérieur. Lire puissant recherche rue reste agiter. Grand banc tapis eh marier mettre.
Fier empire droit mode jeune. Chaise intéresser choix content action liberté.', 'ouvert');
INSERT INTO tickets_service_client (id, utilisateur_id, sujet, description, statut) 
VALUES (56, 84, 'Question sur la garantie', 'Pendre tôt pur depuis. Toi expression présence. Pouvoir payer dimanche.
Deux observer un selon. Capable beaux prétendre. Former nez table lutte contenir goût.
Poste lèvre marché souvenir nez. Rang tomber solitude brusquement mot retomber. Divers créer quoi précéder.
Rose abattre auteur poussière.', 'resolu');
INSERT INTO tickets_service_client (id, utilisateur_id, sujet, description, statut) 
VALUES (57, 16, 'Problème de paiement', 'Parcourir paquet soldat colon éclater fête. Au ami demain jouer recherche. Attendre ramener accomplir.
Blanc main accomplir. Machine venir discuter jour rare occuper essayer point. Yeux rouge traverser pierre feu assez. Son riche absence sombre frais sec.', 'resolu');
INSERT INTO tickets_service_client (id, utilisateur_id, sujet, description, statut) 
VALUES (58, 56, 'Demande de remboursement', 'Voie vaincre rôle. Parti son vêtir.
Déjà joue quart reste étrange travail. Voilà signer tant puissance école corps charge. Sortir réponse prince an lettre bataille savoir.
Commander homme campagne peur déposer crier rapide. Bras votre amener tourner. Tache réflexion dans devoir jambe sur.', 'ferme');
INSERT INTO tickets_service_client (id, utilisateur_id, sujet, description, statut) 
VALUES (59, 50, 'Question sur la garantie', 'Vers haïr déjà dieu échapper ça étage. Tranquille quelqu''un campagne fait si unique mur abattre. Nombre content fixer goutte.
Lutter obliger d''autres force. Seulement enfoncer rose effacer danger poids chef. Chat pierre rêve premier nuit.', 'en_cours');
INSERT INTO tickets_service_client (id, utilisateur_id, sujet, description, statut) 
VALUES (60, 64, 'Modification de commande', 'Toit remonter signe. Également rond tendre cinquante aider folie.
Voiture rassurer foi malade droit poussière corps. Fond certainement ramener nature révolution service presque. Père mur hésiter joie sûr créer rêver.
Exprimer sien bonheur. Ferme visite poète commander.', 'ferme');
INSERT INTO tickets_service_client (id, utilisateur_id, sujet, description, statut) 
VALUES (61, 48, 'Problème de paiement', 'Porter usage penser fenêtre poste. Rencontre soin pendant dos. Fait cas baisser jusque plaine long.
Mot mot dont question rester conduire joli pauvre.
Mort boire attitude tel résultat. François précis fond rouge. Juger lutte neuf prévenir résoudre ceci rang.', 'resolu');
INSERT INTO tickets_service_client (id, utilisateur_id, sujet, description, statut) 
VALUES (62, 11, 'Modification de commande', 'Violent lisser face membre.
Désir après troisième. Peser histoire mur pourtant maintenant. Oeuvre long porter peur appuyer année.
Sien cruel chacun métier non. Cependant palais autrement devant figurer.', 'ferme');
INSERT INTO tickets_service_client (id, utilisateur_id, sujet, description, statut) 
VALUES (63, 11, 'Demande de remboursement', 'Engager représenter feuille véritable. Avec céder bureau mener aujourd''hui. Extraordinaire espace donner soleil.
Accuser fermer vêtement feu branche. Complètement proposer employer sable.', 'en_cours');
INSERT INTO tickets_service_client (id, utilisateur_id, sujet, description, statut) 
VALUES (64, 70, 'Question sur la garantie', 'Feu pur arriver promener. Présent désirer oh présent confondre voie.
Dur un madame prison tombe découvrir partir. Trou frère enfance beau. Avant départ bête moyen.
Mien larme songer venir goutte. Toute chaise lettre politique plusieurs marchand céder.', 'resolu');
INSERT INTO tickets_service_client (id, utilisateur_id, sujet, description, statut) 
VALUES (65, 14, 'Problème de livraison', 'Appeler horizon comme tout reculer taire complet faire. Lourd un goût feuille. Vêtir est poésie sauver servir signifier.
Joindre discussion abri parmi fond. Tourner vaste lui suivre traîner.', 'resolu');
INSERT INTO tickets_service_client (id, utilisateur_id, sujet, description, statut) 
VALUES (66, 85, 'Question sur la garantie', 'Changement quinze accepter sourd. But droite cesser glace éprouver. Clair coucher jeter.
Glace mer réunir prévoir. Ramasser renoncer fortune promettre que saluer.
Valeur respirer celui étendre. Refuser demande poche.', 'resolu');
INSERT INTO tickets_service_client (id, utilisateur_id, sujet, description, statut) 
VALUES (67, 58, 'Support technique', 'Oncle consulter siècle parfaitement chemise casser foule. Voiture tourner grain oublier beaucoup.
Froid employer partager dégager esprit jeter.
Pauvre emmener divers douze être genou. Supérieur confiance à petit entier drôle. Tel bon conscience troubler face.', 'ferme');
INSERT INTO tickets_service_client (id, utilisateur_id, sujet, description, statut) 
VALUES (68, 22, 'Modification de commande', 'Neuf bataille briller parfois obliger. Ni tendre perdu.
Près ton avance mémoire été. Voisin cour prochain approcher contraire mer détail.
Supérieur horizon principe tempête auquel genre. Respect combien dont verser eaux vague atteindre. Quatre former politique sombre vide.', 'ferme');
INSERT INTO tickets_service_client (id, utilisateur_id, sujet, description, statut) 
VALUES (69, 45, 'Demande de remboursement', 'Lieu prochain dieu seulement effacer distinguer carte. Après demi apparence chemin sourd. Docteur résoudre patron désirer.
Campagne peine part vie entrée tromper sourire. Professeur froid oncle entrée assez.
Danger verre comprendre vide marier vingt.', 'ouvert');
INSERT INTO tickets_service_client (id, utilisateur_id, sujet, description, statut) 
VALUES (70, 94, 'Problème de paiement', 'Encore sous rouge. Construire charge grain île payer franc profondément chaleur.
Boire fils bureau admettre sauvage train cerveau regretter.
Travail nul respirer accrocher. Médecin rouler seulement bas.
Recevoir suite rose emporter jeter dernier mêler. Pareil ce salle bord effacer.', 'resolu');
INSERT INTO tickets_service_client (id, utilisateur_id, sujet, description, statut) 
VALUES (71, 79, 'Demande de remboursement', 'Occuper compter manger. Confiance grâce suivant porte par dur sonner doigt.
Toute roche prêt avant abri trace. Rencontre chaud chemin honneur. Rond calme grand prononcer chasse entraîner centre.', 'resolu');
INSERT INTO tickets_service_client (id, utilisateur_id, sujet, description, statut) 
VALUES (72, 82, 'Problème de paiement', 'Demain absence vouloir âge. Inutile cesser but temps exposer serrer rencontrer.
Imposer sec mesure tout glace. Sans aspect chambre venir préparer.
Pousser gouvernement article. Peur autrefois secours sombre. Chaud chant dès.
Sauver gauche réfléchir intéresser changement malade trouver.', 'ouvert');
INSERT INTO tickets_service_client (id, utilisateur_id, sujet, description, statut) 
VALUES (73, 10, 'Modification de commande', 'Presque goutte ci vieil magnifique. Quelque fou aspect folie. Odeur avant pour jardin penser françois fier.
Paysage corde brûler avec obtenir sentir.
Dresser me aucun nouveau rare.
Mesure pas ancien divers village. Appuyer voilà joli arme bête en visage.', 'ferme');
INSERT INTO tickets_service_client (id, utilisateur_id, sujet, description, statut) 
VALUES (74, 47, 'Support technique', 'Ni seul écarter cheveu indiquer sous bête. Sourire rien perdu règle claire. Lumière propre pénétrer tout état reposer et.
Sien gros sueur remarquer fixe crainte on avance. Mon vouloir blanc affaire. Mémoire vêtement renverser bataille bien.', 'en_cours');
INSERT INTO tickets_service_client (id, utilisateur_id, sujet, description, statut) 
VALUES (75, 4, 'Produit défectueux', 'Face dur fruit. Terre cercle faire sentier un faveur pointe lisser. Sou vol apporter vin assez.
Accord si écarter cinq fort autre fixer. Plaire étranger intelligence mari rouler brusquement condition.
Regarder couler envoyer enlever voyager jour. Calmer il même troubler chasser croiser monsieur.', 'ferme');
INSERT INTO tickets_service_client (id, utilisateur_id, sujet, description, statut) 
VALUES (76, 5, 'Produit défectueux', 'Colère étranger genre jamais poser. Verre haïr tendre montrer. Miser suivre coucher.
Chasse pièce saint puissance salle puis adresser supposer. Lever engager respecter pleurer. Madame absolu huit savoir cela. Passage naissance année queue construire poussière remercier.', 'ouvert');
INSERT INTO tickets_service_client (id, utilisateur_id, sujet, description, statut) 
VALUES (77, 31, 'Problème de paiement', 'Premier transformer tantôt boire battre. Beau âgé toute bouche. Toucher boire hier naturel ancien eaux geste d''autres.
Figure corps intéresser ceci verser tenter gagner. Accord femme de droit souffrance discours. Plein absolument tellement ancien aller résoudre.', 'resolu');
INSERT INTO tickets_service_client (id, utilisateur_id, sujet, description, statut) 
VALUES (78, 47, 'Demande de remboursement', 'Caresser mur folie reconnaître terre secours cinquante. Courant bête hasard parfaitement note alors.
Mort air puissance vite. Remplir consentir pensée d''autres conversation seigneur promettre rideau. Rejeter peser dormir train pareil pas.', 'ouvert');
INSERT INTO tickets_service_client (id, utilisateur_id, sujet, description, statut) 
VALUES (79, 78, 'Produit défectueux', 'Parmi siècle car été étoile vous obéir. Cinq que tôt.
Ami ailleurs lors chez soit calmer curiosité envie. Banc poste cent dont couler.
Présenter pensée instant rire haine tromper. Désormais couche sentiment principe venir.', 'ferme');
INSERT INTO tickets_service_client (id, utilisateur_id, sujet, description, statut) 
VALUES (80, 48, 'Question sur la garantie', 'Route hôtel subir valeur détail fuir occasion sou. Étroit ami condition entourer respect existence autre. Faute rendre causer énorme acheter envoyer.
Résultat surprendre mode fin obliger mal bord. Prince tromper rien planche mouvement. Pointe habitude roman couche armer le.', 'ferme');
INSERT INTO tickets_service_client (id, utilisateur_id, sujet, description, statut) 
VALUES (81, 98, 'Problème de livraison', 'Droite pauvre sien. Temps droite selon. Annoncer marché malade essuyer afin de intéresser.
Dormir rapide fou militaire enfance. Arbre égal vivant le passer tempête semblable tranquille. Amener argent acheter branche.', 'en_cours');
INSERT INTO tickets_service_client (id, utilisateur_id, sujet, description, statut) 
VALUES (82, 68, 'Question sur la garantie', 'Respecter feuille précéder ton nerveux cas ensemble chemin. Souvenir vers garçon honneur causer malade musique peu. Entier public début diriger effacer.
Mince son petit puissant court avec. Atteindre admettre cuisine rouler construire bout crainte.', 'ferme');
INSERT INTO tickets_service_client (id, utilisateur_id, sujet, description, statut) 
VALUES (83, 41, 'Modification de commande', 'Disparaître jambe manier étroit. Toucher bande groupe cheval. Gros espace herbe famille armée fil toujours.
Contenir comprendre double offrir lutte. Point pays vaste dangereux.
Moyen dent manquer.
Source précieux franchir fonction dangereux. Léger comment courant parvenir près.', 'resolu');
INSERT INTO tickets_service_client (id, utilisateur_id, sujet, description, statut) 
VALUES (84, 32, 'Problème de livraison', 'Venir pitié grand aide. Soulever commencer recherche accuser étroit. Nécessaire juge désespoir brusquement route monde voiture.
Lier rappeler remettre bois rêver espoir justice. Voiture devoir journal facile admettre étude.', 'ouvert');
INSERT INTO tickets_service_client (id, utilisateur_id, sujet, description, statut) 
VALUES (85, 95, 'Produit défectueux', 'Court beau tirer fête bruit dont. Poésie surtout hors valoir mal discussion poésie souvent. Nom trois double contenter nation premier.
Habiller île vert respirer. But accorder toucher chef point. Vers papier pied embrasser durer réunir affirmer. Curiosité salle ce.', 'ferme');
INSERT INTO tickets_service_client (id, utilisateur_id, sujet, description, statut) 
VALUES (86, 67, 'Demande de remboursement', 'Toute désir poche fine fort taire suivant.
Endormir moins poésie entourer naissance police couler chair. Couler émotion effet toucher impossible connaissance répandre.
Champ hésiter enfance train. Intelligence grand geste fuir alors mine. Beau changer tapis reprendre nature faux.', 'ouvert');
INSERT INTO tickets_service_client (id, utilisateur_id, sujet, description, statut) 
VALUES (87, 34, 'Problème de paiement', 'Parent prix traiter révolution papier. Calmer à occasion casser blanc.
Inutile savoir heureux aspect. Eh joli connaître demain.
Sac point silencieux oui guerre. Conscience rouler personne. Longtemps précieux couleur jeune.
Vaste larme plaindre foi. Inquiéter roman chemin droit.', 'resolu');
INSERT INTO tickets_service_client (id, utilisateur_id, sujet, description, statut) 
VALUES (88, 91, 'Demande de remboursement', 'Étrange présence foi attirer permettre. Permettre moindre important silence changement réponse. Tombe aussi secrétaire joli vent.
Muet toucher remettre maître. Pouvoir noire naturel neuf. Auquel ami puis dégager pierre lever. Entre dégager relation terreur retenir bras souhaiter.', 'en_cours');
INSERT INTO tickets_service_client (id, utilisateur_id, sujet, description, statut) 
VALUES (89, 79, 'Question sur la garantie', 'Bas ainsi veille billet anglais. Suivant expérience froid mémoire. Étaler pointe valeur proposer.
Content couvrir sang liberté exemple surveiller si. Haut paraître son monter. Répandre égal caractère défendre.', 'ferme');
INSERT INTO tickets_service_client (id, utilisateur_id, sujet, description, statut) 
VALUES (90, 26, 'Problème de livraison', 'Courir rouge épais rassurer. Demain autre trou tandis que.
Visible tu nuage or avis mesure.
Profond bout lequel debout être. Embrasser service vide aider as remarquer rocher.', 'en_cours');
INSERT INTO tickets_service_client (id, utilisateur_id, sujet, description, statut) 
VALUES (91, 10, 'Demande de remboursement', 'Après réveiller son désormais assez asseoir haut. Apprendre étranger père derrière éclat. Former personne personnage avant transformer course près roman.
Preuve trembler renoncer éclat perdre mal. Ensemble me bout étoile fumée.', 'en_cours');
INSERT INTO tickets_service_client (id, utilisateur_id, sujet, description, statut) 
VALUES (92, 92, 'Demande de remboursement', 'Hier de feuille petit marchand petit. Me étouffer aller. Rappeler esprit sans dire rapide curieux allumer promettre.
Soir repas tour rang rien mettre. Silence transformer indiquer mot monsieur. Difficile veille instinct volonté demi te douze. Bas désormais meilleur essuyer fonder.', 'ouvert');
INSERT INTO tickets_service_client (id, utilisateur_id, sujet, description, statut) 
VALUES (93, 88, 'Problème de paiement', 'Condamner réfléchir double soleil cent parler. Somme personnage dehors père.
Simplement nation appeler principe atteindre prévoir dieu. Afin De sentier serrer mauvais appuyer.
Brusquement livre calme avec courir montrer. Autour grain droit air officier expliquer.', 'resolu');
INSERT INTO tickets_service_client (id, utilisateur_id, sujet, description, statut) 
VALUES (94, 86, 'Question sur la garantie', 'Valoir voler moitié vraiment. Mener genou puis sept malade arrière interroger mais.
Divers second éclater dernier dernier regard. Défendre enfin vie pourquoi histoire valeur. Exprimer étroit lisser terme perdre odeur.', 'ouvert');
INSERT INTO tickets_service_client (id, utilisateur_id, sujet, description, statut) 
VALUES (95, 71, 'Support technique', 'Quelque celui anglais groupe position voiture cerveau. Tête tandis que éviter franc mille prétendre carte. Nommer oublier vouloir après quart éviter.', 'resolu');
INSERT INTO tickets_service_client (id, utilisateur_id, sujet, description, statut) 
VALUES (96, 39, 'Problème de paiement', 'L''Une maison loi toujours drôle fils rassurer.
Rompre puissant voisin. Gros douleur souffrance enfermer étonner.
Durant journal davantage comme. Voisin rapide tomber place chant.
Secret rappeler allumer tache veille matin retrouver. Juge saint famille.', 'en_cours');
INSERT INTO tickets_service_client (id, utilisateur_id, sujet, description, statut) 
VALUES (97, 92, 'Modification de commande', 'Vert revenir quelqu''un d''autres. Envie livre double parler.
Présent enfin tomber habiller. Ennemi selon peu soudain animer particulier accord. Ni sommet dangereux côte.
Joue considérer lequel certes. Type signer race absence. Justice oncle presser apparaître.', 'en_cours');
INSERT INTO tickets_service_client (id, utilisateur_id, sujet, description, statut) 
VALUES (98, 47, 'Support technique', 'Danger vent sûr reculer. Vêtir entrer peur campagne inquiétude ensemble.
Poussière près remarquer joli revoir jusque. Porte amener distance cruel seuil front.
Dimanche ennemi fois hésiter fort tendre. Jouer danger partout après honte. Mot combat court paraître trou.', 'en_cours');
INSERT INTO tickets_service_client (id, utilisateur_id, sujet, description, statut) 
VALUES (99, 16, 'Produit défectueux', 'Appeler droit ainsi parole porter anglais raconter. Permettre certainement quatre dix bas autrement. Ah quel me tête bientôt noir.
Sauver silencieux réponse grâce quelque. Dont courage discours personnage intérieur. Grave d''autres frère doute droite.', 'en_cours');
INSERT INTO tickets_service_client (id, utilisateur_id, sujet, description, statut) 
VALUES (100, 31, 'Problème de paiement', 'Comme soin juste désormais chant oublier inutile. Recherche attacher le fusil quatre science année.
Frère accepter posséder rappeler rester même enfance pensée. Impossible joindre mieux quartier puis titre. Précieux fer rare classe quitter colon.', 'ferme');
