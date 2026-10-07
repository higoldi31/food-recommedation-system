"""
=============================================================================
STAGE 2: PROGRAMMATIC BIOCHEMICAL MOOD-MAPPING DATASET GENERATOR
Project: MoodFood - Mood-Based Food Recommendation System
=============================================================================
This script generates 320 diverse food items using a dedicated function:
`map_food_to_mood()`
which inspects the food's nutritional composition, ingredients, and tags to
assign the appropriate mood based on nutritional biochemistry principles.
=============================================================================
"""

import os
import csv
from typing import Dict, List, Any


def map_food_to_mood(
    food_name: str,
    ingredients: str,
    dietary_tags: str,
    category: str,
    calories: float,
    protein: float,
    carbs: float,
    fat: float,
    fiber: float,
    sugar: float
) -> str:
    """
    Predefined heuristic mapping function assigning mood based on nutritional biochemistry.
    
    HEURISTIC RULES:
    1. STRESSED:
       - Target Micronutrients: Magnesium, Omega-3 fatty acids, L-theanine.
       - Physiological Target: Downregulation of HPA-axis (cortisol) and muscle tension.
       - Ingredient Cues: Lentils, spinach, pumpkin seeds, salmon, chamomile, walnuts, oats.
    
    2. TIRED (FATIGUE):
       - Target Micronutrients: Bioavailable Iron, B-complex vitamins, clean sustained protein.
       - Physiological Target: Mitochondrial ATP respiration without reactive hypoglycemia.
       - Ingredient Cues: Quinoa, eggs, beans, sprouted legumes, edamame, matcha.
    
    3. RELAXED:
       - Target Micronutrients: Dietary Tryptophan (serotonin -> melatonin precursor), calcium.
       - Physiological Target: Parasympathetic nervous stimulation, low evening digestive load.
       - Ingredient Cues: Chamomile, cod, pumpkin, jasmine rice, lavender, peppermint.
    
    4. HAPPY:
       - Target Micronutrients: Flavonoids, phenylethylamine, dopamine-supportive nutrients.
       - Physiological Target: Sensory enjoyment, endorphin response, colorful social dining.
       - Ingredient Cues: Dark chocolate, berries, mango, artisan sourdough, mozzarella.
    
    5. ENERGETIC:
       - Target Micronutrients: High-BV protein, potassium/electrolytes, dietary nitrates.
       - Physiological Target: Muscle glycogen readiness, cellular hydration, sustained stamina.
       - Ingredient Cues: Banana, peanut butter, beetroot, lean poultry, Greek yogurt, coconut water.
    
    6. LOW MOOD:
       - Target Micronutrients: Probiotic cultures (gut-brain axis), folate, zinc.
       - Physiological Target: Neuro-inflammatory regulation and gentle, steady glycemic comfort.
       - Ingredient Cues: Fermented yogurt/curd, warm broths, ginger, sweet potato, lentils.
    """
    text_corpus = f"{food_name} {ingredients} {dietary_tags} {category}".lower()
    
    # 1. Stress Heuristic: Magnesium, Omega-3s, and soothing herbal compounds
    stress_cues = ["magnesium", "spinach", "lentil", "salmon", "pumpkin seed", "walnut", "oatmeal", "chamomile", "anti-stress"]
    stress_score = sum(2 for cue in stress_cues if cue in text_corpus)
    if "magnesium" in text_corpus or "omega-3" in text_corpus:
        stress_score += 3
        
    # 2. Tired / Fatigue Heuristic: Iron, B-Vitamins, clean endurance fuel
    tired_cues = ["iron", "b-vitamin", "quinoa", "sprout", "egg", "matcha", "burrito", "avocado wrap", "black bean"]
    tired_score = sum(2 for cue in tired_cues if cue in text_corpus)
    if protein >= 18.0 and fiber >= 7.0 and "pre-workout" not in text_corpus:
        tired_score += 2

    # 3. Relaxation Heuristic: Tryptophan, light evening digestion, gentle herbs
    relaxed_cues = ["tryptophan", "peppermint", "lavender", "pumpkin soup", "cod", "jasmine rice", "gentle", "soothing-aromas"]
    relaxed_score = sum(2 for cue in relaxed_cues if cue in text_corpus)
    if "tryptophan" in text_corpus or "sleep" in text_corpus or (fat <= 16.0 and "dinner" in text_corpus and "spicy" not in text_corpus):
        relaxed_score += 2

    # 4. Happy Heuristic: Flavonoid antioxidants, social meals, dark chocolate
    happy_cues = ["dark chocolate", "strawberry", "flatbread", "pizza", "mezze", "biryani", "acai", "taco", "celebration"]
    happy_score = sum(2 for cue in happy_cues if cue in text_corpus)
    if "antioxidant" in text_corpus or "social" in text_corpus or "chocolate" in text_corpus:
        happy_score += 3

    # 5. Energetic Heuristic: High protein density, potassium, nitrates, pre-workout
    energetic_cues = ["pre-workout", "protein bowl", "nitrate", "beetroot", "banana", "peanut butter", "smoothie", "electrolyte", "coconut water"]
    energetic_score = sum(2 for cue in energetic_cues if cue in text_corpus)
    if protein >= 25.0 or "nitrate" in text_corpus or "electrolyte" in text_corpus:
        energetic_score += 3

    # 6. Low Mood Heuristic: Gut-Brain axis probiotics, warm broths, comforting nostalgic grains
    low_mood_cues = ["curd", "probiotic", "ginger broth", "noodle soup", "sweet potato mash", "cannellini", "comforting", "restorative", "gut-brain"]
    low_mood_score = sum(2 for cue in low_mood_cues if cue in text_corpus)
    if "probiotic" in text_corpus or "broth" in text_corpus or "restorative" in text_corpus:
        low_mood_score += 3

    scores = {
        "Stressed": stress_score,
        "Tired": tired_score,
        "Relaxed": relaxed_score,
        "Happy": happy_score,
        "Energetic": energetic_score,
        "Low Mood": low_mood_score
    }
    
    # Return the mood with the highest biochemical score
    assigned_mood = max(scores, key=scores.get)
    
    # Fallback to balanced defaults if scores tie at 0
    if scores[assigned_mood] == 0:
        if protein >= 20.0:
            return "Energetic"
        elif calories <= 300:
            return "Relaxed"
        else:
            return "Happy"
            
    return assigned_mood


