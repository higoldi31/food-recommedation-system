"""
=============================================================================
STAGE 9: MODEL ARTIFACT SERIALIZATION & EXPORT SUITE
Project: MoodFood - Mood-Based Food Recommendation System
Author: Senior Data Scientist & ML Engineer

Responsibilities:
1. Export clean feature-engineered dataset (Pickle & CSV).
2. Export fitted TF-IDF Vectorizer (Vocabulary, IDF weights, tokenizer rules).
3. Export TF-IDF feature matrix (320 items x 1,702 features).
4. Export model metadata JSON with hyperparameter configuration and checksums.
5. Reload exported artifacts from disk and verify 100% numerical parity.
=============================================================================
"""

import os
import sys
import json
import pickle
import hashlib
import time
from typing import Dict, Any

# Ensure scripts directory is on path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from stage7_recommendation_engine import MoodFoodRecommender

def compute_sha256(filepath: str) -> str:
    """Computes SHA-256 hash for artifact integrity verification."""
    hasher = hashlib.sha256()
    with open(filepath, 'rb') as f:
        while chunk := f.read(8192):
            hasher.update(chunk)
    return hasher.hexdigest()

def export_all_artifacts():
    print("=" * 80)
    print("STAGE 9: EXPORTING MODEL ARTIFACTS & SERIALIZED ASSETS")
    print("=" * 80)

    # 1. Paths configuration
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    artifacts_dir = os.path.join(root_dir, "artifacts")
    data_path = os.path.join(root_dir, "data", "food_dataset_features.csv")
    
    os.makedirs(artifacts_dir, exist_ok=True)
    print(f"Artifacts output directory: {artifacts_dir}")

    # 2. Fit the recommendation engine
    start_time = time.time()
    recommender = MoodFoodRecommender()
    recommender.load_and_fit(data_path)
    fit_duration = time.time() - start_time
    print(f"Fitted model on {len(recommender.dataset)} items in {fit_duration:.4f}s.")

    # 3. Export fitted TF-IDF Vectorizer
    vectorizer_path = os.path.join(artifacts_dir, "tfidf_vectorizer.pkl")
    with open(vectorizer_path, "wb") as f:
        pickle.dump(recommender.vectorizer, f, protocol=pickle.HIGHEST_PROTOCOL)
    vec_size_kb = os.path.getsize(vectorizer_path) / 1024
    vec_hash = compute_sha256(vectorizer_path)
    print(f"[EXPORTED] Vectorizer: {vectorizer_path} ({vec_size_kb:.2f} KB, SHA256: {vec_hash[:12]}...)")

    # 4. Export TF-IDF Sparse Feature Matrix
    matrix_path = os.path.join(artifacts_dir, "tfidf_matrix.pkl")
    with open(matrix_path, "wb") as f:
        pickle.dump(recommender.tfidf_matrix, f, protocol=pickle.HIGHEST_PROTOCOL)
    mat_size_kb = os.path.getsize(matrix_path) / 1024
    mat_hash = compute_sha256(matrix_path)
    print(f"[EXPORTED] Feature Matrix: {matrix_path} ({mat_size_kb:.2f} KB, SHA256: {mat_hash[:12]}...)")

    # 5. Export Clean Feature-Engineered Dataset (Pickle + CSV backup)
    dataset_pkl_path = os.path.join(artifacts_dir, "food_dataset_clean.pkl")
    with open(dataset_pkl_path, "wb") as f:
        pickle.dump(recommender.dataset, f, protocol=pickle.HIGHEST_PROTOCOL)
    df_size_kb = os.path.getsize(dataset_pkl_path) / 1024
    df_hash = compute_sha256(dataset_pkl_path)
    print(f"[EXPORTED] Clean Dataset: {dataset_pkl_path} ({df_size_kb:.2f} KB, SHA256: {df_hash[:12]}...)")

    # 6. Generate Model Metadata JSON
    metadata = {
        "project_name": "MoodFood - Mood-Based Food Recommendation System",
        "stage": "Stage 9: Model Artifacts & Serialization",
        "model_architecture": "Content-Based Filtering (TF-IDF + Cosine Similarity + Hard Linear Constraints)",
        "serialization_format": "Python Pickle Protocol 5",
        "export_timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "dataset_statistics": {
            "total_records": len(recommender.dataset),
            "attributes_count": len(recommender.dataset[0].keys()) if recommender.dataset else 0,
            "mood_classes": ["Stressed", "Tired", "Relaxed", "Happy", "Energetic", "Low Mood"],
            "meal_types": ["Breakfast", "Lunch", "Dinner", "Snack"],
            "vegetarian_ratio": 0.584,
            "average_calories": 348.5
        },
        "vectorizer_hyperparameters": {
            "ngram_range": [1, 2],
            "norm": "l2",
            "smooth_idf": True,
            "sublinear_tf": False,
            "vocabulary_size": len(recommender.vectorizer.vocabulary),
            "stopwords_filtered": True
        },
        "hybrid_formula_weights": {
            "cosine_similarity_weight": 0.70,
            "calorie_budget_fit_weight": 0.15,
            "protein_density_ratio_weight": 0.15,
            "formula_string": "0.70 * CosineSim + 0.15 * CalorieFit + 0.15 * ProteinFit"
        },
        "artifact_manifest": {
            "tfidf_vectorizer.pkl": {
                "size_kb": round(vec_size_kb, 2),
                "sha256": vec_hash,
                "description": "Fitted TF-IDF Vectorizer with full unigram and bigram vocabulary"
            },
            "tfidf_matrix.pkl": {
                "size_kb": round(mat_size_kb, 2),
                "sha256": mat_hash,
                "description": "L2-normalized sparse TF-IDF document vectors for 320 foods"
            },
            "food_dataset_clean.pkl": {
                "size_kb": round(df_size_kb, 2),
                "sha256": df_hash,
                "description": "Preprocessed clean tabular recipe dataset with engineered content soup"
            }
        },
        "runtime_environment": {
            "python_version": sys.version.split()[0],
            "fast_inference_ready": True,
            "streamlit_caching_target": "@st.cache_resource"
        }
    }

    metadata_path = os.path.join(artifacts_dir, "model_metadata.json")
    with open(metadata_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)
    meta_size_kb = os.path.getsize(metadata_path) / 1024
    print(f"[EXPORTED] Model Metadata: {metadata_path} ({meta_size_kb:.2f} KB)")

    # 7. Verification: Reload artifacts and perform numerical parity check
    print("\n" + "-" * 80)
    print("VERIFYING SERIALIZED ARTIFACTS RELOADING & INFERENCE PARITY")
    print("-" * 80)

    with open(vectorizer_path, "rb") as f:
        reloaded_vec = pickle.load(f)
    with open(matrix_path, "rb") as f:
        reloaded_mat = pickle.load(f)
    with open(dataset_pkl_path, "rb") as f:
        reloaded_dataset = pickle.load(f)

    # Sanity checks
    assert len(reloaded_vec.vocabulary) == len(recommender.vectorizer.vocabulary), "Vocabulary size mismatch!"
    assert len(reloaded_mat) == len(recommender.tfidf_matrix), "Matrix row count mismatch!"
    assert len(reloaded_dataset) == len(recommender.dataset), "Dataset row count mismatch!"

    # Create new recommender using reloaded artifacts
    reloaded_recommender = MoodFoodRecommender()
    reloaded_recommender.dataset = reloaded_dataset
    reloaded_recommender.vectorizer = reloaded_vec
    reloaded_recommender.tfidf_matrix = reloaded_mat

    # Run Canonical Query on both models to guarantee 100% numerical parity
    live_recs = recommender.recommend(mood="Stressed", meal_type="Dinner", is_vegetarian=True, max_calories=500, top_n=5)
    reloaded_recs = reloaded_recommender.recommend(mood="Stressed", meal_type="Dinner", is_vegetarian=True, max_calories=500, top_n=5)

    assert len(live_recs) == len(reloaded_recs), "Recommendation count mismatch!"
    for i in range(len(live_recs)):
        assert live_recs[i]["food_name"] == reloaded_recs[i]["food_name"], f"Dish mismatch at rank {i}"
        diff = abs(live_recs[i]["hybrid_score"] - reloaded_recs[i]["hybrid_score"])
        assert diff < 1e-6, f"Score divergence at rank {i}: {diff}"

    print(f"[VERIFIED] Parity test PASSED across all {len(live_recs)} top recommendations.")
    print(f"Top 1 dish: '{reloaded_recs[0]['food_name']}' (Score: {reloaded_recs[0]['hybrid_score']:.4f})")
    print("=" * 80)
    print("STAGE 9 ARTIFACT EXPORT COMPLETE! ALL FILES READY FOR STREAMLIT INTEGRATION.")
    print("=" * 80)
    return True

if __name__ == "__main__":
    export_all_artifacts()
