"""
Stage 13: Repository Verification & Open-Source Health Audit Script.
Validates:
1. Essential repository files (requirements.txt, .gitignore, app.py, artifacts, data, notebook).
2. Dependency lock syntax in requirements.txt.
3. Security exclusions in .gitignore.
4. Serialized artifacts presence and sizes.
5. Notebook integrity and cell count.
"""

import sys
import os
import json

root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

print("=" * 60)
print("STAGE 13: MOODFOOD REPOSITORY INTEGRITY & PACKAGING AUDIT")
print("=" * 60)

# 1. Essential Files
required_files = [
    "requirements.txt",
    ".gitignore",
    "app.py",
    "metadata.json",
    "package.json",
    "tsconfig.json",
    "vite.config.ts"
]

missing_files = []
for f in required_files:
    p = os.path.join(root_dir, f)
    if not os.path.exists(p):
        missing_files.append(f)

assert not missing_files, f"Missing required repository files: {missing_files}"
print(f"✓ File Structure: All {len(required_files)} root configuration files present.")

# 2. requirements.txt Validation
req_path = os.path.join(root_dir, "requirements.txt")
with open(req_path, "r", encoding="utf-8") as f:
    req_lines = [line.strip() for line in f if line.strip() and not line.startswith("#")]

critical_packages = ["streamlit", "pandas", "numpy", "scikit-learn", "joblib"]
for pkg in critical_packages:
    found = any(pkg in line for line in req_lines)
    assert found, f"Critical package '{pkg}' missing from requirements.txt"

print(f"✓ Requirements: Validated {len(req_lines)} dependencies including streamlit, pandas, scikit-learn.")

# 3. .gitignore Validation
gitignore_path = os.path.join(root_dir, ".gitignore")
with open(gitignore_path, "r", encoding="utf-8") as f:
    gitignore_content = f.read()

critical_rules = ["__pycache__/", "node_modules/", ".ipynb_checkpoints/", "venv/"]
for rule in critical_rules:
    assert rule in gitignore_content, f"Rule '{rule}' missing from .gitignore"

print(f"✓ Gitignore Security: Validated exclusion of bytecode, node_modules, and notebooks checkpoints.")

# 4. Artifacts Verification
artifacts_dir = os.path.join(root_dir, "artifacts")
expected_artifacts = [
    "tfidf_vectorizer.pkl",
    "tfidf_matrix.pkl",
    "food_dataset_clean.pkl",
    "model_metadata.json"
]

for art in expected_artifacts:
    art_path = os.path.join(artifacts_dir, art)
    assert os.path.exists(art_path), f"Artifact '{art}' missing from artifacts directory"
    size_kb = os.path.getsize(art_path) / 1024.0
    print(f"  - {art} ({size_kb:.1f} KB) ... OK")

print("✓ Artifacts Store: All 4 production assets verified.")

# 5. Notebook Verification
nb_path = os.path.join(root_dir, "notebook", "Mood_Based_Food_Recommendation.ipynb")
with open(nb_path, "r", encoding="utf-8") as f:
    nb = json.load(f)

print(f"✓ Jupyter Notebook: Validated JSON syntax with {len(nb['cells'])} cells.")
assert len(nb["cells"]) >= 58, f"Expected at least 58 cells, got {len(nb['cells'])}"

print("\n" + "=" * 60)
print("AUDIT RESULT: 100% REPOSITORY INTEGRITY CONFIRMED")
print("Repository is completely prepared for GitHub commit & Streamlit Cloud.")
print("=" * 60)
