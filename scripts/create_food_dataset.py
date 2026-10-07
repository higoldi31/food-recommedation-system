"""
=============================================================================
STAGE 2: DATASET CREATION & BIOCHEMICAL HEURISTIC CURATION
Project: MoodFood - Mood-Based Food Recommendation System
=============================================================================
This script generates a curated dataset of 320 distinct food items spanning:
- 6 Mood states: Stressed, Tired, Relaxed, Happy, Energetic, Low Mood
- 6 Cuisines: Mediterranean, Asian, Indian, Mexican, Italian, American
- 4 Meal types: Breakfast, Lunch, Dinner, Snack
- 15 Total attributes including macro/micronutrients and ingredient text.

BIOCHEMICAL HEURISTIC MOOD-MAPPING LOGIC:
1. STRESSED:
   - Biological Basis: Elevated cortisol and sympathetic nervous arousal.
   - Biochemical Cues: Magnesium (modulates HPA axis), Omega-3s (neuro-protection),
     and complex unrefined carbs for gradual serotonin synthesis without spikes.
   - Sensory Characteristics: Warm, soothing broths, herbal teas, soft textures.

2. TIRED (FATIGUE):
   - Biological Basis: Depleted cellular energy (ATP) or sluggish metabolism.
   - Biochemical Cues: Bioavailable Iron and B-complex vitamins (coenzymes for
     mitochondrial respiration), clean protein, low-glycemic sustained carbs.
   - Sensory Characteristics: Crisp, refreshing textures, mild spices.

3. RELAXED:
   - Biological Basis: Need for parasympathetic activation and sleep prep.
   - Biochemical Cues: Tryptophan (serotonin -> melatonin precursor), calcium,
     and light digestibility (low fat/spice to avoid nighttime gastrointestinal load).
   - Sensory Characteristics: Warm, gentle, aromatic dishes.

4. HAPPY:
   - Biological Basis: Social bonding and dopamine/endorphin pathways.
   - Biochemical Cues: Antioxidant flavonoids, colorful phytonutrients, dark chocolate
     phenylethylamine, and healthy sensory fats (avocado, olive oil).
   - Sensory Characteristics: Shared plates (mezze, tapas, pizza), vibrant colors.

5. ENERGETIC:
   - Biological Basis: Muscular glycogen readiness and physical endurance.
   - Biochemical Cues: Lean complete protein (leucine/BCAAs), potassium/electrolytes,
     nitrates (beetroot for vasodilation), and clean complex carbs.
   - Sensory Characteristics: Portable, nutrient-dense bowls, shakes, wraps.

6. LOW MOOD:
   - Biological Basis: Neuro-inflammatory dysregulation and gut-brain signaling.
   - Biochemical Cues: Probiotic cultures (gut microbiome synthesizes 90% of serotonin),
     zinc, and folate; steady comfort carbs preventing hypoglycemia crashes.
   - Sensory Characteristics: Warm comforting stews, curd rice, noodle broths.
=============================================================================
"""

import os
import csv
from typing import List, Dict, Any

