from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Type, get_origin

from loguru import logger
from pydantic import BaseModel

from pydantic_evals.common.typing import get_union_args, is_optional_union, is_union_type, type_to_str


class Metric(BaseModel):
    """
    A metric definition with a name and callback function.
    
    Attributes:
        name: The name of the metric (e.g., "exact_match", "f1_score")
        cb: A callable that takes two arguments (ground truth and prediction) and returns a float score
    """
    name: str
    cb: Callable[[Any, Any], float]


class MetricItem(BaseModel):
    """
    A single metric evaluation result.
    
    Attributes:
        root_model: The name of the root model, e.g. "BaseModel"
        field_name: The name of the field, e.g. "BaseModel.a"
        field_type: The actual type of the field, e.g. int
        field_type_str: The string representation of the field type, e.g. "int" or "list[str]"
        metric_name: The name of the metric, e.g. "ema"
        metric_value: The value of the metric, e.g. 1.0
    """
    root_model: str
    field_name: str
    field_type: Any
    field_type_str: str
    metric_name: str
    metric_value: float


class MetricRegistryItem(BaseModel):
    """
    MetricRegistryItem ties a root model to a type string, and a list of metrics.
        evaluator.register(root_model, type_string, Metric(name=metric_name, cb=metric_cb))
    """
    root_model: Type[BaseModel]
    type_string: str
    metrics: List[Metric] = field(default_factory=list)


def non_null_match(y_true: Optional[Any], y_pred: Optional[Any]) -> float:
    """
    Returns 1.0 if exactly one of y_true, y_pred is None,
    0.0 otherwise.
    """
    if (y_true is None) ^ (y_pred is None):  # XOR
        return 1.0
    return 0.0
