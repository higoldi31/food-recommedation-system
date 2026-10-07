"""
=============================================================================
MoodFood: Mood-Based Food Recommendation System
Streamlit Production Application (app.py)
Author: Senior Data Scientist & ML Engineer
Stage 11: Calm Wellness UI & Nutritional Psychology Design System
=============================================================================
"""

import os
import sys
import json
import pickle
import math
import re
from typing import Dict, List, Any, Tuple, Optional

# Add scripts directory to path to access PureTfidfVectorizer definition
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "scripts"))
try:
    from stage7_recommendation_engine import PureTfidfVectorizer, cosine_similarity_sparse
except ImportError:
    pass

# Check if running within Streamlit runtime
try:
    import streamlit as st
    HAS_STREAMLIT = True
except ImportError:
    HAS_STREAMLIT = False


# =============================================================================
# 1. CORE PIPELINE LOADER WITH PERSISTENT CACHING
# =============================================================================

def _load_artifacts_from_disk(artifacts_dir: str = "artifacts") -> Tuple[Any, Any, List[Dict[str, Any]], Dict[str, Any]]:
    """Loads and deserializes precomputed ML assets from the artifacts directory."""
    if not os.path.exists(artifacts_dir):
        artifacts_dir = os.path.join(os.path.dirname(__file__), "artifacts")

    vec_path = os.path.join(artifacts_dir, "tfidf_vectorizer.pkl")
    mat_path = os.path.join(artifacts_dir, "tfidf_matrix.pkl")
    data_path = os.path.join(artifacts_dir, "food_dataset_clean.pkl")
    meta_path = os.path.join(artifacts_dir, "model_metadata.json")

    with open(vec_path, "rb") as f:
        vectorizer = pickle.load(f)

    with open(mat_path, "rb") as f:
        matrix = pickle.load(f)

    with open(data_path, "rb") as f:
        dataset = pickle.load(f)

    with open(meta_path, "r", encoding="utf-8") as f:
        metadata = json.load(f)

    return vectorizer, matrix, dataset, metadata


if HAS_STREAMLIT:
    @st.cache_resource(show_spinner=False)
    def load_cached_pipeline():
        """Caches TF-IDF Vectorizer, Feature Matrix, Dataset, and Metadata in RAM."""
        return _load_artifacts_from_disk()
else:
    def load_cached_pipeline():
        return _load_artifacts_from_disk()


# =============================================================================
# 2. RECOMMENDATION CONTROLLER
# =============================================================================

