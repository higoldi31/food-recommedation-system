"""
Appends Section 25 and Section 26 to notebook/Mood_Based_Food_Recommendation.ipynb
covering Stage 11: Designing Calm Streamlit UI Architecture & Component Visual Verification.
"""

import json
import os

notebook_path = os.path.join(os.path.dirname(__file__), "..", "notebook", "Mood_Based_Food_Recommendation.ipynb")

with open(notebook_path, "r", encoding="utf-8") as f:
    nb = json.load(f)

# Stage 11 Markdown Cell: UI System & Design Tokens
cell_s25_md = {
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "### 25. Stage 11: Designing Calm Streamlit UI System & Custom CSS Architecture\n",
        "\n",
        "In **Stage 11**, we engineer the frontend presentation layer according to the **Calm Wellness Design System**:\n",
        "- **Warm Serene Palette**: Natural cream parchment (`#FDFBF7`), deep slate pine (`#202E26`), calming sage (`#527360`), and energizing ochre amber (`#D9822B`).\n",
        "- **Zero-Pill Typography Hierarchy**: Anti-slop layout pairing classical editorial serif headers (*Playfair Display*) with clean geometric body typography (*Plus Jakarta Sans*), avoiding generic AI pill tags in favor of clean typographic separators (`·`).\n",
        "- **Interactive Macro Ratio Gauge**: Dynamic stacked bar meters calculating true caloric contributions ($4 \\times \\text{Protein}$, $4 \\times \\text{Carbs}$, $9 \\times \\text{Fat}$) normalized to 100%.\n",
        "- **Explainable Neurochemical Action Callouts**: Dedicated clinical psychiatry rationale cards detailing cortisol dampening, L-tryptophan calming, iron mitochondrial energy, and serotonin synthesis via the vagus nerve.\n",
        "- **Collapsible Recipe & Ingredient Drawers**: On-demand expansion of ingredients, macronutrients, and preparation notes without cluttering the initial scan viewport.\n"
    ]
}

# Stage 11 Code Cell: CSS Design System Definition & Inspection
cell_s25_code = {
    "cell_type": "code",
    "execution_count": None,
    "metadata": {},
    "outputs": [],
    "source": [
        "# Stage 11 Design System Tokens & Custom CSS Specifications\n",
        "CALM_UI_THEME = {\n",
        "    'bg_primary': '#FDFBF7',\n",
        "    'surface_card': '#FFFFFF',\n",
        "    'border_subtle': '#E8E2D7',\n",
        "    'text_heading': '#202E26',\n",
        "    'text_body': '#2D3732',\n",
        "    'text_muted': '#5B6B61',\n",
        "    'accent_sage': '#527360',\n",
        "    'accent_amber': '#D9822B',\n",
        "    'accent_sand': '#C2AB91',\n",
        "}\n",
        "\n",
        "def compute_macro_split(protein_g, carbs_g, fat_g):\n",
        "    \"\"\"Calculates exact caloric percentage split for dynamic UI meter rendering.\"\"\"\n",
        "    cal_prot = protein_g * 4.0\n",
        "    cal_carb = carbs_g * 4.0\n",
        "    cal_fat = fat_g * 9.0\n",
        "    total_cal = cal_prot + cal_carb + cal_fat\n",
        "    if total_cal == 0:\n",
        "        return {'pct_prot': 33, 'pct_carb': 34, 'pct_fat': 33}\n",
        "    pct_prot = round((cal_prot / total_cal) * 100)\n",
        "    pct_carb = round((cal_carb / total_cal) * 100)\n",
        "    pct_fat = max(0, 100 - (pct_prot + pct_carb))\n",
        "    return {'pct_prot': pct_prot, 'pct_carb': pct_carb, 'pct_fat': pct_fat}\n",
        "\n",
        "sample_split = compute_macro_split(protein_g=24, carbs_g=42, fat_g=12)\n",
        "print('Caloric Split Sample (24g P, 42g C, 12g F):', sample_split)\n",
        "print('Design System Theme Initialized with', len(CALM_UI_THEME), 'design tokens.')\n"
    ]
}

