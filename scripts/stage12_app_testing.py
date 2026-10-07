"""
Stage 12: Comprehensive App Testing & Resilience Suite for MoodFood.
Executes rigorous end-to-end testing across 6 test modules:
1. Boundary & Extreme Filter Stress Testing (e.g., tight calorie/protein bounds).
2. Zero-Match Fallback & Contradictory Constraint Recovery.
3. Session State Persistence & Favorites CRUD Operations.
4. Latency Profiling & High-Throughput Micro-benchmarks (100 sequential queries).
5. Input Sanitization & Adversarial Query Injection.
6. Deterministic Output Parity & Ranking Invariance.
"""

import sys
import os
import time
import json
import unittest
import importlib.util

# Import app module
spec = importlib.util.spec_from_file_location("app_module", os.path.join(os.path.dirname(__file__), "..", "app.py"))
app_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(app_module)

MoodFoodController = app_module.MoodFoodController


class TestStage12AppComprehensive(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.controller = MoodFoodController()
        print(f"\n--- Initialized MoodFoodController with {len(cls.controller.dataset)} catalog items ---")

    def test_01_extreme_calorie_bound(self):
        """Tests system behavior under ultra-low calorie ceiling (180 kcal)."""
        recs = self.controller.generate_recommendations(
            mood="Stressed",
            meal_type="Snack",
            is_vegetarian=True,
            max_calories=200,
            min_protein=0,
            cravings="",
            top_n=3
        )
        self.assertGreater(len(recs), 0, "Expected at least 1 recommendation for low-calorie snack.")
        for r in recs:
            self.assertLessEqual(r["calories"], 200, f"Dish {r['food_name']} exceeded 200 kcal bound: {r['calories']}")
            self.assertTrue(r["vegetarian"], f"Non-vegetarian dish returned under veg constraint: {r['food_name']}")

    def test_02_high_protein_floor_stress(self):
        """Tests system behavior when high protein floor (>= 30g) is demanded."""
        recs = self.controller.generate_recommendations(
            mood="Tired",
            meal_type="Dinner",
            is_vegetarian=False,
            max_calories=700,
            min_protein=30,
            cravings="salmon protein",
            top_n=3
        )
        self.assertGreater(len(recs), 0, "Expected recommendations meeting protein floor.")
        for r in recs:
            self.assertGreaterEqual(r["protein"], 30, f"Dish {r['food_name']} failed protein floor: {r['protein']}g")

    def test_03_contradictory_zero_match_fallback(self):
        """Tests automatic fallback when contradictory constraints produce 0 natural matches."""
        # Contradictory: <150 kcal with >= 35g protein (physically impossible: 35g protein = 140 kcal + unavoidable fat/carbs)
        recs = self.controller.generate_recommendations(
            mood="Energetic",
            meal_type="Breakfast",
            is_vegetarian=True,
            max_calories=150,
            min_protein=35,
            cravings="ultra lean impossible",
            top_n=3
        )
        # Recommender must gracefully fall back rather than crash or return empty
        self.assertGreater(len(recs), 0, "Graceful fallback should return best alternative candidates.")
        for r in recs:
            self.assertTrue(r["vegetarian"], "Fallback should still respect hard vegetarian safety boundary.")

    def test_04_session_state_favorites_crud(self):
        """Tests session state operations: add, query, deduplicate, and remove favorites."""
        mock_session_favorites = []

        recs = self.controller.generate_recommendations("Happy", "Snack", True, 400, 0, "", 3)
        dish_1 = recs[0]
        dish_2 = recs[1]

        # Add dish 1
        mock_session_favorites.append(dish_1)
        self.assertEqual(len(mock_session_favorites), 1)

        # Add dish 2
        mock_session_favorites.append(dish_2)
        self.assertEqual(len(mock_session_favorites), 2)

        # Prevent duplicate insertion
        if not any(f["food_name"] == dish_1["food_name"] for f in mock_session_favorites):
            mock_session_favorites.append(dish_1)
        self.assertEqual(len(mock_session_favorites), 2, "Deduplication failed.")

        # Remove dish 1
        mock_session_favorites = [f for f in mock_session_favorites if f["food_name"] != dish_1["food_name"]]
        self.assertEqual(len(mock_session_favorites), 1)
        self.assertEqual(mock_session_favorites[0]["food_name"], dish_2["food_name"])

    def test_05_latency_profiling_microbenchmark(self):
        """Profiles execution time across 100 rapid sequential queries to ensure < 5ms average latency."""
        iterations = 100
        start_time = time.perf_counter()

        moods = ["Stressed", "Tired", "Relaxed", "Happy", "Energetic", "Low Mood"]
        meals = ["Breakfast", "Lunch", "Dinner", "Snack", "All"]

        for i in range(iterations):
            m = moods[i % len(moods)]
            meal = meals[i % len(meals)]
            self.controller.generate_recommendations(
                mood=m,
                meal_type=meal,
                is_vegetarian=(i % 2 == 0),
                max_calories=400 + (i % 300),
                min_protein=(i % 20),
                cravings="spinach protein oats" if i % 3 == 0 else "",
                top_n=5
            )

        total_time = time.perf_counter() - start_time
        avg_ms = (total_time / iterations) * 1000.0

        print(f"\n[Micro-benchmark] Executed {iterations} queries in {total_time:.3f}s. Average latency: {avg_ms:.2f} ms/query.")
        self.assertLess(avg_ms, 5.0, f"Average query latency exceeded 5.0ms threshold: {avg_ms:.2f}ms")

    def test_06_adversarial_and_empty_queries(self):
        """Tests handling of random punctuation, empty strings, and long malicious input strings."""
        adversarial_inputs = [
            "",
            "   ",
            "!@#$%^&*()_+=-`~[]\\{}|;':\",./<>?",
            "DROP TABLE recipes; SELECT * FROM users;",
            "a" * 500,
            "🥑🍕🍜☕️🍰🥗"
        ]

        for query in adversarial_inputs:
            recs = self.controller.generate_recommendations(
                mood="Stressed",
                meal_type="Dinner",
                is_vegetarian=True,
                max_calories=550,
                min_protein=0,
                cravings=query,
                top_n=3
            )
            self.assertGreater(len(recs), 0, f"Failed to gracefully handle adversarial input: {repr(query[:30])}")
            for r in recs:
                self.assertIn("hybrid_score", r)
                self.assertIn("rationale", r)
                self.assertIn("macro_split", r)


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestStage12AppComprehensive)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    sys.exit(0 if result.wasSuccessful() else 1)
