
import pytest

from geo_convert_util import Conversion


class TestConversions:

    def test_ha_to_alqpta(self):
        """
        Test the conversion from hectares to alqueires paulistas.
        Given:
            A value in hectares (input_value = 2.42)
        When:
            Converting it to alqueires paulistas using the Conversion.ha_to_alqpta method.
        Then:
            The result should be the expected value (expected_value = 1).
        """

        input_value = 2.42
        expected_value = 1
        
        assert Conversion.ha_to_alqpta(input_value) == expected_value

        
    def test_ha_to_m2(self):
        """
        Test the conversion from hectares to square meters.
        Given:
            A value in hectares (input_value = 1)
        When:
            Converting it to square meters using the Conversion.ha_to_m2 method.
        Then:
            The result should be the expected value (expected_value = 10000).
        """

        input_value = 1
        expected_value = 10000

        assert Conversion.ha_to_m2(input_value) == expected_value

    def test_m2_to_alqpta(self):
        """
        Test the conversion from square meters to alqueires paulistas.
        Given:
            A value in square meters (input_value = 24200)
        When:
            Converting it to alqueires paulistas using the Conversion.m2_to_alqpta method.
        Then:
            The result should be the expected value (expected_value = 1).
        """

        input_value = 24200
        expected_value = 1

        assert Conversion.m2_to_alqpta(input_value) == expected_value

    def test_m2_to_ha(self):
        """
        Test the conversion from square meters to hectares.
        Given:
            A value in square meters (input_value = 10000)
        When:
            Converting it to hectares using the Conversion.m2_to_ha method.
        Then:
            The result should be the expected value (expected_value = 1).
        """

        input_value = 10000
        expected_value = 1

        assert Conversion.m2_to_ha(input_value) == expected_value

    def test_alqpta_to_ha(self):
        """
        Test the conversion from alqueires paulistas to hectares.
        Given:
            A value in alqueires paulistas (input_value = 1)
        When:
            Converting it to hectares using the Conversion.alqpta_to_ha method.
        Then:
            The result should be the expected value (expected_value = 2.42).
        """

        input_value = 1
        expected_value = 2.42

        assert Conversion.alqpta_to_ha(input_value) == expected_value

    def test_alqpta_to_m2(self):
        """
        Test the conversion from alqueires paulistas to square meters.
        Given:
            A value in alqueires paulistas (input_value = 1)
        When:
            Converting it to square meters using the Conversion.alqpta_to_m2 method.
        Then:
            The result should be the expected value (expected_value = 24200).
        """

        input_value = 1
        expected_value = 24200

        assert Conversion.alqpta_to_m2(input_value) == expected_value


if __name__ == '__main__':
    pytest.main()

