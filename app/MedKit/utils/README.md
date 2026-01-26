# Utilities Module

Shared utilities and helper functions for MedKit.

## Overview

The Utilities Module provides reusable components, base classes, error handling, logging, and helper functions used across all MedKit modules.

## Module Components

```
utils/
├── cli_base.py                 # Base classes for CLI modules
├── error_handler.py            # Error handling utilities
├── error_recovery.py           # Error recovery patterns
├── output_formatter.py         # Output formatting
├── privacy_compliance.py       # Privacy and compliance
├── storage_config.py           # Storage configuration
├── logging_config.py           # Logging configuration
├── pydantic_prompt_generator.py # Prompt generation helpers
├── biomcp_article_search.py    # Article search
├── ddg_images.py               # Image search
├── sl_ddg_images.py            # Alternative image search
├── sl_ddg_videos.py            # Video search
├── update_question_ids.py      # Question ID management
└── __init__.py                 # Module initialization
```

## Core Components

### 1. BaseCLI: Command-Line Interface Base Class

Provides unified interface for all CLI modules.

```python
from utils.cli_base import BaseCLI
import argparse

class MyModuleCLI(BaseCLI):
    def setup_arguments(self, parser: argparse.ArgumentParser):
        parser.add_argument('--input', required=True)
        parser.add_argument('--output')

    def execute(self, args: argparse.Namespace):
        # Implementation here
        pass
```

**Features**:
- Unified argument parsing
- Automatic help generation
- Logging setup
- Error handling
- LiteClient initialization

### 2. BaseGenerator: LLM Processing Base Class

Manages LLM interactions with error handling.

```python
from utils.cli_base import BaseGenerator
from lite.lite_client import LiteClient
from pydantic import BaseModel

class MyGenerator(BaseGenerator):
    def generate_text(self, input_data: str) -> MyOutput:
        response = self.call_llm(system_prompt, user_prompt)
        return MyOutput.parse_raw(response)
```

**Features**:
- LLM client management
- Error handling and retries
- Structured output support
- Logging integration

### 3. BasePromptBuilder: Prompt Template Base Class

Centralizes prompt creation.

```python
from utils.cli_base import BasePromptBuilder

class MyPromptBuilder(BasePromptBuilder):
    @staticmethod
    def create_system_prompt() -> str:
        return "You are a domain expert..."

    @staticmethod
    def create_user_prompt(data: str) -> str:
        return f"Process this: {data}"
```

**Features**:
- Consistent prompt creation
- System and user prompt separation
- Structured output format specification
- Reusability across modules

### 4. Error Handler: Exception Management

Comprehensive error handling utilities.

```python
from utils.error_handler import ErrorHandler
from medkit_exceptions import MedKitError

try:
    result = generator.generate_text("input")
except MedKitError as e:
    handled_result = ErrorHandler.handle_medkit_error(e)
```

**Features**:
- Custom exception hierarchy
- Error categorization
- Recovery suggestions
- Logging integration

### 5. Error Recovery: Retry Logic

Automatic retry with backoff.

```python
from utils.error_recovery import retry_with_backoff

@retry_with_backoff(max_retries=3, backoff_factor=2)
def call_generator():
    return generator.generate_text("input")
```

**Features**:
- Exponential backoff
- Configurable retry count
- Error condition handling
- Logging of retries

### 6. Output Formatter: Result Formatting

Format and display results.

```python
from utils.output_formatter import print_result

print_result(
    title="Medicine Information",
    data=result.dict(),
    format="json"
)
```

**Features**:
- Multiple output formats
- Console formatting
- File output
- Data structuring

### 7. Privacy Compliance: Data Protection

Handle sensitive data securely.

```python
from utils.privacy_compliance import PrivacyHandler

# De-identify data
sanitized = PrivacyHandler.remove_pii(data)

# Encrypt output
encrypted = PrivacyHandler.encrypt_data(data)
```

