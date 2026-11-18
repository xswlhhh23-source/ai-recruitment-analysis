import unittest

from src.analyzer import analyze_job_fit, extract_skills


class AnalyzerTests(unittest.TestCase):
    def test_extracts_english_and_chinese_aliases(self):
        found = extract_skills("熟悉 Excel、VLOOKUP 和数据分析，了解 SQL。")
        labels = {item["label"] for item in found}
        self.assertIn("Excel", labels)
        self.assertIn("VLOOKUP", labels)
        self.assertIn("Data analysis", labels)
        self.assertIn("SQL", labels)

    def test_calculates_match_ratio(self):
        result = analyze_job_fit(
            "要求 Excel、SQL、Python",
            "使用 Excel 和 SQL 完成课程项目",
        )
        self.assertEqual(result["total_requirements"], 3)
        self.assertEqual(len(result["matched"]), 2)
        self.assertEqual(len(result["gaps"]), 1)
        self.assertAlmostEqual(result["match_ratio"], 66.6666, places=2)

    def test_empty_taxonomy_result_is_safe(self):
        result = analyze_job_fit("团队合作，积极主动", "认真负责")
        self.assertEqual(result["total_requirements"], 0)
        self.assertEqual(result["match_ratio"], 0.0)
        self.assertTrue(result["suggestions"])


if __name__ == "__main__":
    unittest.main()
