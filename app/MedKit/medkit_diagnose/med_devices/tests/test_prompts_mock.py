import unittest

from medical_test_devices_prompts import PromptBuilder


class TestPromptBuilder(unittest.TestCase):
    def test_create_system_prompt(self):
        system_prompt = PromptBuilder.create_system_prompt()
        self.assertIsInstance(system_prompt, str)
        self.assertIn("medical device information specialist", system_prompt)
        self.assertIn("FDA", system_prompt)

    def test_create_user_prompt(self):
        device_name = "Ultrasound Machine"
        user_prompt = PromptBuilder.create_user_prompt(device_name)
        self.assertIsInstance(user_prompt, str)
        self.assertIn(device_name, user_prompt)
        self.assertIn("Intended use and applications", user_prompt)


if __name__ == "__main__":
    unittest.main()