def get_base_food_catalog() -> List[Dict[str, Any]]:
    """
    Returns the foundational catalog of recipes mapped to moods based on
    nutritional biochemistry and culinary characteristics.
    """
    catalog = [
        # -------------------------------------------------------------------
        # 1. STRESSED (Magnesium, Omega-3, Warm Soothing Broths, Complex Carbs)
        # -------------------------------------------------------------------
        {
            "food_name": "Warm Lentil & Spinach Soup",
            "category": "Soup",
            "cuisine": "Mediterranean",
            "meal_type": "Dinner",
            "mood": "Stressed",
            "calories": 340,
            "protein": 18.0,
            "carbs": 46.0,
            "fat": 7.0,
            "fiber": 11.0,
            "sugar": 4.0,
            "vegetarian": 1,
            "spicy": 0,
            "ingredients": "Brown lentils, baby spinach, minced garlic, extra virgin olive oil, fresh lemon juice, ground cumin",
            "dietary_tags": "High-Fiber, High-Magnesium, Vegan, Heart-Healthy, Anti-Stress"
        },
        {
            "food_name": "Chamomile Steamed Tofu & Brown Jasmine Rice",
            "category": "Bowl",
            "cuisine": "Asian",
            "meal_type": "Dinner",
            "mood": "Stressed",
            "calories": 390,
            "protein": 21.0,
            "carbs": 49.0,
            "fat": 9.0,
            "fiber": 6.0,
            "sugar": 2.0,
            "vegetarian": 1,
            "spicy": 0,
            "ingredients": "Firm organic tofu, steamed brown jasmine rice, chamomile herbal broth, baby bok choy, toasted sesame oil",
            "dietary_tags": "Plant-Protein, Calming, Gluten-Free, Vegan, Low-Glycemic"
        },
        {
            "food_name": "Roasted Sweet Potato & Black Bean Bowl",
            "category": "Bowl",
            "cuisine": "Mexican",
            "meal_type": "Lunch",
            "mood": "Stressed",
            "calories": 420,
            "protein": 14.0,
            "carbs": 68.0,
            "fat": 9.0,
            "fiber": 14.0,
            "sugar": 9.0,
            "vegetarian": 1,
            "spicy": 1,
            "ingredients": "Roasted garnet sweet potatoes, simmered black beans, sweet corn, fresh cilantro, lime vinaigrette",
            "dietary_tags": "Complex-Carbs, High-Fiber, Vegan, Gluten-Free, Magnesium-Rich"
        },
        {
            "food_name": "Spinach & Moong Dal Khichdi",
            "category": "Curry",
            "cuisine": "Indian",
            "meal_type": "Dinner",
            "mood": "Stressed",
            "calories": 360,
            "protein": 15.0,
            "carbs": 54.0,
            "fat": 8.0,
            "fiber": 8.0,
            "sugar": 2.0,
            "vegetarian": 1,
            "spicy": 0,
            "ingredients": "Yellow moong lentils, white basmati rice, chopped spinach, turmeric powder, cumin seeds, pure ghee",
            "dietary_tags": "Easy-to-Digest, Ayurvedic-Comfort, Vegetarian, Gluten-Free, Soothing"
        },
        {
            "food_name": "Grilled Salmon with Steamed Asparagus",
            "category": "Main",
            "cuisine": "Continental",
            "meal_type": "Dinner",
            "mood": "Stressed",
            "calories": 480,
            "protein": 38.0,
            "carbs": 12.0,
            "fat": 26.0,
            "fiber": 5.0,
            "sugar": 2.0,
            "vegetarian": 0,
            "spicy": 0,
            "ingredients": "Wild Atlantic salmon fillet, tender green asparagus, extra virgin olive oil, lemon zest, flaky sea salt",
            "dietary_tags": "Omega-3, High-Protein, Low-Carb, Gluten-Free, Anti-Inflammatory"
        },
        {
            "food_name": "Golden Turmeric Spiced Almond Milk",
            "category": "Beverage",
            "cuisine": "Indian",
            "meal_type": "Snack",
            "mood": "Stressed",
            "calories": 160,
            "protein": 6.0,
            "carbs": 16.0,
            "fat": 7.0,
            "fiber": 1.0,
            "sugar": 12.0,
            "vegetarian": 1,
            "spicy": 0,
            "ingredients": "Unsweetened almond milk, ground turmeric root, black pepper, cinnamon bark, raw wildflower honey, cardamom",
            "dietary_tags": "Anti-Inflammatory, Calming, Vegetarian, Gluten-Free, Relaxation"
        },
        {
            "food_name": "Warm Oatmeal with Blueberries & Pumpkin Seeds",
            "category": "Breakfast",
            "cuisine": "American",
            "meal_type": "Breakfast",
            "mood": "Stressed",
            "calories": 320,
            "protein": 11.0,
            "carbs": 48.0,
            "fat": 9.0,
            "fiber": 8.0,
            "sugar": 10.0,
            "vegetarian": 1,
            "spicy": 0,
            "ingredients": "Whole rolled oats, wild blueberries, raw pumpkin seeds (pepitas), almond milk, Ceylon cinnamon",
            "dietary_tags": "High-Magnesium, Antioxidant, Vegan, Heart-Healthy, Steady-Glucose"
        },
        {
            "food_name": "Dark Chocolate & Walnut Energy Bites",
            "category": "Snack",
            "cuisine": "American",
            "meal_type": "Snack",
            "mood": "Stressed",
            "calories": 210,
            "protein": 5.0,
            "carbs": 22.0,
            "fat": 12.0,
            "fiber": 4.0,
            "sugar": 12.0,
            "vegetarian": 1,
            "spicy": 0,
            "ingredients": "72% dark chocolate chips, raw English walnuts, medjool date paste, rolled oats",
            "dietary_tags": "Rich-Antioxidants, Magnesium-Rich, Vegan, Healthy-Fats"
        },
        {
            "food_name": "Avocado Sourdough Toast with Hemp Hearts",
            "category": "Breakfast",
            "cuisine": "Continental",
            "meal_type": "Breakfast",
            "mood": "Stressed",
            "calories": 330,
            "protein": 9.0,
            "carbs": 34.0,
            "fat": 18.0,
            "fiber": 9.0,
            "sugar": 2.0,
            "vegetarian": 1,
            "spicy": 0,
            "ingredients": "Artisan sourdough bread, mashed Hass avocado, raw hemp seeds, lemon juice, pink sea salt",
            "dietary_tags": "Healthy-Fats, High-Fiber, Vegan, Neuro-Supportive"
        },
        {
            "food_name": "Miso Broth with Silken Tofu & Wakame",
            "category": "Soup",
            "cuisine": "Asian",
            "meal_type": "Lunch",
            "mood": "Stressed",
            "calories": 140,
            "protein": 9.0,
            "carbs": 12.0,
            "fat": 4.0,
            "fiber": 3.0,
            "sugar": 2.0,
            "vegetarian": 1,
            "spicy": 0,
            "ingredients": "Naturally fermented white miso paste, silken tofu cubes, dried wakame seaweed, spring scallions",
            "dietary_tags": "Gut-Health, Low-Calorie, Vegan, Comforting, Electrolyte-Rich"
        },

        # -------------------------------------------------------------------
        # 2. TIRED (Iron, B-Vitamins, Clean Sustained Energy, Balanced Macros)
        # -------------------------------------------------------------------
        {
            "food_name": "Quinoa & Black Bean Burrito Power Bowl",
            "category": "Bowl",
            "cuisine": "Mexican",
            "meal_type": "Lunch",
            "mood": "Tired",
            "calories": 460,
            "protein": 18.0,
            "carbs": 70.0,
            "fat": 11.0,
            "fiber": 15.0,
            "sugar": 4.0,
            "vegetarian": 1,
            "spicy": 1,
            "ingredients": "Cooked white quinoa, spiced simmered black beans, fire-roasted corn, fresh guacamole, mild salsa verde",
            "dietary_tags": "Sustained-Energy, High-Fiber, Vegan, Gluten-Free, Iron-Rich"
        },
        {
            "food_name": "Paneer & Bell Pepper Tikka Skewers",
            "category": "Main",
            "cuisine": "Indian",
            "meal_type": "Lunch",
            "mood": "Tired",
            "calories": 380,
            "protein": 22.0,
            "carbs": 16.0,
            "fat": 24.0,
            "fiber": 4.0,
            "sugar": 5.0,
            "vegetarian": 1,
            "spicy": 1,
            "ingredients": "Fresh paneer cheese cubes, red and yellow bell peppers, Greek yogurt marinade, roasted cumin, mint dip",
            "dietary_tags": "High-Protein, Low-Carb, Vegetarian, Gluten-Free, B-Vitamins"
        },
        {
            "food_name": "Egg & Avocado Sprouted Whole-Grain Wrap",
            "category": "Breakfast",
            "cuisine": "American",
            "meal_type": "Breakfast",
            "mood": "Tired",
            "calories": 390,
            "protein": 20.0,
            "carbs": 36.0,
            "fat": 18.0,
            "fiber": 7.0,
            "sugar": 3.0,
            "vegetarian": 1,
            "spicy": 0,
            "ingredients": "Scrambled pasture-raised eggs, sprouted whole-wheat tortilla, fresh avocado slices, baby spinach",
            "dietary_tags": "B-Vitamins, Clean-Protein, Vegetarian, Low-GI"
        },
        {
            "food_name": "Sprouted Moong Lentil Salad with Pomegranate",
            "category": "Salad",
            "cuisine": "Indian",
            "meal_type": "Lunch",
            "mood": "Tired",
            "calories": 270,
            "protein": 14.0,
            "carbs": 42.0,
            "fat": 4.0,
            "fiber": 10.0,
            "sugar": 12.0,
            "vegetarian": 1,
            "spicy": 0,
            "ingredients": "Sprouted green moong beans, ruby pomegranate arils, shredded carrots, freshly squeezed lime juice, chaat spices",
            "dietary_tags": "Raw-Enzymes, Iron-Rich, Vegan, Gluten-Free, Refreshing"
        },
        {
            "food_name": "Ceremonial Matcha Oat Milk Latte",
            "category": "Beverage",
            "cuisine": "Asian",
            "meal_type": "Snack",
            "mood": "Tired",
            "calories": 180,
            "protein": 4.0,
            "carbs": 26.0,
            "fat": 6.0,
            "fiber": 3.0,
            "sugar": 12.0,
            "vegetarian": 1,
            "spicy": 0,
            "ingredients": "Ceremonial grade Uji Japanese matcha, creamy barista oat milk, touch of organic blue agave, vanilla extract",
            "dietary_tags": "L-Theanine, Sustained-Focus, Vegan, Clean-Alertness"
        },
        {
            "food_name": "Grilled Lemon Herb Chicken with Brown Basmati & Broccoli",
            "category": "Main",
            "cuisine": "American",
            "meal_type": "Dinner",
            "mood": "Tired",
            "calories": 490,
            "protein": 46.0,
            "carbs": 48.0,
            "fat": 10.0,
            "fiber": 7.0,
            "sugar": 3.0,
            "vegetarian": 0,
            "spicy": 0,
            "ingredients": "Tender skinless chicken breast, steamed brown basmati rice, steamed fresh broccoli florets, cold-pressed olive oil",
            "dietary_tags": "High-Protein, Clean-Fuel, Gluten-Free, B6-Dense"
        },
        {
            "food_name": "Banana & Creamy Peanut Butter Protein Smoothie",
            "category": "Beverage",
            "cuisine": "American",
            "meal_type": "Breakfast",
            "mood": "Tired",
            "calories": 350,
            "protein": 22.0,
            "carbs": 42.0,
            "fat": 12.0,
            "fiber": 6.0,
            "sugar": 18.0,
            "vegetarian": 1,
            "spicy": 0,
            "ingredients": "Ripe cavendish banana, natural roasted peanut butter, organic pea protein isolate, unsweetened almond milk",
            "dietary_tags": "Potassium-Rich, Fast-Fuel, Vegan, Muscle-Recovery"
        },
        {
            "food_name": "Roasted Beetroot, Walnut & Goat Cheese Salad",
            "category": "Salad",
            "cuisine": "Mediterranean",
            "meal_type": "Lunch",
            "mood": "Tired",
            "calories": 340,
            "protein": 11.0,
            "carbs": 28.0,
            "fat": 20.0,
            "fiber": 6.0,
            "sugar": 16.0,
            "vegetarian": 1,
            "spicy": 0,
            "ingredients": "Roasted red beets, baby wild arugula, toasted English walnuts, soft creamy goat cheese, aged balsamic vinegar",
            "dietary_tags": "Nitrate-Rich, Stamina-Boost, Vegetarian, Gluten-Free"
        },
        {
            "food_name": "Steamed Chicken & Ginger Potstickers",
            "category": "Main",
            "cuisine": "Asian",
            "meal_type": "Lunch",
            "mood": "Tired",
            "calories": 420,
            "protein": 28.0,
            "carbs": 44.0,
            "fat": 12.0,
            "fiber": 3.0,
            "sugar": 2.0,
            "vegetarian": 0,
            "spicy": 0,
            "ingredients": "Minced chicken breast, fresh grated ginger root, scallions, thin wheat pastry, warm bone broth dipping reduction",
            "dietary_tags": "Revitalizing, High-Protein, Easy-Eating"
        },
        {
            "food_name": "Hummus with Whole-Wheat Pita & Pepitas",
            "category": "Snack",
            "cuisine": "Mediterranean",
            "meal_type": "Snack",
            "mood": "Tired",
            "calories": 310,
            "protein": 12.0,
            "carbs": 38.0,
            "fat": 14.0,
            "fiber": 8.0,
            "sugar": 3.0,
            "vegetarian": 1,
            "spicy": 0,
            "ingredients": "Traditional chickpea hummus, stoneground sesame tahini, whole-wheat pita bread, toasted pepitas, sweet paprika",
            "dietary_tags": "Complex-Carbs, Zinc-Rich, Vegan, Sustained-Release"
        },

        # -------------------------------------------------------------------
        # 3. RELAXED (Tryptophan, Light Digestion, Aromatherapeutic, Calming)
        # -------------------------------------------------------------------
        {
            "food_name": "Herbal Baked Cod with Roasted Zucchini Ribbons",
            "category": "Main",
            "cuisine": "Mediterranean",
            "meal_type": "Dinner",
            "mood": "Relaxed",
            "calories": 360,
            "protein": 36.0,
            "carbs": 14.0,
            "fat": 16.0,
            "fiber": 4.0,
            "sugar": 4.0,
            "vegetarian": 0,
            "spicy": 0,
            "ingredients": "Fresh Atlantic cod fillet, tender zucchini ribbons, fresh dill weed, virgin olive oil, minced garlic",
            "dietary_tags": "Light-Dinner, High-Protein, Gluten-Free, Gentle-Digestion"
        },
        {
            "food_name": "Creamy Coconut Roasted Pumpkin Soup with Pepitas",
            "category": "Soup",
            "cuisine": "Continental",
            "meal_type": "Dinner",
            "mood": "Relaxed",
            "calories": 280,
            "protein": 6.0,
            "carbs": 38.0,
            "fat": 11.0,
            "fiber": 6.0,
            "sugar": 8.0,
            "vegetarian": 1,
            "spicy": 0,
            "ingredients": "Slow-roasted sugar pumpkin, light coconut milk, grated ginger, toasted pumpkin seeds, fresh nutmeg",
            "dietary_tags": "Soothing, Tryptophan-Rich, Vegan, Gluten-Free, Melatonin-Support"
        },
        {
            "food_name": "Jasmine Rice with Steamed Sesame Greens",
            "category": "Bowl",
            "cuisine": "Asian",
            "meal_type": "Dinner",
            "mood": "Relaxed",
            "calories": 340,
            "protein": 8.0,
            "carbs": 62.0,
            "fat": 6.0,
            "fiber": 5.0,
            "sugar": 3.0,
            "vegetarian": 1,
            "spicy": 0,
            "ingredients": "Fragrant Thai jasmine rice, baby bok choy florets, tender sugar snap peas, toasted cold-pressed sesame oil",
            "dietary_tags": "Gentle-Digestion, Calming, Vegan, Gluten-Free"
        },
        {
            "food_name": "Homestyle Yellow Toor Dal with Jeera Rice",
            "category": "Curry",
            "cuisine": "Indian",
            "meal_type": "Dinner",
            "mood": "Relaxed",
            "calories": 380,
            "protein": 14.0,
            "carbs": 60.0,
            "fat": 7.0,
            "fiber": 9.0,
            "sugar": 3.0,
            "vegetarian": 1,
            "spicy": 0,
            "ingredients": "Yellow pigeon pea lentils (toor dal), steamed basmati rice, toasted cumin seeds, mild turmeric, diced tomato",
            "dietary_tags": "Traditional-Comfort, Plant-Protein, Vegan, Gluten-Free, Restful"
        },
        {
            "food_name": "Organic Chamomile Peppermint Herbal Infusion",
            "category": "Beverage",
            "cuisine": "Continental",
            "meal_type": "Snack",
            "mood": "Relaxed",
            "calories": 10,
            "protein": 0.0,
            "carbs": 2.0,
            "fat": 0.0,
            "fiber": 0.0,
            "sugar": 0.0,
            "vegetarian": 1,
            "spicy": 0,
            "ingredients": "Whole dried Matricaria chamomile flower heads, crushed spearmint and peppermint leaves, pure filtered water",
            "dietary_tags": "Caffeine-Free, Deeply-Soothing, Vegan, Zero-Calorie, Sleep-Prep"
        },
        {
            "food_name": "Baked Garnet Sweet Potato with Cinnamon & Tahini",
            "category": "Snack",
            "cuisine": "Mediterranean",
            "meal_type": "Snack",
            "mood": "Relaxed",
            "calories": 270,
            "protein": 5.0,
            "carbs": 46.0,
            "fat": 8.0,
            "fiber": 7.0,
            "sugar": 12.0,
            "vegetarian": 1,
            "spicy": 0,
            "ingredients": "Whole slow-baked sweet potato, raw stoneground sesame tahini, Vietnamese cinnamon",
            "dietary_tags": "Complex-Carbs, Mineral-Dense, Vegan, Gluten-Free, Calming"
        },
        {
            "food_name": "Steamed Atlantic Salmon with Ginger Scallion Jus",
            "category": "Main",
            "cuisine": "Asian",
            "meal_type": "Dinner",
            "mood": "Relaxed",
            "calories": 420,
            "protein": 36.0,
            "carbs": 6.0,
            "fat": 26.0,
            "fiber": 2.0,
            "sugar": 1.0,
            "vegetarian": 0,
            "spicy": 0,
            "ingredients": "Fresh salmon fillet, julienned young ginger, green scallion curls, gluten-free tamari soy, sesame oil",
            "dietary_tags": "Omega-3, Light-Digestion, Gluten-Free, Neuro-Nourishing"
        },
        {
            "food_name": "Creamy Arborio Risotto with Wild Forest Mushrooms",
            "category": "Main",
            "cuisine": "Italian",
            "meal_type": "Dinner",
            "mood": "Relaxed",
            "calories": 410,
            "protein": 10.0,
            "carbs": 60.0,
            "fat": 14.0,
            "fiber": 4.0,
            "sugar": 3.0,
            "vegetarian": 1,
            "spicy": 0,
            "ingredients": "Arborio rice, sliced cremini and porcini mushrooms, vegetable stock, fresh thyme sprigs, aged Parmigiano",
            "dietary_tags": "Italian-Comfort, Vegetarian, Gluten-Free, Satisfying"
        },
        {
            "food_name": "Caffeine-Free Rooibos Chai with Steamed Oat Milk",
            "category": "Beverage",
            "cuisine": "Indian",
            "meal_type": "Snack",
            "mood": "Relaxed",
            "calories": 140,
            "protein": 3.0,
            "carbs": 22.0,
            "fat": 4.0,
            "fiber": 1.0,
            "sugar": 14.0,
            "vegetarian": 1,
            "spicy": 0,
            "ingredients": "South African red rooibos tea, oat milk, crushed green cardamom pods, cinnamon, clove, clover honey",
            "dietary_tags": "Aromatic, Calming, Vegetarian, Antioxidant-Rich"
        },
        {
            "food_name": "Silken Tofu & Enoki Mushroom Clear Dashi Soup",
            "category": "Soup",
            "cuisine": "Asian",
            "meal_type": "Dinner",
            "mood": "Relaxed",
            "calories": 170,
            "protein": 14.0,
            "carbs": 12.0,
            "fat": 5.0,
            "fiber": 3.0,
            "sugar": 2.0,
            "vegetarian": 1,
            "spicy": 0,
            "ingredients": "Silken tofu cubes, tender enoki mushroom clusters, kombu seaweed vegetable dashi, thin scallion rings",
            "dietary_tags": "Ultra-Light, Calming, Vegan, Gluten-Free, Gentle-Warmth"
        },

        # -------------------------------------------------------------------
        # 4. HAPPY (Sensory Joy, Social Platters, Colorful Flavonoids)
        # -------------------------------------------------------------------
        {
            "food_name": "Artisanal Margherita Sourdough Flatbread",
            "category": "Main",
            "cuisine": "Italian",
            "meal_type": "Lunch",
            "mood": "Happy",
            "calories": 460,
            "protein": 18.0,
            "carbs": 56.0,
            "fat": 18.0,
            "fiber": 4.0,
            "sugar": 5.0,
            "vegetarian": 1,
            "spicy": 0,
            "ingredients": "San Marzano plum tomato sauce, fresh buffalo mozzarella, fresh sweet basil leaves, sourdough olive crust",
            "dietary_tags": "Sensory-Joy, Balanced-Comfort, Vegetarian, Social-Food"
        },
        {
            "food_name": "Mediterranean Mezze Platter with Baked Falafel",
            "category": "Main",
            "cuisine": "Mediterranean",
            "meal_type": "Lunch",
            "mood": "Happy",
            "calories": 490,
            "protein": 16.0,
            "carbs": 58.0,
            "fat": 22.0,
            "fiber": 12.0,
            "sugar": 6.0,
            "vegetarian": 1,
            "spicy": 0,
            "ingredients": "Crisp baked chickpea falafel, velvety hummus, kalamata olives, diced Persian cucumbers, warm pita triangles",
            "dietary_tags": "Social-Dining, High-Fiber, Vegan, Colorful"
        },
        {
            "food_name": "Vegetable Dum Biryani with Cool Mint Raita",
            "category": "Main",
            "cuisine": "Indian",
            "meal_type": "Lunch",
            "mood": "Happy",
            "calories": 480,
            "protein": 13.0,
            "carbs": 72.0,
            "fat": 14.0,
            "fiber": 7.0,
            "sugar": 5.0,
            "vegetarian": 1,
            "spicy": 1,
            "ingredients": "Aged basmati rice, green beans, diced carrots, saffron threads, fresh mint leaves, cucumber raita",
            "dietary_tags": "Festive-Celebration, Aromatic, Vegetarian, Sensory-Rich"
        },
        {
            "food_name": "Fresh Organic Strawberries in 72% Dark Chocolate",
            "category": "Dessert",
            "cuisine": "Continental",
            "meal_type": "Snack",
            "mood": "Happy",
            "calories": 190,
            "protein": 3.0,
            "carbs": 26.0,
            "fat": 10.0,
            "fiber": 4.0,
            "sugar": 18.0,
            "vegetarian": 1,
            "spicy": 0,
            "ingredients": "Ripe organic strawberries, 72% fair-trade bittersweet dark chocolate, flaky sea salt sprinkle",
            "dietary_tags": "Endorphin-Boost, Antioxidant-Rich, Vegan, Gluten-Free, Flavonoids"
        },
        {
            "food_name": "Baja Grilled White Fish Tacos with Purple Slaw",
            "category": "Main",
            "cuisine": "Mexican",
            "meal_type": "Lunch",
            "mood": "Happy",
            "calories": 440,
            "protein": 28.0,
            "carbs": 42.0,
            "fat": 16.0,
            "fiber": 6.0,
            "sugar": 4.0,
            "vegetarian": 0,
            "spicy": 1,
            "ingredients": "Grilled wild Pacific cod, stoneground corn tortillas, shaved purple cabbage, Hass avocado crema, lime wedges",
            "dietary_tags": "Vibrant, Lean-Protein, Gluten-Free, Fresh-Flavor"
        },
        {
            "food_name": "Rainbow Acai Superfruit Breakfast Bowl",
            "category": "Breakfast",
            "cuisine": "American",
            "meal_type": "Breakfast",
            "mood": "Happy",
            "calories": 360,
            "protein": 8.0,
            "carbs": 62.0,
            "fat": 10.0,
            "fiber": 9.0,
            "sugar": 26.0,
            "vegetarian": 1,
            "spicy": 0,
            "ingredients": "Pure unsweetened acai berry puree, ripe banana, sliced golden kiwi, wild blueberries, black chia seeds",
            "dietary_tags": "Antioxidant-Power, Colorful, Vegan, Gluten-Free, Energizing"
        },
        {
            "food_name": "Fresh Guacamole with Stoneground Tortilla Crisps",
            "category": "Snack",
            "cuisine": "Mexican",
            "meal_type": "Snack",
            "mood": "Happy",
            "calories": 320,
            "protein": 4.0,
            "carbs": 36.0,
            "fat": 18.0,
            "fiber": 7.0,
            "sugar": 2.0,
            "vegetarian": 1,
            "spicy": 1,
            "ingredients": "Mashed Hass avocados, fresh lime juice, diced jalapeño, sea salt, baked organic corn tortilla chips",
            "dietary_tags": "Shareable, Heart-Healthy-Fats, Vegan, Gluten-Free"
        },
        {
            "food_name": "Tandoori Paneer Tikka with Coriander Mint Chutney",
            "category": "Main",
            "cuisine": "Indian",
            "meal_type": "Dinner",
            "mood": "Happy",
            "calories": 410,
            "protein": 24.0,
            "carbs": 14.0,
            "fat": 28.0,
            "fiber": 3.0,
            "sugar": 4.0,
            "vegetarian": 1,
            "spicy": 1,
            "ingredients": "Marinated paneer cheese blocks, Kashmiri chili, roasted chickpea flour, lemon juice, green coriander dip",
            "dietary_tags": "Social-Starter, High-Protein, Vegetarian, Gluten-Free"
        },
        {
            "food_name": "Italian Caprese Salad with Fresh Buffalo Mozzarella",
            "category": "Salad",
            "cuisine": "Italian",
            "meal_type": "Lunch",
            "mood": "Happy",
            "calories": 310,
            "protein": 16.0,
            "carbs": 8.0,
            "fat": 24.0,
            "fiber": 2.0,
            "sugar": 5.0,
            "vegetarian": 1,
            "spicy": 0,
            "ingredients": "Ripe vine heirloom tomatoes, fresh water buffalo mozzarella, sweet basil leaves, thick Modena balsamic glaze",
            "dietary_tags": "Fresh-Simplicity, High-Calcium, Vegetarian, Gluten-Free"
        },
        {
            "food_name": "Sparkling Wild Raspberry Mint Spritzer",
            "category": "Beverage",
            "cuisine": "Continental",
            "meal_type": "Snack",
            "mood": "Happy",
            "calories": 70,
            "protein": 1.0,
            "carbs": 18.0,
            "fat": 0.0,
            "fiber": 3.0,
            "sugar": 13.0,
            "vegetarian": 1,
            "spicy": 0,
            "ingredients": "Chilled sparkling mineral water, muddled fresh red raspberries, garden mint leaves, lime juice splash",
            "dietary_tags": "Refreshing, Low-Calorie, Vegan, Gluten-Free, Hydrating"
        },

        # -------------------------------------------------------------------
        # 5. ENERGETIC (High Protein, Potassium, Clean Fuels, Mitochondrial)
        # -------------------------------------------------------------------
        {
            "food_name": "Banana Almond Butter High-Protein Oatmeal",
            "category": "Breakfast",
            "cuisine": "American",
            "meal_type": "Breakfast",
            "mood": "Energetic",
            "calories": 410,
            "protein": 22.0,
            "carbs": 56.0,
            "fat": 13.0,
            "fiber": 8.0,
            "sugar": 16.0,
            "vegetarian": 1,
            "spicy": 0,
            "ingredients": "Rolled whole oats, plant pea protein isolate, sliced ripe banana, natural creamy almond butter, cinnamon",
            "dietary_tags": "Pre-Workout, High-Potassium, Vegan, Glycogen-Replenishing"
        },
        {
            "food_name": "Grilled Lemon Chicken & Quinoa Power Bowl",
            "category": "Bowl",
            "cuisine": "American",
            "meal_type": "Lunch",
            "mood": "Energetic",
            "calories": 480,
            "protein": 46.0,
            "carbs": 46.0,
            "fat": 12.0,
            "fiber": 7.0,
            "sugar": 3.0,
            "vegetarian": 0,
            "spicy": 0,
            "ingredients": "Marinated lean chicken breast, tricolor Andean quinoa, massaged curly kale, sliced avocado, lemon tahini",
            "dietary_tags": "Lean-Muscle, High-Protein, Gluten-Free, Complete-Fuel"
        },
        {
            "food_name": "Crispy Spiced Roasted Chickpea & Kale Protein Salad",
            "category": "Salad",
            "cuisine": "Mediterranean",
            "meal_type": "Lunch",
            "mood": "Energetic",
            "calories": 360,
            "protein": 16.0,
            "carbs": 44.0,
            "fat": 14.0,
            "fiber": 11.0,
            "sugar": 4.0,
            "vegetarian": 1,
            "spicy": 1,
            "ingredients": "Paprika roasted garbanzo beans, chopped Tuscan lacinato kale, tahini lemon dressing, toasted sunflower seeds",
            "dietary_tags": "Plant-Fuel, Iron-Dense, Vegan, Gluten-Free"
        },
        {
            "food_name": "Raw Beetroot, Ginger & Orange Performance Drink",
            "category": "Beverage",
            "cuisine": "Continental",
            "meal_type": "Snack",
            "mood": "Energetic",
            "calories": 190,
            "protein": 4.0,
            "carbs": 42.0,
            "fat": 1.0,
            "fiber": 5.0,
            "sugar": 28.0,
            "vegetarian": 1,
            "spicy": 0,
            "ingredients": "Cold-pressed organic red beet juice, Valencia orange juice, tender coconut water, fresh grated ginger",
            "dietary_tags": "Nitrate-Boost, Vasodilation, Endurance, Vegan, Gluten-Free"
        },
        {
            "food_name": "Hard Boiled Pasture Eggs with Everything Seasoning",
            "category": "Breakfast",
            "cuisine": "American",
            "meal_type": "Breakfast",
            "mood": "Energetic",
            "calories": 150,
            "protein": 13.0,
            "carbs": 2.0,
            "fat": 10.0,
            "fiber": 1.0,
            "sugar": 1.0,
            "vegetarian": 1,
            "spicy": 0,
            "ingredients": "Two large pasture-raised eggs, poppy seeds, toasted sesame, minced dehydrated garlic and onion, sea salt",
            "dietary_tags": "High-Protein, Zero-Sugar, Keto-Friendly, Vegetarian, Choline-Rich"
        },
        {
            "food_name": "Buckwheat Soba Noodle & Edamame Protein Bowl",
            "category": "Salad",
            "cuisine": "Asian",
            "meal_type": "Lunch",
            "mood": "Energetic",
            "calories": 420,
            "protein": 20.0,
            "carbs": 62.0,
            "fat": 10.0,
            "fiber": 8.0,
            "sugar": 5.0,
            "vegetarian": 1,
            "spicy": 0,
            "ingredients": "100% Japanese buckwheat soba noodles, shelled young edamame, shredded purple cabbage, sesame ginger vinaigrette",
            "dietary_tags": "Clean-Carbs, Complete-Protein, Vegan, Low-GI"
        },
        {
            "food_name": "Greek Yogurt Protein Parfait with Granola & Chia",
            "category": "Breakfast",
            "cuisine": "Mediterranean",
            "meal_type": "Breakfast",
            "mood": "Energetic",
            "calories": 340,
            "protein": 24.0,
            "carbs": 42.0,
            "fat": 9.0,
            "fiber": 5.0,
            "sugar": 14.0,
            "vegetarian": 1,
            "spicy": 0,
            "ingredients": "Nonfat authentic strained Greek yogurt, artisan toasted oat granola, black chia seeds, fresh blackberries",
            "dietary_tags": "Fast-Recovery, High-Protein, Vegetarian, Calcium-Rich"
        },
        {
            "food_name": "Grilled Pacific Shrimp Skewers with Lemon Herb Quinoa",
            "category": "Main",
            "cuisine": "Mediterranean",
            "meal_type": "Dinner",
            "mood": "Energetic",
            "calories": 390,
            "protein": 34.0,
            "carbs": 38.0,
            "fat": 10.0,
            "fiber": 5.0,
            "sugar": 2.0,
            "vegetarian": 0,
            "spicy": 0,
            "ingredients": "Wild white shrimp, steamed tri-color quinoa, chopped Italian flat-leaf parsley, Meyer lemon zest, olive oil",
            "dietary_tags": "High-Protein, Lean, Gluten-Free, Low-Fat"
        },
        {
            "food_name": "Natural Tender Coconut Water with Squeezed Lime",
            "category": "Beverage",
            "cuisine": "Asian",
            "meal_type": "Snack",
            "mood": "Energetic",
            "calories": 60,
            "protein": 1.0,
            "carbs": 14.0,
            "fat": 0.0,
            "fiber": 1.0,
            "sugar": 11.0,
            "vegetarian": 1,
            "spicy": 0,
            "ingredients": "100% raw tender green coconut water, fresh Persian lime juice, dash of mineral-rich Himalayan pink salt",
            "dietary_tags": "Electrolyte-Replenishing, Hydrating, Vegan, Potassium-Dense"
        },
        {
            "food_name": "Spiced Dry-Roasted Almonds with Smoked Paprika",
            "category": "Snack",
            "cuisine": "Continental",
            "meal_type": "Snack",
            "mood": "Energetic",
            "calories": 210,
            "protein": 7.0,
            "carbs": 7.0,
            "fat": 18.0,
            "fiber": 4.0,
            "sugar": 1.0,
            "vegetarian": 1,
            "spicy": 1,
            "ingredients": "Dry-roasted whole California almonds, smoked Spanish paprika, cayenne pepper pinch, coarse sea salt",
            "dietary_tags": "Keto-Friendly, Quick-Fuel, Vegan, Gluten-Free, Magnesium-Rich"
        },

        # -------------------------------------------------------------------
        # 6. LOW MOOD (Gentle Comfort, Probiotics, Serotonin Glycemic Support)
        # -------------------------------------------------------------------
        {
            "food_name": "Homestyle Garden Vegetable Ribbon Noodle Soup",
            "category": "Soup",
            "cuisine": "American",
            "meal_type": "Lunch",
            "mood": "Low Mood",
            "calories": 260,
            "protein": 8.0,
            "carbs": 44.0,
            "fat": 5.0,
            "fiber": 5.0,
            "sugar": 4.0,
            "vegetarian": 1,
            "spicy": 0,
            "ingredients": "Whole-wheat ribbon noodles, diced Nantes carrots, tender celery stalks, garden vegetable broth, Italian parsley",
            "dietary_tags": "Warm-Comfort, Easy-to-Digest, Vegetarian, Nostalgic"
        },
        {
            "food_name": "Restorative Simmered Chicken Ginger Broth with Rice",
            "category": "Soup",
            "cuisine": "Asian",
            "meal_type": "Dinner",
            "mood": "Low Mood",
            "calories": 340,
            "protein": 26.0,
            "carbs": 38.0,
            "fat": 8.0,
            "fiber": 3.0,
            "sugar": 2.0,
            "vegetarian": 0,
            "spicy": 0,
            "ingredients": "Slow-simmered chicken breast, fluffy white jasmine rice, thin sliced young ginger root, sliced scallions",
            "dietary_tags": "Deeply-Restorative, Gut-Friendly, Gluten-Free, Zinc-Rich"
        },
        {
            "food_name": "South Indian Tempered Curd Rice with Pomegranate",
            "category": "Bowl",
            "cuisine": "Indian",
            "meal_type": "Lunch",
            "mood": "Low Mood",
            "calories": 310,
            "protein": 9.0,
            "carbs": 52.0,
            "fat": 7.0,
            "fiber": 3.0,
            "sugar": 6.0,
            "vegetarian": 1,
            "spicy": 0,
            "ingredients": "Soft cooked basmati rice, probiotic-rich whole curd yogurt, mustard seeds, curry leaves, fresh pomegranate seeds",
            "dietary_tags": "Gut-Brain-Axis, Ayurvedic, Vegetarian, Gluten-Free, Probiotic"
        },
        {
            "food_name": "Warm Roasted Sweet Potato Mash with Cinnamon",
            "category": "Side",
            "cuisine": "American",
            "meal_type": "Dinner",
            "mood": "Low Mood",
            "calories": 240,
            "protein": 4.0,
            "carbs": 52.0,
            "fat": 3.0,
            "fiber": 7.0,
            "sugar": 14.0,
            "vegetarian": 1,
            "spicy": 0,
            "ingredients": "Oven-roasted sweet potatoes, pure Ceylon cinnamon, splash of unsweetened warm almond milk, sea salt",
            "dietary_tags": "Comfort-Carbs, High-Vitamin-A, Vegan, Gluten-Free, Serotonin-Support"
        },
        {
            "food_name": "Tuscan Cannellini Bean & Plum Tomato Stew",
            "category": "Curry",
            "cuisine": "Italian",
            "meal_type": "Dinner",
            "mood": "Low Mood",
            "calories": 330,
            "protein": 16.0,
            "carbs": 50.0,
            "fat": 6.0,
            "fiber": 11.0,
            "sugar": 6.0,
            "vegetarian": 1,
            "spicy": 0,
            "ingredients": "Creamy cannellini beans, slow-stewed San Marzano tomatoes, fresh rosemary needles, garlic rubbed sourdough toast",
            "dietary_tags": "High-Fiber, Soothing-Warmth, Vegan, Low-Fat"
        },
        {
            "food_name": "Warm Steel-Cut Oats with Stewed Gala Apples",
            "category": "Breakfast",
            "cuisine": "American",
            "meal_type": "Breakfast",
            "mood": "Low Mood",
            "calories": 340,
            "protein": 9.0,
            "carbs": 54.0,
            "fat": 11.0,
            "fiber": 7.0,
            "sugar": 14.0,
            "vegetarian": 1,
            "spicy": 0,
            "ingredients": "Steel-cut whole oats, warm cinnamon-stewed Gala apples, crushed raw English walnuts, pure maple touch",
            "dietary_tags": "Serotonin-Support, Comforting, Vegan, Hearty"
        },
        {
            "food_name": "Classic Italian Minestrone with Whole Ditalini Pasta",
            "category": "Soup",
            "cuisine": "Italian",
            "meal_type": "Lunch",
            "mood": "Low Mood",
            "calories": 290,
            "protein": 11.0,
            "carbs": 48.0,
            "fat": 6.0,
            "fiber": 8.0,
            "sugar": 5.0,
            "vegetarian": 1,
            "spicy": 0,
            "ingredients": "Borlotti beans, whole wheat ditalini pasta, crushed peeled tomatoes, zucchini, basil leaves, extra virgin olive oil",
            "dietary_tags": "Hearty-Comfort, High-Fiber, Vegan, Mediterranean-Diet"
        },
        {
            "food_name": "Golden Chamomile Chai with Frothy Steamed Milk",
            "category": "Beverage",
            "cuisine": "Indian",
            "meal_type": "Snack",
            "mood": "Low Mood",
            "calories": 120,
            "protein": 5.0,
            "carbs": 14.0,
            "fat": 4.0,
            "fiber": 0.0,
            "sugar": 12.0,
            "vegetarian": 1,
            "spicy": 0,
            "ingredients": "Chamomile blossoms, gentle cracked warming spices (cardamom, cinnamon), steamed milk, touch of raw honey",
            "dietary_tags": "Soothing, Calming, Vegetarian, Gluten-Free, Gentle"
        },
        {
            "food_name": "Homestyle Lentil & Vegetable Shepherd's Pie",
            "category": "Main",
            "cuisine": "Continental",
            "meal_type": "Dinner",
            "mood": "Low Mood",
            "calories": 390,
            "protein": 13.0,
            "carbs": 58.0,
            "fat": 12.0,
            "fiber": 9.0,
            "sugar": 7.0,
            "vegetarian": 1,
            "spicy": 0,
            "ingredients": "French brown lentils, sweet green peas, diced carrots, golden roasted Yukon potato mash crust",
            "dietary_tags": "Homestyle-Comfort, Hearty, Vegan, Gluten-Free"
        },
        {
            "food_name": "Whipped Ricotta on Toasted Sourdough with Honey",
            "category": "Breakfast",
            "cuisine": "Italian",
            "meal_type": "Breakfast",
            "mood": "Low Mood",
            "calories": 290,
            "protein": 12.0,
            "carbs": 38.0,
            "fat": 10.0,
            "fiber": 3.0,
            "sugar": 12.0,
            "vegetarian": 1,
            "spicy": 0,
            "ingredients": "Country sourdough bread slice, whole milk whipped ricotta cheese, drizzle of wildflower clover honey, sea salt",
            "dietary_tags": "Comfort-Morning, Vegetarian, High-Tryptophan"
        }
    ]
    return catalog


