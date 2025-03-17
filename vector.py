import math


class Vector(object):
    """
    Represents a 2D vector with basic vector operations.

    Attributes:
        x (float): X-coordinate of the vector.
        y (float): Y-coordinate of the vector.
        thresh (float): Threshold for equality comparison.
    """

    def __init__(self, x=0, y=0):
        """
        Initializes a Vector instance.

        Args:
            x (float): X-coordinate. Defaults to 0.
            y (float): Y-coordinate. Defaults to 0.
        """
        self.x = x
        self.y = y
        self.thresh = 0.000001

    def __add__(self, other):
        """
        Adds two vectors.

        Args:
            other (Vector): The vector to add.

        Returns:
            Vector: The resulting vector after addition.
        """
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        """
        Subtracts one vector from another.

        Args:
            other (Vector): The vector to subtract.

        Returns:
            Vector: The resulting vector after subtraction.
        """
        return Vector(self.x - other.x, self.y - other.y)

    def __neg__(self):
        """
        Negates the vector.

        Returns:
            Vector: A vector with negated components.
        """
        return Vector(-self.x, -self.y)

    def __mul__(self, scalar):
        """
        Multiplies the vector by a scalar.

        Args:
            scalar (float): The scalar value.

        Returns:
            Vector: The resulting scaled vector.
        """
        return Vector(self.x * scalar, self.y * scalar)

    def __div__(self, scalar):
        """
        Divides the vector by a scalar.

        Args:
            scalar (float): The scalar value.

        Returns:
            Vector or None: The resulting vector or None if scalar is zero.
        """
        if scalar != 0:
            return Vector(self.x / scalar, self.y / scalar)
        return None

    def __truediv__(self, scalar):
        """
        True division for Python 3 compatibility.

        Args:
            scalar (float): The scalar value.

        Returns:
            Vector or None: The resulting vector or None if scalar is zero.
        """
        return self.__div__(scalar)

    def __eq__(self, other):
        """
        Checks if two vectors are equal within a small threshold.

        Args:
            other (Vector): The vector to compare.

        Returns:
            bool: True if vectors are equal within the threshold, otherwise False.
        """
        if abs(self.x - other.x) < self.thresh and abs(self.y - other.y) < self.thresh:
            return True
        return False

    def magnitudeSquared(self):
        """
        Computes the squared magnitude of the vector.

        Returns:
            float: The squared magnitude.
        """
        return self.x**2 + self.y**2

    def magnitude(self):
        """
        Computes the magnitude (length) of the vector.

        Returns:
            float: The magnitude.
        """
        return math.sqrt(self.magnitudeSquared())

    def copy(self):
        """
        Creates a copy of the vector.

        Returns:
            Vector: A new vector with the same components.
        """
        return Vector(self.x, self.y)

    def asTuple(self):
        """
        Returns the vector as a tuple.

        Returns:
            tuple: A tuple representation (x, y).
        """
        return self.x, self.y

    def asInt(self):
        """
        Returns the vector as an integer tuple.

        Returns:
            tuple: A tuple with integer components (int(x), int(y)).
        """
        return int(self.x), int(self.y)

    def __str__(self):
        """
        Returns a string representation of the vector.

        Returns:
            str: The formatted string representation.
        """
        return f"<{str(self.x)}, {str(self.y)}>"
