import pytest

from src.parcel_fee import delivery_fee


@pytest.mark.parametrize(
    "weight_grams, expected_fee",
    [
        (1, 500),
        (2, 500),
        (500, 500),
        (999, 500),
        # Specification 3.1 includes 1000 grams in the 500-cent band.
        (1000, 500),
        (1001, 1000),
        (1002, 1000),
        (10000, 1000),
        (19999, 1000),
        (20000, 1000),
    ],
)
def test_delivery_fee_returns_expected_fee(weight_grams, expected_fee):
    # Arrange: inputs and expected fees are provided by parametrize.
    # Act
    actual_fee = delivery_fee(weight_grams)

    # Assert: the fee must have the correct type and value.
    assert type(actual_fee) is int
    assert actual_fee == expected_fee


@pytest.mark.parametrize("weight_grams", [-1, 0, 20001])
def test_delivery_fee_out_of_range_raises_value_error(weight_grams):
    with pytest.raises(ValueError):
        delivery_fee(weight_grams)


@pytest.mark.parametrize(
    "weight_grams",
    ["1000", 1000.0, None, True, False, [], {}],
)
def test_delivery_fee_invalid_type_raises_type_error(weight_grams):
    with pytest.raises(TypeError):
        delivery_fee(weight_grams)
