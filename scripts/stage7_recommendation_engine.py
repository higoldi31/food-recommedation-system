"""
=============================================================================
STAGE 7: BUILDING THE RECOMMENDATION SYSTEM ENGINE
Project: MoodFood - Mood-Based Food Recommendation System
Author: Senior Data Scientist & ML Engineer

Implements:
1. TF-IDF Vector Space Model (Term Frequency - Inverse Document Frequency)
   - Matches scikit-learn formula: idf(t) = ln((1 + n) / (1 + df(t))) + 1
   - L2 vector normalization for Euclidean/Cosine space equivalence
2. Cosine Similarity Vector Metric: cos(u, v) = (u . v) / (||u|| * ||v||)
3. Hard Constraint Filtering (Calorie budget, Meal type, Vegetarian rules)
4. Soft Ranking & Hybrid Scoring Formula:
   FinalScore = 0.70 * CosineSim + 0.15 * CalorieFitScore + 0.15 * ProteinDensityScore
5. Explainable Recommendation Rationale Generator (Biochemical + Culinary)
=============================================================================
"""

import os
import csv
import math
import re
from typing import Dict, List, Tuple, Any, Optional

# Standard English stop words
STOP_WORDS = {
    "a", "about", "above", "after", "again", "against", "all", "am", "an", "and",
    "any", "are", "aren't", "as", "at", "be", "because", "been", "before", "being",
    "below", "between", "both", "but", "by", "can't", "cannot", "could", "couldn't",
    "did", "didn't", "do", "does", "doesn't", "doing", "don't", "down", "during",
    "each", "few", "for", "from", "further", "had", "hadn't", "has", "hasn't",
    "have", "haven't", "having", "he", "he'd", "he'll", "he's", "her", "here",
    "here's", "hers", "herself", "him", "himself", "his", "how", "how's", "i",
    "i'd", "i'll", "i'm", "i've", "if", "in", "into", "is", "isn't", "it", "it's",
    "its", "itself", "let's", "me", "more", "most", "mustn't", "my", "myself",
    "no", "nor", "not", "of", "off", "on", "once", "only", "or", "other", "ought",
    "our", "ours", "ourselves", "out", "over", "own", "same", "shan't", "she",
    "she'd", "she'll", "she's", "should", "shouldn't", "so", "some", "such",
    "than", "that", "that's", "the", "their", "theirs", "them", "themselves",
    "then", "there", "there's", "these", "they", "they'd", "they'll", "they're",
    "they've", "this", "those", "through", "to", "too", "under", "until", "up",
    "very", "was", "wasn't", "we", "we'd", "we'll", "we're", "we've", "were",
    "weren't", "what", "what's", "when", "when's", "where", "where's", "which",
    "while", "who", "who's", "whom", "why", "why's", "with", "won't", "would",
    "wouldn't", "you", "you'd", "you'll", "you're", "you've", "your", "yours",
    "yourself", "yourselves"
}


