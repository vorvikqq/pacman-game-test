import pytest
from vector import Vector
from math import isclose


class TestVector:

    @pytest.mark.parametrize(
        "v1, v2, expected",
        [
            (Vector(3, 4), Vector(1, 2), (4, 6)),
            (Vector(5, 5), Vector(2, 3), (7, 8)),
            (Vector(0, 0), Vector(0, 0), (0, 0)),
        ]
    )
    def test_vector_addition(self, v1, v2, expected):
        result = v1 + v2
        assert result.x == expected[0]
        assert result.y == expected[1]

    @pytest.mark.parametrize(
        "v1, v2, expected",
        [
            (Vector(3, 4), Vector(1, 2), (2, 2)),
            (Vector(5, 5), Vector(2, 3), (3, 2)),
            (Vector(0, 0), Vector(0, 0), (0, 0)),
        ]
    )
    def test_vector_subtraction(self, v1, v2, expected):
        result = v1 - v2
        assert result.x == expected[0]
        assert result.y == expected[1]

    @pytest.mark.parametrize(
        "v, expected",
        [
            (Vector(3, 4), (-3, -4)),
            (Vector(5, 5), (-5, -5)),
            (Vector(0, 0), (0, 0)),
        ]
    )
    def test_vector_negation(self, v, expected):
        result = -v
        assert result.x == expected[0]
        assert result.y == expected[1]

    @pytest.mark.parametrize(
        "v, scalar, expected",
        [
            (Vector(3, 4), 2, (6, 8)),
            (Vector(5, 5), 3, (15, 15)),
            (Vector(0, 0), 2, (0, 0)),
        ]
    )
    def test_vector_multiplication(self, v, scalar, expected):
        result = v * scalar
        assert result.x == expected[0]
        assert result.y == expected[1]

    @pytest.mark.parametrize(
        "v, scalar, expected",
        [
            (Vector(3, 4), 2, (1.5, 2)),
            (Vector(5, 5), 5, (1, 1)),
            (Vector(0, 0), 2, (0, 0)),
        ]
    )
    def test_vector_division(self, v, scalar, expected):
        result = v / scalar
        assert result.x == expected[0]
        assert result.y == expected[1]

    @pytest.mark.parametrize(
        "v, scalar",
        [
            (Vector(3, 4), 0),
            (Vector(5, 5), 0),
            (Vector(0, 0), 0),
        ]
    )
    def test_vector_division_by_zero(self, v, scalar):
        result = v / scalar
        assert result is None

    @pytest.mark.parametrize(
        "v1, v2, expected",
        [
            (Vector(3, 4), Vector(3, 4), True),
            (Vector(3, 4), Vector(1, 2), False),
            (Vector(0, 0), Vector(0, 0), True),
        ]
    )
    def test_vector_equality(self, v1, v2, expected):
        assert (v1 == v2) == expected

    @pytest.mark.parametrize(
        "v, expected",
        [
            (Vector(3, 4), 5),
            (Vector(5, 12), 13),
            (Vector(0, 0), 0),
        ]
    )
    def test_vector_magnitude(self, v, expected):
        assert isclose(v.magnitude(), expected)

    @pytest.mark.parametrize(
        "v, expected",
        [
            (Vector(3, 4), 25),
            (Vector(5, 12), 169),
            (Vector(0, 0), 0),
        ]
    )
    def test_vector_magnitude_squared(self, v, expected):
        assert v.magnitudeSquared() == expected

    @pytest.mark.parametrize(
        "v, expected",
        [
            (Vector(3, 4), (3, 4)),
            (Vector(5, 5), (5, 5)),
            (Vector(0, 0), (0, 0)),
        ]
    )
    def test_vector_as_tuple(self, v, expected):
        assert v.asTuple() == expected

    @pytest.mark.parametrize(
        "v, expected",
        [
            (Vector(3, 4), (3, 4)),
            (Vector(5, 5), (5, 5)),
            (Vector(0, 0), (0, 0)),
        ]
    )
    def test_vector_as_int(self, v, expected):
        assert v.asInt() == expected

    @pytest.mark.parametrize(
        "v, expected",
        [
            (Vector(3, 4), "<3, 4>"),
            (Vector(5, 5), "<5, 5>"),
            (Vector(0, 0), "<0, 0>"),
        ]
    )
    def test_vector_str(self, v, expected):
        assert str(v) == expected
