import pytest

import rio


@pytest.mark.parametrize(
    "laba_in,laba_out",
    [],
)
def create_from_oklab(
    laba_in: tuple[float, float, float, float],
    laba_out: tuple[float, float, float, float],
) -> None:
    """
    Instantiates a `Color` object from oklab values and verifies the internally
    stored values match the expected ones.
    """
    color = rio.Color.from_oklab(*laba_in)

    assert color._l == laba_out[0]
    assert color._a == laba_out[1]
    assert color._b == laba_out[2]
    assert color._opacity == laba_out[3]
