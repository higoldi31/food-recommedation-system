import json
import os

notebook_path = os.path.join(os.path.dirname(__file__), "..", "notebook", "Mood_Based_Food_Recommendation.ipynb")
with open(notebook_path, "r", encoding="utf-8") as f:
    nb = json.load(f)

# Check if Section 16 is already present
has_s16 = any("16. Mood & Food Feature Engineering" in "".join(c.get("source", [])) for c in nb["cells"])

if not has_s16:
    markdown_cell = {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "---\n",
            "### 16. Mood & Food Feature Engineering (Stage 6)\n",
            "To prepare our foods for TF-IDF vector space modeling and cosine similarity, we cannot rely on raw columns independently. We engineer a weighted composite text feature called the **Content Soup**.\n",
            "\n",
            "#### Feature Weighting Architecture:\n",
            "1. **Mood Primacy (3x weight):** The user's emotional state is the primary intent. We repeat the mood token (`mood_stressed mood_stressed mood_stressed stressed stressed`) so its Term Frequency (TF) receives high initial weighting.\n",
            "2. **Domain Prefixing:** Cuisines, categories, and meal types are prefixed (`cuisine_mediterranean`, `category_soup`, `meal_dinner`) to avoid semantic collision with raw ingredient text.\n",
            "3. **Macro Flag Ingestion:** We convert continuous nutritional metrics into discrete semantic tokens (`high_protein_rich`, `light_meal`, `high_fiber_satiety`, `steady_glucose`) so the vectorizer can align user qualitative health goals.\n",
            "4. **Protein Density Ratio:** We calculate Protein Density = (Protein / Calories) * 100 as an engineered numerical feature."
        ]
    }

    code_cell = {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "import re\n",
            "\n",
            "def build_content_soup(row):\n",
            "    # 1. Cased mood token with 3x repetition\n",
            "    mood_slug = str(row['mood']).lower().replace(' ', '_')\n",
            "    mood_tokens = f\"mood_{mood_slug} mood_{mood_slug} mood_{mood_slug} {mood_slug} {mood_slug}\"\n",
            "    \n",
            "    # 2. Domain prefixes\n",
            "    cuisine_token = f\"cuisine_{str(row['cuisine']).lower()}\"\n",
            "    cat_token = f\"category_{str(row['category']).lower()}\"\n",
            "    meal_token = f\"meal_{str(row['meal_type']).lower()}\"\n",
            "    diet_token = \"diet_vegetarian plant_based\" if int(row['vegetarian']) == 1 else \"diet_non_veg animal_protein\"\n",
            "    \n",
            "    # 3. Macro nutritional tags\n",
            "    macro_flags = []\n",
            "    if float(row['protein']) >= 20.0:\n",
            "        macro_flags.append('high_protein_rich muscle_fuel')\n",
            "    elif float(row['protein']) >= 12.0:\n",
            "        macro_flags.append('balanced_protein')\n",
            "        \n",
            "    if float(row['calories']) <= 280:\n",
            "        macro_flags.append('light_meal low_calorie')\n",
            "    elif float(row['calories']) >= 450:\n",
            "        macro_flags.append('hearty_substantial high_energy')\n",
            "        \n",
            "    if float(row['fiber']) >= 7.0:\n",
            "        macro_flags.append('high_fiber_satiety digestive_support')\n",
            "        \n",
            "    if float(row['sugar']) <= 4.0:\n",
            "        macro_flags.append('low_sugar steady_glucose')\n",
            "        \n",
            "    macro_str = ' '.join(macro_flags)\n",
            "    \n",
            "    # 4. Cleaned ingredients and dietary tags\n",
            "    ing_clean = re.sub(r'[^a-zA-Z0-9\\s]', ' ', str(row['ingredients']).lower())\n",
            "    tags_clean = re.sub(r'[^a-zA-Z0-9\\s]', ' ', str(row['dietary_tags']).lower())\n",
            "    \n",
            "    # Combine all into content soup\n",
            "    soup = f\"{mood_tokens} {cuisine_token} {cat_token} {meal_token} {diet_token} {macro_str} {tags_clean} {ing_clean}\"\n",
            "    return ' '.join(soup.split())\n",
            "\n",
            "# Apply feature engineering\n",
            "df['content_soup'] = df.apply(build_content_soup, axis=1)\n",
            "df['protein_density_ratio'] = ((df['protein'] / df['calories']) * 100).round(2)\n",
            "\n",
            "# Export enriched feature dataset\n",
            "feat_export_path = os.path.join('..', 'data', 'food_dataset_features.csv')\n",
            "df.to_csv(feat_export_path, index=False)\n",
            "\n",
            "print(f\"Feature engineering complete! Enriched dataset exported to '{feat_export_path}'.\")\n",
            "print('\\nSample Content Soup (First Recipe):')\n",
            "print(df[['food_name', 'content_soup']].iloc[0].to_dict())\n"
        ]
    }

    nb["cells"].extend([markdown_cell, code_cell])

    with open(notebook_path, "w", encoding="utf-8") as f:
        json.dump(nb, f, indent=1)

    print("Appended Section 16 successfully!")
else:
    print("Section 16 already present.")