def build_raw_recipe_pool() -> List[Dict[str, Any]]:
    """
    Compiles 64 core recipe prototypes across cuisines, categories, and nutrient ranges
    which will have moods programmatically computed by map_food_to_mood().
    """
    recipes = [
        # --- Soups & Broths ---
        {"food_name": "Warm Lentil & Baby Spinach Soup", "category": "Soup", "cuisine": "Mediterranean", "meal_type": "Dinner", "calories": 340, "protein": 18.0, "carbs": 46.0, "fat": 7.0, "fiber": 11.0, "sugar": 4.0, "vegetarian": 1, "spicy": 0, "ingredients": "Brown lentils, baby spinach, minced garlic, extra virgin olive oil, lemon, cumin", "dietary_tags": "High-Fiber, Magnesium, Vegan, Anti-Stress"},
        {"food_name": "Ginger Simmered Chicken Broth with Rice", "category": "Soup", "cuisine": "Asian", "meal_type": "Dinner", "calories": 340, "protein": 26.0, "carbs": 38.0, "fat": 8.0, "fiber": 3.0, "sugar": 2.0, "vegetarian": 0, "spicy": 0, "ingredients": "Poached chicken breast, white jasmine rice, sliced young ginger, scallions", "dietary_tags": "Restorative, Broth, Gut-Friendly, Gluten-Free"},
        {"food_name": "Creamy Roasted Pumpkin Soup with Pepitas", "category": "Soup", "cuisine": "Continental", "meal_type": "Dinner", "calories": 280, "protein": 6.0, "carbs": 38.0, "fat": 11.0, "fiber": 6.0, "sugar": 8.0, "vegetarian": 1, "spicy": 0, "ingredients": "Roasted sugar pumpkin, light coconut milk, pumpkin seed pepitas, nutmeg", "dietary_tags": "Tryptophan, Soothing, Vegan, Gluten-Free"},
        {"food_name": "Homestyle Garden Vegetable Noodle Soup", "category": "Soup", "cuisine": "American", "meal_type": "Lunch", "calories": 260, "protein": 8.0, "carbs": 44.0, "fat": 5.0, "fiber": 5.0, "sugar": 4.0, "vegetarian": 1, "spicy": 0, "ingredients": "Whole-wheat ribbon noodles, diced carrots, celery, fragrant herb vegetable broth", "dietary_tags": "Noodle Soup, Restorative, Warm-Comfort, Vegetarian"},
        {"food_name": "Fermented Miso Soup with Silken Tofu & Wakame", "category": "Soup", "cuisine": "Asian", "meal_type": "Lunch", "calories": 140, "protein": 9.0, "carbs": 12.0, "fat": 4.0, "fiber": 3.0, "sugar": 2.0, "vegetarian": 1, "spicy": 0, "ingredients": "Naturally fermented white miso, silken tofu cubes, wakame seaweed, spring green onions", "dietary_tags": "Probiotic, Gut-Health, Low-Calorie, Vegan"},
        {"food_name": "Tuscan White Bean & Tomato Minestrone", "category": "Soup", "cuisine": "Italian", "meal_type": "Dinner", "calories": 310, "protein": 14.0, "carbs": 50.0, "fat": 6.0, "fiber": 10.0, "sugar": 5.0, "vegetarian": 1, "spicy": 0, "ingredients": "Cannellini beans, stewed plum tomatoes, zucchini, whole grain ditalini pasta, basil", "dietary_tags": "Cannellini, High-Fiber, Soothing, Mediterranean-Diet, Vegan"},
        {"food_name": "Spiced Black Bean Soup with Crispy Tortillas", "category": "Soup", "cuisine": "Mexican", "meal_type": "Lunch", "calories": 330, "protein": 17.0, "carbs": 52.0, "fat": 6.0, "fiber": 14.0, "sugar": 3.0, "vegetarian": 1, "spicy": 1, "ingredients": "Simmered black beans, cumin, Mexican oregano, baked corn tortilla crisps, cilantro", "dietary_tags": "Black Bean, Iron, High-Fiber, Vegan, Gluten-Free"},
        {"food_name": "Silken Tofu & Enoki Mushroom Dashi", "category": "Soup", "cuisine": "Asian", "meal_type": "Dinner", "calories": 170, "protein": 14.0, "carbs": 12.0, "fat": 5.0, "fiber": 3.0, "sugar": 2.0, "vegetarian": 1, "spicy": 0, "ingredients": "Silken tofu, enoki mushrooms, kombu vegetable dashi broth, scallions", "dietary_tags": "Gentle, Calming, Tryptophan, Ultra-Light, Vegan"},

        # --- Power Bowls & Grains ---
        {"food_name": "Quinoa & Black Bean Burrito Power Bowl", "category": "Bowl", "cuisine": "Mexican", "meal_type": "Lunch", "calories": 460, "protein": 18.0, "carbs": 70.0, "fat": 11.0, "fiber": 15.0, "sugar": 4.0, "vegetarian": 1, "spicy": 1, "ingredients": "White quinoa, spiced simmered black beans, roasted corn, guacamole, salsa verde", "dietary_tags": "Burrito, Iron, Sustained-Energy, High-Fiber, Vegan"},
        {"food_name": "Roasted Sweet Potato & Black Bean Bowl", "category": "Bowl", "cuisine": "Mexican", "meal_type": "Lunch", "calories": 420, "protein": 14.0, "carbs": 68.0, "fat": 9.0, "fiber": 14.0, "sugar": 9.0, "vegetarian": 1, "spicy": 1, "ingredients": "Garnet sweet potatoes, black beans, sweet corn, cilantro, lime vinaigrette", "dietary_tags": "Magnesium, Complex-Carbs, Vegan, Gluten-Free"},
        {"food_name": "Grilled Lemon Herb Chicken & Quinoa Power Bowl", "category": "Bowl", "cuisine": "American", "meal_type": "Lunch", "calories": 480, "protein": 46.0, "carbs": 46.0, "fat": 12.0, "fiber": 7.0, "sugar": 3.0, "vegetarian": 0, "spicy": 0, "ingredients": "Grilled chicken breast, Andean tricolor quinoa, massaged kale, avocado, lemon tahini", "dietary_tags": "Protein Bowl, Pre-Workout, High-Protein, Lean-Muscle"},
        {"food_name": "South Indian Tempered Curd Rice with Pomegranate", "category": "Bowl", "cuisine": "Indian", "meal_type": "Lunch", "calories": 310, "protein": 9.0, "carbs": 52.0, "fat": 7.0, "fiber": 3.0, "sugar": 6.0, "vegetarian": 1, "spicy": 0, "ingredients": "Cooked basmati rice, probiotic whole curd yogurt, mustard seeds, curry leaves, pomegranate", "dietary_tags": "Curd, Probiotic, Gut-Brain, Ayurvedic, Vegetarian"},
        {"food_name": "Chamomile Steamed Tofu & Brown Jasmine Rice", "category": "Bowl", "cuisine": "Asian", "meal_type": "Dinner", "calories": 390, "protein": 21.0, "carbs": 49.0, "fat": 9.0, "fiber": 6.0, "sugar": 2.0, "vegetarian": 1, "spicy": 0, "ingredients": "Firm tofu cubes, brown jasmine rice, chamomile herbal broth, baby bok choy, sesame oil", "dietary_tags": "Chamomile, Calming, Magnesium, Plant-Protein, Vegan"},
        {"food_name": "Fragrant Jasmine Rice with Steamed Sesame Greens", "category": "Bowl", "cuisine": "Asian", "meal_type": "Dinner", "calories": 340, "protein": 8.0, "carbs": 62.0, "fat": 6.0, "fiber": 5.0, "sugar": 3.0, "vegetarian": 1, "spicy": 0, "ingredients": "Thai jasmine rice, baby bok choy, sugar snap peas, cold-pressed sesame oil", "dietary_tags": "Jasmine Rice, Gentle, Easy-Digestion, Tryptophan, Vegan"},
        {"food_name": "Buckwheat Soba & Edamame Protein Bowl", "category": "Bowl", "cuisine": "Asian", "meal_type": "Lunch", "calories": 420, "protein": 20.0, "carbs": 62.0, "fat": 10.0, "fiber": 8.0, "sugar": 5.0, "vegetarian": 1, "spicy": 0, "ingredients": "100% buckwheat soba noodles, steamed edamame, purple cabbage, sesame ginger vinaigrette", "dietary_tags": "Protein Bowl, Pre-Workout, Clean-Carbs, Vegan"},

        # --- Curries & Mains ---
        {"food_name": "Spinach & Moong Dal Khichdi with Ghee", "category": "Curry", "cuisine": "Indian", "meal_type": "Dinner", "calories": 360, "protein": 15.0, "carbs": 54.0, "fat": 8.0, "fiber": 8.0, "sugar": 2.0, "vegetarian": 1, "spicy": 0, "ingredients": "Yellow moong lentils, basmati rice, fresh spinach, turmeric, cumin seeds, pure cow ghee", "dietary_tags": "Spinach, Lentil, Magnesium, Ayurvedic-Comfort, Soothing"},
        {"food_name": "Homestyle Yellow Toor Dal with Cumin Rice", "category": "Curry", "cuisine": "Indian", "meal_type": "Dinner", "calories": 380, "protein": 14.0, "carbs": 60.0, "fat": 7.0, "fiber": 9.0, "sugar": 3.0, "vegetarian": 1, "spicy": 0, "ingredients": "Yellow toor dal lentils, steamed basmati rice, toasted cumin, mild turmeric, ripe tomato", "dietary_tags": "Lentil, Traditional-Comfort, Tryptophan, Gentle, Vegan"},
        {"food_name": "Iron-Rich Palak Paneer with Whole Wheat Roti", "category": "Curry", "cuisine": "Indian", "meal_type": "Dinner", "calories": 420, "protein": 20.0, "carbs": 38.0, "fat": 22.0, "fiber": 7.0, "sugar": 4.0, "vegetarian": 1, "spicy": 1, "ingredients": "Fresh spinach puree, paneer cheese, whole wheat flour roti, garlic, garam masala", "dietary_tags": "Iron, B-Vitamin, High-Protein, Vegetarian"},
        {"food_name": "Wild Atlantic Salmon with Steamed Asparagus", "category": "Main", "cuisine": "Continental", "meal_type": "Dinner", "calories": 480, "protein": 38.0, "carbs": 12.0, "fat": 26.0, "fiber": 5.0, "sugar": 2.0, "vegetarian": 0, "spicy": 0, "ingredients": "Wild salmon fillet, green asparagus spears, virgin olive oil, lemon zest, sea salt", "dietary_tags": "Salmon, Omega-3, Magnesium, High-Protein, Gluten-Free"},
        {"food_name": "Herbal Baked Atlantic Cod with Zucchini", "category": "Main", "cuisine": "Mediterranean", "meal_type": "Dinner", "calories": 360, "protein": 36.0, "carbs": 14.0, "fat": 16.0, "fiber": 4.0, "sugar": 4.0, "vegetarian": 0, "spicy": 0, "ingredients": "Cod fillet, tender zucchini ribbons, fresh dill, virgin olive oil, garlic", "dietary_tags": "Cod, Tryptophan, Gentle, Light-Dinner, High-Protein"},
        {"food_name": "Grilled Lemon Herb Chicken with Brown Rice", "category": "Main", "cuisine": "American", "meal_type": "Dinner", "calories": 490, "protein": 46.0, "carbs": 48.0, "fat": 10.0, "fiber": 7.0, "sugar": 3.0, "vegetarian": 0, "spicy": 0, "ingredients": "Skinless chicken breast, steamed brown basmati rice, steamed fresh broccoli, olive oil", "dietary_tags": "High-Protein, Pre-Workout, Clean-Fuel, Gluten-Free"},
        {"food_name": "Grilled Pacific Shrimp with Lemon Herb Quinoa", "category": "Main", "cuisine": "Mediterranean", "meal_type": "Dinner", "calories": 390, "protein": 34.0, "carbs": 38.0, "fat": 10.0, "fiber": 5.0, "sugar": 2.0, "vegetarian": 0, "spicy": 0, "ingredients": "Wild white shrimp, tri-color quinoa, Italian flat-leaf parsley, lemon zest, olive oil", "dietary_tags": "Pre-Workout, High-Protein, Lean, Gluten-Free"},
        {"food_name": "Artisanal Margherita Sourdough Flatbread", "category": "Main", "cuisine": "Italian", "meal_type": "Lunch", "calories": 460, "protein": 18.0, "carbs": 56.0, "fat": 18.0, "fiber": 4.0, "sugar": 5.0, "vegetarian": 1, "spicy": 0, "ingredients": "San Marzano plum tomatoes, fresh buffalo mozzarella, sweet basil, sourdough olive crust", "dietary_tags": "Flatbread, Pizza, Social, Sensory-Joy, Vegetarian"},
        {"food_name": "Mediterranean Mezze Platter with Baked Falafel", "category": "Main", "cuisine": "Mediterranean", "meal_type": "Lunch", "calories": 490, "protein": 16.0, "carbs": 58.0, "fat": 22.0, "fiber": 12.0, "sugar": 6.0, "vegetarian": 1, "spicy": 0, "ingredients": "Baked chickpea falafel, velvety hummus, kalamata olives, diced cucumbers, warm pita", "dietary_tags": "Mezze, Social, High-Fiber, Vegan"},
        {"food_name": "Vegetable Dum Biryani with Cool Mint Raita", "category": "Main", "cuisine": "Indian", "meal_type": "Lunch", "calories": 480, "protein": 13.0, "carbs": 72.0, "fat": 14.0, "fiber": 7.0, "sugar": 5.0, "vegetarian": 1, "spicy": 1, "ingredients": "Aged basmati rice, green beans, carrots, saffron threads, fresh mint, cucumber raita", "dietary_tags": "Biryani, Celebration, Social, Aromatic, Vegetarian"},
        {"food_name": "Baja Grilled White Fish Tacos with Purple Slaw", "category": "Main", "cuisine": "Mexican", "meal_type": "Lunch", "calories": 440, "protein": 28.0, "carbs": 42.0, "fat": 16.0, "fiber": 6.0, "sugar": 4.0, "vegetarian": 0, "spicy": 1, "ingredients": "Grilled cod, stoneground corn tortillas, shaved purple cabbage, avocado crema, lime", "dietary_tags": "Taco, Social, Lean-Protein, Gluten-Free"},
        {"food_name": "Tandoori Paneer Tikka with Mint Chutney", "category": "Main", "cuisine": "Indian", "meal_type": "Dinner", "calories": 410, "protein": 24.0, "carbs": 14.0, "fat": 28.0, "fiber": 3.0, "sugar": 4.0, "vegetarian": 1, "spicy": 1, "ingredients": "Marinated paneer cheese blocks, Kashmiri chili, chickpea flour, lemon, green mint dip", "dietary_tags": "Social, High-Protein, Vegetarian, Gluten-Free"},

        # --- Breakfast Items ---
        {"food_name": "Oatmeal with Blueberries & Pumpkin Seeds", "category": "Breakfast", "cuisine": "American", "meal_type": "Breakfast", "calories": 320, "protein": 11.0, "carbs": 48.0, "fat": 9.0, "fiber": 8.0, "sugar": 10.0, "vegetarian": 1, "spicy": 0, "ingredients": "Rolled whole oats, wild blueberries, raw pumpkin seeds, almond milk, Ceylon cinnamon", "dietary_tags": "Oatmeal, Pumpkin Seed, Magnesium, Antioxidant, Vegan"},
        {"food_name": "Banana Almond Butter High-Protein Oatmeal", "category": "Breakfast", "cuisine": "American", "meal_type": "Breakfast", "calories": 410, "protein": 22.0, "carbs": 56.0, "fat": 13.0, "fiber": 8.0, "sugar": 16.0, "vegetarian": 1, "spicy": 0, "ingredients": "Rolled oats, plant protein isolate, ripe banana, natural almond butter, cinnamon", "dietary_tags": "Banana, Peanut Butter, Pre-Workout, Protein Bowl, Vegan"},
        {"food_name": "Egg & Avocado Sprouted Whole-Grain Wrap", "category": "Breakfast", "cuisine": "American", "meal_type": "Breakfast", "calories": 390, "protein": 20.0, "carbs": 36.0, "fat": 18.0, "fiber": 7.0, "sugar": 3.0, "vegetarian": 1, "spicy": 0, "ingredients": "Scrambled pasture eggs, sprouted tortilla, fresh avocado slices, baby spinach", "dietary_tags": "Avocado Wrap, Egg, B-Vitamin, Clean-Protein, Vegetarian"},
        {"food_name": "Avocado Sourdough Toast with Raw Hemp Hearts", "category": "Breakfast", "cuisine": "Continental", "meal_type": "Breakfast", "calories": 330, "protein": 9.0, "carbs": 34.0, "fat": 18.0, "fiber": 9.0, "sugar": 2.0, "vegetarian": 1, "spicy": 0, "ingredients": "Artisan sourdough bread, mashed Hass avocado, raw hemp seeds, lemon juice, sea salt", "dietary_tags": "Magnesium, Healthy-Fats, High-Fiber, Vegan"},
        {"food_name": "Greek Yogurt Parfait with Granola & Chia Seeds", "category": "Breakfast", "cuisine": "Mediterranean", "meal_type": "Breakfast", "calories": 340, "protein": 24.0, "carbs": 42.0, "fat": 9.0, "fiber": 5.0, "sugar": 14.0, "vegetarian": 1, "spicy": 0, "ingredients": "Nonfat strained Greek yogurt, artisan oat granola, black chia seeds, fresh blackberries", "dietary_tags": "Pre-Workout, High-Protein, Vegetarian, Calcium-Rich"},
        {"food_name": "Rainbow Acai Superfruit Breakfast Bowl", "category": "Breakfast", "cuisine": "American", "meal_type": "Breakfast", "calories": 360, "protein": 8.0, "carbs": 62.0, "fat": 10.0, "fiber": 9.0, "sugar": 26.0, "vegetarian": 1, "spicy": 0, "ingredients": "Acai berry puree, ripe banana, golden kiwi slices, wild blueberries, black chia seeds", "dietary_tags": "Acai, Antioxidant, Colorful, Vegan, Flavonoid"},
        {"food_name": "Hard Boiled Pasture Eggs with Everything Spice", "category": "Breakfast", "cuisine": "American", "meal_type": "Breakfast", "calories": 150, "protein": 13.0, "carbs": 2.0, "fat": 10.0, "fiber": 1.0, "sugar": 1.0, "vegetarian": 1, "spicy": 0, "ingredients": "Two large pasture-raised eggs, poppy seeds, toasted sesame, garlic flakes, sea salt", "dietary_tags": "Egg, Iron, High-Protein, Zero-Sugar, Vegetarian"},
        {"food_name": "Warm Steel-Cut Oats with Stewed Gala Apples", "category": "Breakfast", "cuisine": "American", "meal_type": "Breakfast", "calories": 340, "protein": 9.0, "carbs": 54.0, "fat": 11.0, "fiber": 7.0, "sugar": 14.0, "vegetarian": 1, "spicy": 0, "ingredients": "Steel-cut oats, cinnamon-stewed Gala apples, crushed raw walnuts, pure maple touch", "dietary_tags": "Oatmeal, Walnut, Comforting, Serotonin-Support, Vegan"},
        {"food_name": "Whipped Ricotta Toast on Sourdough with Honey", "category": "Breakfast", "cuisine": "Italian", "meal_type": "Breakfast", "calories": 290, "protein": 12.0, "carbs": 38.0, "fat": 10.0, "fiber": 3.0, "sugar": 12.0, "vegetarian": 1, "spicy": 0, "ingredients": "Country sourdough bread, whipped whole milk ricotta cheese, clover honey, sea salt", "dietary_tags": "Tryptophan, Comforting, Vegetarian"},

        # --- Salads ---
        {"food_name": "Sprouted Moong Lentil Salad with Pomegranate", "category": "Salad", "cuisine": "Indian", "meal_type": "Lunch", "calories": 270, "protein": 14.0, "carbs": 42.0, "fat": 4.0, "fiber": 10.0, "sugar": 12.0, "vegetarian": 1, "spicy": 0, "ingredients": "Sprouted green moong beans, ruby pomegranate arils, shredded carrots, lime juice", "dietary_tags": "Sprout, Iron, Raw-Enzymes, Vegan, Gluten-Free"},
        {"food_name": "Roasted Beetroot, Walnut & Goat Cheese Salad", "category": "Salad", "cuisine": "Mediterranean", "meal_type": "Lunch", "calories": 340, "protein": 11.0, "carbs": 28.0, "fat": 20.0, "fiber": 6.0, "sugar": 16.0, "vegetarian": 1, "spicy": 0, "ingredients": "Roasted red beets, baby arugula, toasted walnuts, creamy goat cheese, aged balsamic", "dietary_tags": "Beetroot, Nitrate, Walnut, Magnesium, Vegetarian"},
        {"food_name": "Crispy Spiced Chickpea & Tuscan Kale Salad", "category": "Salad", "cuisine": "Mediterranean", "meal_type": "Lunch", "calories": 360, "protein": 16.0, "carbs": 44.0, "fat": 14.0, "fiber": 11.0, "sugar": 4.0, "vegetarian": 1, "spicy": 1, "ingredients": "Paprika roasted chickpeas, chopped lacinato kale, tahini lemon dressing, sunflower seeds", "dietary_tags": "Iron, Pre-Workout, Protein Bowl, Vegan"},
        {"food_name": "Italian Caprese Salad with Buffalo Mozzarella", "category": "Salad", "cuisine": "Italian", "meal_type": "Lunch", "calories": 310, "protein": 16.0, "carbs": 8.0, "fat": 24.0, "fiber": 2.0, "sugar": 5.0, "vegetarian": 1, "spicy": 0, "ingredients": "Vine heirloom tomatoes, fresh water buffalo mozzarella, sweet basil, balsamic glaze", "dietary_tags": "Social, Fresh-Simplicity, High-Calcium, Vegetarian"},

        # --- Beverages & Snacks ---
        {"food_name": "Golden Turmeric Spiced Warm Almond Milk", "category": "Beverage", "cuisine": "Indian", "meal_type": "Snack", "calories": 160, "protein": 6.0, "carbs": 16.0, "fat": 7.0, "fiber": 1.0, "sugar": 12.0, "vegetarian": 1, "spicy": 0, "ingredients": "Almond milk, ground turmeric root, black pepper, cinnamon, raw honey, cardamom", "dietary_tags": "Anti-Stress, Calming, Anti-Inflammatory, Vegetarian"},
        {"food_name": "Organic Chamomile Peppermint Herbal Infusion", "category": "Beverage", "cuisine": "Continental", "meal_type": "Snack", "calories": 10, "protein": 0.0, "carbs": 2.0, "fat": 0.0, "fiber": 0.0, "sugar": 0.0, "vegetarian": 1, "spicy": 0, "ingredients": "Whole dried chamomile flower heads, crushed spearmint and peppermint leaves, pure water", "dietary_tags": "Chamomile, Peppermint, Soothing, Caffeine-Free, Vegan"},
        {"food_name": "Ceremonial Matcha Oat Milk Green Tea Latte", "category": "Beverage", "cuisine": "Asian", "meal_type": "Snack", "calories": 180, "protein": 4.0, "carbs": 26.0, "fat": 6.0, "fiber": 3.0, "sugar": 12.0, "vegetarian": 1, "spicy": 0, "ingredients": "Ceremonial Japanese matcha, barista oat milk, organic blue agave, vanilla extract", "dietary_tags": "Matcha, Iron, Sustained-Focus, Vegan"},
        {"food_name": "Raw Beetroot, Ginger & Orange Performance Juice", "category": "Beverage", "cuisine": "Continental", "meal_type": "Snack", "calories": 190, "protein": 4.0, "carbs": 42.0, "fat": 1.0, "fiber": 5.0, "sugar": 28.0, "vegetarian": 1, "spicy": 0, "ingredients": "Cold-pressed red beet juice, Valencia orange juice, tender coconut water, fresh ginger", "dietary_tags": "Beetroot, Nitrate, Electrolyte, Pre-Workout, Vegan"},
        {"food_name": "Natural Tender Coconut Water with Fresh Lime", "category": "Beverage", "cuisine": "Asian", "meal_type": "Snack", "calories": 60, "protein": 1.0, "carbs": 14.0, "fat": 0.0, "fiber": 1.0, "sugar": 11.0, "vegetarian": 1, "spicy": 0, "ingredients": "Raw tender green coconut water, Persian lime juice, Himalayan pink salt pinch", "dietary_tags": "Coconut Water, Electrolyte, Hydrating, Potassium, Vegan"},
        {"food_name": "Sparkling Wild Raspberry Garden Mint Spritzer", "category": "Beverage", "cuisine": "Continental", "meal_type": "Snack", "calories": 70, "protein": 1.0, "carbs": 18.0, "fat": 0.0, "fiber": 3.0, "sugar": 13.0, "vegetarian": 1, "spicy": 0, "ingredients": "Sparkling mineral water, muddled red raspberries, fresh garden mint, lime splash", "dietary_tags": "Berry, Social, Refreshing, Flavonoid, Vegan"},
        {"food_name": "Caffeine-Free Rooibos Chai with Steamed Oat Milk", "category": "Beverage", "cuisine": "Indian", "meal_type": "Snack", "calories": 140, "protein": 3.0, "carbs": 22.0, "fat": 4.0, "fiber": 1.0, "sugar": 14.0, "vegetarian": 1, "spicy": 0, "ingredients": "Red rooibos tea, oat milk, crushed green cardamom pods, cinnamon, clove, honey", "dietary_tags": "Soothing-Aromas, Calming, Tryptophan, Vegetarian"},
        {"food_name": "Fresh Organic Strawberries in 72% Dark Chocolate", "category": "Dessert", "cuisine": "Continental", "meal_type": "Snack", "calories": 190, "protein": 3.0, "carbs": 26.0, "fat": 10.0, "fiber": 4.0, "sugar": 18.0, "vegetarian": 1, "spicy": 0, "ingredients": "Organic ripe strawberries, 72% dark bittersweet chocolate, flaky sea salt", "dietary_tags": "Dark Chocolate, Strawberry, Flavonoid, Endorphin-Boost, Vegan"},
        {"food_name": "Dark Chocolate & Walnut Magnesium Energy Bites", "category": "Snack", "cuisine": "American", "meal_type": "Snack", "calories": 210, "protein": 5.0, "carbs": 22.0, "fat": 12.0, "fiber": 4.0, "sugar": 12.0, "vegetarian": 1, "spicy": 0, "ingredients": "72% dark chocolate chips, raw English walnuts, medjool dates, rolled oats", "dietary_tags": "Dark Chocolate, Walnut, Magnesium, Anti-Stress, Vegan"},
        {"food_name": "Fresh Guacamole with Stoneground Tortilla Chips", "category": "Snack", "cuisine": "Mexican", "meal_type": "Snack", "calories": 320, "protein": 4.0, "carbs": 36.0, "fat": 18.0, "fiber": 7.0, "sugar": 2.0, "vegetarian": 1, "spicy": 1, "ingredients": "Hass avocados, lime juice, jalapeño, sea salt, organic corn tortilla chips", "dietary_tags": "Social, Shareable, Heart-Healthy-Fats, Vegan"},
        {"food_name": "Hummus with Whole-Wheat Pita & Toasted Pepitas", "category": "Snack", "cuisine": "Mediterranean", "meal_type": "Snack", "calories": 310, "protein": 12.0, "carbs": 38.0, "fat": 14.0, "fiber": 8.0, "sugar": 3.0, "vegetarian": 1, "spicy": 0, "ingredients": "Chickpea hummus, sesame tahini, whole-wheat pita bread, toasted pepitas, paprika", "dietary_tags": "Pumpkin Seed, Iron, B-Vitamin, Vegan"},
        {"food_name": "Spiced Dry-Roasted Almonds with Smoked Paprika", "category": "Snack", "cuisine": "Continental", "meal_type": "Snack", "calories": 210, "protein": 7.0, "carbs": 7.0, "fat": 18.0, "fiber": 4.0, "sugar": 1.0, "vegetarian": 1, "spicy": 1, "ingredients": "Dry-roasted whole California almonds, smoked Spanish paprika, sea salt", "dietary_tags": "Pre-Workout, Quick-Fuel, Keto-Friendly, Vegan"},
        {"food_name": "Warm Roasted Sweet Potato Mash with Cinnamon", "category": "Side", "cuisine": "American", "meal_type": "Dinner", "calories": 240, "protein": 4.0, "carbs": 52.0, "fat": 3.0, "fiber": 7.0, "sugar": 14.0, "vegetarian": 1, "spicy": 0, "ingredients": "Roasted sweet potatoes, Ceylon cinnamon, warm unsweetened almond milk, sea salt", "dietary_tags": "Sweet Potato Mash, Restorative, Comforting, Serotonin-Support, Vegan"}
    ]
    return recipes


