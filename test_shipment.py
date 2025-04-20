import unittest
from unittest.mock import patch

class TestSHIPSmart(unittest.TestCase):

    @patch('requests.get')
    def test_get_student_data(self, mock_get):
        # Simulate a successful API response
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {'uc_student_uid': '918859330', 'first_name': 'Alex'}

        result = get_student_data("918859330")
        self.assertEqual(result['first_name'], 'Alex')
        self.assertEqual(result['uc_student_uid'], '918859330')

    @patch('openai.resources.chat.Completions.create')
    def test_estimate_cost(self, mock_create):
        # Simulate OpenAI response
        mock_create.return_value.choices = [{'message': {'content': 'Estimated cost is $150.'}}]

        result = estimate_cost("I need a dental cleaning", "918859330")
        self.assertIn("Estimated cost", result)
        self.assertEqual(result, 'Estimated cost is $150.')

    @patch('cerebras.cloud.sdk.Cerebras.create_issue')
    def test_contact_provider_and_insurer(self, mock_create_issue):
        # Simulate issue creation
        mock_create_issue.return_value = {"status": "success", "issue_id": 123}

        issue_id = contact_provider_and_insurer("918859330", "HealthyCare Clinic", 150.00, 120.00)
        self.assertEqual(issue_id, 123)

    def test_book_appointment(self):
        # Test booking an appointment
        with patch('requests.get') as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.json.return_value = {'uc_student_uid': '918859330', 'first_name': 'Alex'}

            result = book_appointment("918859330", 1, "Dental Cleaning")
            self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()
