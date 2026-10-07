"""
STAGE 6: MOOD AND FOOD FEATURE ENGINEERING
Project: MoodFood - Mood-Based Food Recommendation System
"""

import os
import csv
import re
from typing import Dict, List, Any

# Standard English stop words to filter from the content soup
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

def clean_tokens(text: str) -> str:
    """Removes non-alphanumeric characters, converts to lowercase, and filters stop words."""
    # Replace commas, slashes, and periods with spaces
    text = re.sub(r'[,/\\-]', ' ', text.lower())
    # Remove remaining punctuation
    text = re.sub(r'[^a-z0-9\s]', '', text)
    tokens = text.split()
    filtered = [t for t in tokens if t not in STOP_WORDS and len(t) > 1]
    return " ".join(filtered)

def construct_content_soup(row: Dict[str, Any]) -> str:
    """
    Constructs an engineered, weighted feature document (content soup) for each food.
    
    FEATURE WEIGHTING ARCHITECTURE:
    1. Mood Weight: Repeated 3x to give emotional resonance priority in TF-IDF.
    2. Category & Cuisine: Prefixed with domain tags (e.g. 'cuisine_italian', 'category_soup').
    3. Dietary Rule: 'diet_vegetarian' or 'diet_non_veg'
    4. Macro Nutritional Flags:
       - High Protein (>= 20g) -> 'high_protein_rich muscle_fuel'
       - Low Calorie (<= 300 kcal) -> 'light_meal low_calorie'
       - High Fiber (>= 7g) -> 'high_fiber_satiety gut_nourishing'
       - Low Sugar (<= 5g) -> 'low_glycemic steady_glucose'
    5. Raw Ingredients & Dietary Wellness Tags: Cleaned token stream.
    """
    mood_str = row["mood"].lower().replace(" ", "_")
    cuisine_str = f"cuisine_{row['cuisine'].lower()}"
    cat_str = f"category_{row['category'].lower()}"
    meal_str = f"meal_{row['meal_type'].lower()}"
    
    # 1. Weight mood 3x
    weighted_mood = f"mood_{mood_str} mood_{mood_str} mood_{mood_str} {mood_str} {mood_str}"
    
    # 2. Dietary flag
    veg_flag = "diet_vegetarian plant_based" if str(row["vegetarian"]) == "1" else "diet_non_veg animal_protein"
    
    # 3. Engineered Macro Flags
    cal = float(row["calories"])
    p = float(row["protein"])
    fib = float(row["fiber"])
    sug = float(row["sugar"])
    
    macro_flags = []
    if p >= 20.0:
        macro_flags.append("high_protein_rich muscle_fuel")
    elif p >= 12.0:
        macro_flags.append("balanced_protein")
        
    if cal <= 280.0:
        macro_flags.append("light_meal low_calorie light_energy")
    elif cal >= 450.0:
        macro_flags.append("hearty_substantial high_energy")
        
    if fib >= 7.0:
        macro_flags.append("high_fiber_satiety digestive_support")
        
    if sug <= 4.0:
        macro_flags.append("low_sugar steady_glucose")
        
    macro_str = " ".join(macro_flags)
    
    # 4. Clean ingredients and tags
    ing_clean = clean_tokens(row["ingredients"])
    tags_clean = clean_tokens(row["dietary_tags"])
    
    # 5. Assemble total soup
    soup_components = [
        weighted_mood,
        cuisine_str,
        cat_str,
        meal_str,
        veg_flag,
        macro_str,
        tags_clean,
        ing_clean
    ]
    
    full_soup = " ".join([c for c in soup_components if c])
    return full_soup

def run_feature_engineering_pipeline(
    input_filepath: str,
    output_filepath: str
) -> List[Dict[str, Any]]:
    """Reads cleaned dataset, creates engineered features, and exports updated CSV."""
    print(f"[STAGE 6] Reading cleaned data from: {input_filepath}")
    
    with open(input_filepath, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        fieldnames = list(reader.fieldnames)
        
    # Append new engineered columns
    new_fieldnames = fieldnames + ["content_soup", "protein_density_ratio"]
    
    enriched_rows = []
    
    for row in rows:
        # Calculate content soup
        soup = construct_content_soup(row)
        
        # Calculate engineered protein-to-calorie ratio (g protein per 100 kcal)
        cal = max(1.0, float(row["calories"]))
        p = float(row["protein"])
        p_density = round((p / cal) * 100, 2)
        
        row["content_soup"] = soup
        row["protein_density_ratio"] = p_density
        enriched_rows.append(row)
        
    # Write enriched dataset
    os.makedirs(os.path.dirname(os.path.abspath(output_filepath)), exist_ok=True)
    with open(output_filepath, mode="w", newline="", encoding="utf-8") as out_f:
        writer = csv.DictWriter(out_f, fieldnames=new_fieldnames)
        writer.writeheader()
        writer.writerows(enriched_rows)
        
    print(f"[STAGE 6] Enriched dataset written to: {output_filepath}")
    print(f"[STAGE 6] Total features: {len(new_fieldnames)} (Added 'content_soup', 'protein_density_ratio')")
    
    # Print sample soup
    sample = enriched_rows[0]
    print("\n--- SAMPLE ENGINEERED CONTENT SOUP ---")
    print(f"Food Name : {sample['food_name']}")
    print(f"Mood      : {sample['mood']}")
    print(f"Soup Text : {sample['content_soup']}")
    print("---------------------------------------\n")
    
    return enriched_rows

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    clean_csv = os.path.join(script_dir, "..", "data", "food_dataset_cleaned.csv")
    feat_csv = os.path.join(script_dir, "..", "data", "food_dataset_features.csv")
    
    run_feature_engineering_pipeline(clean_csv, feat_csv)