**Features**:
- PII removal
- Data encryption
- HIPAA compliance
- GDPR support

### 8. Storage Configuration: File Management

Manage file paths and storage.

```python
from utils.storage_config import StorageConfig

config = StorageConfig()
output_path = config.get_output_path("medicine_info")
```

**Features**:
- Path management
- Directory creation
- File organization
- Configuration loading

## Usage Examples

### Example 1: Creating a New CLI Module

```python
from utils.cli_base import BaseCLI, BaseGenerator, BasePromptBuilder
from pydantic import BaseModel

class OutputModel(BaseModel):
    result: str

class MyPromptBuilder(BasePromptBuilder):
    @staticmethod
    def create_system_prompt() -> str:
        return "You are helpful..."

    @staticmethod
    def create_user_prompt(input_data: str) -> str:
        return f"Process: {input_data}"

class MyGenerator(BaseGenerator):
    def generate_text(self, input_data: str) -> OutputModel:
        system = MyPromptBuilder.create_system_prompt()
        user = MyPromptBuilder.create_user_prompt(input_data)
        response = self.call_llm(system, user, structured=True)
        return OutputModel.parse_raw(response)

class MyCLI(BaseCLI):
    def setup_arguments(self, parser):
        parser.add_argument('--input', required=True)
        parser.add_argument('--output')

    def execute(self, args):
        generator = MyGenerator(self.client)
        return generator.generate_text(args.input)

if __name__ == '__main__':
    cli = MyCLI()
    cli.run()
```

### Example 2: Error Handling

```python
from medkit_exceptions import MedKitError, ValidationError, LLMError
from utils.error_handler import ErrorHandler

try:
    result = generator.generate_text("input")
except ValidationError as e:
    print(f"Input error: {e}")
    error_result = ErrorHandler.handle_validation_error(e)
except LLMError as e:
    print(f"LLM error: {e}")
    error_result = ErrorHandler.handle_llm_error(e)
except MedKitError as e:
    error_result = ErrorHandler.handle_medkit_error(e)
```

### Example 3: Retry Logic

```python
from utils.error_recovery import retry_with_backoff

@retry_with_backoff(max_retries=3, backoff_factor=2)
def get_medicine_info(medicine: str):
    generator = MedicineInfoGenerator()
    return generator.generate_text(medicine, structured=True)

# Will retry up to 3 times with exponential backoff
result = get_medicine_info("aspirin")
```

### Example 4: Output Formatting

```python
from utils.output_formatter import print_result
import json

# Format and print result
print_result(
    title="Medicine Information",
    data=result.dict(),
    format="json"
)

# Save to file
with open("result.json", "w") as f:
    json.dump(result.dict(), f, indent=2)
```

### Example 5: Privacy Handling

```python
from utils.privacy_compliance import PrivacyHandler

# Remove personally identifiable information
data_with_pii = {
    "patient_name": "John Doe",
    "ssn": "123-45-6789",
    "medical_info": "Has diabetes"
}

sanitized = PrivacyHandler.remove_pii(data_with_pii)
# Returns data without PII
```

## Base Class Patterns

### CLI Module Pattern

```python
# 1. Inherit from BaseCLI
class MyModuleCLI(BaseCLI):
    # 2. Implement setup_arguments
    def setup_arguments(self, parser):
        parser.add_argument('--input', required=True)

    # 3. Implement execute
    def execute(self, args):
        generator = MyGenerator(self.client)
        return generator.generate_text(args.input)

# 4. Provide CLI entry point
if __name__ == '__main__':
    cli = MyModuleCLI()
    cli.run()
```

### Generator Pattern

```python
# 1. Inherit from BaseGenerator
class MyGenerator(BaseGenerator):
    # 2. Implement generate_text
    def generate_text(self, input_data: str) -> OutputModel:
        system = PromptBuilder.create_system_prompt()
        user = PromptBuilder.create_user_prompt(input_data)
        response = self.call_llm(system, user, structured=True)
        return OutputModel.parse_raw(response)

# 3. Use in code
generator = MyGenerator()
result = generator.generate_text("input")
```

