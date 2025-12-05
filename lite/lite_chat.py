"""Unified LiteChat for text and vision model interactions."""

import argparse
import logging
import os
from datetime import datetime
from typing import Any, Dict, List, Optional, Union

from litellm import completion, APIError

from lite import __version__
from lite.config import ModelConfig, ChatConfig, ModelInput, DEFAULT_TEMPERATURE
from lite.image_utils import ImageUtils

logger = logging.getLogger(__name__)
DEFAULT_MAX_HISTORY = 10

class LiteChat:
    """Unified client for interacting with both text and vision models."""

    @staticmethod
    def handle_generation_exception(
        error: Exception,
        is_image_request: bool
    ) -> Union[str, Dict[str, Any]]:
        """
        Handle exceptions from generate_text with appropriate logging and response format.

        Args:
            error: The exception that was raised
            is_image_request: Whether the request involved image analysis

        Returns:
            Error message formatted as string or dict depending on request type
        """
        if isinstance(error, FileNotFoundError):
            error_msg = f"File error: {str(error)}"
        elif isinstance(error, ValueError):
            error_msg = f"Validation Error: {str(error)}"
        elif isinstance(error, APIError):
            error_msg = f"API Error: {str(error)}"
        else:
            error_msg = f"Unexpected error: {str(error)}"

        logger.error(error_msg)

        # Return dict for image requests, string for text-only requests
        return {"error": error_msg} if is_image_request else error_msg

    def __init__(self, model_config: Optional[ModelConfig] = None, chat_config: Optional[ChatConfig] = None):
        """
        Initialize LiteChat with optional ModelConfig and ChatConfig.

        Args:
            model_config: Optional ModelConfig instance for model configuration.
            chat_config: Optional ChatConfig instance for chat session management.
        """
        self.model_config = model_config
        chat_config = chat_config or ChatConfig()
        # Ensure max_history is an even number to maintain prompt-response pairs
        self.max_history = chat_config.max_history
        if self.max_history % 2 != 0:
            logger.warning(
                f"max_history ({self.max_history}) is not an even number. "
                "Decrementing to {self.max_history - 1} to maintain prompt-response pairs."
            )
            self.max_history -= 1
        self.auto_save = chat_config.auto_save
        self.save_dir = chat_config.save_dir
        self.conversation_history: List[Dict[str, Any]] = []
        self.conversation_file: Optional[str] = None
        self._file_initialized = False
        self.image_cache: Dict[int, List[Dict[str, Any]]] = {}  # Maps turn_number -> images
        self._turn_counter = 0  # Global turn counter for image tracking

    @staticmethod
    def _format_content(content: Any) -> str:
        """
        Format content for display, extracting text from list-based content.

        Args:
            content: Message content (string or list of content blocks)

        Returns:
            Formatted string content
        """
        if isinstance(content, list):
            text_parts = [item.get("text", "") for item in content if item.get("type") == "text"]
            return " ".join(text_parts) if text_parts else str(content)
        return str(content)

    def _reconstruct_messages_with_images(self) -> List[Dict[str, Any]]:
        """
        Reconstruct messages by merging conversation history with cached images.

        Images are always included from the cache, regardless of whether their
        original message is still in history (after trimming).

        Returns:
            Full message list with images included for API calls
        """
        reconstructed = []
        for idx, msg in enumerate(self.conversation_history):
            if idx in self.image_cache:
                # User message with images - reconstruct full content
                content = msg["content"].copy() if isinstance(msg["content"], list) else [{"type": "text", "text": msg["content"]}]
                content.extend(self.image_cache[idx])
                reconstructed.append({"role": msg["role"], "content": content})
            else:
                # No images - use as-is
                reconstructed.append(msg)

        # Add any cached images that don't correspond to messages in current history
        # (these are from messages that were trimmed but images should persist)
        for cache_idx, image_blocks in self.image_cache.items():
            if cache_idx >= len(self.conversation_history):
                # This is a cached image from a trimmed message - add a synthetic message for it
                reconstructed.append({
                    "role": "user",
                    "content": image_blocks
                })

        return reconstructed

    def add_message_to_history(self, role: str, content: Any) -> None:
        """
        Add a message to conversation history.

        Args:
            role: Message role ("user" or "assistant")
            content: Message content (string or list of content blocks)
        """
        self.conversation_history.append({"role": role, "content": content})

        # Trim history if it exceeds max_history, ensuring full prompt-response pairs are removed.
        # This loop removes pairs from the beginning until the history length is within limits
        # and maintains a coherent conversational flow.
        # Note: Images in the cache persist and are always sent to the API.
        while len(self.conversation_history) > self.max_history:
            if len(self.conversation_history) >= 2:
                # Remove the oldest user message
                self.conversation_history.pop(0)
                # Remove the corresponding oldest assistant message
                self.conversation_history.pop(0)
            else:
                # If only one message remains and it still exceeds max_history (e.g., max_history is 0),
                # remove that single message. This handles edge cases where max_history is very small.
                self.conversation_history.pop(0)
                break # Exit loop after removing the last message if no pair can be formed.


    def create_message(self, model_input: ModelInput) -> List[Dict[str, Any]]:
        """
        Create a message for the model, including conversation history.

        Args:
            model_input: ModelInput object containing prompt and image parameters

        Returns:
            Message list formatted for the completion API with full conversation history
        """
        if not model_input.user_prompt or not model_input.user_prompt.strip():
            raise ValueError("user_prompt cannot be empty")

        # Build content with text
        text_content = [{"type": "text", "text": model_input.user_prompt}]
        image_blocks = []

        # Handle images separately
        if model_input.image_path:
            base64_url = ImageUtils.encode_to_base64(model_input.image_path)
            image_block = {"type": "image_url", "image_url": {"url": base64_url}}
            image_blocks.append(image_block)

        # Cache images using turn counter (persists even if message is trimmed from history)
        if image_blocks:
            self.image_cache[self._turn_counter] = image_blocks

        # Increment turn counter for next message
        self._turn_counter += 1

        # Add text-only content to history
        self.add_message_to_history("user", text_content)

        # Return reconstructed messages with images for API call
        return self._reconstruct_messages_with_images()

    def generate_text(
        self,
        model_input: ModelInput,
        model_config: Optional[ModelConfig] = None,
    ) -> Union[str, Dict[str, Any]]:
        """
        Generate text from a prompt or analyze an image with a prompt.

        Args:
            model_input: ModelInput object containing prompt and image parameters
            model_config: Optional ModelConfig object for model configuration.
                         If not provided, uses the instance's model_config.

        Returns:
            Generated text response or error message
        """
        # Use provided model_config or instance's model_config
        config = model_config or self.model_config
        if not config:
            raise ValueError("ModelConfig must be provided either as argument or during initialization")

        try:
            log_action = "Analyzing image" if model_input.image_path else "Generating text"
            logger.info(f"{log_action} with model: {config.model}")

            # Create message and call completion
            messages = self.create_message(model_input)

            response = completion(
                model=config.model,
                messages=messages,
                temperature=config.temperature,
                response_format=model_input.response_format,
            )

            logger.info("Request successful")
            assistant_response = response.choices[0].message.content

            # Add assistant response to history
            self.add_message_to_history("assistant", assistant_response)

            # Auto-save conversation if enabled
            if self.auto_save:
                self.save_conversation()

            return assistant_response

        except (FileNotFoundError, ValueError, APIError) as e:
            is_image_request = model_input.image_path is not None
            return self.handle_generation_exception(e, is_image_request)
        except Exception as e:
            logger.error(f"Unexpected error during generation: {str(e)}")
            is_image_request = model_input.image_path is not None
            return self.handle_generation_exception(e, is_image_request)

    def reset_conversation(self) -> None:
        """Clear conversation history, image cache, and turn counter."""
        self.conversation_history = []
        self.image_cache = {}
        self._turn_counter = 0
        logger.info("Conversation history cleared")

    def get_conversation_history(self) -> List[Dict[str, Any]]:
        """
        Get the full conversation history.

        Returns:
            List of all messages in the conversation
        """
        return self.conversation_history.copy()

    def save_conversation(self) -> None:
        """
        Append the latest user and assistant messages to a markdown file.
        File is created once with a human-readable timestamp.
        """

        # Initialize file on first call
        if not self._file_initialized:
            timestamp = datetime.now().strftime("%d-%m-%Y@%H:%M:%S")
            filename = f"conversation_{timestamp}.md"
            self.conversation_file = os.path.join(self.save_dir, filename)
            with open(self.conversation_file, "w") as f:
                f.write(f"# Conversation\n\n")
                f.write(f"*Started at: {timestamp}*\n\n")
            self._file_initialized = True

        # Append the last user message and assistant message
        if len(self.conversation_history) >= 2:
            with open(self.conversation_file, "a") as f:
                user_msg = self.conversation_history[-2]
                assistant_msg = self.conversation_history[-1]

                user_role = user_msg["role"].capitalize()
                user_content = self._format_content(user_msg["content"])
                f.write(f"**{user_role}:** {user_content}\n\n")

                assistant_role = assistant_msg["role"].capitalize()
                assistant_content = self._format_content(assistant_msg["content"])
                f.write(f"**{assistant_role}:** {assistant_content}\n\n")
            logger.info(f"Conversation appended to {self.conversation_file}")

