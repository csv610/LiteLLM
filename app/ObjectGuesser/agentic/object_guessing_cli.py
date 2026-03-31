import argparse
from .object_guesser_game import ObjectGuesserGame

def object_guesser_cli():
    """Main entry point for the multi-agent guessing game."""
    parser = argparse.ArgumentParser(
        description="Play a multi-agent object guessing game with an LLM"
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

    # Note: The new multi-agent game uses low temperature internally for state/extraction
    # but could use the arg for strategy if we wanted to pass it through.
    game = ObjectGuesserGame(model=args.model, temperature=args.temperature, max_questions=args.max_questions)
    game.play()

if __name__ == "__main__":
    object_guesser_cli()
