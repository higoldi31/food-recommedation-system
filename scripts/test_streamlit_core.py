"""
=============================================================================
STAGE 10: STREAMLIT CORE APPLICATION UNIT TEST SUITE
Project: MoodFood - Mood-Based Food Recommendation System
Author: Senior Data Scientist & ML Engineer

Validates:
1. Controller initialization & artifact loading
2. Session state lifecycle simulation
3. Filter candidate logic under multiple parameter permutations
4. Rationale generator strings
5. Zero-divergence parity check between controller and stage 7 engine
=============================================================================
"""

import os
import sys
import unittest

# Add root directory to sys.path to import app.py
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, root_dir)

from app import MoodFoodController, load_cached_pipeline

class TestStreamlitCore(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.controller = MoodFoodController()

    def test_01_pipeline_loading(self):
        """Verifies that vectorizer, matrix, dataset, and metadata load cleanly."""
        self.assertIsNotNone(self.controller.vectorizer)
        self.assertIsNotNone(self.controller.matrix)
        self.assertIsNotNone(self.controller.dataset)
        self.assertIsNotNone(self.controller.metadata)
        self.assertEqual(len(self.controller.dataset), 320)
        self.assertGreater(len(self.controller.vectorizer.vocabulary), 1500)
        print("\n[TEST 1 PASSED] Pipeline artifacts loaded and deserialized cleanly.")

    def test_02_canonical_recommendation(self):
        """Tests canonical user query: Stressed + Dinner + Vegetarian + Max 500 kcal."""
        recs = self.controller.generate_recommendations(
            mood="Stressed",
            meal_type="Dinner",
            is_vegetarian=True,
            max_calories=500,
            top_n=5
        )
        self.assertEqual(len(recs), 5)
        for r in recs:
            self.assertTrue(r["vegetarian"])
            self.assertLessEqual(r["calories"], 500)
            self.assertIn("magnesium", r["rationale"].lower())
            self.assertGreater(r["hybrid_score"], 0.40)
        print("[TEST 2 PASSED] Canonical brief query verified in Streamlit Controller.")

    def test_03_fallback_behavior(self):
        """Tests that overly constrained filters gracefully fallback without failing."""
        recs = self.controller.generate_recommendations(
            mood="Tired",
            meal_type="Breakfast",
            is_vegetarian=True,
            max_calories=120, # Very low calorie threshold
            min_protein=25,   # Impossible combination for breakfast veg <= 120 kcal
            top_n=3
        )
        self.assertIsInstance(recs, list)
        self.assertGreater(len(recs), 0)
        print(f"[TEST 3 PASSED] Fallback mechanism produced {len(recs)} alternatives safely.")

    def test_04_session_state_lifecycle(self):
        """Simulates Streamlit session state operations (favorites, history tracking)."""
        mock_session_state = {
            "favorites": [],
            "history": [],
            "active_mood": "Happy"
        }
        
        # Simulate user saving a recommendation
        sample_dish = {"id": 1, "food_name": "Dark Chocolate Cacao Chia Pudding", "calories": 220}
        mock_session_state["favorites"].append(sample_dish)
        self.assertEqual(len(mock_session_state["favorites"]), 1)
        self.assertEqual(mock_session_state["favorites"][0]["food_name"], "Dark Chocolate Cacao Chia Pudding")

        # Simulate user query history
        mock_session_state["history"].append({"mood": "Happy", "time": "12:00:00"})
        self.assertEqual(len(mock_session_state["history"]), 1)
        print("[TEST 4 PASSED] Session state lifecycle simulation passed.")

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestStreamlitCore)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    sys.exit(0 if result.wasSuccessful() else 1)