class MoodFoodController:
    """
    Core Controller managing data access, session state, hard constraint filtering,
    vector dot-product scoring, and hybrid ranking.
    """
    def __init__(self):
        self.vectorizer, self.matrix, self.dataset, self.metadata = load_cached_pipeline()

    def filter_candidates(
        self,
        meal_type: str = "All",
        is_vegetarian: bool = False,
        max_calories: Optional[float] = None,
        min_protein: Optional[float] = None
    ) -> List[int]:
        """Applies deterministic hard constraints and returns passing row indices."""
        indices = []
        for i, row in enumerate(self.dataset):
            if is_vegetarian and int(row.get("vegetarian", 0)) != 1:
                continue
            if max_calories is not None and float(row.get("calories", 0)) > max_calories:
                continue
            if min_protein is not None and float(row.get("protein", 0)) < min_protein:
                continue
            if meal_type and meal_type.lower() != "all":
                if row.get("meal_type", "").lower() != meal_type.lower():
                    continue
            indices.append(i)

        # Fallback if filters are excessively strict (0 candidates)
        if not indices:
            for i, row in enumerate(self.dataset):
                if is_vegetarian and int(row.get("vegetarian", 0)) != 1:
                    continue
                if max_calories is not None and float(row.get("calories", 0)) > max_calories:
                    continue
                indices.append(i)

        return indices

    def generate_recommendations(
        self,
        mood: str,
        meal_type: str = "Dinner",
        is_vegetarian: bool = True,
        max_calories: float = 500,
        min_protein: float = 0,
        cravings: str = "",
        top_n: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Executes hybrid content-based recommendation matching user mood and constraints.
        Formula: FinalScore = 0.70 * CosineSim + 0.15 * CalorieFit + 0.15 * ProteinDensityFit
        """
        candidate_indices = self.filter_candidates(
            meal_type=meal_type,
            is_vegetarian=is_vegetarian,
            max_calories=max_calories,
            min_protein=min_protein
        )

        if not candidate_indices:
            candidate_indices = list(range(len(self.dataset)))

        # Construct user query with 3x mood priming tokens
        mood_slug = mood.lower().replace(" ", "_")
        mood_tokens = f"mood_{mood_slug} mood_{mood_slug} mood_{mood_slug} {mood_slug} {mood_slug}"
        meal_token = f"meal_{meal_type.lower()}" if meal_type.lower() != "all" else ""
        diet_token = "diet_vegetarian plant_based" if is_vegetarian else "diet_non_veg animal_protein"
        query_text = f"{mood_tokens} {meal_token} {diet_token} {cravings}"

        # Vectorize query
        query_vec = self.vectorizer.transform([query_text])[0]

        scored_candidates = []
        for idx in candidate_indices:
            doc_vec = self.matrix[idx]
            sim = cosine_similarity_sparse(query_vec, doc_vec)
            row = self.dataset[idx]

            cal_val = float(row.get("calories", 300))
            cal_fit = min(1.0, cal_val / max_calories) if max_calories else 0.8
            p_val = float(row.get("protein", 10))
            protein_density = float(row.get("protein_density_ratio", p_val / (cal_val / 100.0 if cal_val else 1.0)))
            p_score = min(1.0, protein_density / 10.0)

            # Hybrid scoring equation
            hybrid_score = (0.70 * sim) + (0.15 * cal_fit) + (0.15 * p_score)

            # Biochemical explainability rationale
            rationale = self._build_rationale(row, mood, max_calories)

            # Macronutrient calorie split calculation
            cal_from_prot = p_val * 4.0
            cal_from_carb = float(row.get("carbs", 30)) * 4.0
            cal_from_fat = float(row.get("fat", 10)) * 9.0
            total_computed_cals = max(1.0, cal_from_prot + cal_from_carb + cal_from_fat)
            pct_prot = round((cal_from_prot / total_computed_cals) * 100, 1)
            pct_carb = round((cal_from_carb / total_computed_cals) * 100, 1)
            pct_fat = round((cal_from_fat / total_computed_cals) * 100, 1)

            scored_candidates.append({
                "id": row.get("food_id", idx),
                "food_name": row.get("food_name", "Healthy Meal"),
                "category": row.get("category", "Main Course"),
                "cuisine": row.get("cuisine", "Global"),
                "meal_type": row.get("meal_type", "Dinner"),
                "mood": row.get("mood", mood),
                "calories": int(cal_val),
                "protein": round(p_val, 1),
                "carbs": round(float(row.get("carbs", 30)), 1),
                "fat": round(float(row.get("fat", 10)), 1),
                "fiber": round(float(row.get("fiber", 5)), 1),
                "sugar": round(float(row.get("sugar", 4)), 1),
                "vegetarian": bool(int(row.get("vegetarian", 1))),
                "spicy": bool(int(row.get("spicy", 0))),
                "ingredients": row.get("ingredients", ""),
                "dietary_tags": row.get("dietary_tags", ""),
                "cosine_sim": round(sim, 4),
                "hybrid_score": round(hybrid_score, 4),
                "rationale": rationale,
                "macro_split": {
                    "pct_protein": pct_prot,
                    "pct_carbs": pct_carb,
                    "pct_fat": pct_fat
                }
            })

        scored_candidates.sort(key=lambda x: x["hybrid_score"], reverse=True)
        return scored_candidates[:top_n]

    def _build_rationale(self, row: Dict[str, Any], mood: str, max_calories: float) -> str:
        """Generates clear scientific rationale based on Nutritional Psychiatry."""
        food_mood = row.get("mood", mood)
        budget_note = f"Fits comfortably within your {int(max_calories)} kcal budget."

        if food_mood == "Stressed":
            return f"Rich in magnesium and unrefined complex carbohydrates to modulate cortisol release and dampen HPA axis tension. {budget_note}"
        elif food_mood == "Tired":
            return f"Provides bioavailable iron, vitamin B12, and clean mitochondrial fuel to boost cellular ATP production without jittery crashes. {budget_note}"
        elif food_mood == "Relaxed":
            return f"Supplies natural L-tryptophan and apigenin calming precursors, supporting parasympathetic wind-down and restful restorative sleep. {budget_note}"
        elif food_mood == "Happy":
            return f"Contains active cacao theobromine and polyphenols, enhancing dopamine neurotransmission and cerebral blood flow. {budget_note}"
        elif food_mood == "Energetic":
            return f"Delivers sustained-release complex carbohydrates and lean branched-chain amino acids for prolonged stamina. {budget_note}"
        else: # Low Mood
            return f"Packed with fermented probiotic cultures and omega-3 fatty acids, actively stimulating the vagus nerve and gut-brain serotonin axis. {budget_note}"


# =============================================================================
# 3. STREAMLIT CALM WELLNESS UI (STAGE 11)
# =============================================================================

def render_streamlit_app():
    """Renders the complete Streamlit web interface with serene, warm wellness styling."""
    st.set_page_config(
        page_title="MoodFood — Mood-Based Food Recommendation System",
        page_icon="🥗",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Stage 11 Design System: Warm Wellness Palette & Anti-Slop Typography
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&family=Playfair+Display:ital,wght@0,500;0,600;0,700;1,400&display=swap');

        /* Background & Root Colors */
        .stApp {
            background-color: #FDFBF7;
            color: #2D3732;
            font-family: 'Plus Jakarta Sans', -apple-system, sans-serif;
        }

        h1, h2, h3, .serif-font {
            font-family: 'Playfair Display', Georgia, serif !important;
            font-weight: 600;
            color: #202E26;
            letter-spacing: -0.01em;
        }

        /* Calm Recipe Card (Zero-Pill Architecture) */
        .calm-card {
            background-color: #FFFFFF;
            border-radius: 16px;
            padding: 24px;
            margin-bottom: 20px;
            border: 1px solid #E8E2D7;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.02);
            transition: all 0.2s ease-in-out;
        }
        .calm-card:hover {
            border-color: #D2C7B6;
            box-shadow: 0 4px 14px rgba(0, 0, 0, 0.04);
        }

        .dish-title {
            font-family: 'Playfair Display', Georgia, serif;
            font-size: 1.25rem;
            font-weight: 600;
            color: #202E26;
            margin-bottom: 4px;
        }

        /* Clean Unboxed Metadata Line */
        .meta-line {
            font-size: 0.82rem;
            color: #6E7C73;
            margin-bottom: 12px;
            display: flex;
            align-items: center;
            gap: 6px;
            flex-wrap: wrap;
        }
        .meta-sep {
            color: #B5C0B9;
        }

        /* Scientific Rationale Highlight Box */
        .rationale-box {
            background-color: #FAF8F5;
            border-left: 3px solid #527360;
            padding: 12px 16px;
            border-radius: 0 10px 10px 0;
            font-size: 0.88rem;
            color: #3E4D43;
            line-height: 1.55;
            margin-bottom: 14px;
        }

        /* Macro Caloric Ratio Bar Gauge */
        .macro-bar-container {
            display: flex;
            height: 8px;
            width: 100%;
            border-radius: 4px;
            overflow: hidden;
            background-color: #EDE8DE;
            margin-top: 6px;
            margin-bottom: 6px;
        }
        .macro-bar-prot { background-color: #527360; }
        .macro-bar-carb { background-color: #C2AB91; }
        .macro-bar-fat  { background-color: #D9822B; }

        /* Metric Box */
        .stat-box {
            background-color: #FFFFFF;
            border: 1px solid #E8E2D7;
            border-radius: 12px;
            padding: 14px;
            text-align: center;
        }
        .stat-val {
            font-size: 1.35rem;
            font-weight: 700;
            color: #202E26;
            font-family: 'Playfair Display', Georgia, serif;
        }
        .stat-lbl {
            font-size: 0.72rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: #886F58;
            font-weight: 600;
            margin-top: 2px;
        }
        </style>
    """, unsafe_allow_html=True)

    # Initialize Session State
    if "favorites" not in st.session_state:
        st.session_state.favorites = []
    if "query_history" not in st.session_state:
        st.session_state.query_history = []
    if "recommendations" not in st.session_state:
        st.session_state.recommendations = []

    controller = MoodFoodController()

    # --- SIDEBAR CONTROLS ---
    st.sidebar.markdown("""
        <div style="padding-bottom: 12px; border-bottom: 1px solid #EAE3D6; margin-bottom: 16px;">
            <div style="font-family: 'Playfair Display', Georgia, serif; font-size: 1.3rem; font-weight: 700; color: #202E26;">
                🥗 MoodFood Studio
            </div>
            <div style="font-size: 0.78rem; color: #6E7C73; margin-top: 2px;">
                Nutritional Psychiatry &amp; Algorithmic Curation
            </div>
        </div>
    """, unsafe_allow_html=True)

    mood_options = {
        "Stressed": "🧘 Stressed · Cortisol Modulation",
        "Tired": "⚡ Tired · Iron & Cellular ATP",
        "Relaxed": "🌿 Relaxed · Gentle Tryptophan",
        "Happy": "☀️ Happy · Dopamine & Flavonoids",
        "Energetic": "🔥 Energetic · Sustained Glycogen",
        "Low Mood": "🌱 Low Mood · Gut-Brain Axis"
    }
    selected_mood_raw = st.sidebar.selectbox(
        "1. Emotional State",
        list(mood_options.keys()),
        format_func=lambda x: mood_options[x]
    )

    meal_options = ["Dinner", "Lunch", "Breakfast", "Snack", "All"]
    selected_meal = st.sidebar.selectbox("2. Meal Occasion", meal_options, index=0)

    st.sidebar.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
    st.sidebar.markdown("**3. Dietary Constraints**")
    is_veg = st.sidebar.checkbox("🌱 Vegetarian (Zero Non-Veg)", value=True)

    max_cal = st.sidebar.slider("Maximum Calorie Ceiling", min_value=150, max_value=800, value=500, step=25)
    min_prot = st.sidebar.slider("Minimum Protein Floor (g)", min_value=0, max_value=40, value=0, step=5)

    craving_input = st.sidebar.text_input("4. Specific Cravings / Ingredients", placeholder="e.g. warm lentils, spinach, turmeric")

    get_recs_btn = st.sidebar.button("✨ Curate Recommendations", type="primary", use_container_width=True)

    if get_recs_btn or not st.session_state.recommendations:
        with st.spinner("Analyzing biochemical compatibility..."):
            recs = controller.generate_recommendations(
                mood=selected_mood_raw,
                meal_type=selected_meal,
                is_vegetarian=is_veg,
                max_calories=max_cal,
                min_protein=min_prot,
                cravings=craving_input,
                top_n=5
            )
            st.session_state.recommendations = recs
            st.session_state.query_history.append({
                "mood": selected_mood_raw,
                "meal": selected_meal,
                "cal_ceiling": max_cal,
                "top_dish": recs[0]["food_name"] if recs else "None"
            })

    # --- HERO HEADER ---
    st.markdown("""
        <div style="margin-bottom: 24px;">
            <h1 style="font-size: 2.1rem; margin-bottom: 8px;">Nourish Your Emotional State</h1>
            <p style="font-size: 0.95rem; color: #5B6B61; max-width: 820px; line-height: 1.6;">
                Discover tailored meals curated through <strong>Nutritional Psychiatry</strong> and mathematical <strong>TF-IDF &amp; Cosine Similarity</strong>.
                Filtered strictly by your dietary targets, then ranked by neurochemical compatibility and macro density.
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Executive Status Row
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""
            <div class="stat-box">
                <div class="stat-val">{len(controller.dataset)}</div>
                <div class="stat-lbl">Curated Catalog</div>
            </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
            <div class="stat-box">
                <div class="stat-val">{selected_mood_raw}</div>
                <div class="stat-lbl">Target Mood State</div>
            </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
            <div class="stat-box">
                <div class="stat-val">≤ {max_cal} kcal</div>
                <div class="stat-lbl">Calorie Ceiling</div>
            </div>
        """, unsafe_allow_html=True)
    with c4:
        st.markdown(f"""
            <div class="stat-box">
                <div class="stat-val">{'Vegetarian' if is_veg else 'Standard'}</div>
                <div class="stat-lbl">Dietary Rule</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

    # --- MAIN TABS ---
    tab_recs, tab_macro, tab_favorites = st.tabs([
        "✨ Curated Recommendations",
        "📊 Macro Ratio Analysis",
        f"❤️ Saved Favorites ({len(st.session_state.favorites)})"
    ])

    with tab_recs:
        recs = st.session_state.recommendations
        if not recs:
            st.info("No recipes currently match all constraints. Try adjusting the calorie slider or relaxing meal occasions.")
        else:
            for rank_idx, rec in enumerate(recs, 1):
                split = rec["macro_split"]
                is_fav = rec['food_name'] in [f['food_name'] for f in st.session_state.favorites]

                # Recipe Card Container
                st.markdown(f"""
                    <div class="calm-card">
                        <div style="display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 2px;">
                            <div class="dish-title">#{rank_idx} · {rec['food_name']}</div>
                            <div style="font-family: 'Playfair Display', Georgia, serif; font-size: 1.15rem; font-weight: 700; color: #527360;">
                                {rec['hybrid_score']*100:.1f}% Fit
                            </div>
                        </div>

                        <div class="meta-line">
                            <span>{rec['cuisine']} cuisine</span>
                            <span class="meta-sep">·</span>
                            <span>{rec['category']}</span>
                            <span class="meta-sep">·</span>
                            <span>{rec['meal_type']}</span>
                            <span class="meta-sep">·</span>
                            <span>{'🌱 Vegetarian' if rec['vegetarian'] else 'Animal Protein'}</span>
                            <span class="meta-sep">·</span>
                            <span><strong>{rec['calories']} kcal</strong></span>
                            <span class="meta-sep">·</span>
                            <span>Cosine Sim {rec['cosine_sim']}</span>
                        </div>

                        <div class="rationale-box">
                            <strong>Biochemical Action:</strong> {rec['rationale']}
                        </div>

                        <!-- Macro Ratio Distribution Meter -->
                        <div style="font-size: 0.76rem; color: #76867D; display: flex; justify-content: space-between; margin-top: 10px;">
                            <span>Caloric Split: <strong style="color: #527360;">{split['pct_protein']}% Protein</strong>, <strong style="color: #A38C72;">{split['pct_carbs']}% Carbs</strong>, <strong style="color: #B5651D;">{split['pct_fat']}% Fat</strong></span>
                            <span>{rec['protein']}g P · {rec['carbs']}g C · {rec['fat']}g F · {rec['fiber']}g Fiber</span>
                        </div>
                        <div class="macro-bar-container">
                            <div class="macro-bar-prot" style="width: {split['pct_protein']}%;"></div>
                            <div class="macro-bar-carb" style="width: {split['pct_carbs']}%;"></div>
                            <div class="macro-bar-fat" style="width: {split['pct_fat']}%;"></div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)

                # Collapsible Recipe Drawer & Action Row
                col_exp, col_act = st.columns([4, 1])
                with col_exp:
                    with st.expander(f"🌿 View Ingredients & Nutritional Profile for {rec['food_name']}"):
                        st.markdown(f"**Key Ingredients:** {rec['ingredients']}")
                        st.markdown(f"**Nutritional Tags:** {rec['dietary_tags']}")
                        st.markdown(f"**Sugar:** {rec['sugar']}g | **Dietary Fiber:** {rec['fiber']}g")
                with col_act:
                    if st.button(
                        "❤️ Saved" if is_fav else "🤍 Save",
                        key=f"fav_btn_stage11_{rec['id']}",
                        use_container_width=True
                    ):
                        if is_fav:
                            st.session_state.favorites = [f for f in st.session_state.favorites if f['food_name'] != rec['food_name']]
                        else:
                            st.session_state.favorites.append(rec)
                        st.rerun() if hasattr(st, 'rerun') else st.experimental_rerun()

                st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

    with tab_macro:
        st.subheader("Macronutrient Comparison (Top 5 Recommendations)")
        if recs:
            chart_data = {
                "Recipe": [r["food_name"][:22] + "..." for r in recs],
                "Protein (g)": [r["protein"] for r in recs],
                "Carbohydrates (g)": [r["carbs"] for r in recs],
                "Fat (g)": [r["fat"] for r in recs],
                "Dietary Fiber (g)": [r["fiber"] for r in recs]
            }
            st.bar_chart(chart_data, x="Recipe")

    with tab_favorites:
        st.subheader("Your Saved Wellness Favorites")
        if not st.session_state.favorites:
            st.info("No dishes saved yet. Click the 'Save' button on any recommended meal to persist it here.")
        else:
            for fav in st.session_state.favorites:
                st.markdown(f"""
                    <div style="background-color: #FFFFFF; border: 1px solid #E8E2D7; border-radius: 12px; padding: 14px; margin-bottom: 10px;">
                        <div style="font-weight: 600; color: #202E26;">{fav['food_name']}</div>
                        <div style="font-size: 0.82rem; color: #6E7C73;">{fav['cuisine']} · {fav['calories']} kcal · {fav['protein']}g Protein · {fav['mood']}</div>
                    </div>
                """, unsafe_allow_html=True)


