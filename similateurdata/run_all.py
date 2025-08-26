#!/usr/bin/env python3
"""
Script principal pour exécuter automatiquement toute la simulation de données
"""

import subprocess
import sys
import os
import time

def run_script(script_name, description):
    """Exécuter un script Python et afficher le résultat"""
    print(f"\n{'='*60}")
    print(f"🚀 {description}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run([sys.executable, script_name], 
                              capture_output=True, text=True, cwd=os.path.dirname(__file__))
        
        if result.returncode == 0:
            print("✅ Succès!")
            if result.stdout:
                print(result.stdout)
        else:
            print("❌ Erreur!")
            if result.stderr:
                print(f"Erreur: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur d'exécution: {e}")
        return False
    
    return True

def main():
    print("🎯 SIMULATEUR DE DONNÉES COMPLET")
    print("Ce script va générer et insérer toutes les données simulées")
    
    # Vérifier que les services sont démarrés
    print("\n📋 Vérification des prérequis...")
    print("Assurez-vous que Postgres et Qdrant sont démarrés avec :")
    print("docker-compose -f catalogue/docker-compose.yml up -d")
    
    input("\nAppuyez sur Entrée pour continuer...")
    
    # 1. Générer les données BDR
    if not run_script("generate_bdr_data.py", "Génération des données BDR (Postgres)"):
        print("❌ Échec de la génération BDR. Arrêt.")
        return
    
    # 2. Générer les données BDV
    if not run_script("generate_bdv_data.py", "Génération des données BDV (Qdrant)"):
        print("❌ Échec de la génération BDV. Arrêt.")
        return
    
    # 3. Insérer toutes les données
    if not run_script("insert_data.py", "Insertion des données dans Postgres et Qdrant"):
        print("❌ Échec de l'insertion. Arrêt.")
        return
    
    print(f"\n{'='*60}")
    print("🎉 SIMULATION TERMINÉE AVEC SUCCÈS!")
    print(f"{'='*60}")
    print("✅ Données BDR générées et insérées dans Postgres")
    print("✅ Données BDV générées et insérées dans Qdrant")
    print("✅ Toutes les tables et collections sont remplies")
    print("\nVous pouvez maintenant utiliser votre application avec des données réalistes!")

if __name__ == "__main__":
    main()
