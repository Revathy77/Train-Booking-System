import json
import random
import string
import os

# ---------- User System ----------
def load_users():
    if os.path.exists("users.json"):
        with open("users.json", "r") as f:
            return json.load(f)
    return {}

def save_users(users):
    with open("users.json", "w") as f:
        json.dump(users, f)

def register():
    users = load_users()
    username = input("Choose username: ")
    if username in users:
        print("Username already exists.")
        return None
    password = input("Choose password: ")
    users[username] = password
    save_users(users)
    print("Registration successful.")
    return username

def login():
    users = load_users()
    username = input("Username: ")
    password = input("Password: ")
    if users.get(username) == password:
        print("Login successful.")
        return username
    print("Invalid credentials.")
    return None

# ---------- Booking System ----------
class Train:
    def __init__(self, train_id, name, classes):
        self.train_id = train_id
        self.name = name
        self.classes = classes  # e.g., {'Sleeper': 10, 'AC': 5}

    def display(self):
        print(f"{self.train_id}. {self.name}")
        for cls, seats in self.classes.items():
            print(f"   {cls}: {seats} seats available")

class BookingSystem:
    def __init__(self, current_user):
        self.current_user = current_user
        self.trains = [
            Train(1, "Express 101", {'Sleeper': 10, 'AC': 5}),
            Train(2, "Intercity 202", {'Sleeper': 8, 'AC': 3}),
        ]
        self.bookings = self.load_bookings()

    def load_bookings(self):
        if os.path.exists("bookings.json"):
            with open("bookings.json", "r") as f:
                return json.load(f)
        return []

    def save_bookings(self):
        with open("bookings.json", "w") as f:
            json.dump(self.bookings, f)

    def generate_pnr(self):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

    def show_menu(self):
        while True:
            print(f"\nWelcome, {self.current_user}")
            print("1. View Trains\n2. Book Ticket\n3. Cancel Ticket\n4. View My Bookings\n5. Logout")
            choice = input("Choose option: ")
            if choice == "1":
                self.display_trains()
            elif choice == "2":
                self.book_ticket()
            elif choice == "3":
                self.cancel_ticket()
            elif choice == "4":
                self.view_my_bookings()
            elif choice == "5":
                break
            else:
                print("Invalid option.")

    def display_trains(self):
        for train in self.trains:
            train.display()

    def book_ticket(self):
        self.display_trains()
        train_id = int(input("Enter Train ID: "))
        train = next((t for t in self.trains if t.train_id == train_id), None)
        if not train:
            print("Train not found.")
            return
        cls = input("Enter class (Sleeper/AC): ")
        if cls not in train.classes or train.classes[cls] <= 0:
            print("Invalid class or no seats available.")
            return
        passenger = input("Enter passenger name: ")
        train.classes[cls] -= 1
        pnr = self.generate_pnr()
        ticket = {
            "user": self.current_user,
            "passenger": passenger,
            "train": train.name,
            "class": cls,
            "pnr": pnr
        }
        self.bookings.append(ticket)
        self.save_bookings()
        print(f"Ticket booked! PNR: {pnr}")

    def cancel_ticket(self):
        pnr = input("Enter PNR to cancel: ")
        for ticket in self.bookings:
            if ticket["pnr"] == pnr and ticket["user"] == self.current_user:
                for train in self.trains:
                    if train.name == ticket["train"]:
                        train.classes[ticket["class"]] += 1
                self.bookings.remove(ticket)
                self.save_bookings()
                print("Ticket cancelled.")
                return
        print("Booking not found or access denied.")

    def view_my_bookings(self):
        found = False
        for ticket in self.bookings:
            if ticket["user"] == self.current_user:
                print(f"PNR: {ticket['pnr']} | {ticket['passenger']} - {ticket['train']} ({ticket['class']})")
                found = True
        if not found:
            print("No bookings found.")

# ---------- Main App ----------
def main():
    print("Welcome to the Train Booking System")
    while True:
        print("\n1. Register\n2. Login\n3. Exit")
        option = input("Choose option: ")
        if option == "1":
            user = register()
            if user:
                BookingSystem(user).show_menu()
        elif option == "2":
            user = login()
            if user:
                BookingSystem(user).show_menu()
        elif option == "3":
            break
        else:
            print("Invalid option.")

if __name__ == "__main__":
    main()
