from unittest import TestCase, main
from unittest.mock import patch
from fib_py.fib_calcs.fib_numbers import calculate_numbers

class TestCalculateNumbers(TestCase):
    # The patch function enables us to insert a MagicMock object in place of our recurring_fibonacci_number function.
    @patch("fib_py.fib_calcs.fib_numbers."
        "recurring_fibonacci_number")
    def test_calculate_numbers(self, mock_number):
        expected_outcome = [mock_number.return_value, mock_number.return_value]
        self.assertEqual(expected_outcome, calculate_numbers(numbers=[4,5]))
        self.assertEqual(2, len(mock_number.call_args_list))
        self.assertEqual({'number': 4}, mock_number.call_args_list[0][1])
        self.assertEqual({'number': 5}, mock_number.call_args_list[1][1])

    def test_functional(self):
        self.assertEqual([0, 1, 1, 2, 3, 5], calculate_numbers([0, 1, 2, 3, 4, 5])) 

if __name__ == "__main__":
    main()