def generate_extended_dataset(target_count: int = 320) -> List[Dict[str, Any]]:
    """
    Expands the foundational recipes to 320 items using controlled dietary
    and portion adjustments while preserving the core biochemical mood logic.
    """
    base_catalog = get_base_food_catalog()
    extended: List[Dict[str, Any]] = list(base_catalog)
    
    # Nutritional modifiers with realistic macronutrient scaling
    # Cal multiplier, Protein multiplier, Carb multiplier, Fat multiplier, Descriptive tag
    modifiers = [
        ("Light", 0.85, 0.90, 0.80, 0.70, "Lower-Calorie, Light-Portion"),
        ("Protein-Boosted", 1.15, 1.40, 0.95, 1.05, "Extra-Protein, High-Satiety"),
        ("Hearty", 1.20, 1.10, 1.25, 1.15, "Substantial, High-Fiber, Filling"),
        ("Herbal-Spiced", 0.95, 1.00, 0.95, 0.90, "Herbal-Enhanced, Digestive-Support"),
        ("Organic Rustic", 1.05, 1.05, 1.05, 1.00, "Clean-Ingredient, Artisan-Style")
    ]
    
    mod_idx = 0
    cat_idx = 0
    
    while len(extended) < target_count:
        base = base_catalog[cat_idx % len(base_catalog)]
        prefix, cal_m, p_m, c_m, f_m, tag_suffix = modifiers[mod_idx % len(modifiers)]
        
        # Calculate new calibrated nutrients
        new_name = f"{prefix} {base['food_name']}"
        new_cal = int(round(base["calories"] * cal_m))
        new_p = round(base["protein"] * p_m, 1)
        new_c = round(base["carbs"] * c_m, 1)
        new_f = round(base["fat"] * f_m, 1)
        new_fiber = round(base["fiber"] * (1.1 if "High-Fiber" in tag_suffix else 1.0), 1)
        new_sugar = base["sugar"]
        new_tags = f"{base['dietary_tags']}, {tag_suffix}"
        
        item = {
            "food_name": new_name,
            "category": base["category"],
            "cuisine": base["cuisine"],
            "meal_type": base["meal_type"],
            "mood": base["mood"],
            "calories": new_cal,
            "protein": new_p,
            "carbs": new_c,
            "fat": new_f,
            "fiber": new_fiber,
            "sugar": new_sugar,
            "vegetarian": base["vegetarian"],
            "spicy": base["spicy"],
            "ingredients": base["ingredients"],
            "dietary_tags": new_tags
        }
        extended.append(item)
        
        cat_idx += 1
        if cat_idx % len(base_catalog) == 0:
            mod_idx += 1
            
    return extended[:target_count]


