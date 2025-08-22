from .base_agent import BaseAgent
from typing import Dict, Any, List, Optional
from ..models.database import SessionLocal, User, Product, Order
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
import logging
from datetime import datetime, timedelta

class SustainabilityAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="sustainability_agent",
            description="Agent spécialisé dans la durabilité et la responsabilité environnementale"
        )
        self.logger = logging.getLogger(__name__)
        
        # Critères de durabilité
        self.sustainability_criteria = {
            "eco_friendly": ["recyclé", "biologique", "durable", "éco-responsable"],
            "energy_efficient": ["basse consommation", "A+++", "économies d'énergie"],
            "packaging": ["emballage minimal", "recyclable", "compostable"],
            "materials": ["bois certifié", "coton bio", "métaux recyclés"],
            "manufacturing": ["production locale", "éthique", "responsable"]
        }
        
        # Options de livraison écologique
        self.eco_delivery_options = {
            "bike_delivery": {"co2_saved": 0.5, "cost": 2.99, "delay": "2-3h"},
            "electric_vehicle": {"co2_saved": 0.3, "cost": 4.99, "delay": "1-2h"},
            "consolidated_shipping": {"co2_saved": 0.4, "cost": 1.99, "delay": "3-4j"},
            "pickup_point": {"co2_saved": 0.6, "cost": 0.00, "delay": "2-3j"}
        }
    
    def get_system_prompt(self) -> str:
        return """
        Vous êtes un expert en durabilité et responsabilité environnementale e-commerce.
        Votre rôle est d'informer et guider les clients vers des choix éco-responsables.
        
        Responsabilités:
        - Évaluer la durabilité des produits
        - Proposer des options de livraison écologique
        - Conseiller sur l'entretien et la durée de vie
        - Promouvoir les pratiques durables
        - Calculer l'impact environnemental
        
        Soyez toujours transparent et encouragez les choix responsables.
        """
    
    async def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        # Exemple de réponse dynamique
        state["response_text"] = "Pour un achat responsable, privilégiez les produits éco-labellisés ou issus du commerce équitable."
        return state
    
    async def get_product_sustainability_safe(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Obtenir les informations de durabilité d'un produit"""
        try:
            product_id = state.get("product_id")
            
            if not product_id:
                return {"error": "ID produit requis"}
            
            # Simulation des données de durabilité
            sustainability_data = {
                "eco_score": 75,
                "certifications": ["FSC", "GOTS", "OEKO-TEX"],
                "materials": "Bois certifié FSC, coton bio",
                "packaging": "Emballage recyclable",
                "manufacturing": "Production locale",
                "carbon_footprint": "2.3 kg CO2",
                "recyclability": "85%"
            }
            
            return {
                "product_id": product_id,
                "sustainability_score": sustainability_data["eco_score"],
                "certifications": sustainability_data["certifications"],
                "materials": sustainability_data["materials"],
                "packaging": sustainability_data["packaging"],
                "manufacturing": sustainability_data["manufacturing"],
                "environmental_impact": {
                    "carbon_footprint": sustainability_data["carbon_footprint"],
                    "recyclability": sustainability_data["recyclability"]
                }
            }
            
        except Exception as e:
            self.logger.error(f"Erreur durabilité produit: {str(e)}")
            return {"error": str(e)}
    
    async def get_eco_delivery_options_safe(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Obtenir les options de livraison écologique"""
        try:
            delivery_address = state.get("delivery_address", "")
            
            # Vérifier la disponibilité selon l'adresse
            available_options = {}
            for option, details in self.eco_delivery_options.items():
                is_available = "paris" in delivery_address.lower() or "lyon" in delivery_address.lower()
                available_options[option] = {
                    **details,
                    "available": is_available,
                    "environmental_benefit": f"Économie de {details['co2_saved']} kg CO2"
                }
            
            total_co2_saved = sum(
                details["co2_saved"] for details in available_options.values() 
                if details["available"]
            )
            
            return {
                "eco_delivery_options": available_options,
                "total_environmental_impact": {
                    "co2_saved": total_co2_saved,
                    "equivalent_trees": round(total_co2_saved * 0.1, 1)
                }
            }
            
        except Exception as e:
            self.logger.error(f"Erreur options livraison écologique: {str(e)}")
            return {"error": str(e)}
    
    async def get_product_lifespan_advice_safe(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Obtenir des conseils sur la durée de vie et l'entretien d'un produit"""
        try:
            product_id = state.get("product_id")
            
            if not product_id:
                return {"error": "ID produit requis"}
            
            # Conseils génériques selon le type de produit
            advice = {
                "maintenance": {
                    "frequency": "Mensuel",
                    "tasks": [
                        "Nettoyer régulièrement",
                        "Vérifier l'état général",
                        "Entretenir selon les instructions"
                    ]
                },
                "lifespan": {
                    "expected": "3-7 ans",
                    "extension_tips": [
                        "Maintenance préventive",
                        "Utilisation appropriée",
                        "Protection des éléments"
                    ]
                },
                "repair_recycle": {
                    "repair": ["Contacter le SAV", "Utiliser des services locaux"],
                    "recycle": ["Déposer en magasin", "Utiliser les filières appropriées"]
                }
            }
            
            return {
                "product_id": product_id,
                "maintenance_advice": advice["maintenance"],
                "lifespan_advice": advice["lifespan"],
                "repair_recycle_advice": advice["repair_recycle"]
            }
            
        except Exception as e:
            self.logger.error(f"Erreur conseils durée de vie: {str(e)}")
            return {"error": str(e)}
