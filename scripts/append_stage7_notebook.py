"""
Appends Stage 7 (Recommendation Engine) cells to notebook/Mood_Based_Food_Recommendation.ipynb
"""

import json
import os

nb_path = os.path.join(os.path.dirname(__file__), "..", "notebook", "Mood_Based_Food_Recommendation.ipynb")

with open(nb_path, "r", encoding="utf-8") as f:
    nb = json.load(f)

# Stage 7 cells
stage7_cells = [
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## STAGE 7: Building the Recommendation System Engine\n",
            "---\n",
            "In this stage, we implement the mathematical heart of MoodFood: a **Content-Based Recommendation Engine** using **TF-IDF (Term Frequency-Inverse Document Frequency)** and **Cosine Similarity**, paired with **Multi-Objective Constraint Filtering** and **Hybrid Ranking**.\n",
            "\n",
            "### Mathematical Formulation:\n",
            "1. **Term Frequency-Inverse Document Frequency (TF-IDF)**:\n",
            "$$\\text{TF}(t, d) = \\frac{f_{t,d}}{\\sum_{t' \\in d} f_{t',d}}$$\n",
            "$$\\text{IDF}(t, D) = \\ln\\left(\\frac{1 + |D|}{1 + |\\{d \\in D : t \\in d\\}|}\\right) + 1$$\n",
            "$$\\text{TF-IDF}(t, d, D) = \\text{TF}(t, d) \\times \\text{IDF}(t, D)$$\n",
            "\n",
            "2. **Cosine Similarity**:\n",
            "$$\\cos(\\mathbf{q}, \\mathbf{d}) = \\frac{\\mathbf{q} \\cdot \\mathbf{d}}{\\|\\mathbf{q}\\|_2 \\|\\mathbf{d}\\|_2} = \\frac{\\sum_{i=1}^{m} q_i d_i}{\\sqrt{\\sum_{i=1}^{m} q_i^2} \\sqrt{\\sum_{i=1}^{m} d_i^2}}$$\n",
            "\n",
            "3. **Hybrid Multi-Objective Score**:\n",
            "$$\\text{Score}_{\\text{hybrid}} = 0.70 \\cdot \\text{CosineSim} + 0.15 \\cdot \\text{CalorieFit} + 0.15 \\cdot \\text{ProteinDensity}$$"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "### 17. Fitting the TF-IDF Vectorizer (Scikit-Learn)\n",
            "We vectorize the engineered `content_soup` documents using unigrams and bigrams (`ngram_range=(1, 2)`)."
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "from sklearn.feature_extraction.text import TfidfVectorizer\n",
            "from sklearn.metrics.pairwise import cosine_similarity\n",
            "\n",
            "# Initialize TF-IDF Vectorizer with unigrams and bigrams\n",
            "tfidf = TfidfVectorizer(\n",
            "    stop_words='english',\n",
            "    ngram_range=(1, 2),\n",
            "    min_df=1\n",
            ")\n",
            "\n",
            "# Fit and transform content soup\n",
            "tfidf_matrix = tfidf.fit_transform(df['content_soup'])\n",
            "\n",
            "print(f\"TF-IDF Matrix Shape: {tfidf_matrix.shape} (Items x Vocabulary Features)\")\n",
            "print(f\"Total unique n-grams extracted: {len(tfidf.get_feature_names_out())}\")"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "### 18. Building the Complete Recommendation Function\n",
            "We define `recommend_food()` which takes user inputs (mood, meal type, vegetarian preference, calorie limit, protein threshold, and optional cravings) and returns ranked results with explanations."
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "import re\n",
            "\n",
            "def recommend_food(\n",
            "    mood: str,\n",
            "    meal_type: str = \"Dinner\",\n",
            "    vegetarian: bool = True,\n",
            "    max_calories: float = 500,\n",
            "    min_protein: float = 0,\n",
            "    cravings: str = \"\",\n",
            "    top_n: int = 5\n",
            "):\n",
            "    \"\"\"\n",
            "    Executes hybrid content-based recommendation pipeline.\n",
            "    \"\"\"\n",
            "    # 1. Hard constraint filtering\n",
            "    mask = pd.Series(True, index=df.index)\n",
            "    \n",
            "    if vegetarian is not None:\n",
            "        mask &= (df[\"vegetarian\"] == (1 if vegetarian else 0)) | (~vegetarian)\n",
            "        \n",
            "    if max_calories:\n",
            "        mask &= (df[\"calories\"] <= max_calories)\n",
            "        \n",
            "    if min_protein:\n",
            "        mask &= (df[\"protein\"] >= min_protein)\n",
            "        \n",
            "    if meal_type and meal_type.lower() != \"all\":\n",
            "        mask &= (df[\"meal_type\"].str.lower() == meal_type.lower())\n",
            "        \n",
            "    candidate_indices = df[mask].index.tolist()\n",
            "    \n",
            "    # Relax constraints if zero candidates\n",
            "    if len(candidate_indices) == 0:\n",
            "        print(\"Notice: Strict constraints returned 0 items. Relaxing meal type constraint.\")\n",
            "        mask_relaxed = (df[\"vegetarian\"] == (1 if vegetarian else 0)) & (df[\"calories\"] <= max_calories)\n",
            "        candidate_indices = df[mask_relaxed].index.tolist()\n",
            "        \n",
            "    # 2. Build user query text matching soup syntax\n",
            "    mood_slug = mood.lower().replace(\" \", \"_\")\n",
            "    mood_tokens = f\"mood_{mood_slug} mood_{mood_slug} mood_{mood_slug} {mood_slug} {mood_slug}\"\n",
            "    meal_token = f\"meal_{meal_type.lower()}\" if meal_type else \"\"\n",
            "    diet_token = \"diet_vegetarian plant_based\" if vegetarian else \"diet_non_veg animal_protein\"\n",
            "    query_str = f\"{mood_tokens} {meal_token} {diet_token} {cravings}\"\n",
            "    \n",
            "    # 3. Vectorize query & compute cosine similarity\n",
            "    query_vec = tfidf.transform([query_str])\n",
            "    cos_sims = cosine_similarity(query_vec, tfidf_matrix).flatten()\n",
            "    \n",
            "    # 4. Rank candidates with hybrid score\n",
            "    ranked = []\n",
            "    for idx in candidate_indices:\n",
            "        sim = cos_sims[idx]\n",
            "        row = df.iloc[idx]\n",
            "        \n",
            "        # Calorie fit & Protein density bonus\n",
            "        cal_fit = min(1.0, row[\"calories\"] / max_calories) if max_calories else 0.8\n",
            "        p_score = min(1.0, row[\"protein_density_ratio\"] / 10.0)\n",
            "        \n",
            "        hybrid_score = 0.70 * sim + 0.15 * cal_fit + 0.15 * p_score\n",
            "        \n",
            "        ranked.append({\n",
            "            \"food_name\": row[\"food_name\"],\n",
            "            \"category\": row[\"category\"],\n",
            "            \"cuisine\": row[\"cuisine\"],\n",
            "            \"calories\": int(row[\"calories\"]),\n",
            "            \"protein\": row[\"protein\"],\n",
            "            \"fiber\": row[\"fiber\"],\n",
            "            \"mood\": row[\"mood\"],\n",
            "            \"cosine_sim\": round(sim, 4),\n",
            "            \"hybrid_score\": round(hybrid_score, 4)\n",
            "        })\n",
            "        \n",
            "    ranked_df = pd.DataFrame(ranked).sort_values(\"hybrid_score\", ascending=False).head(top_n)\n",
            "    return ranked_df\n",
            "\n",
            "# Test with Canonical Scenario (Mood: Stressed, Meal: Dinner, Vegetarian: True, Max Calories: 500)\n",
            "test_results = recommend_food(mood=\"Stressed\", meal_type=\"Dinner\", vegetarian=True, max_calories=500)\n",
            "print(\"Top 5 Recommendations for Stressed + Vegetarian Dinner under 500 kcal:\")\n",
            "test_results"
        ]
    }
]

nb["cells"].extend(stage7_cells)

with open(nb_path, "w", encoding="utf-8") as f:
    json.dump(nb, f, indent=1)

print(f"Appended Stage 7 cells to {nb_path}. Total cells now: {len(nb['cells'])}")
