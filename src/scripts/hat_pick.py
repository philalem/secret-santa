import random
from pathlib import Path

path = Path(__file__).parent / "../../data/emails.txt"

class Hat_Pick:
    names_to_emails = {}
    names_to_picks = {}

    def __init__(self, names_and_emails):
        self.names_to_emails = {}
        self.names_to_picks = {}

        with open(names_and_emails, 'r') as f:
            for pair in f:
                split_pair = pair.split()
                name, email =  split_pair[0], split_pair[1]
                self.names_to_emails[name] = email

    def pick_from_hat(self):
        names_to_emails_list = list(self.names_to_emails)

        for name in names_to_emails_list:
            self.make_random_pairs(names_to_emails_list, name)

        return self.names_to_picks

    def make_random_pairs(self, names_to_emails_list, name):
        random_name = random.choice(names_to_emails_list)

        while random_name in self.names_to_picks.values() or random_name == name:
            random_name = random.choice(names_to_emails_list)

        self.names_to_picks[name] = random_name
                    

    def send_picks(self):
        pass



# hat_pick = Hat_Pick(path)
# hat_pick.pick_from_hat()