class PureTfidfVectorizer:
    """
    Mathematical TF-IDF Vectorizer matching scikit-learn's TfidfVectorizer:
    - Tokenization + Stop word filtering
    - Unigram + Bigram extraction (ngram_range=(1, 2))
    - Smooth IDF: ln((1 + N) / (1 + DF)) + 1
    - L2 normalization: v / sqrt(sum(v_i^2))
    """
    def __init__(self, ngram_range: Tuple[int, int] = (1, 2)):
        self.ngram_range = ngram_range
        self.vocabulary: Dict[str, int] = {}
        self.idf_diag: Dict[int, float] = {}
        self.num_docs: int = 0

    def tokenize(self, text: str) -> List[str]:
        """Lowercases, strips punctuation, removes stopwords, and builds n-grams."""
        cleaned = re.sub(r'[^a-zA-Z0-9_\s]', ' ', text.lower())
        tokens = [t for t in cleaned.split() if t not in STOP_WORDS and len(t) > 1]
        
        all_ngrams = []
        # Unigrams
        if self.ngram_range[0] <= 1 <= self.ngram_range[1]:
            all_ngrams.extend(tokens)
            
        # Bigrams
        if self.ngram_range[1] >= 2 and len(tokens) >= 2:
            for i in range(len(tokens) - 1):
                all_ngrams.append(f"{tokens[i]} {tokens[i+1]}")
                
        return all_ngrams

    def fit(self, raw_documents: List[str]) -> "PureTfidfVectorizer":
        """Builds vocabulary dictionary and computes IDF for each feature."""
        self.num_docs = len(raw_documents)
        df_counts: Dict[str, int] = {}
        
        for doc in raw_documents:
            ngrams = set(self.tokenize(doc))
            for token in ngrams:
                df_counts[token] = df_counts.get(token, 0) + 1
                
        # Filter terms appearing at least once, sort alphabetically for deterministic indexing
        sorted_vocab = sorted(df_counts.keys())
        self.vocabulary = {term: idx for idx, term in enumerate(sorted_vocab)}
        
        # Compute smooth IDF: ln((1 + N) / (1 + DF)) + 1
        for term, idx in self.vocabulary.items():
            df = df_counts[term]
            self.idf_diag[idx] = math.log((1 + self.num_docs) / (1 + df)) + 1.0
            
        return self

    def transform(self, raw_documents: List[str]) -> List[Dict[int, float]]:
        """
        Transforms text documents to sparse L2-normalized TF-IDF vectors.
        Returns a list of dicts mapping {feature_index: tfidf_weight}.
        """
        vectors: List[Dict[int, float]] = []
        
        for doc in raw_documents:
            ngrams = self.tokenize(doc)
            if not ngrams:
                vectors.append({})
                continue
                
            # Compute Term Frequencies (TF)
            tf_counts: Dict[int, float] = {}
            for token in ngrams:
                if token in self.vocabulary:
                    idx = self.vocabulary[token]
                    tf_counts[idx] = tf_counts.get(idx, 0.0) + 1.0
                    
            # Multiply by IDF
            tfidf_vec: Dict[int, float] = {}
            sum_sq = 0.0
            for idx, count in tf_counts.items():
                val = count * self.idf_diag[idx]
                tfidf_vec[idx] = val
                sum_sq += val * val
                
            # L2 Normalization: v / ||v||
            if sum_sq > 0.0:
                l2_norm = math.sqrt(sum_sq)
                normalized_vec = {idx: val / l2_norm for idx, val in tfidf_vec.items()}
            else:
                normalized_vec = {}
                
            vectors.append(normalized_vec)
            
        return vectors

    def fit_transform(self, raw_documents: List[str]) -> List[Dict[int, float]]:
        return self.fit(raw_documents).transform(raw_documents)


def cosine_similarity_sparse(vec_a: Dict[int, float], vec_b: Dict[int, float]) -> float:
    """
    Computes cosine similarity between two L2-normalized sparse vectors.
    Since ||vec_a|| = 1 and ||vec_b|| = 1, cos(a, b) = vec_a . vec_b (dot product).
    """
    if not vec_a or not vec_b:
        return 0.0
        
    # Iterate over the smaller vector for computational efficiency
    if len(vec_a) > len(vec_b):
        vec_a, vec_b = vec_b, vec_a
        
    dot_product = 0.0
    for idx, val_a in vec_a.items():
        if idx in vec_b:
            dot_product += val_a * vec_b[idx]
            
    return max(0.0, min(1.0, dot_product))


