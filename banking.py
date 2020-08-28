from random import randint


class SBS:
    def __init__(self):
        self.cards = {}
        self.cans = []

    def create_account(self):
        while True:
            can = str(randint(0, 999999999)).rjust(9, '0')  # customer account number (CAN)
            if can in self.cans:
                continue
            else:
                break
        self.cans.append(can)
        card_number = "400000" + can
        card_number += self.checksum(card_number)
        card_pin = str(randint(0, 9999)).rjust(4, '0')
        self.cards[card_number] = card_pin
        print(f"Your card has been created\nYour card number:\n{card_number}\nYour card PIN:\n{card_pin}\n")

    @staticmethod
    def checksum(card_number):
        odd = 1
        sum = 0
        for char in card_number:
            char = int(char)
            if odd % 2 != 0:
                char *= 2
                if char > 9:
                    char -= 9
            odd += 1
            sum += char
        return "0" if sum % 10 == 0 else str(10 - sum % 10)

    def login(self):
        print("Enter your card number:")
        card_number = input(">")
        print("Enter your PIN:")
        card_pin = input(">")
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
