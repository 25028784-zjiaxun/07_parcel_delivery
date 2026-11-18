import pytest

from src.parcel_acceptance import is_parcel_accepted


@pytest.mark.parametrize(
    "weight_grams, length_cm, expected",
    [
        # Valid weights with a valid length.
        (1, 50, True),
        (2, 50, True),
        (500, 50, True),
        (19999, 50, True),
        (20000, 50, True),
        # Valid lengths with a valid weight.
        (500, 1, True),
        (500, 2, True),
        (500, 199, True),
        # Specification 3.2 accepts lengths up to and including 200 cm.
        (500, 200, True),
        # Combinations of the minimum and maximum accepted values.
        (1, 1, True),
        (1, 200, True),
        (20000, 1, True),
        (20000, 200, True),
        # Nonnegative measurements outside the acceptance limits.
        (0, 50, False),
        (20001, 50, False),
        (500, 0, False),
        (500, 201, False),
        (0, 0, False),
        (20001, 201, False),
        (0, 201, False),
        (20001, 0, False),
    ],
)
def test_parcel_acceptance_returns_expected_result(weight_grams, length_cm, expected):
    # Arrange: measurements and expected results are provided by parametrize.
    # Act
    actual_result = is_parcel_accepted(weight_grams, length_cm)

    # Assert: require an exact bool, not a truthy or falsy value.
    assert actual_result is expected


@pytest.mark.parametrize(
    "weight_grams, length_cm",
    [
        (-1, 50),
        (500, -1),
        (-1, -1),
    ],
)
def test_parcel_acceptance_negative_measurement_raises_value_error(
    weight_grams, length_cm
):
    with pytest.raises(ValueError):
        is_parcel_accepted(weight_grams, length_cm)


@pytest.mark.parametrize("weight_grams", ["50", 50.0, None, True, False, [], {}])
def test_parcel_acceptance_invalid_weight_type_raises_type_error(weight_grams):
    # Keep length valid so this test checks only the weight type.
    length_cm = 50

    with pytest.raises(TypeError):
        is_parcel_accepted(weight_grams, length_cm)


@pytest.mark.parametrize("length_cm", ["50", 50.0, None, True, False, [], {}])
def test_parcel_acceptance_invalid_length_type_raises_type_error(length_cm):
    # Keep weight valid so this test checks only the length type.
    weight_grams = 500

    with pytest.raises(TypeError):
        is_parcel_accepted(weight_grams, length_cm)
