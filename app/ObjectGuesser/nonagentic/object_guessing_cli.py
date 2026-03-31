import argparse
from .object_guesser_game import ObjectGuessingGame

def object_guesser_cli():
    """Main entry point for the game."""
    parser = argparse.ArgumentParser(
        description="Play an object guessing game with an LLM"
    )
    parser.add_argument(
        "-m", "--model",
        default="ollama/gemma3",
        help="Model to use (default: ollama/gemma3)",
    )
    parser.add_argument(
        "--temperature",
        type=float,
        default=0.7,
        help="Temperature for model responses (default: 0.7)",
    )
    parser.add_argument(
        "--max-questions",
        type=int,
        default=20,
        help="Maximum number of questions allowed (default: 20)",
    )

    args = parser.parse_args()

    game = ObjectGuessingGame(model=args.model, temperature=args.temperature, max_questions=args.max_questions)
    game.play()

if __name__ == "__main__":
    object_guesser_cli()
