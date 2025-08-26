import streamlit as st
from sqlalchemy.orm import Session
from backend.database import SessionLocal
from backend.models import Product, Category
from backend.qdrant_client import insert_embedding
from sentence_transformers import SentenceTransformer
import numpy as np

st.title("Ajout d’un produit au catalogue")

# Charger le modèle d'embedding
@st.cache_resource
def load_model():
    return SentenceTransformer("all-MiniLM-L6-v2")

model = load_model()

# Formulaire d’ajout de produit
with st.form("add_product_form"):
    nom = st.text_input("Nom du produit", max_chars=255)
    prix = st.number_input("Prix (€)", min_value=0.01, step=0.01, format="%.2f")
    stock = st.number_input("Stock", min_value=0, step=1)
    categorie_id = st.number_input("ID Catégorie", min_value=1, step=1)
    description_courte = st.text_area("Description courte")
    caracteristiques_structurées = st.text_area("Caractéristiques structurées (JSON)")
    submitted = st.form_submit_button("Ajouter le produit")

if submitted:
    # Validation
    if not nom.strip():
        st.error("Le nom du produit est obligatoire.")
    else:
        try:
            # Convertir les caractéristiques en JSON
            import json
            try:
                caracteristiques_json = json.loads(caracteristiques_structurées) if caracteristiques_structurées.strip() else {}
            except Exception:
                st.error("Caractéristiques structurées : format JSON invalide.")
                st.stop()

            # Insertion dans Postgres
            db: Session = SessionLocal()
            new_product = Product(
                nom=nom.strip(),
                prix=prix,
                stock=stock,
                categorie_id=categorie_id,
                description_courte=description_courte.strip(),
                caracteristiques_structurées=caracteristiques_json
            )
            db.add(new_product)
            db.commit()
            db.refresh(new_product)

            # Générer l'embedding (nom + description)
            text_to_embed = f"{nom.strip()} {description_courte.strip()}"
            embedding = model.encode(text_to_embed)
            embedding = np.array(embedding, dtype=np.float32)

            # Indexer dans Qdrant
            insert_embedding(
                collection="produits_embeddings",
                id=new_product.id,
                embedding=embedding.tolist(),
                payload={"nom": nom.strip(), "categorie_id": categorie_id}
            )

            st.success(f"Produit '{nom}' ajouté et indexé avec succès !")
        except Exception as e:
            st.error(f"Erreur lors de l’ajout du produit : {e}")