def generate_full_dataset(target_count: int = 320) -> List[Dict[str, Any]]:
    """
    Expands the prototypes to exactly 320 items and computes mood dynamically
    using map_food_to_mood().
    """
    base_pool = build_raw_recipe_pool()
    full_items: List[Dict[str, Any]] = []
    
    variations = [
        ("Original", 1.0, 1.0, 1.0, 1.0, ""),
        ("Light", 0.85, 0.90, 0.80, 0.70, "Lower-Calorie, Light-Portion"),
        ("Protein-Boosted", 1.15, 1.40, 0.95, 1.05, "Extra-Protein, High-Satiety"),
        ("Hearty", 1.20, 1.10, 1.25, 1.15, "Substantial, Filling, High-Energy"),
        ("Herbal-Spiced", 0.95, 1.00, 0.95, 0.90, "Herbal-Enhanced, Digestive-Support"),
        ("Organic Artisan", 1.05, 1.05, 1.05, 1.00, "Clean-Ingredient, Artisan-Style"),
        ("Restorative Portion", 0.90, 0.95, 0.90, 0.85, "Gentle-Portion, Soothing")
    ]
    
    var_idx = 0
    item_idx = 0
    
    while len(full_items) < target_count:
        base = base_pool[item_idx % len(base_pool)]
        prefix, cal_m, p_m, c_m, f_m, tag_extra = variations[var_idx % len(variations)]
        
        name = base["food_name"] if prefix == "Original" else f"{prefix} {base['food_name']}"
        cal = int(round(base["calories"] * cal_m))
        p = round(base["protein"] * p_m, 1)
        c = round(base["carbs"] * c_m, 1)
        f = round(base["fat"] * f_m, 1)
        fib = base["fiber"]
        sug = base["sugar"]
        tags = base["dietary_tags"] if not tag_extra else f"{base['dietary_tags']}, {tag_extra}"
        
        # PROGRAMMATIC BIOCHEMICAL MOOD MAPPING FUNCTION CALL
        computed_mood = map_food_to_mood(
            food_name=name,
            ingredients=base["ingredients"],
            dietary_tags=tags,
            category=base["category"],
            calories=cal,
            protein=p,
            carbs=c,
            fat=f,
            fiber=fib,
            sugar=sug
        )
        
        entry = {
            "food_name": name,
            "category": base["category"],
            "cuisine": base["cuisine"],
            "meal_type": base["meal_type"],
            "mood": computed_mood,
            "calories": cal,
            "protein": p,
            "carbs": c,
            "fat": f,
            "fiber": fib,
            "sugar": sug,
            "vegetarian": base["vegetarian"],
            "spicy": base["spicy"],
            "ingredients": base["ingredients"],
            "dietary_tags": tags
        }
        full_items.append(entry)
        
        item_idx += 1
        if item_idx % len(base_pool) == 0:
            var_idx += 1

    return full_items[:target_count]


