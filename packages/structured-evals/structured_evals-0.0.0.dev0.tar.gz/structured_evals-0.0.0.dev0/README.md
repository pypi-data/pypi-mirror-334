<div align="center">
<p align="center" style="width: 100%;">
    <img src="https://raw.githubusercontent.com/vlm-run/.github/refs/heads/main/profile/assets/vlm-black.svg" alt="VLM Run Logo" width="80" style="margin-bottom: -5px; color: #2e3138; vertical-align: middle; padding-right: 5px;"><br>
</p>
<h2>Structured Evals</h2>
<p align="center"><a href="https://docs.vlm.run"><b>Website</b></a> | <a href="https://discord.gg/AMApC2UzVY"><b>Discord</b></a>
</p>
<p align="center">
<a href="https://github.com/vlm-run/structured-evals/blob/main/LICENSE"><img alt="License" src="https://img.shields.io/github/license/vlm-run/structured-evals.svg"></a>
<a href="https://discord.gg/AMApC2UzVY"><img alt="Discord" src="https://img.shields.io/badge/discord-chat-purple?color=%235765F2&label=discord&logo=discord"></a>
</p>
</div>

# structured-evals

A framework for evaluating LLMs with structured outputs (i.e., JSON-mode) using pydantic models.

## 🔍 Overview

`structured-evals` is a Python library for evaluating the quality of structured outputs from language models. It provides a flexible framework for registering and applying metrics to pydantic models (compatible with Pydantic v2), making it easy to evaluate the accuracy of model predictions against ground truth data.

## ✨ Features

- **Structured Evaluation**: Evaluate nested pydantic models with type-specific metrics
- **Flexible Metric Registration**: Register custom metrics for specific field types
- **Pandas Integration**: Convert evaluation results to pandas DataFrames for easy analysis
- **Optional Integrations**: Seamlessly integrate with other evaluation frameworks like `autoevals` and OpenAI's `evals`
- **Comprehensive Type Support**: Support for primitive types, lists, dictionaries, nested models, and more

## 📦 Installation

```bash
# Basic installation (requires Pydantic v2)
pip install structured-evals

# With optional dependencies
pip install structured-evals[autoevals]  # For autoevals integration
pip install structured-evals[openai-evals]  # For OpenAI evals integration
pip install structured-evals[all]  # For all optional dependencies
```

## 🚀 Quickstart

```python
from pydantic import BaseModel
from structured_evals.metrics import Evaluator, Metric

# Define your pydantic model
class Person(BaseModel):
    name: str
    age: int
    is_active: bool

# Create ground truth and prediction instances
x_gt = Person(name="John Doe", age=30, is_active=True)
x = Person(name="John Doe", age=32, is_active=True)

# Create evaluator and register metrics
evaluator = Evaluator()
evaluator.register(Person, (int, float, bool, str), Metric(name="exact_match", cb=lambda a, b: float(a == b)))
evaluator.register(Person, (int, float), Metric(name="abs_diff", cb=lambda a, b: abs(a - b)))

# Evaluate prediction against ground truth
results = evaluator(x_gt, x)

# View results as a dictionary
print(results)
# Example output: {'Person.name': {'exact_match': 1.0}, 'Person.age': {'exact_match': 0.0, 'abs_diff': 2.0}, 'Person.is_active': {'exact_match': 1.0}}
```

## 🔧 Custom Metrics

You can register custom metrics for specific field types:

```python
from structured_evals.metrics import Evaluator, Metric

# Define a custom metric using Jaccard similarity
def jaccard_similarity(text1: str, text2: str) -> float:
    """
    Calculate Jaccard similarity between two strings.
    
    Jaccard similarity is the size of the intersection divided by the size of the union of two sets.
    """
    if not text1 or not text2:
        return 0.0
    
    set1 = set(text1.lower().split())
    set2 = set(text2.lower().split())
    
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    
    return intersection / union if union > 0 else 0.0

# Register the custom metric
evaluator.register(
    Person,  # The model class
    str,     # The field type
    Metric(name="jaccard_similarity", cb=jaccard_similarity)
)

# Evaluate with the custom metric
results = evaluator(x_gt, x)

# View results as a dictionary
print(results)
# Example output: {'Person.name': {'jaccard_similarity': 1.0}, 'Person.age': {'exact_match': 0.0, 'abs_diff': 2.0}, 'Person.is_active': {'exact_match': 1.0}}
```

## 🔄 Integration with Other Frameworks

You can easily integrate with other evaluation frameworks by creating custom metrics that wrap their functionality:

```python
from structured_evals.metrics import Evaluator, Metric

# Example integration with autoevals
# Note: This requires installing the optional dependencies with `pip install structured-evals[autoevals]`
from autoevals.llm import Factuality

# Create the autoevals metric
factuality = Factuality()

def factuality_metric(text1: str, text2: str) -> float:
    """Evaluate factuality using autoevals."""
    if not isinstance(text1, str) or not isinstance(text2, str):
        return 0.0
    result = factuality(text2, text1, input="Determine if the following two answers are consistent.")
    return result.score

# Register the metric
evaluator.register(
    Person,
    str,
    Metric(name="factuality", cb=factuality_metric)
)

# Evaluate with the integrated metrics
results = evaluator(x_gt, x)

# View results as a dictionary
print(results)
# Example output: {'Person.name': {'factuality': 0.95, 'exact_match': 1.0}, 'Person.age': {'exact_match': 0.0, 'abs_diff': 2.0}, 'Person.is_active': {'exact_match': 1.0}}
```

## 📝 Writing Custom Evals

See [docs/custom-eval.md](docs/custom-eval.md) for detailed instructions on writing custom evaluations.

## 📄 License

MIT
