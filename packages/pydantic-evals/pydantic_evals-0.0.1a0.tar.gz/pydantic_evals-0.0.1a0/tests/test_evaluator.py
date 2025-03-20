import pytest
from enum import Enum
from typing import Dict, List, Literal, Optional, Union

from pydantic import BaseModel, Field

from pydantic_evals.metrics import Evaluator, Metric

# Define a simple exact_match function for testing
def exact_match(x, y):
    """Simple exact match function for testing."""
    return float(x == y)


class Color(Enum):
    RED = "red"
    GREEN = "green"
    BLUE = "blue"


class TeamInfo(BaseModel):
    name: Optional[str] = Field(None, description="Name of the team")
    score: Optional[int] = Field(None, description="Current score of the team")


class SimpleModel(BaseModel):
    a: int
    b: str
    c: bool


class ComplexModel(BaseModel):
    name: str
    value: int
    tags: List[str]
    metadata: Dict[str, str]
    color: Color
    status: Literal["active", "inactive", "pending"]
    data: Union[int, str, bool]
    optional_value: Optional[float] = None


class GameState(BaseModel):
    description: Optional[str] = Field(None, description="Text description of the current game state")
    teams: Optional[List[TeamInfo]] = Field(None, description="List of teams playing in the game")
    status: Optional[str] = Field(None, description="Current status of the game, e.g., 'in_progress', 'final'")
    quarter: Optional[int] = Field(None, description="Current quarter of the game (1-4, or 5 for overtime)")
    clock_time: Optional[str] = Field(None, description="Time remaining in the current quarter, e.g., '14:56'")
    possession_team: Optional[str] = Field(None, description="Name of the team currently in possession")
    down: Optional[str] = Field(None, description="Current down (1st, 2nd, 3rd, 4th)")
    distance: Optional[int] = Field(None, description="Yards needed for first down")
    yard_line: Optional[int] = Field(None, description="Current yard line position")
    network: Optional[str] = Field(None, description="TV network broadcasting the game")
    is_shown: Optional[bool] = Field(None, description="Whether the game is currently being shown")


def test_evaluator_basic_type_metric():
    """Test basic type metrics with a simple model."""
    class SimpleTestModel(BaseModel):
        a: int

    evaluator = Evaluator()
    evaluator.register(SimpleTestModel, int, Metric(name="abs_diff", cb=lambda a, b: abs(a - b)))
    
    x = SimpleTestModel(a=10)
    x_pred = SimpleTestModel(a=12)

    metrics = evaluator(x, x_pred)
    assert len(metrics) == 1  # only one field: 'a'

    record = metrics[0]
    assert record.field_name == "SimpleTestModel.a"
    assert record.field_type_str == "int"
    assert record.metric_name == "abs_diff"
    assert record.metric_value == 2.0


def test_evaluator_optional_field():
    """
    Test that optional fields are properly evaluated.
    """
    class Model(BaseModel):
        val: Optional[int]

    evaluator = Evaluator()
    evaluator.register(Model, int, Metric(name="equiv", cb=lambda a, b: float(a == b)))

    x_none = Model(val=None)
    x_val = Model(val=10)

    # 1) none vs 10
    results_1 = evaluator(x_none, x_val)
    assert len(results_1) == 1
    rec = results_1[0]
    assert rec.field_name == "Model.val"
    assert rec.metric_name == "equiv"
    assert rec.metric_value == 0.0

    # 2) 10 vs 12
    x1 = Model(val=10)
    x2 = Model(val=12)
    results_2 = evaluator(x1, x2)
    rec = results_2[0]
    assert rec.field_name == "Model.val"
    assert rec.metric_name == "equiv"
    assert rec.metric_value == 0.0

    # 3) 12 vs 12
    x1 = Model(val=12)
    x2 = Model(val=12)
    results_3 = evaluator(x1, x2)
    rec = results_3[0]
    assert rec.field_name == "Model.val"
    assert rec.metric_name == "equiv"
    assert rec.metric_value == 1.0


