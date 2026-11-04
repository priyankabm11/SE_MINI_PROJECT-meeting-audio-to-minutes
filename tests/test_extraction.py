
import unittest

from app.extraction import extract_minutes


class TestExtractMinutes(unittest.TestCase):

    # 1. Test empty transcript
    def test_empty_transcript(self):
        result = extract_minutes("")

        self.assertEqual(result["topics"], [])
        self.assertEqual(result["decisions"], [])
        self.assertEqual(result["action_items"], [])

    # 2. Test non-string transcript
    def test_non_string_transcript(self):
        result = extract_minutes(None)

        self.assertEqual(result["topics"], [])
        self.assertEqual(result["decisions"], [])
        self.assertEqual(result["action_items"], [])

    # 3. Test topics and decisions
    def test_extract_topics_and_decisions(self):
        transcript = (
            "We discussed the project timeline. "
            "We decided to move the meeting to Friday."
        )

        result = extract_minutes(transcript)

        self.assertTrue(result["topics"])
        self.assertTrue(result["decisions"])

        self.assertIn(
            "We decided to move the meeting to Friday.",
            result["decisions"],
        )

    # 4. Test action item, owner and deadline
    def test_extract_action_owner_and_deadline(self):
        transcript = "Priya will prepare the report by Monday."

        result = extract_minutes(transcript)

        self.assertEqual(len(result["action_items"]), 1)

        item = result["action_items"][0]

        self.assertEqual(item["owner"], "Priya")
        self.assertEqual(item["deadline"], "Monday")
        self.assertIn("prepare the report", item["task"])

    # 5. Test missing owner
    def test_missing_owner(self):
        transcript = "The team will prepare the report by Monday."

        result = extract_minutes(transcript)

        self.assertEqual(len(result["action_items"]), 1)

        item = result["action_items"][0]

        self.assertIsNone(item["owner"])
        self.assertEqual(item["deadline"], "Monday")

    # 6. Test missing deadline
    def test_missing_deadline(self):
        transcript = "Priya will prepare the report."

        result = extract_minutes(transcript)

        self.assertEqual(len(result["action_items"]), 1)

        item = result["action_items"][0]

        self.assertEqual(item["owner"], "Priya")
        self.assertIsNone(item["deadline"])

    # 7. Test duplicate topics and decisions
    def test_duplicate_topics_and_decisions(self):
        transcript = (
            "We discussed the project timeline. "
            "We discussed the project timeline. "
            "We decided to move the meeting. "
            "We decided to move the meeting."
        )

        result = extract_minutes(transcript)

        self.assertEqual(len(result["topics"]), 1)
        self.assertEqual(len(result["decisions"]), 1)

    # 8. Test duplicate action items
    def test_duplicate_action_items(self):
        transcript = (
            "Priya will prepare the report. "
            "Priya will prepare the report."
        )

        result = extract_minutes(transcript)

        # Current extractor retains duplicate action items.
        self.assertEqual(len(result["action_items"]), 2)

    # 9. Test sentence without action item
    def test_sentence_without_action_item(self):
        transcript = "The weather is pleasant today."

        result = extract_minutes(transcript)

        self.assertEqual(result["action_items"], [])


if __name__ == "__main__":
    unittest.main()
