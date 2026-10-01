import unittest

from dernivtrsimplfd import improve_function, invert, simplify


class ImprovedFunctionTests(unittest.TestCase):
    def test_simplify_removes_blank_values_and_strips_text(self):
        payload = {"name": "  Alice  ", "nickname": "", "active": True, "count": 0, "ignored": None}

        self.assertEqual(simplify(payload), {"name": "Alice", "active": True, "count": 0})

    def test_invert_swaps_mapping_keys_and_values(self):
        payload = {"alpha": "beta", "gamma": "delta"}

        self.assertEqual(invert(payload), {"beta": "alpha", "delta": "gamma"})

    def test_improve_function_uses_new_concept_pipeline(self):
        payload = {"name": "  Bob  ", "middle": "", "numbers": [1, 2, 3, None, "   "]}

        improved = improve_function(payload, invert_data=True)
        self.assertEqual(improved, {"Bob": "name", "[1, 2, 3]": "numbers"})

    def test_improve_function_supports_direct_simplify_only(self):
        payload = ["  one  ", "", None, "two", 7]

        self.assertEqual(improve_function(payload, invert_data=False, simplify_data=True), ["one", "two", 7])

    def test_improve_function_rejects_unknown_concepts(self):
        with self.assertRaises(ValueError):
            improve_function({"name": "Alice"}, concept="legacy")


if __name__ == "__main__":
    unittest.main()
