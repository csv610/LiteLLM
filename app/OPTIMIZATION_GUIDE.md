# Pydantic Model Optimization with DSPydantic

This guide explains how to optimize Pydantic models in each application using DSPydantic with Ollama.

## Overview

DSPydantic allows you to automatically optimize Pydantic models using example data and a validation metric. This can improve the quality and consistency of model outputs.

## General Optimization Pattern

For each application with Pydantic models, you can follow this pattern:

```python
import dspy
from your_app.models import YourModel  # Import the Pydantic model

# Configure DSPy with Ollama
ollama_lm = dspy.Ollama(model='llama3', max_tokens=2000)
dspy.settings.configure(lm=ollama_lm)

# Define your validation metric
def your_model_metric(example, pred, trace=None):
    # Return True if prediction meets quality criteria
    return True  # Customize this based on your model

# Prepare training examples
trainset = [
    dspy.Example(
        # Input fields
        field1="value1",
        field2="value2",
        # Output fields (what the model should generate)
        output_field1="expected_value1",
        output_field2="expected_value2"
    ).with_inputs('field1', 'field2'),  # Specify input fields
    # Add more examples...
]

# Optimize using one of DSPy's optimizers
from dspy.teleprompt import BootstrapFewShot  # or MIPRO, COPRO, etc.

optimizer = BootstrapFewShot(metric=your_model_metric, max_bootstrapped_demos=3)
optimized_model = optimizer.compile(YourModel, trainset=trainset)

# Use the optimized model
result = optimized_model(input_field1="new_value1", input_field2="new_value2")
```

## Application-Specific Optimizers

Each application folder below contains specific optimization code for its key Pydantic models.

### How to Use These Optimizers

1. Install DSPy if not already installed: `pip install dspy-ai`
2. Ensure Ollama is running with a model: `ollama run llama3`
3. Run the optimizer script for the application you want to optimize
4. Use the optimized model in your application code

## Best Practices

1. Start with 5-10 high-quality examples for training
2. Customize the metric function to match your specific quality requirements
3. Test optimized models thoroughly before deploying
4. Consider saving optimized models for reuse: `pickle.dump(optimized_model, file)`
5. Different optimizers work better for different scenarios:
   - BootstrapFewShot: Good starting point, works well with few examples
   - MIPRO: Often better performance, more computation
   - COPRO: Good for few-shot optimization

Let's look at each application's specific optimization code.