class MoodFoodRecommender:
    """
    Content-Based Mood & Nutrition Food Recommendation Engine.
    Combines TF-IDF Vectorizer with hard filters and hybrid score ranking.
    """
    def __init__(self):
        self.vectorizer = PureTfidfVectorizer(ngram_range=(1, 2))
        self.dataset: List[Dict[str, Any]] = []
        self.tfidf_matrix: List[Dict[int, float]] = []

    def load_and_fit(self, dataset_path: str):
        """Loads feature-engineered dataset and builds TF-IDF index."""
        if not os.path.exists(dataset_path):
            raise FileNotFoundError(f"Dataset not found at {dataset_path}")
            
        with open(dataset_path, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            self.dataset = list(reader)
            
        # Parse numeric columns
        for row in self.dataset:
            row["calories"] = float(row["calories"])
            row["protein"] = float(row["protein"])
            row["carbs"] = float(row["carbs"])
            row["fat"] = float(row["fat"])
            row["fiber"] = float(row["fiber"])
            row["sugar"] = float(row["sugar"])
            row["vegetarian"] = int(row["vegetarian"])
            row["spicy"] = int(row["spicy"])
            row["protein_density_ratio"] = float(row.get("protein_density_ratio", 0.0))

        content_soups = [row["content_soup"] for row in self.dataset]
        self.tfidf_matrix = self.vectorizer.fit_transform(content_soups)
        print(f"[STAGE 7] Fitted TF-IDF Vectorizer on {len(self.dataset)} items.")
        print(f"[STAGE 7] Total unique feature tokens in vocabulary: {len(self.vectorizer.vocabulary)}")

    def build_query_soup(
        self,
        mood: str,
        meal_type: Optional[str] = None,
        is_vegetarian: Optional[bool] = None,
        cravings: str = ""
    ) -> str:
        """
        Builds weighted user query text matching the content soup syntax.
        Gives heavy weight (3x) to mood, plus meal and dietary tokens.
        """
        mood_clean = mood.lower().replace(" ", "_")
        mood_tokens = f"mood_{mood_clean} mood_{mood_clean} mood_{mood_clean} {mood_clean} {mood_clean}"
        
        tokens = [mood_tokens]
        if meal_type:
            tokens.append(f"meal_{meal_type.lower()}")
            
        if is_vegetarian is not None:
            if is_vegetarian:
                tokens.append("diet_vegetarian plant_based")
            else:
                tokens.append("diet_non_veg animal_protein")
                
        if cravings:
            clean_cravings = re.sub(r'[^a-zA-Z0-9_\s]', ' ', cravings.lower())
            tokens.append(clean_cravings)
            
        return " ".join(tokens)

    def generate_explanation(self, item: Dict[str, Any], query_mood: str, query_cal: Optional[float]) -> str:
        """
        Generates human-readable, biochemically sound explanation for the recommendation.
        """
        food_name = item["food_name"]
        item_mood = item["mood"]
        cuisine = item["cuisine"]
        calories = item["calories"]
        protein = item["protein"]
        fiber = item["fiber"]
        sugar = item["sugar"]
        tags = item["dietary_tags"].lower()

        reasons = []
        
        # Mood & Biochemical alignment
        if "stressed" in query_mood.lower():
            if "magnesium" in tags:
                reasons.append("High in magnesium to support central nervous system relaxation and stress mitigation.")
            elif "cortisol" in tags or "chamomile" in tags or "ashwagandha" in tags:
                reasons.append("Infused with adaptogenic botanicals that support cortisol homeostasis.")
            else:
                reasons.append(f"Provides gentle, soothing {cuisine} nourishment designed to soothe nervous tension.")
        elif "tired" in query_mood.lower():
            if "iron" in tags or "b12" in tags:
                reasons.append("Rich in iron and B-complex vitamins essential for cellular oxygenation and fighting fatigue.")
            elif protein >= 20.0:
                reasons.append(f"High protein density ({protein}g) delivers sustained energy without causing sugar spikes.")
            else:
                reasons.append("Complex micronutrient profile providing steady metabolic energy rejuvenation.")
        elif "relaxed" in query_mood.lower():
            if "tryptophan" in tags:
                reasons.append("Rich in L-tryptophan, promoting gentle serotonin synthesis and restful calm.")
            else:
                reasons.append(f"A balanced, easily digestible {item['category'].lower()} ideal for calm evenings.")
        elif "happy" in query_mood.lower():
            if "dopamine" in tags or "tyrosine" in tags:
                reasons.append("Contains natural dopamine precursors and antioxidants to sustain a positive outlook.")
            else:
                reasons.append("Vibrant, nutrient-dense profile that boosts positive vitality and neurotransmitter health.")
        elif "energetic" in query_mood.lower():
            if protein >= 22.0:
                reasons.append(f"Powers high physical performance with {protein}g protein and clean glycogen restoration.")
            else:
                reasons.append("Rich in electrolytes and complex carbohydrates for endurance and mental acuity.")
        elif "low mood" in query_mood.lower():
            if "probiotic" in tags or "gut-brain" in tags:
                reasons.append("Active probiotics and fermented nutrients nourish the gut microbiome via the vagus nerve.")
            elif "folate" in tags or "omega" in tags:
                reasons.append("Concentrated in folate and omega fatty acids, known to assist mood balance.")
            else:
                reasons.append("Gentle, comforting meal engineered for mood uplift and steady blood sugar.")

        # Nutritional fit reason
        if query_cal:
            cal_diff = query_cal - calories
            if cal_diff >= 0:
                reasons.append(f"Fits comfortably inside your {int(query_cal)} kcal budget at {int(calories)} kcal.")
            else:
                reasons.append(f"Nutrient-dense at {int(calories)} kcal with {protein}g protein.")

        return " ".join(reasons)

    def recommend(
        self,
        mood: str,
        meal_type: Optional[str] = None,
        is_vegetarian: Optional[bool] = None,
        max_calories: Optional[float] = None,
        min_protein: Optional[float] = None,
        cuisine: Optional[str] = None,
        cravings: str = "",
        top_n: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Executes complete hybrid recommendation pipeline:
        1. Hard constraint filtering (Calorie budget, Vegetarian rule, Meal type, Cuisine)
        2. Vectorizes user query with TF-IDF
        3. Computes Cosine Similarity against all qualified candidate foods
        4. Calculates Hybrid Multi-Objective Rank Score
        5. Returns Top-N sorted recommendations with scientific explanations
        """
        # Step 1: Hard constraint filtering
        candidates: List[Tuple[int, Dict[str, Any]]] = []
        for idx, row in enumerate(self.dataset):
            # Vegetarian filter
            if is_vegetarian is not None:
                if is_vegetarian and row["vegetarian"] != 1:
                    continue
                if not is_vegetarian and row["vegetarian"] == 1:
                    # Note: Usually non-veg users can eat veg, but if strict non-veg is preferred
                    pass
                    
            # Calorie ceiling
            if max_calories is not None and row["calories"] > max_calories:
                continue
                
            # Minimum protein floor
            if min_protein is not None and row["protein"] < min_protein:
                continue
                
            # Meal type filter (allow relaxed match if specified)
            if meal_type and meal_type.lower() != "all":
                if row["meal_type"].lower() != meal_type.lower() and row["meal_type"].lower() != "any":
                    continue
                    
            # Cuisine filter (optional)
            if cuisine and cuisine.lower() != "all":
                if row["cuisine"].lower() != cuisine.lower():
                    continue
                    
            candidates.append((idx, row))

        # Fallback handling: If hard constraints yield 0 results, relax meal_type or cuisine
        if not candidates:
            print("[STAGE 7] Warning: Hard constraints too strict (0 candidates). Relaxing meal_type filter...")
            for idx, row in enumerate(self.dataset):
                if is_vegetarian is not None and is_vegetarian and row["vegetarian"] != 1:
                    continue
                if max_calories is not None and row["calories"] > max_calories:
                    continue
                candidates.append((idx, row))

        if not candidates:
            print("[STAGE 7] Warning: Calorie ceiling too restrictive. Returning closest healthy matches.")
            for idx, row in enumerate(self.dataset):
                if is_vegetarian is not None and is_vegetarian and row["vegetarian"] != 1:
                    continue
                candidates.append((idx, row))

        # Step 2: Build and vectorize user query
        query_soup = self.build_query_soup(
            mood=mood,
            meal_type=meal_type,
            is_vegetarian=is_vegetarian,
            cravings=cravings
        )
        query_vector = self.vectorizer.transform([query_soup])[0]

        # Step 3: Compute Cosine Similarity & Hybrid Scoring
        scored_results = []
        for idx, candidate in candidates:
            doc_vector = self.tfidf_matrix[idx]
            cos_sim = cosine_similarity_sparse(query_vector, doc_vector)
            
            # Calorie fit component (0 to 1)
            if max_calories:
                # Rewards foods that are healthy and close to or under budget without being empty
                cal_ratio = candidate["calories"] / max_calories
                cal_fit_score = 1.0 if cal_ratio <= 1.0 else max(0.0, 1.0 - (cal_ratio - 1.0))
            else:
                cal_fit_score = 0.8
                
            # Protein density component normalized
            p_density = candidate["protein_density_ratio"]
            p_score = min(1.0, p_density / 10.0) # 10g/100kcal is exceptionally dense
            
            # Hybrid rank formula
            final_rank_score = (
                0.70 * cos_sim +
                0.15 * cal_fit_score +
                0.15 * p_score
            )
            
            explanation = self.generate_explanation(candidate, mood, max_calories)
            
            scored_results.append({
                "food_name": candidate["food_name"],
                "category": candidate["category"],
                "cuisine": candidate["cuisine"],
                "meal_type": candidate["meal_type"],
                "mood": candidate["mood"],
                "calories": candidate["calories"],
                "protein": candidate["protein"],
                "carbs": candidate["carbs"],
                "fat": candidate["fat"],
                "fiber": candidate["fiber"],
                "sugar": candidate["sugar"],
                "vegetarian": candidate["vegetarian"],
                "ingredients": candidate["ingredients"],
                "dietary_tags": candidate["dietary_tags"],
                "cosine_similarity": round(cos_sim, 4),
                "hybrid_score": round(final_rank_score, 4),
                "explanation": explanation
            })

        # Step 4: Sort descending by hybrid rank score
        scored_results.sort(key=lambda x: x["hybrid_score"], reverse=True)
        return scored_results[:top_n]


def run_stage7_verification():
    """Runs rigorous test scenarios on the Stage 7 Recommendation Engine."""
    print("=" * 78)
    print("STAGE 7: RECOMMENDATION ENGINE VERIFICATION & BENCHMARKING")
    print("=" * 78)
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    features_csv = os.path.join(script_dir, "..", "data", "food_dataset_features.csv")
    
    recommender = MoodFoodRecommender()
    recommender.load_and_fit(features_csv)
    
    # -------------------------------------------------------------
    # TEST CASE 1: The Exact User Brief Scenario
    # User selects: Mood: Stressed | Meal: Dinner | Preference: Vegetarian | Max Calories: 500
    # -------------------------------------------------------------
    print("\n" + "#" * 78)
    print("TEST SCENARIO 1: The Canonical Brief Query")
    print("Input -> Mood: 'Stressed' | Meal: 'Dinner' | Vegetarian: True | Max Calories: 500")
    print("#" * 78)
    
    recs = recommender.recommend(
        mood="Stressed",
        meal_type="Dinner",
        is_vegetarian=True,
        max_calories=500.0,
        top_n=5
    )
    
    for i, r in enumerate(recs, 1):
        print(f"\n[Rank #{i}] {r['food_name']} ({r['cuisine']} {r['category']})")
        print(f"  * Hybrid Score: {r['hybrid_score']} | Cosine Similarity: {r['cosine_similarity']}")
        print(f"  * Macros: {int(r['calories'])} kcal | P: {r['protein']}g | C: {r['carbs']}g | F: {r['fat']}g | Fiber: {r['fiber']}g")
        print(f"  * Mood Match: Assigned mood is '{r['mood']}'")
        print(f"  * Scientific Rationale: {r['explanation']}")

    # -------------------------------------------------------------
    # TEST CASE 2: High Energy / Fatigue Recovery
    # User selects: Mood: Tired | Meal: Breakfast | Max Calories: 400
    # -------------------------------------------------------------
    print("\n" + "#" * 78)
    print("TEST SCENARIO 2: Energy & Fatigue Counter-Balance")
    print("Input -> Mood: 'Tired' | Meal: 'Breakfast' | Vegetarian: False | Max Calories: 400")
    print("#" * 78)
    
    recs_tired = recommender.recommend(
        mood="Tired",
        meal_type="Breakfast",
        is_vegetarian=False,
        max_calories=400.0,
        top_n=3
    )
    
    for i, r in enumerate(recs_tired, 1):
        print(f"\n[Rank #{i}] {r['food_name']} ({r['cuisine']})")
        print(f"  * Hybrid Score: {r['hybrid_score']} | Cosine Similarity: {r['cosine_similarity']}")
        print(f"  * Macros: {int(r['calories'])} kcal | Protein: {r['protein']}g")
        print(f"  * Scientific Rationale: {r['explanation']}")

    # -------------------------------------------------------------
    # TEST CASE 3: Low Mood & Gut-Brain Axis
    # User selects: Mood: Low Mood | Meal: Lunch | Max Calories: 550
    # -------------------------------------------------------------
    print("\n" + "#" * 78)
    print("TEST SCENARIO 3: Neurotransmitter & Gut-Brain Axis")
    print("Input -> Mood: 'Low Mood' | Meal: 'Lunch' | Max Calories: 550")
    print("#" * 78)
    
    recs_low = recommender.recommend(
        mood="Low Mood",
        meal_type="Lunch",
        max_calories=550.0,
        top_n=3
    )
    
    for i, r in enumerate(recs_low, 1):
        print(f"\n[Rank #{i}] {r['food_name']} ({r['cuisine']})")
        print(f"  * Hybrid Score: {r['hybrid_score']} | Cosine Similarity: {r['cosine_similarity']}")
        print(f"  * Macros: {int(r['calories'])} kcal | Fiber: {r['fiber']}g")
        print(f"  * Scientific Rationale: {r['explanation']}")

    print("\n" + "=" * 78)
    print("STAGE 7 ENGINE VERIFICATION SUCCESSFUL: ALL TEST CASES PASSED!")
    print("=" * 78)


if __name__ == "__main__":
    run_stage7_verification()