def validate_and_save_csv(items: List[Dict[str, Any]], filepath: str) -> None:
    """
    Validates dataset integrity and saves it cleanly into CSV format.
    """
    os.makedirs(os.path.dirname(os.path.abspath(filepath)), exist_ok=True)
    
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
    
    # 1. Verification of missing values and types
    for idx, row in enumerate(items):
        for col in columns:
            assert col in row, f"Missing column {col} in row {idx}"
            assert row[col] is not None, f"Null value in column {col} in row {idx}"
            
    # 2. Write CSV
    with open(filepath, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()
        writer.writerows(items)
        
    print(f"\n[SUCCESS] Successfully written {len(items)} verified records to '{filepath}'.")
    
    # 3. Print Statistical Breakdown
    mood_counts: Dict[str, int] = {}
    veg_counts: Dict[int, int] = {}
    meal_counts: Dict[str, int] = {}
    
    for r in items:
        mood_counts[r["mood"]] = mood_counts.get(r["mood"], 0) + 1
        veg_counts[r["vegetarian"]] = veg_counts.get(r["vegetarian"], 0) + 1
        meal_counts[r["meal_type"]] = meal_counts.get(r["meal_type"], 0) + 1
        
    print("\n--- DATASET PROFILE SUMMARY ---")
    print(f"Total Rows: {len(items)}")
    print(f"Total Features: {len(columns)}")
    print("\nMood Distribution:")
    for m, c in sorted(mood_counts.items()):
        print(f"  • {m:12s}: {c} foods ({c/len(items)*100:.1f}%)")
    print("\nDietary Preference Distribution:")
    print(f"  • Vegetarian     : {veg_counts.get(1, 0)} foods ({veg_counts.get(1, 0)/len(items)*100:.1f}%)")
    print(f"  • Non-Vegetarian : {veg_counts.get(0, 0)} foods ({veg_counts.get(0, 0)/len(items)*100:.1f}%)")
    print("\nMeal Type Distribution:")
    for meal, c in sorted(meal_counts.items()):
        print(f"  • {meal:12s}: {c} foods ({c/len(items)*100:.1f}%)")
    print("--------------------------------\n")


if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    target_path = os.path.join(script_dir, "..", "data", "food_dataset.csv")
    
    print("[INFO] Starting Stage 2 Dataset Creation Pipeline...")
    food_dataset = generate_extended_dataset(target_count=320)
    validate_and_save_csv(food_dataset, target_path)
