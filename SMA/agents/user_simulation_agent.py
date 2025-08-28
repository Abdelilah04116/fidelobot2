from .base_agent import BaseAgent
from typing import Dict, Any, Optional
import random
import time
import httpx

class UserSimulationAgent(BaseAgent):
    """
    Agent SMA simulant un utilisateur humain sur un site e-commerce.
    Il peut se connecter, rechercher des produits, ajouter au panier, passer commande, laisser des avis, etc.
    Les comportements sont variés et peuvent être scriptés ou aléatoires.
    """

    def __init__(self, user_profile: Optional[Dict[str, Any]] = None, scenario: Optional[str] = None):
        """
        Initialise l'agent avec un profil utilisateur et un scénario optionnel.
        :param user_profile: Dictionnaire décrivant le profil (préférences, historique, etc.)
        :param scenario: Nom ou description du scénario à jouer
        """
        super().__init__(name="user_simulation_agent", description="Agent simulant un utilisateur e-commerce")
        self.user_profile = user_profile or {
            "email": f"user{random.randint(1000,9999)}@test.com",
            "password": "test1234",
            "prenom": "Test",
            "nom": "Utilisateur"
        }
        self.scenario = scenario
        self.state = {}

    def get_system_prompt(self) -> str:
        """
        Prompt système pour l'agent utilisateur simulé (peut être personnalisé selon le scénario).
        """
        return "Vous êtes un agent simulant un utilisateur humain sur un site e-commerce."

    async def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Point d'entrée principal : déroule un scénario utilisateur.
        :param state: Etat courant du SMA
        :return: Etat mis à jour
        """
        # TODO: Enchaîner les actions selon le scénario ou un comportement aléatoire
        await self.simulate_behavior()
        return state

    async def simulate_behavior(self):
        """
        Simule une séquence d'actions utilisateur (connexion, navigation, achat, etc.)
        """
        await self.action_connect_or_signup()
        await self.action_search_products(query="smartphone", filters={"price_max": 500})
        await self.action_add_to_cart()
        # TODO: Enchaîner les autres actions
        # await self.action_browse_categories()
        # ...

    async def action_connect_or_signup(self):
        """
        Tente de se connecter via l'API backend, ou s'inscrit si l'utilisateur n'existe pas.
        Stocke le token/session dans l'état de l'agent.
        """
        base_url = "http://localhost:8000"  # À adapter selon config
        email = self.user_profile["email"]
        password = self.user_profile["password"]
        async with httpx.AsyncClient() as client:
            # Tentative de connexion
            try:
                resp = await client.post(f"{base_url}/api/auth/login", json={
                    "email": email,
                    "password": password
                })
                if resp.status_code == 200:
                    data = resp.json()
                    self.state["token"] = data.get("access_token")
                    self.state["user_id"] = data.get("user_id")
                    print(f"[AUI] Connecté comme {email}")
                    return
            except Exception as e:
                print(f"[AUI] Erreur connexion: {e}")
            # Si échec, inscription
            try:
                resp = await client.post(f"{base_url}/api/auth/register", json={
                    "email": email,
                    "password": password,
                    "username": self.user_profile["prenom"].lower()
                })
                if resp.status_code in (200, 201):
                    data = resp.json()
                    self.state["token"] = data.get("access_token")
                    self.state["user_id"] = data.get("user_id")
                    print(f"[AUI] Inscrit et connecté comme {email}")
                    return
                else:
                    print(f"[AUI] Échec inscription: {resp.text}")
            except Exception as e:
                print(f"[AUI] Erreur inscription: {e}")

    async def action_browse_categories(self):
        """
        Simule la navigation dans les catégories de produits.
        """
        # TODO: Appeler l'API de catalogue pour lister les catégories
        pass

    async def action_search_products(self, query: str = "", filters: Optional[Dict[str, Any]] = None):
        """
        Effectue une recherche de produits via l'API backend.
        :param query: Terme de recherche (ex: "smartphone")
        :param filters: Dictionnaire de filtres (ex: {"price_max": 500})
        Stocke les résultats dans l'état de l'agent.
        """
        base_url = "http://localhost:8000"  # À adapter selon config
        token = self.state.get("token")
        params = {"q": query}
        if filters:
            params.update(filters)
        headers = {"Authorization": f"Bearer {token}"} if token else {}
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get(f"{base_url}/api/products/", params=params, headers=headers)
                if resp.status_code == 200:
                    data = resp.json()
                    self.state["search_results"] = data
                    print(f"[AUI] Recherche produits: {len(self.state['search_results'])} résultats trouvés.")
                else:
                    print(f"[AUI] Échec recherche produits: {resp.text}")
        except Exception as e:
            print(f"[AUI] Erreur recherche produits: {e}")

    async def action_compare_products(self):
        """
        Simule la comparaison de plusieurs produits.
        """
        # TODO: Implémenter la logique de comparaison
        pass

    async def action_add_to_cart(self, product_id: Optional[int] = None, quantity: int = 1):
        """
        Ajoute un produit au panier via l'API backend.
        :param product_id: ID du produit à ajouter (si None, prend le premier résultat de recherche)
        :param quantity: Quantité à ajouter
        Stocke l'état du panier dans l'agent.
        """
        base_url = "http://localhost:8000"  # À adapter selon config
        token = self.state.get("token")
        user_id = self.state.get("user_id")
        headers = {"Authorization": f"Bearer {token}"} if token else {}
        # Sélectionner un produit si non spécifié
        if product_id is None:
            results = self.state.get("search_results", [])
            if not results:
                print("[AUI] Aucun produit à ajouter au panier.")
                return
            product_id = results[0].get("id") if isinstance(results[0], dict) else results[0]
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.post(f"{base_url}/api/cart/add", json={
                    "user_id": user_id,
                    "product_id": product_id,
                    "quantite": quantity
                }, headers=headers)
                if resp.status_code == 200:
                    data = resp.json()
                    self.state["cart"] = data
                    print(f"[AUI] Produit {product_id} ajouté au panier.")
                else:
                    print(f"[AUI] Échec ajout panier: {resp.text}")
        except Exception as e:
            print(f"[AUI] Erreur ajout panier: {e}")

    async def action_checkout(self):
        """
        Simule le passage de commande.
        """
        # TODO: Appeler l'API commande
        pass

    async def action_leave_review(self):
        """
        Simule la rédaction d'un avis sur un produit.
        """
        # TODO: Appeler l'API avis
        pass

    async def action_contact_support(self):
        """
        Simule une question ou une demande au service client.
        """
        # TODO: Appeler l'API support client
        pass

# Exemple de scénario utilisateur (à adapter dans simulate_behavior)
# 1. Connexion ou inscription
# 2. Recherche d'un produit (ex: "smartphone")
# 3. Navigation sur plusieurs pages de résultats
# 4. Ajout d'un produit au panier, hésitation, retrait/ajout
# 5. Passage de commande
# 6. Rédaction d'un avis
# 7. Question au service client
#
# TODO: Implémenter la logique de scénario et d'aléa pour simuler un vrai comportement humain
