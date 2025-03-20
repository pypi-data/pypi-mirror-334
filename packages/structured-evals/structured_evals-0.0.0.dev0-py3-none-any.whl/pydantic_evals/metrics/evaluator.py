from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple, Type, get_origin
import pandas as pd

from loguru import logger
from pydantic import BaseModel
from rich.console import Console
from rich.text import Text

from pydantic_evals.common.typing import get_union_args, is_optional_union, is_union_type, type_to_str
from pydantic_evals.metrics.base import Metric, MetricItem, MetricRegistryItem


@dataclass
class Evaluator:
    """
    A simple, stateless evaluator for pydantic models:
      - register(root_model, field_type, metric_name, metric_fn)
      - call evaluator(x, x_pred) -> list of records:
        [
          {
            "root_model": "BaseModel",
            "field_name": "this.a",
            "type": "int",
            "metric_name": "ema",
            "metric_value": 1.0
          },
          ...
        ]
    Each method returns lists (no stateful accumulation), so it's easier to parallelize.
    """

    _registry: Dict[str, MetricRegistryItem] = field(default_factory=dict)

    def __str__(self):
        """Return a string representation of the evaluator.

        Evaluator:
        └── Person
            └── name: str                  (exact_match, f1)
            └── age: int                   (accuracy)
            └── created_at: datetime
            └── address: Address
                └── street: str            (exact_match)
                └── city: str              (exact_match)
                └── postal_code: str
        """
        # Create a string buffer console to capture the output
        console = Console(file=None)
        with console.capture() as capture:
            console.print(self.__repr__())

        # Return the rendered string with ANSI codes
        return capture.get()

    def __repr__(self):
        """Developer-friendly representation, delegates to _get_tree_repr."""
        return self._get_tree_repr()

    def _get_tree_repr(self) -> str:
        """Internal helper to generate the tree representation."""
        if not self._registry:
            return "[bold]Evaluator[/bold](empty)"

        lines = ["[bold]Evaluator:[/bold]"]

        def _format_model(model: Type[BaseModel], indent: str = "") -> List[Tuple[str, str, bool]]:
            """Returns list of tuples (field_desc, metrics_str, has_metrics)"""
            result = []
            # Add model name without metrics
            result.append((f"{indent}└── [bold blue]{model.__name__}[/bold blue]", "", False))

            # Iterate over model fields
            for field_name, field_info in model.model_fields.items():
                field_type = field_info.annotation

                # Get type string and metrics
                type_str = type_to_str(field_type)

                # If type is optional, we'll run metrics for the non-None type
                if is_optional_union(field_type):
                    args = get_union_args(field_type)
                    non_none_type = next(a for a in args if a is not type(None))
                    resolved_type_str = type_to_str(non_none_type)
                else:
                    resolved_type_str = type_str

                # Get metrics for this type
                metrics = self._get_metrics(model, resolved_type_str)
                has_metrics = bool(metrics)
                metrics_str = f"[cyan]{', '.join(m.name for m in metrics)}[/cyan]" if metrics else ""

                # Indent for nested fields
                # Escape [ and ] in type_str
                field_indent = indent + "    "
                type_str_esc = type_str.replace("[", "\\[").replace("]", "]")
                field_desc = (
                    f"{field_indent}└── {field_name}: [green]{type_str_esc}[/green]"
                    if has_metrics
                    else f"{field_indent}└── [dim]{field_name}: {type_str_esc}[/dim]"
                )
                result.append((field_desc, metrics_str, has_metrics))

                # If field is a nested BaseModel, recurse
                origin = get_origin(field_type)
                if origin is None and isinstance(field_type, type) and issubclass(field_type, BaseModel):
                    nested_lines = _format_model(field_type, field_indent)
                    result.extend(nested_lines)

            return result

        # Process each root model in registry and collect all lines
        seen_models = set()
        all_lines = []
        for reg_item in self._registry.values():
            model = reg_item.root_model
            if model not in seen_models:
                seen_models.add(model)
                all_lines.extend(_format_model(model))

        # Calculate the maximum length of field descriptions (excluding markup)
        max_len = max(len(Text.from_markup(field_desc).plain) for field_desc, _, _ in all_lines)

        # Format all lines with aligned metrics
        formatted_lines = [lines[0]]  # Start with "Evaluator:" header
        for field_desc, metrics_str, _has_metrics in all_lines:
            if metrics_str:
                # Calculate padding needed (accounting for markup)
                plain_len = len(Text.from_markup(field_desc).plain)
                padding = " " * (max_len - plain_len)
                formatted_lines.append(f"{field_desc}{padding}  ({metrics_str})")
            else:
                formatted_lines.append(field_desc)

        return "\n".join(formatted_lines)

    def register(self, root_model: Type[BaseModel], field_type: Any, metric: Metric):
        """
        Register a metric for (root_model, field_type). One registration automatically applies to nested submodels as well.

        Usage:
            >> evaluator.register(CustomModel, int, Metric(name="ema", cb=ema))
        """
        # Support list / tuples of field types
        if isinstance(field_type, (list, tuple)):
            for _field_type in field_type:
                self.register(root_model, _field_type, metric)
            return

        # Register the metric
        t_str = type_to_str(field_type)

        # Check if the (root_model, type_str) pair is already registered with a metric
        key = f"{root_model.__name__}-{t_str}"
        if key in self._registry:
            self._registry[key].metrics.append(metric)
            return

        # No existing entry => create a new one
        self._registry[key] = MetricRegistryItem(root_model=root_model, type_string=t_str, metrics=[metric])

    def __call__(self, x: BaseModel, x_pred: BaseModel) -> List[MetricItem]:
        """
        Evaluate x vs x_pred, returning a list of MetricItem records.
        """
        if not isinstance(x_pred, type(x)):
            raise TypeError("x_pred must have the same type as x")

        # We'll use the class name as the root prefix
        return self._evaluate_model(root_model=x.__class__, x=x, x_pred=x_pred, prefix=f"{x.__class__.__name__}")

    def _evaluate_model(
        self, root_model: Type[BaseModel], x: BaseModel, x_pred: BaseModel, prefix: str
    ) -> List[MetricItem]:
        results: List[MetricItem] = []

        # Iterate over model fields
        for field_name, field_info in x.model_fields.items():
            field_type = field_info.annotation
            field_path = f"{prefix}.{field_name}"
            val_true = getattr(x, field_name)
            val_pred = getattr(x_pred, field_name)

            # Evaluate the field
            field_results = self._evaluate_field(root_model, field_type, val_true, val_pred, field_path)
            # Add the field results to the overall results
            results.extend(field_results)
        return results

    def _evaluate_field(
        self, root_model: Type[BaseModel], field_type: Any, v: Any, v_pred: Any, field_path: str
    ) -> List[MetricItem]:
        """
        Returns a list of MetricItem records.
        """
        origin = get_origin(field_type)
        records: List[MetricItem] = []

        # 1. If it's an "optional" union (int | None)
        if is_optional_union(field_type):
            # Evaluate further if both sides are non-None
            args = get_union_args(field_type)
            non_none_type = next(a for a in args if a is not type(None))
            deeper = self._evaluate_field(root_model, non_none_type, v, v_pred, field_path)
            records.extend(deeper)
            return records

        # 2. If it's a union of multiple types (e.g. int | float | str?), handle how you like
        if is_union_type(field_type) and not is_optional_union(field_type):
            # For Union types, use the actual runtime type of the values
            if v is not None and v_pred is not None:
                # Use the actual runtime type for metrics
                actual_type = type(v)
                metrics = self._get_metrics(root_model, actual_type.__name__)
                for metric in metrics:
                    val = metric.cb(v, v_pred)
                    records.append(
                        MetricItem(
                            root_model=root_model.__name__,
                            field_name=field_path,
                            field_type=field_type,
                            field_type_str=type_to_str(field_type),
                            metric_name=metric.name,
                            metric_value=val,
                        )
                    )
            return records

        # 3. list
        if origin is list:
            # Also run any metrics for list[...] or fallback
            list_records = self._run_metrics(root_model, field_type, v, v_pred, field_path)
            records.extend(list_records)
            return records

        # 3. dict
        if origin is dict:
            # Note: For now, we ignore the dict type and just evaluate the dict as a whole.
            # sub_args = get_args(field_type)
            # if len(sub_args) == 2 and isinstance(v, dict) and isinstance(v_pred, dict):
            #     # sub_args[0] is key type, sub_args[1] is value type
            #     val_type = sub_args[1]
            #     shared_keys = set(v.keys()).intersection(v_pred.keys())
            #     for k in shared_keys:
            #         sub_path = f"{field_path}[{k}]"
            #         sub_records = self._evaluate_field(root_model, val_type, v[k], v_pred[k], sub_path)
            #         records.extend(sub_records)

            # Also run any "dict"-level metrics
            dict_records = self._run_metrics(root_model, field_type, v, v_pred, field_path)
            records.extend(dict_records)
            return records

        # 4. If it's a nested BaseModel
        if isinstance(v, BaseModel) and isinstance(v_pred, BaseModel):
            sub_records = self._evaluate_model(root_model, v, v_pred, field_path)
            records.extend(sub_records)
            return records

        # 5. Primitive type: run metrics
        primitive_records = self._run_metrics(root_model, field_type, v, v_pred, field_path)
        records.extend(primitive_records)
        return records

    def _run_metrics(
        self, root_model: Type[BaseModel], field_type: Any, y_true: Any, y_pred: Any, field_path: str
    ) -> List[MetricItem]:
        """
        Look up metrics for (root_model, type_string) or fallback (e.g. "list").
        Return a list of MetricItem records.
        """
        records: List[MetricItem] = []
        t_str = type_to_str(field_type)

        # Try exact match based on type string, or fallback
        metrics = self._get_metrics(root_model, t_str)

        # Add metric computation for each metric
        for reg in metrics:
            val = reg.cb(y_true, y_pred)
            records.append(
                MetricItem(
                    root_model=root_model.__name__,
                    field_name=field_path,
                    field_type=field_type,
                    field_type_str=t_str,
                    metric_name=reg.name,
                    metric_value=val,
                )
            )
        return records

    def _has_type_registered(self, root_model: Type[BaseModel], type_str: str) -> bool:
        key = f"{root_model.__name__}-{type_str}"
        return key in self._registry

    def _get_metrics(self, root_model: Type[BaseModel], type_str: str) -> List[Metric]:
        key = f"{root_model.__name__}-{type_str}"
        if key in self._registry:
            return self._registry[key].metrics

        # If no exact match, try fallback
        # fallback, e.g. list[str] -> list
        fallback_type_str = self._fallback_type(type_str)
        if fallback_type_str:
            return self._get_metrics(root_model, fallback_type_str)

        logger.warning(
            f"No metrics or fallback found [root_model={root_model}, type_str={type_str}, fallback_type_str={fallback_type_str}]"
        )
        return []

    def _fallback_type(self, type_str: str) -> Optional[str]:
        """
        e.g. "list[str]" -> "list", "dict[str,int]" -> "dict", "Literal" -> "str"
        """
        # Special case for Literal types
        if type_str.startswith("Literal"):
            return "str"
            
        # Handle generic types with brackets
        bracket_idx = type_str.find("[")
        if bracket_idx > 0:
            return type_str[:bracket_idx]  # e.g. "list"
            
        return None
        
    def to_dataframe(self, results: List[MetricItem]) -> pd.DataFrame:
        """
        Convert the evaluation results to a pandas DataFrame for easier analysis.
        
        Args:
            results: List of MetricItem objects from evaluator(x, x_pred)
            
        Returns:
            pd.DataFrame: A DataFrame with columns for root_model, field_name, field_type_str, 
                          metric_name, and metric_value.
        """
        if not results:
            return pd.DataFrame(columns=['root_model', 'field_name', 'field_type_str', 'metric_name', 'metric_value'])
        
        return pd.DataFrame([item.model_dump() for item in results])
