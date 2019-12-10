import random
import smtplib
from email.headerregistry import Address
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import make_msgid
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
        #TODO: Fix random pairing algorithm to prevent stalling 
        random_name = random.choice(names_to_emails_list)

        while random_name in self.names_to_picks.values() or random_name == name:
            random_name = random.choice(names_to_emails_list)

        self.names_to_picks[name] = random_name
                    
    def iterate_through_names_and_call_email_picks(self):
        for name in list(self.names_to_picks):
            self.email_pick(name, self.names_to_emails[name])
    
    def email_pick(self, name, email):
        mail_user = 'email@email.com'
        mail_password = 'pass'
        msg = self.create_email(name, email)

        try:
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.ehlo()
            server.login(mail_user, mail_password)
            server.send_message(msg)
            server.close()
            print('Email sent!')
        except Exception as ex:
            print('Something went wrong...')
            print(ex)

    def create_email(self, email, name):
        email_id = email.split('@')[0]
        domain = email.split('@')[1]
        msg = EmailMessage()
        msg['Subject'] = "Secret Santa 2019"
        msg['From'] = Address("Buddy the Bot", "email", "email.com")
        msg['To'] = Address(name, email_id, domain)
        image = make_msgid()

        msg.add_alternative("""\
        <html>
        <head></head>
        <body>
            <p>""" + 'Hi {}!'.format(name) + """</p>
            <p>You are receiving this message because you are participating in the Family's 
            2019 Secret Santa! Please let me formally introduce myself. My name is Buddy (no relation to Buddy the Elf), 
            the Secret Santa bot. Your friend, Phillip, created me. What a great guy!
            </p>
            <p>
            My job is to tell you to get 
            </p>
        <b>"""+ '{}'.format(self.names_to_picks[name])+"""</b> 
            <p>
            a $20 gift for Secret Santa this year.
            </p>
            <p>
            I know I know. You must be thinking "But it's not a secret if Phillip created you! 
            He must know everyone's respective secret santa," but that is where you are wrong!
            Phillip thought about this when he created me, and he created an algorithm to randomly 
            draw names for people without him knowing who drew whom.
            </p>
            <p>
            Anyway, please remember to get a $20 gift for <b>"""+ '{}'.format(self.names_to_picks[name]) +"""</b>! 
            I need to get going as I am very busy around this time of year.
            </p>
            <p>
            Have a blessed Christmas!
            </p>
            <p>
            - Buddy the Bot
            </p>
            <p>
            01001101 01100101 01110010 01110010 01111001 00100000 01000011 01101000 
            01110010 01101001 01110011 01110100 01101101 01100001 01110011
            </p>
        </body>
        </html>
        """.format(image=image[1:-1]), subtype='html')
        return msg