def cli():
    """Main entry point for the LiteChat CLI interactive chat."""
    parser = argparse.ArgumentParser(
        description="Interactive multi-turn chat with vision model support"
    )

    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
        help="Show program's version number and exit",
    )
    parser.add_argument(
        "-i",
        "--image_path",
        type=str,
        default=None,
        help="Path to the image file for the first message (vision analysis)",
    )
    parser.add_argument(
        "-m",
        "--model",
        type=str,
        default="gemini/gemini-2.5-flash",
        help="The model identifier (default: gemini/gemini-2.5-flash)",
    )
    parser.add_argument(
        "-t",
        "--temperature",
        type=float,
        default=DEFAULT_TEMPERATURE,
        help=f"Sampling temperature (default: {DEFAULT_TEMPERATURE})",
    )
    parser.add_argument(
        "--max-history",
        type=int,
        default=DEFAULT_MAX_HISTORY,
        help=f"Maximum number of messages to keep in conversation history (default: {DEFAULT_MAX_HISTORY})",
    )
    parser.add_argument(
        "--auto-save",
        action="store_true",
        help="Automatically save conversation to a markdown file after each turn",
    )
    parser.add_argument(
        "--save-dir",
        type=str,
        default=".",
        help="Directory to save conversation files (default: current directory)",
    )

    args = parser.parse_args()

    # Initialize client with ModelConfig and ChatConfig
    model_config = ModelConfig(model=args.model, temperature=args.temperature)
    chat_config = ChatConfig(
        max_history=args.max_history,
        auto_save=args.auto_save,
        save_dir=args.save_dir
    )
    client = LiteChat(
        model_config=model_config,
        chat_config=chat_config
    )

    # Handle initial image if provided
    if args.image_path:
        print(f"Image loaded: {args.image_path}\n")
        first_image_path = args.image_path
    else:
        first_image_path = None

    # Build help text based on auto-save setting
    help_text = "Interactive multi-turn chat mode. Type 'exit' to quit, 'history' to view conversation, 'clear' to reset."
    if args.auto_save:
        help_text += f" Conversations auto-save to '{args.save_dir}' after each turn."
    print(f"{help_text}\n")

    first_turn = True
    while True:
        try:
            user_input = input("You: ").strip()

            if user_input.lower() == "exit":
                print("Exiting chat...")
                break
            elif user_input.lower() == "history":
                history = client.get_conversation_history()
                if not history:
                    print("No conversation history yet.\n")
                else:
                    print("\n--- Conversation History ---")
                    for msg in history:
                        role = msg["role"].capitalize()
                        content = LiteChat._format_content(msg["content"])
                        print(f"{role}: {content}\n")
                    print("--- End History ---\n")
                continue
            elif user_input.lower() == "clear":
                client.reset_conversation()
                print("Conversation cleared.\n")
                continue
            elif not user_input:
                continue

            # Use image path only on first turn if provided
            image_path = first_image_path if first_turn else None
            first_turn = False

            model_input = ModelInput(
                user_prompt=user_input,
                image_path=image_path
            )
            result = client.generate_text(model_input=model_input)
            print(f"Assistant: {result}\n")

        except KeyboardInterrupt:
            print("\n\nExiting chat...")
            break


if __name__ == "__main__":
    cli()