### PromptBuilder Pattern

```python
# 1. Inherit from BasePromptBuilder
class MyPromptBuilder(BasePromptBuilder):
    # 2. Implement create_system_prompt
    @staticmethod
    def create_system_prompt() -> str:
        return "Your system prompt here"

    # 3. Implement create_user_prompt
    @staticmethod
    def create_user_prompt(input_data: str) -> str:
        return f"Your user prompt here: {input_data}"

# 4. Use in generator
system = MyPromptBuilder.create_system_prompt()
user = MyPromptBuilder.create_user_prompt("data")
```

## Configuration

### Environment Variables

```bash
export MEDKIT_LOG_LEVEL=INFO
export MEDKIT_OUTPUT_DIR=/path/to/outputs
export MEDKIT_CACHE_DIR=/path/to/cache
export MEDKIT_LOG_FILE=medkit.log
```

### Logging Setup

```python
from lite.logging_config import configure_logging
import logging

configure_logging(
    log_file="mymodule.log",
    level=logging.INFO,
    verbosity=3
)

logger = logging.getLogger(__name__)
logger.info("Message here")
```

## Common Patterns

### Pattern 1: Simple CLI

Most modules follow this pattern:
- BaseCLI subclass handles arguments
- BaseGenerator subclass handles processing
- BasePromptBuilder subclass creates prompts
- Pydantic models for data validation

### Pattern 2: Batch Processing

```python
items = ["item1", "item2", "item3"]
for item in items:
    result = generator.generate_text(item)
    result.save(f"{item}.json")
```

### Pattern 3: Error Handling

```python
try:
    result = generator.generate_text(input_data)
except ValidationError:
    # Handle validation errors
except LLMError:
    # Handle LLM errors
except Exception:
    # Handle unexpected errors
```

### Pattern 4: Logging

```python
logger.debug("Debug message")
logger.info("Info message")
logger.warning("Warning message")
logger.error("Error message")
logger.critical("Critical message")
```

## Best Practices

1. **Always Inherit**: Use base classes for consistency
2. **Error Handling**: Catch and handle specific exceptions
3. **Logging**: Log important operations and errors
4. **Validation**: Use Pydantic for input validation
5. **Documentation**: Document all public methods
6. **Type Hints**: Include type hints for better IDE support

## Advanced Features

### Custom Error Recovery

```python
from utils.error_recovery import ErrorRecoveryStrategy

class CustomRecovery(ErrorRecoveryStrategy):
    def handle_error(self, error, retry_count):
        # Custom recovery logic
        pass
```

### Custom Output Formatting

```python
from utils.output_formatter import OutputFormatter

class CustomFormatter(OutputFormatter):
    def format_json(self, data):
        # Custom JSON formatting
        pass
```

## Integration Points

All utilities are designed for seamless integration:
- Base classes work with Pydantic models
- Error handling integrates with logging
- Output formatting works with data models
- Privacy utilities handle any data format

## Related Documentation

- [ARCHITECTURE.md](../ARCHITECTURE.md) - Detailed architecture
- [API.md](../API.md) - API reference
- [CONTRIBUTING.md](../CONTRIBUTING.md) - Contribution guidelines
- [CODE_STYLE_GUIDE.md](../CODE_STYLE_GUIDE.md) - Style standards

## Support

For help:
1. See [TROUBLESHOOTING.md](../TROUBLESHOOTING.md)
2. Check [API.md](../API.md)
3. Review examples in module READMEs
4. Check [CONTRIBUTING.md](../CONTRIBUTING.md)

---

**Last Updated**: January 25, 2026
**Related**: [ARCHITECTURE.md](../ARCHITECTURE.md) | [API.md](../API.md) | [README.md](../README.md)
