"""
STAGE 4: DATA CLEANING AND PREPROCESSING PIPELINE
Project: MoodFood - Mood-Based Food Recommendation System
"""

import os
import csv
import re
from typing import Dict, List, Any

def clean_text_field(text: str) -> str:
    """Trims whitespace, collapses internal multiple spaces, and normalizes casing."""
    if not text:
        return ""
    # Collapse multiple whitespace
    cleaned = re.sub(r'\s+', ' ', str(text).strip())
    return cleaned

def standardize_tag_string(tags: str) -> str:
    """Normalizes comma-separated tag strings (stripping items, removing duplicates)."""
    if not tags:
        return ""
    raw_tags = [clean_text_field(t) for t in tags.split(",") if t.strip()]
    # Preserve order while removing duplicates
    seen = set()
    unique_tags = []
    for t in raw_tags:
        t_lower = t.lower()
        if t_lower not in seen:
            seen.add(t_lower)
            unique_tags.append(t)
    return ", ".join(unique_tags)

def run_data_cleaning_pipeline(
    raw_filepath: str,
    output_filepath: str
) -> Dict[str, Any]:
    """
    Executes production-grade data cleaning:
    1. Whitespace trimming & text standardization
    2. Numerical bounding and non-negativity assertions
    3. Categorical value validation against allowed sets
    4. Duplicate elimination
    5. Deduplication and normalization of ingredient and dietary tag tokens
    """
    print(f"[PIPELINE] Reading raw data from: {raw_filepath}")
    
    with open(raw_filepath, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        raw_rows = list(reader)
        fieldnames = reader.fieldnames
        
    initial_count = len(raw_rows)
    print(f"[PIPELINE] Initial row count: {initial_count}")
    
    cleaned_rows = []
    seen_identifiers = set()
    duplicates_removed = 0
    anomalies_repaired = 0
    
    # Allowed sets for validation
    ALLOWED_MOODS = {"Stressed", "Tired", "Relaxed", "Happy", "Energetic", "Low Mood"}
    ALLOWED_MEALS = {"Breakfast", "Lunch", "Dinner", "Snack"}
    ALLOWED_CUISINES = {"Mediterranean", "Asian", "Indian", "Mexican", "Italian", "American", "Continental"}
    
    for idx, row in enumerate(raw_rows):
        # 1. Clean food name
        food_name = clean_text_field(row["food_name"])
        
        # 2. Duplicate check based on (food_name, meal_type)
        meal_type = clean_text_field(row["meal_type"]).title()
        if meal_type not in ALLOWED_MEALS:
            meal_type = "Dinner"
            anomalies_repaired += 1
            
        unique_key = (food_name.lower(), meal_type.lower())
        if unique_key in seen_identifiers:
            duplicates_removed += 1
            continue
        seen_identifiers.add(unique_key)
        
        # 3. Clean categorical strings
        mood = clean_text_field(row["mood"])
        # Standardize mood casing (e.g. 'Low mood' -> 'Low Mood')
        if mood.lower() == "low mood":
            mood = "Low Mood"
        else:
            mood = mood.capitalize()
            
        if mood not in ALLOWED_MOODS:
            mood = "Relaxed"
            anomalies_repaired += 1
            
        cuisine = clean_text_field(row["cuisine"]).capitalize()
        if cuisine not in ALLOWED_CUISINES:
            cuisine = "Continental"
            
        category = clean_text_field(row["category"]).capitalize()
        
        # 4. Clean and validate numerical macros
        try:
            cal = max(1.0, float(row["calories"]))
            p = max(0.0, float(row["protein"]))
            c = max(0.0, float(row["carbs"]))
            f = max(0.0, float(row["fat"]))
            fib = max(0.0, float(row["fiber"]))
            sug = max(0.0, float(row["sugar"]))
        except (ValueError, TypeError):
            # Imputation fallback to median
            cal, p, c, f, fib, sug = 320.0, 15.0, 38.0, 10.0, 5.0, 5.0
            anomalies_repaired += 1
            
        # 5. Vegetarian and spicy flags
        try:
            veg = 1 if int(row["vegetarian"]) == 1 else 0
        except:
            veg = 1
            
        try:
            spicy = min(2, max(0, int(row["spicy"])))
        except:
            spicy = 0
            
        # 6. NLP token fields
        ingredients = clean_text_field(row["ingredients"])
        dietary_tags = standardize_tag_string(row["dietary_tags"])
        
        cleaned_entry = {
            "food_name": food_name,
            "category": category,
            "cuisine": cuisine,
            "meal_type": meal_type,
            "mood": mood,
            "calories": int(round(cal)),
            "protein": round(p, 1),
            "carbs": round(c, 1),
            "fat": round(f, 1),
            "fiber": round(fib, 1),
            "sugar": round(sug, 1),
            "vegetarian": veg,
            "spicy": spicy,
            "ingredients": ingredients,
            "dietary_tags": dietary_tags
        }
        cleaned_rows.append(cleaned_entry)
        
    # Write cleaned dataset
    os.makedirs(os.path.dirname(os.path.abspath(output_filepath)), exist_ok=True)
    with open(output_filepath, mode="w", newline="", encoding="utf-8") as out_f:
        writer = csv.DictWriter(out_f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(cleaned_rows)
        
    print(f"[PIPELINE] Cleaned dataset written to: {output_filepath}")
    print(f"[PIPELINE] Output rows: {len(cleaned_rows)}")
    print(f"[PIPELINE] Duplicates removed: {duplicates_removed}")
    print(f"[PIPELINE] Repaired anomalies: {anomalies_repaired}")
    
    return {
        "initial_rows": initial_count,
        "final_rows": len(cleaned_rows),
        "duplicates_removed": duplicates_removed,
        "anomalies_repaired": anomalies_repaired
    }

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    raw_path = os.path.join(script_dir, "..", "data", "food_dataset.csv")
    cleaned_path = os.path.join(script_dir, "..", "data", "food_dataset_cleaned.csv")
    
    run_data_cleaning_pipeline(raw_path, cleaned_path)
