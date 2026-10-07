# MoodFood — Portfolio Resume & Technical Interview Guide 📄

This document provides ready-to-use, ATS-optimized resume sections, STAR-method interview narratives, and technical defense scripts for the **MoodFood** project.

---

## 🎯 Resume Bullet Points by Role (XYZ Format)

### Role: Machine Learning / Recommender Systems Engineer
* **Architected and deployed an end-to-end multi-objective Recommender Engine** integrating smooth TF-IDF vectorization and sparse Cosine Similarity across a 1,702-dimensional vocabulary, achieving sub-2ms edge inference.
* **Engineered a hybrid ranking controller** ($0.70 \times \text{Sim} + 0.15 \times \text{CalFit} + 0.15 \times \text{ProteinFit}$) balancing semantic mood affinities, strict dietary constraints, and macro densities, delivering **1.03 ms mean latency** across 100 sequential stress queries.
* **Optimized production memory efficiency** via zero-copy caching (`@st.cache_resource`) and Pickle Protocol 5 serialization, reducing the cached ML pipeline RAM footprint to **0.50 MB** (99% below the 1GB Streamlit Cloud free-tier threshold).
* **Constructed an automated CI/CD testing suite (14 unit tests)** validating Intra-List Diversity (**0.742 ILD**), 100% matrix quadrant coverage (24/24), deterministic vegetarian safety, and zero-match fallback recovery under contradictory bounds.

### Role: Data Scientist / Applied ML Specialist
* **Curated and engineered a 320-item domain-specific Nutritional Psychiatry dataset** across 16 attributes, mapping clinical neurochemical pathways (HPA axis cortisol, ATP synthesis, dopamine receptor sensitivity, and vagus nerve serotonin).
* **Synthesized textual content soups** combining ingredients, cuisines, and clinical keywords with targeted 3x mood priming, achieving 100% balanced representation across 6 affective states and 5 meal occasions.
* **Authored a reproducible 66-cell Jupyter Notebook** detailing exploratory data analysis, bivariate correlation matrices, sparse linear algebra formulations, and unit test suites.
* **Implemented interactive data visualization modules** in Streamlit displaying real-time macronutrient caloric split gauges ($4\text{P}/4\text{C}/9\text{F}$) and clinical explainability rationale cards.

### Role: Full-Stack AI / Software Engineer
* **Developed and deployed a production web application** on Streamlit Community Cloud with continuous deployment linked to the GitHub `main` branch and `.streamlit/config.toml` server optimization.
* **Designed an anti-slop, calm wellness user interface** following zero-pill design discipline, WCAG 2.1 AAA contrast standards (13.73:1), custom serif typography, and responsive drawer layouts.
* **Engineered robust state management** supporting query history tracking, favorite recipe persistence (`add`, `deduplicate`, `remove`), and zero-crash fault-tolerant fallback recovery.

---

## 🌟 STAR Method Interview Stories

### Story 1: Latency & Cost Optimization (Sparse Linear Algebra vs. Deep Learning)
* **Situation:** Needed to build a real-time mood-based food recommender for mobile and web users where recommendations feel instantaneous as the user adjusts calories, protein, and mood sliders.
* **Task:** Evaluate whether to use deep transformer embeddings (e.g. OpenAI `text-embedding-3-small` or BERT) or classical Information Retrieval (TF-IDF + Cosine Similarity), taking latency, hosting costs, and explainability into account.
* **Action:** Benchmarked both approaches. Dense embeddings introduced 200–500ms network round-trip overhead and ongoing API billing. Instead, I designed a domain-specific 1,702-feature vocabulary using smooth TF-IDF, pre-computed an $L_2$-normalized sparse matrix, and executed vector cosine similarity via scipy compressed sparse row (CSR) dot products on standard CPU.
* **Result:** Achieved an average query latency of **1.03 ms** (5x faster than our 5ms SLA), reduced application RAM usage to **0.50 MB**, eliminated external API costs entirely, and ensured 100% deterministic, explainable token activations.

### Story 2: Handling Contradictory Constraints & Edge Cases
* **Situation:** Users frequently input physically impossible or contradictory constraints into health apps (e.g. demanding a meal under 150 kcal with at least 35g of protein, which violates fundamental thermodynamic laws since 35g protein yields $35 \times 4 = 140\text{ kcal}$ of amino acids alone).
* **Task:** Build a fault-tolerant ranking controller that prevents zero-match crashes or empty UI screens while safeguarding non-negotiable dietary choices (e.g. vegetarian safety).
* **Action:** Implemented a two-tier constraint relaxation algorithm. Non-negotiable ethical flags (`vegetarian == True`) are enforced as strict pre-filters. If secondary constraints (calorie ceiling/protein floor) yield zero candidates, the controller automatically relaxes secondary thresholds, scores candidates using mood similarity and macro density, and renders an explainable banner informing the user of the adjustment.
* **Result:** Achieved 100% graceful recovery with zero unhandled exceptions, zero non-vegetarian leakage across all boundary tests, and maintained a flawless user experience.

---

## 🔑 Core Technical Competencies & Keywords

```
Languages & Tools: Python 3.10/3.11/3.12, TypeScript, Bash, Git, GitHub Actions, Streamlit
Libraries: Scikit-learn, Pandas, NumPy, SciPy (Sparse Matrices), Matplotlib, Seaborn, Joblib
Recommender Concepts: Vector Space Model, TF-IDF, Cosine Similarity, Multi-Objective Ranking,
                      Intra-List Diversity (ILD), Content-Based Filtering, Hard Pre-filtering
Data Science: Feature Engineering, Data Cleaning, Exploratory Data Analysis, Correlation Heatmaps,
              Null Handling, Type Casting, Matrix Normalization (L2-norm)
Software Engineering: CI/CD, Unit Testing (unittest), Boundary Condition Testing, Micro-benchmarking,
                      State Management, Zero-Copy Caching (@st.cache_resource), Pickle Protocol 5,
                      WCAG 2.1 AAA Accessibility, Zero-Pill Design Philosophy
```