def test_evaluator_list_field_fallback():
    """Test registering just 'list' metric, but field is list[int]."""
    class Model(BaseModel):
        nums: List[int]

    evaluator = Evaluator()
    evaluator.register(Model, list, Metric(name="length_diff", cb=lambda a, b: abs(len(a) - len(b))))
    
    x = Model(nums=[1, 2, 3])
    x_pred = Model(nums=[1, 2])

    results = evaluator(x, x_pred)

    # Expect one record for 'Model.nums'
    assert len(results) == 1
    rec = results[0]
    assert rec.field_name == "Model.nums"
    assert rec.field_type_str == "list[int]"
    assert rec.metric_name == "length_diff"
    assert rec.metric_value == 1


def test_evaluator_dict_field_fallback():
    """Test dict fallback from dict[str,int] to dict."""
    class Model(BaseModel):
        data: Dict[str, int]

    evaluator = Evaluator()
    evaluator.register(Model, dict, Metric(name="len_diff", cb=lambda a, b: abs(len(a) - len(b))))

    x = Model(data={"a": 1, "b": 2})
    x_pred = Model(data={"a": 10, "b": 20, "c": 30})

    results = evaluator(x, x_pred)
    # We'll see a single record for 'Model.data'
    assert len(results) == 1
    rec = results[0]
    assert rec.field_name == "Model.data"
    assert rec.field_type_str == "dict[str,int]"
    assert rec.metric_name == "len_diff"
    assert rec.metric_value == 1


def test_enum_field():
    """Test evaluation of enum fields."""
    class ModelWithEnum(BaseModel):
        color: Color

    evaluator = Evaluator()
    evaluator.register(ModelWithEnum, Color, Metric(name="exact_match", cb=lambda a, b: float(a == b)))
    
    x = ModelWithEnum(color=Color.RED)
    x_pred = ModelWithEnum(color=Color.RED)
    
    results = evaluator(x, x_pred)
    assert len(results) == 1
    assert results[0].metric_value == 1.0
    
    x_pred = ModelWithEnum(color=Color.BLUE)
    results = evaluator(x, x_pred)
    assert results[0].metric_value == 0.0


def test_literal_field():
    """Test evaluation of Literal fields."""
    class ModelWithLiteral(BaseModel):
        status: Literal["active", "inactive", "pending"]

    evaluator = Evaluator()
    # For Literal fields, we need to register with the underlying type (str in this case)
    evaluator.register(ModelWithLiteral, str, Metric(name="exact_match", cb=lambda a, b: float(a == b)))
    
    x = ModelWithLiteral(status="active")
    x_pred = ModelWithLiteral(status="active")
    
    results = evaluator(x, x_pred)
    assert len(results) == 1
    assert results[0].metric_value == 1.0
    
    x_pred = ModelWithLiteral(status="inactive")
    results = evaluator(x, x_pred)
    assert results[0].metric_value == 0.0


def test_union_field():
    """Test evaluation of Union fields."""
    class ModelWithUnion(BaseModel):
        data: Union[int, str]

    evaluator = Evaluator()
    evaluator.register(ModelWithUnion, int, Metric(name="exact_match", cb=lambda a, b: float(a == b)))
    evaluator.register(ModelWithUnion, str, Metric(name="exact_match", cb=lambda a, b: float(a == b)))
    
    x = ModelWithUnion(data=42)
    x_pred = ModelWithUnion(data=42)
    
    results = evaluator(x, x_pred)
    assert len(results) == 1
    assert results[0].metric_value == 1.0
    
    x = ModelWithUnion(data="hello")
    x_pred = ModelWithUnion(data="world")
    
    results = evaluator(x, x_pred)
    assert len(results) == 1
    assert results[0].metric_value == 0.0