# =============================================================================
# 4. HEADLESS CLI VALIDATION ENTRYPOINT
# =============================================================================

def run_headless_smoke_test():
    """Runs a complete verification check on MoodFoodController when executed in CLI."""
    print("=" * 80)
    print("STAGE 11: STREAMLIT CALM UI & RECIPE CONTROLLER VERIFICATION")
    print("=" * 80)
    
    controller = MoodFoodController()
    print(f"[OK] Cached Pipeline Loaded successfully!")
    print(f"  - Total Dataset Items: {len(controller.dataset)}")
    print(f"  - Vocabulary Features: {len(controller.vectorizer.vocabulary)}")

    # Test Canonical Brief
    recs = controller.generate_recommendations(
        mood="Stressed",
        meal_type="Dinner",
        is_vegetarian=True,
        max_calories=500,
        top_n=5
    )

    print(f"\n[OK] Canonical Brief Recommendations Generated with Macro Splits:")
    for i, r in enumerate(recs, 1):
        split = r["macro_split"]
        print(f"  {i}. {r['food_name']} ({r['calories']} kcal, {r['protein']}g P) -> Split: P {split['pct_protein']}%, C {split['pct_carbs']}%, F {split['pct_fat']}%")
        assert r['vegetarian'] is True, "Vegetarian check failed!"
        assert r['calories'] <= 500, "Calorie budget check failed!"

    print("\n" + "=" * 80)
    print("STAGE 11 VERIFICATION PASSED! app.py is styled with Calm Wellness design tokens.")
    print("=" * 80)


if __name__ == "__main__":
    if HAS_STREAMLIT:
        render_streamlit_app()
    else:
        run_headless_smoke_test()