def export_dataset_to_csv(dataset: List[Dict[str, Any]], filepath: str) -> None:
    """Exports and verifies CSV structure."""
    columns = [
        "food_name",
        "category",
        "cuisine",
        "meal_type",
        "mood",
        "calories",
        "protein",
        "carbs",
        "fat",
        "fiber",
        "sugar",
        "vegetarian",
        "spicy",
        "ingredients",
        "dietary_tags"
    ]
    
    os.makedirs(os.path.dirname(os.path.abspath(filepath)), exist_ok=True)
    
    with open(filepath, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()
        writer.writerows(dataset)
        
    print(f"\n[EXPORT SUCCESS] Generated {len(dataset)} items into '{filepath}'.")
    
    # Statistical validation
    mood_distribution: Dict[str, int] = {}
    for d in dataset:
        mood_distribution[d["mood"]] = mood_distribution.get(d["mood"], 0) + 1
        
    print("\n--- BIOCHEMICAL HEURISTIC ASSIGNMENT RESULTS ---")
    for mood, count in sorted(mood_distribution.items()):
        print(f"  • {mood:12s}: {count:3d} items ({count / len(dataset) * 100:.1f}%)")
    print("------------------------------------------------\n")


if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_target = os.path.join(script_dir, "..", "data", "food_dataset.csv")
    
    print("[RUNNING] Generating dataset via predefined `map_food_to_mood()` function...")
    dataset_records = generate_full_dataset(target_count=320)
    export_dataset_to_csv(dataset_records, csv_target)
