from litellm import completion
import json
import re


class KeywordExtractor:
    """Extract keywords from documents using LiteLLM."""

    def __init__(self, model: str = "gemini/gemini-2.5-flash"):
        """
        Initialize the KeywordExtractor.

        Args:
            model: LiteLLM model to use for extraction
        """
        self.model = model

    def _parse_text_file(self, file_path: str) -> str:
        """Parse plain text file."""
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()

    def _parse_json_file(self, file_path: str) -> str:
        """Parse JSON file and extract text content."""
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Extract all string values from the JSON
        def extract_text(obj):
            texts = []
            if isinstance(obj, dict):
                for value in obj.values():
                    texts.extend(extract_text(value))
            elif isinstance(obj, list):
                for item in obj:
                    texts.extend(extract_text(item))
            elif isinstance(obj, str):
                texts.append(obj)
            return texts

        extracted_text = extract_text(data)
        return " ".join(extracted_text)

    def _parse_markdown_file(self, file_path: str) -> str:
        """Parse Markdown file and extract plain text content."""
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Remove markdown syntax
        # Remove links [text](url)
        content = re.sub(r"\[([^\]]+)\]\([^\)]+\)", r"\1", content)
        # Remove bold/italic **text** or __text__
        content = re.sub(r"[*_]{2,3}([^*_]+)[*_]{2,3}", r"\1", content)
        # Remove inline code `code`
        content = re.sub(r"`([^`]+)`", r"\1", content)
        # Remove code blocks (```...```)
        content = re.sub(r"```[\s\S]*?```", "", content)
        # Remove headings (#, ##, etc.)
        content = re.sub(r"^#+\s+", "", content, flags=re.MULTILINE)
        # Remove HTML comments
        content = re.sub(r"<!--[\s\S]*?-->", "", content)

        return content

    def load_file(self, file_path: str) -> str:
        """
        Auto-detect and parse file based on extension.

        Args:
            file_path: Path to file (.txt, .json, or .md)

        Returns:
            Extracted text content
        """
        if file_path.endswith(".json"):
            return self._parse_json_file(file_path)
        elif file_path.endswith(".md"):
            return self._parse_markdown_file(file_path)
        else:
            # Default to plain text
            return self._parse_text_file(file_path)

    def get_input_text(self, text: str | None, file: str | None) -> str:
        """
        Get input text from either direct text or file.

        Args:
            text: Direct text input
            file: File path to load text from

        Returns:
            Text content to process
        """
        if text:
            return text
        elif file:
            return self.load_file(file)
        else:
            raise ValueError("Either text or file must be provided")

    def extract(self, text: str) -> list[str]:
        """
        Extract keywords from text using LiteLLM.

        Args:
            text: Text to extract keywords from

        Returns:
            Sorted list of unique keywords
        """
        prompt = f"""Extract the most important keywords from the following document.
Return ONLY a comma-separated list of keywords, nothing else.

Document:
\"\"\"{text}\"\"\""""

        response = completion(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
        )

        # Parse model output
        output = response["choices"][0]["message"]["content"]
        keywords = [k.strip() for k in output.split(",") if k.strip()]

        # Return unique, sorted keywords
        return sorted(list(set(keywords)))


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Extract keywords from documents using LiteLLM"
    )

    # Input options (mutually exclusive: either text or file)
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument("-t", "--text", help="Text to extract keywords from")
    input_group.add_argument(
        "-f", "--file", help="Path to file (supports .txt, .json, .md)"
    )

    parser.add_argument(
        "-m",
        "--model",
        default="gemini/gemini-2.5-flash",
        help="LiteLLM model to use (default: gemini/gemini-2.5-flash)",
    )

    parser.add_argument(
        "-o",
        "--output",
        choices=["text", "json"],
        default="text",
        help="Output format (default: text)",
    )

    args = parser.parse_args()

    # Initialize extractor with specified model
    extractor = KeywordExtractor(model=args.model)

    # Get input text
    document_text = extractor.get_input_text(args.text, args.file)

    # Extract keywords
    keywords = extractor.extract(document_text)

    # Output results
    if args.output == "json":
        print(json.dumps({"keywords": keywords}))
    else:
        print("Extracted Keywords:")
        for keyword in keywords:
            print(f"  - {keyword}")
