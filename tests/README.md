# Tests SMA - Prompts pour chaque Agent

Ce dossier contient des fichiers de test pour chaque agent du système SMA (Système Multi-Agent).

## Structure des fichiers

Chaque fichier `.txt` contient des prompts spécifiques pour tester un agent particulier :

- `conversation_agent.txt` - Tests pour l'agent de conversation
- `product_search_agent.txt` - Tests pour l'agent de recherche de produits
- `recommendation_agent.txt` - Tests pour l'agent de recommandation
- `order_management_agent.txt` - Tests pour l'agent de gestion des commandes
- `cart_management_agent.txt` - Tests pour l'agent de gestion du panier
- `customer_service_agent.txt` - Tests pour l'agent de service client
- `escalation_agent.txt` - Tests pour l'agent d'escalade
- `summarizer_agent.txt` - Tests pour l'agent de synthèse
- `customer_profiling_agent.txt` - Tests pour l'agent de profilage client
- `security_agent.txt` - Tests pour l'agent de sécurité
- `gdpr_agent.txt` - Tests pour l'agent RGPD
- `sustainability_agent.txt` - Tests pour l'agent de durabilité
- `multimodal_agent.txt` - Tests pour l'agent multimodal
- `monitoring_agent.txt` - Tests pour l'agent de monitoring
- `social_agent.txt` - Tests pour l'agent social

## Comment utiliser ces tests

1. **Copier un prompt** depuis le fichier correspondant à l'agent que vous voulez tester
2. **Coller le prompt** dans l'interface de chat
3. **Observer la réponse** et vérifier que l'agent approprié est utilisé
4. **Vérifier les logs** pour confirmer le routage vers le bon agent

## Exemples d'utilisation

### Test de l'agent de recherche de produits
```
Prompt: "donner moi le catalogue"
Attendu: Routage vers ProductSearchAgent
```

### Test de l'agent de recommandation
```
Prompt: "recommandez-moi des produits"
Attendu: Routage vers RecommendationAgent
```

### Test de l'agent de service client
```
Prompt: "j'ai un problème"
Attendu: Routage vers CustomerServiceAgent
```

## Vérification du routage

Pour vérifier que le bon agent est utilisé, regardez les logs qui affichent :
- L'intention détectée
- Les agents utilisés
- Le flux de traitement

## Notes importantes

- Les prompts sont organisés par catégorie dans chaque fichier
- Certains prompts peuvent déclencher plusieurs agents
- Le système SMA route automatiquement vers l'agent le plus approprié
- Les réponses doivent être dynamiques et non statiques








