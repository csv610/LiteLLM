from nobel_prize_prompts import PromptBuilder

def test_create_nobel_prize_prompt():
    category = "Physics"
    year = "2020"
    prompt = PromptBuilder.create_nobel_prize_prompt(category, year)
    assert category in prompt
    assert year in prompt
    assert "BIOGRAPHICAL INFORMATION" in prompt
    assert "SCIENTIFIC WORK" in prompt
    assert "EDUCATIONAL CONTENT" in prompt

def test_create_validation_prompt():
    prompt = PromptBuilder.create_validation_prompt()
    assert "accuracy" in prompt.lower()
    assert "completeness" in prompt.lower()
