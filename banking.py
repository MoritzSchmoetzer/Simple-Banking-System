from random import randint


class SBS:
    def __init__(self):
        self.cards = {}
        self.cans = []

    def create_account(self):
        while True:
            can = randint(0000000000, 9999999999)  # customer account number (CAN)
            if can in self.cans:
                continue
            else:
                break
        self.cans.append(can)
        card_number = 4000000000000000 + can
        card_pin = randint(0000, 9999)
        card_pin = (0000 + card_pin)
        self.cards[card_number] = card_pin
        print("Your card has been created")
        print("Your card number:")
        print(card_number)
        print("Your card PIN:")
        print(f"{card_pin}\n")

    def login(self):
        print("Enter your card number:")
        card_number = int(input(">"))
        print("Enter your PIN:")
        card_pin = int(input(">"))

        if card_number in self.cards:
            if self.cards[card_number] == card_pin:
                print("\nYou have successfully logged in!\n")
                self.logged_in()
            else:
                print("\nWrong card number or PIN!\n")
        else:
            print("\nWrong card number or PIN!\n")

    @staticmethod
    def logged_in():
        while True:
            print("1. Balance\n2. Log out\n0. Exit")
            user_input = int(input(">"))
            print()
            if user_input == 1:
                print(f"Balance: 0\n")
            elif user_input == 2:
                print("You have successfully logged out!\n")
                break
            elif user_input == 0:
                exit()

    def program(self):
        while True:
            print("1. Create an account\n2. Log into account\n0. Exit")
            user_input = int(input(">"))
            print()
            if user_input == 1:
                self.create_account()
                continue
            elif user_input == 2:
                self.login()
                continue
            elif user_input == 0:
                print("Bye!")
                break


sbs = SBS()
sbs.program()