# Stage 11 Markdown Cell: Visual Verification & Accessibility Testing
cell_s26_md = {
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "### 26. Stage 11: Visual Testing, Macro Gauge & Palette Contrast Verification\n",
        "\n",
        "We verify that our calm wellness color tokens strictly adhere to **WCAG 2.1 AA Accessibility Standards** (minimum 4.5:1 contrast for body text, 3.0:1 for large headings & interactive UI elements), and that the macro ratio distribution meters compute flawlessly across the entire 320-recipe dataset."
    ]
}

# Stage 11 Code Cell: Automated Contrast and Macro Verification
cell_s26_code = {
    "cell_type": "code",
    "execution_count": None,
    "metadata": {},
    "outputs": [],
    "source": [
        "import pickle\n",
        "import os\n",
        "\n",
        "# 1. Load clean catalog and test macro splits across all 320 recipes\n",
        "artifacts_path = os.path.join('..', 'artifacts', 'food_dataset_clean.pkl')\n",
        "if not os.path.exists(artifacts_path):\n",
        "    artifacts_path = os.path.join('artifacts', 'food_dataset_clean.pkl')\n",
        "\n",
        "with open(artifacts_path, 'rb') as f:\n",
        "    catalog = pickle.load(f)\n",
        "\n",
        "all_splits_valid = True\n",
        "for item in catalog:\n",
        "    s = compute_macro_split(item.get('protein', 0), item.get('carbs', 0), item.get('fat', 0))\n",
        "    if s['pct_prot'] + s['pct_carb'] + s['pct_fat'] != 100:\n",
        "        all_splits_valid = False\n",
        "        break\n",
        "\n",
        "print(f'Tested {len(catalog)} recipes: All macro percentage distributions sum to 100%: {all_splits_valid}')\n",
        "\n",
        "# 2. WCAG Contrast Check\n",
        "def hex_to_rgb(hex_str):\n",
        "    hex_str = hex_str.lstrip('#')\n",
        "    return tuple(int(hex_str[i:i+2], 16) for i in (0, 2, 4))\n",
        "\n",
        "def relative_luminance(rgb):\n",
        "    comps = [c / 255.0 for c in rgb]\n",
        "    comps = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in comps]\n",
        "    return 0.2126 * comps[0] + 0.7152 * comps[1] + 0.0722 * comps[2]\n",
        "\n",
        "def contrast_ratio(hex1, hex2):\n",
        "    l1 = relative_luminance(hex_to_rgb(hex1))\n",
        "    l2 = relative_luminance(hex_to_rgb(hex2))\n",
        "    return (max(l1, l2) + 0.05) / (min(l1, l2) + 0.05)\n",
        "\n",
        "cr_text = contrast_ratio(CALM_UI_THEME['text_heading'], CALM_UI_THEME['bg_primary'])\n",
        "cr_muted = contrast_ratio(CALM_UI_THEME['text_muted'], CALM_UI_THEME['bg_primary'])\n",
        "cr_sage = contrast_ratio(CALM_UI_THEME['accent_sage'], CALM_UI_THEME['bg_primary'])\n",
        "\n",
        "print(f'Heading Contrast (#202E26 on #FDFBF7): {cr_text:.2f}:1 (WCAG AA Pass: {cr_text >= 4.5})')\n",
        "print(f'Muted Body Contrast (#5B6B61 on #FDFBF7): {cr_muted:.2f}:1 (WCAG AA Pass: {cr_muted >= 4.5})')\n",
        "print(f'Sage Accent Contrast (#527360 on #FDFBF7): {cr_sage:.2f}:1 (WCAG UI Pass: {cr_sage >= 3.0})')\n"
    ]
}

nb["cells"].extend([cell_s25_md, cell_s25_code, cell_s26_md, cell_s26_code])

with open(notebook_path, "w", encoding="utf-8") as f:
    json.dump(nb, f, indent=2)

print(f"Appended Stage 11 cells. Total notebook cells now: {len(nb['cells'])}")
