import sqlite3
from random import randint


class SBS:
    @staticmethod
    def create_table():
        with sqlite3.connect("card.s3db") as conn:
            cur = conn.cursor()
            cur.execute("""CREATE TABLE IF NOT EXISTS card(
                        id INTEGER,
                        number TEXT, 
                        pin TEXT,
                        balance INTEGER DEFAULT 0);""")
            conn.commit()

    @staticmethod
    def insert_values(number, pin, balance):
        with sqlite3.connect("card.s3db") as conn:
            cur = conn.cursor()
            cur.execute("INSERT INTO card (number, pin, balance) VALUES (?, ?, ?);", (number, pin, balance))
            conn.commit()

    @staticmethod
    def balance(number):
        with sqlite3.connect("card.s3db") as conn:
            cur = conn.cursor()
            cur.execute("SELECT balance FROM card WHERE number = ?;", (number,))
            result = cur.fetchone()
            print(result[0])
            conn.commit()

    @staticmethod
    def add_income(number):
        balance = int(input("Enter income:\n>"))
        with sqlite3.connect("card.s3db") as conn:
            cur = conn.cursor()
            cur.execute("UPDATE card SET balance = balance + ? WHERE number = ?;", (balance, number))
            conn.commit()

    @staticmethod
    def close_account(number):
        with sqlite3.connect("card.s3db") as conn:
            cur = conn.cursor()
            cur.execute("DELETE FROM card WHERE number = ?", (number,))
            conn.commit()

    def do_transfer(self, number):
        target_number = input("Transfer\nEnter card number:\n>")
        if target_number == number:
            print("You can't transfer money to the same account!\n")
            return
        if target_number[-1:] != self.checksum(target_number[:-1]):
            print("Probably you made a mistake in the card number. Please try again!\n")
            return
        if self.check_number(target_number) is False:
            print("Such a card does not exist.\n")
            return
        transfer_balance = int(input("Enter how much money you want to transfer:\n>"))
        print()
        with sqlite3.connect("card.s3db") as conn:
            cur = conn.cursor()
            cur.execute("SELECT balance FROM card WHERE balance > ? AND number = ?;", (transfer_balance, number))
            result = bool(cur.fetchone())
            if result is False:
                print("Not enough money!")
                return
            cur.execute("UPDATE card SET balance = balance + ? WHERE number = ?;", (transfer_balance, target_number))
            conn.commit()
            cur.execute("UPDATE card SET balance = balance - ? WHERE number = ?;", (transfer_balance, number))
            conn.commit()

    @staticmethod
    def check_number(number):
        with sqlite3.connect("card.s3db") as conn:
            cur = conn.cursor()
            cur.execute("SELECT number FROM card WHERE number = ?;", (number,))
            result = bool(cur.fetchone())
            conn.commit()
            return result

    @staticmethod
    def check_login(number, pin):
        with sqlite3.connect("card.s3db") as conn:
            cur = conn.cursor()
            cur.execute("SELECT number FROM card WHERE number = ? AND pin = ?;", (number, pin))
            result = bool(cur.fetchone())
            conn.commit()
            return result

    def create_card_number(self):
        while True:
            card_number = "400000" + str(randint(0, 999999999)).rjust(9, '0')
            card_number += self.checksum(card_number)
            if self.check_number(card_number):
                continue
            else:
                break
        return card_number

    @staticmethod
    def create_card_pin():
        card_pin = str(randint(0, 9999)).rjust(4, '0')
        return card_pin

    def create_account(self):
        card_number = self.create_card_number()
        card_pin = self.create_card_pin()
        self.insert_values(card_number, card_pin, 0)
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
        if self.check_number(card_number):
            if self.check_login(card_number, card_pin):
                print("\nYou have successfully logged in!\n")
                self.logged_in(card_number)
            else:
                print("\nWrong card number or PIN!\n")
        else:
            print("\nWrong card number or PIN!\n")

    def logged_in(self, number):
        while True:
            print("1. Balance\n2. Add income\n3. Do transfer\n4. Close account\n5. Log out\n0. Exit")
            user_input = int(input(">"))
            print()
            if user_input == 1:  # 1. Balance
                self.balance(number)
                print()
            elif user_input == 2:  # 2. Add income
                self.add_income(number)
                print("Income was added!\n")
            elif user_input == 3:  # 3. Do transfer
                self.do_transfer(number)
            elif user_input == 4:  # 4. Close account
                self.close_account(number)
                print("The account has been closed!\n")
                break
            elif user_input == 5:  # 5. Log out
                print("You have successfully logged out!\n")
                break
            elif user_input == 0:  # 0. Exit
                exit()

    def program(self):
        self.create_table()
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
