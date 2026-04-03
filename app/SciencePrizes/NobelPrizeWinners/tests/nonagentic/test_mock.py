import unittest
from unittest.mock import MagicMock, patch
import sys
from pathlib import Path

# Add project root to sys.path to ensure we can import the local modules
# In this environment, it seems the structure is assumed to be NobelPrizeWinners/nonagentic
# and we might need to adjust sys.path if we want to import NobelPrizeWinnerInfo properly
# since it also tries to import 'lite'
current_dir = Path(__file__).parent
if str(current_dir) not in sys.path:
    sys.path.insert(0, str(current_dir))

# Mock 'lite' before importing NobelPrizeWinnerInfo if it's not available
# or just patch it during the test.
# Let's try to import and see if it fails.
try:
    from nobel_prize_explorer import NobelPrizeWinnerInfo
    from nobel_prize_models import PrizeWinner, PrizeResponse, PersonalBackground, CareerPosition, BroaderRecognition, FAQItem, GlossaryItem
except ImportError as e:
    print(f"Import error: {e}")
    # If imports fail due to 'lite' missing, we might need to mock it in sys.modules
    mock_lite = MagicMock()
    sys.modules["lite"] = mock_lite
    sys.modules["lite.lite_client"] = mock_lite.lite_client
    sys.modules["lite.config"] = mock_lite.config
    sys.modules["lite.logging_config"] = mock_lite.logging_config
    
    from nobel_prize_explorer import NobelPrizeWinnerInfo
    from nobel_prize_models import PrizeWinner, PrizeResponse, PersonalBackground, CareerPosition, BroaderRecognition, FAQItem, GlossaryItem

class TestNobelPrizeWinnerInfoMock(unittest.TestCase):
    @patch('nobel_prize_explorer.LiteClient')
    def test_fetch_winners_mock(self, mock_lite_client_class):
        # Setup mock client
        mock_client_instance = mock_lite_client_class.return_value
        
        # Create a mock PrizeWinner
        mock_winner = PrizeWinner(
            name="Pierre Agostini",
            year=2023,
            category="Physics",
            contribution="Experimental methods that generate attosecond pulses of light for the study of electron dynamics in matter.",
            personal_background=PersonalBackground(
                birth_date="1941-07-23",
                birth_place="Tunis, Tunisia",
                nationality="French-American",
                family_background="Grew up in Tunisia and France.",
                education=["Ph.D. Physics, Aix-Marseille University (1968)"],
                early_influences="Mentored by leading researchers in atomic physics."
            ),
            career_timeline=[
                CareerPosition(
                    title="Professor",
                    institution="Ohio State University",
                    location="Columbus, USA",
                    start_year=2005,
                    description="Research in attosecond physics."
                )
            ],
            broader_recognition=BroaderRecognition(
                honors_and_awards=["Nobel Prize in Physics (2023)"],
                academy_memberships=["Member of National Academy of Sciences"],
                editorial_roles=[],
                mentorship_contributions="Mentored many students in ultrafast optics.",
                leadership_roles=[],
                public_engagement="Public lectures on attosecond science."
            ),
            history="Developed techniques for characterizing attosecond pulses that allow for the study of electron dynamics in matter at extremely short timescales.",
            impact="Revolutionized time-resolved spectroscopy by allowing scientists to observe electronic processes that occur in attoseconds, which was previously impossible.",
            foundation="Impacted fields like solid state physics and chemistry by providing a new tool to study quantum mechanical effects in real-time within atoms and molecules.",
            applications=["Study of electron motion in molecules"],
            relevancy="Attosecond pulses are key to understanding quantum processes and are currently being used to develop faster electronics and understand chemical reactions better.",
            advancements=["Higher harmonic generation improvements"],
            refinements=["Pulse duration measurement techniques"],
            gaps=["Improving pulse intensity and accessibility"],
            keywords=["Attosecond", "Electrons", "Ultrafast"],
            learning_objectives=["Understand light-matter interaction"],
            faq=[FAQItem(question="What is an attosecond?", answer="10^-18 seconds")],
            glossary=[GlossaryItem(term="Attosecond", definition="Extremely short unit of time")]
        )
        
        mock_response = PrizeResponse(winners=[mock_winner])
        mock_client_instance.generate_text.return_value = mock_response
        
        # Initialize explorer
        mock_model_config = MagicMock()
        mock_model_config.model = "test-model"
        explorer = NobelPrizeWinnerInfo(mock_model_config)
        
        # Call the method
        winners = explorer.fetch_winners("Physics", "2023")
        
        # Assertions
        self.assertEqual(len(winners), 1)
        self.assertEqual(winners[0].name, "Pierre Agostini")
        self.assertEqual(winners[0].year, 2023)
        mock_client_instance.generate_text.assert_called_once()

    def test_invalid_model_name(self):
        # Initialize explorer
        mock_model_config = MagicMock()
        mock_model_config.model = "test-model"
        # Mock LiteClient during initialization
        with patch('nobel_prize_explorer.LiteClient'):
            explorer = NobelPrizeWinnerInfo(mock_model_config)
        
        # Call with invalid model name
        with self.assertRaisesRegex(ValueError, "Invalid model name"):
            explorer.fetch_winners("Physics", "2023", model="invalid*model")

if __name__ == "__main__":
    unittest.main()