def test_complex_model_with_multiple_types():
    """Test evaluation of a complex model with multiple field types."""
    # Create test instances
    x = ComplexModel(
        name="Test Model",
        value=42,
        tags=["tag1", "tag2", "tag3"],
        metadata={"key1": "value1", "key2": "value2"},
        color=Color.GREEN,
        status="active",
        data="string data",
        optional_value=3.14
    )
    
    # Create evaluator
    evaluator = Evaluator()
    
    # Register metrics for different types
    evaluator.register(ComplexModel, str, Metric(name="exact_match", cb=exact_match))
    evaluator.register(ComplexModel, int, Metric(name="abs_diff", cb=lambda a, b: abs(a - b)))
    evaluator.register(ComplexModel, float, Metric(name="abs_diff", cb=lambda a, b: abs(a - b)))
    evaluator.register(ComplexModel, list, Metric(name="length_match", cb=lambda a, b: float(len(a) == len(b))))
    evaluator.register(ComplexModel, dict, Metric(name="key_match", cb=lambda a, b: len(set(a.keys()) & set(b.keys())) / max(len(a), len(b))))
    evaluator.register(ComplexModel, Color, Metric(name="exact_match", cb=lambda a, b: float(a == b)))
    
    # Test 1: Perfect match
    x_pred = ComplexModel(
        name="Test Model",
        value=42,
        tags=["tag1", "tag2", "tag3"],
        metadata={"key1": "value1", "key2": "value2"},
        color=Color.GREEN,
        status="active",
        data="string data",
        optional_value=3.14
    )
    
    results = evaluator(x, x_pred)
    
    # Check that all metrics have perfect scores
    assert all(r.metric_value == 1.0 for r in results if r.metric_name == "exact_match")
    assert all(r.metric_value == 0.0 for r in results if r.metric_name == "abs_diff")
    assert all(r.metric_value == 1.0 for r in results if r.metric_name == "length_match")
    assert all(r.metric_value == 1.0 for r in results if r.metric_name == "key_match")
    
    # Test 2: Modified values
    x_pred = ComplexModel(
        name="Different Name",
        value=100,
        tags=["tag1", "tag2", "tag3", "tag4"],
        metadata={"key1": "value1", "key3": "value3"},
        color=Color.BLUE,
        status="inactive",
        data=42,  # Changed type from str to int
        optional_value=2.71
    )
    
    results = evaluator(x, x_pred)
    
    # Check specific fields
    name_metric = next(r for r in results if r.field_name == "ComplexModel.name")
    assert name_metric.metric_value == 0.0  # Names don't match
    
    value_metric = next(r for r in results if r.field_name == "ComplexModel.value")
    assert value_metric.metric_value == 58.0  # |42 - 100| = 58
    
    tags_metric = next(r for r in results if r.field_name == "ComplexModel.tags")
    assert tags_metric.metric_value == 0.0  # Lengths don't match
    
    color_metric = next(r for r in results if r.field_name == "ComplexModel.color")
    assert color_metric.metric_value == 0.0  # Colors don't match


def test_complex_model_evaluation():
    """Test evaluation of a complex model with nested fields."""
    # Create test instances
    x = GameState(
        description="A short commentary on the current state of an NFL game.",
        teams=[TeamInfo(name="Cincinnati Bengals", score=3), TeamInfo(name="Tennessee Titans", score=0)],
        status="in_progress",
        quarter=1,
        clock_time="5:18",
        down="2nd",
        distance=9,
        is_shown=True,
    )
    
    # Create evaluator
    evaluator = Evaluator()
    
    # Register metrics
    evaluator.register(GameState, (int, float, bool), Metric(name="equiv", cb=lambda a, b: float(a == b)))
    evaluator.register(GameState, str, Metric(name="exact_match", cb=exact_match))
    evaluator.register(GameState, list, Metric(name="length_match", cb=lambda a, b: float(len(a) == len(b))))
    
    # Test 1: Perfect match
    x_pred = x.model_copy()
    results = evaluator(x, x_pred)
    
    # Check that all metrics have value 1.0 (perfect match)
    assert all(r.metric_value == 1.0 for r in results)
    
    # Test 2: Modify a field
    x_pred = x.model_copy()
    x_pred.distance = 10
    results = evaluator(x, x_pred)
    
    # Find the specific field that was modified
    distance_metric = next(r for r in results if r.field_name == "GameState.distance")
    assert distance_metric.metric_value == 0.0  # Not equal
