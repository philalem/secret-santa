import unittest
from pathlib import Path
from unittest import mock

from ..scripts.hat_pick import Hat_Pick

path = Path(__file__).parent / "./test_data/test_emails.txt"

class Hat_Pick_Test(unittest.TestCase):

    def populate_names_list(self, names_and_emails):
        names = []
        
        with open(names_and_emails, 'r') as f:
            for pair in f:
                split_pair = pair.split()
                name =  split_pair[0]
                names.append(name)

        return names

    def test_pick_from_hat(self):
        hat_pick = Hat_Pick(path)
        self.assertEqual(len(hat_pick.pick_from_hat()), 4)

    def test_that_no_person_has_been_drawn_more_than_once(self):
        hat_pick = Hat_Pick(path)
        names = self.populate_names_list(path)
        dict_of_picks = hat_pick.pick_from_hat()

        for name in range(len(names)):
            self.assertIn(names[name], dict_of_picks.values())

    def test_that_the_email_method_has_been_called_x_times(self):
        hat_pick = Hat_Pick(path)
        names = self.populate_names_list(path)
        hat_pick.pick_from_hat()
        hat_pick.email_pick = mock.MagicMock()
        #hat_pick.email_pick.server = mock.MagicMock()
        hat_pick.iterate_through_names_and_call_email_picks()
        self.assertEqual(hat_pick.email_pick.call_count, 4)

if __name__ == "__main__":
    unittest.main()
