import tempfile
import os
from func_to_script.config_loader import Struct, load_config_from_yaml


def test_struct_dict_like_access():
    """Test that Struct supports dictionary-style access"""
    # Arrange
    struct = Struct(name="test", value=42, nested={"inner": "data"})

    # Act & Assert - __getitem__
    assert struct["name"] == "test"
    assert struct["value"] == 42
    assert struct["nested"]["inner"] == "data"

    # Act & Assert - dot notation still works
    assert struct.name == "test"
    assert struct.value == 42
    assert struct.nested.inner == "data"


def test_struct_iteration():
    """Test that Struct can be iterated over like a dict"""
    # Arrange
    struct = Struct(a=1, b=2, c=3)

    # Act
    keys = list(struct)
    struct_keys = set(struct.keys())
    struct_values = set(struct.values())
    struct_items = set(struct.items())

    # Assert
    assert set(keys) == {"a", "b", "c"}
    assert struct_keys == {"a", "b", "c"}
    assert struct_values == {1, 2, 3}
    assert struct_items == {("a", 1), ("b", 2), ("c", 3)}


def test_struct_get_method():
    """Test the get method with default values"""
    # Arrange
    struct = Struct(existing="value")

    # Act
    existing_value = struct.get("existing")
    missing_value_default = struct.get("missing")
    missing_value_custom = struct.get("missing", "default")

    # Assert
    assert existing_value == "value"
    assert missing_value_default is None
    assert missing_value_custom == "default"


def test_struct_nested_dict_behavior():
    """Test that nested structs also have dict-like behavior"""
    # Arrange
    struct = Struct(
        level1={
            "level2": {
                "level3": "deep_value"
            },
            "simple": "value"
        }
    )

    # Act & Assert - mixed access patterns
    assert struct["level1"]["level2"]["level3"] == "deep_value"
    assert struct.level1["simple"] == "value"
    assert struct["level1"].level2.level3 == "deep_value"


def test_yaml_config_dict_access():
    """Test that YAML-loaded configs have dict-like access"""
    # Arrange
    yaml_content = """
data:
  num_classes: 80
  max_instances: 65
  image_size: 640
training:
  batch_size: 32
  learning_rate: 0.001
"""

    # Act
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        f.write(yaml_content)
        f.flush()

        try:
            config = load_config_from_yaml(f.name)

            # Assert - dot notation access
            assert config.data.num_classes == 80
            assert config.training.batch_size == 32

            # Assert - dict-style access
            assert config["data"]["num_classes"] == 80
            assert config["training"]["batch_size"] == 32

            # Assert - mixed access
            assert config.data["max_instances"] == 65
            assert config["training"].learning_rate == 0.001

            # Assert - get method
            assert config.get("data").num_classes == 80
            assert config.get("missing", "default") == "default"

            # Assert - iteration
            top_level_keys = set(config.keys())
            assert top_level_keys == {"data", "training"}

        finally:
            os.unlink(f.name)


def test_struct_contains_and_len():
    """Test __contains__ and __len__ methods"""
    # Arrange
    struct = Struct(a=1, b=2, c=3)

    # Act & Assert - __contains__
    assert "a" in struct
    assert "b" in struct
    assert "missing" not in struct

    # Act & Assert - __len__
    assert len(struct) == 3


def test_struct_repr():
    """Test that __repr__ works correctly"""
    # Arrange
    struct = Struct(a=1, b="test")

    # Act
    repr_str = repr(struct)

    # Assert
    assert "a" in repr_str
    assert "1" in repr_str
    assert "b" in repr_str
    assert "test" in repr_str