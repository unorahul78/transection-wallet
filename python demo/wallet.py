import tkinter as tk
from tkinter import messagebox
import uuid
import random

class Wallet:
    def __init__(self, user_name, balance=0):
        self.user_name = user_name
        self.balance = balance
        self.transactions = []

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            transaction_id = uuid.uuid4().hex  # Generate UUID for transaction ID
            serial_number = self.generate_serial_number()  # Generate serial number
            self.transactions.append((transaction_id, serial_number, 'Deposit', amount, self.user_name))
            return transaction_id
        else:
            raise ValueError("Deposit amount must be greater than zero")

    def withdraw(self, amount):
        if amount > 0 and self.balance >= amount:
            self.balance -= amount
            transaction_id = uuid.uuid4().hex  # Generate UUID for transaction ID
            serial_number = self.generate_serial_number()  # Generate serial number
            self.transactions.append((transaction_id, serial_number, 'Withdrawal', amount, self.user_name))
            return transaction_id
        else:
            raise ValueError("Withdrawal amount must be greater than zero and less than or equal to balance")

    def generate_serial_number(self):
        return ''.join([str(random.randint(0, 9)) for _ in range(15)])

    def get_balance(self):
        return self.balance

    def get_transactions(self):
        return self.transactions

    def send_money(self, recipient_wallet, amount):
        if amount > 0 and self.balance >= amount:
            self.balance -= amount
            recipient_wallet.deposit(amount)
            transaction_id = uuid.uuid4().hex  # Generate UUID for transaction ID
            self.transactions.append((transaction_id, None, 'Sent', amount, recipient_wallet.user_name))
            recipient_wallet.transactions.append((transaction_id, self.generate_serial_number(), 'Received', amount, self.user_name))
        else:
            raise ValueError("Transfer amount must be greater than zero and less than or equal to balance")

class WalletApp:
    def __init__(self, root):
        self.root = root
        self.root.title("My wallet")

        self.wallet1 = Wallet(user_name="User1")
        self.wallet2 = Wallet(user_name="User2")
        
        self.current_user = self.wallet1  # Default to user1
        
        # Validation for amount entry (only integers)
        self.validate_numeric = (self.root.register(self.validate_entry), '%P')
        
        # Labels and Entry widgets
        self.balance_label = tk.Label(root, text="Current Balance:")
        self.balance_label.grid(row=0, column=0, padx=10, pady=10)
        
        self.balance_value = tk.Label(root, text=f"Rs{self.current_user.get_balance()}")
        self.balance_value.grid(row=0, column=1, padx=10, pady=10)
        
        self.amount_label = tk.Label(root, text="Enter amount:")
        self.amount_label.grid(row=1, column=0, padx=10, pady=10)
        
        self.amount_entry = tk.Entry(root, validate='key', validatecommand=self.validate_numeric)
        self.amount_entry.grid(row=1, column=1, padx=10, pady=10)
        
        self.user_selector = tk.StringVar(value=self.current_user.user_name)
        self.user1_radio = tk.Radiobutton(root, text="User1", variable=self.user_selector, value="User1", command=self.select_user)
        self.user2_radio = tk.Radiobutton(root, text="User2", variable=self.user_selector, value="User2", command=self.select_user)
        
        self.user1_radio.grid(row=2, column=0, padx=10, pady=10)
        self.user2_radio.grid(row=2, column=1, padx=10, pady=10)

        self.recipient_selector = tk.StringVar(value="User1")
        self.recipient_label = tk.Label(root, text="Select recipient:")
        self.recipient_label.grid(row=3, column=0, padx=10, pady=10)
        
        self.recipient_option = tk.OptionMenu(root, self.recipient_selector,"User1", "User2")
        self.recipient_option.grid(row=3, column=1, padx=10, pady=10)
        
        # Buttons
        self.deposit_button = tk.Button(root, text="Deposit", command=self.deposit, bg="lightblue", fg="black")
        self.deposit_button.grid(row=4, column=0, padx=10, pady=10)

        
        self.withdraw_button = tk.Button(root, text="Withdraw", command=self.withdraw , bg="red",fg="white")
        self.withdraw_button.grid(row=4, column=1, padx=10, pady=10)
        
        self.send_button = tk.Button(root, text="Send Money", command=self.send_money , bg="green", fg="white")
        self.send_button.grid(row=5, column=0, padx=10, pady=10)
        
        self.history_button = tk.Button(root, text="Transaction History", command=self.show_history)
        self.history_button.grid(row=6, column=0, columnspan=2, padx=10, pady=10)
        
        self.view_serial_button = tk.Button(root, text="View Serial Numbers", command=self.show_serial_numbers)
        self.view_serial_button.grid(row=7, column=0, columnspan=2, padx=10, pady=10)
        
        self.exit_button = tk.Button(root, text="Exit", command=root.quit)
        self.exit_button.grid(row=8, column=0, columnspan=2, padx=10, pady=10)
        
    def validate_entry(self, new_value):
        if new_value.isdigit() or new_value == "":
            return True
        else:
            return False

    def select_user(self):
        selected_user = self.user_selector.get()
        if selected_user == "User1":
            self.current_user = self.wallet1
        else:
            self.current_user = self.wallet2
        self.update_balance()
    
    def deposit(self):
        try:
            amount = int(self.amount_entry.get())
            transaction_id = self.current_user.deposit(amount)
            self.update_balance()
            messagebox.showinfo("Deposit", f"Deposited Rs{amount}. Transaction ID: {transaction_id}")
        except ValueError as e:
            messagebox.showerror("Error", str(e))
    
    def withdraw(self):
        try:
            amount = int(self.amount_entry.get())
            transaction_id = self.current_user.withdraw(amount)
            self.update_balance()
            messagebox.showinfo("Withdrawal", f"Withdrew Rs{amount}. Transaction ID: {transaction_id}")
        except ValueError as e:
            messagebox.showerror("Error", str(e))
    
    def send_money(self):
        try:
            amount = int(self.amount_entry.get())
            recipient_name = self.recipient_selector.get()
            recipient_wallet = self.wallet1 if recipient_name == "User1" else self.wallet2
            self.current_user.send_money(recipient_wallet, amount)
            self.update_balance()
            messagebox.showinfo("Send Money", f"Sent Rs{amount} to {recipient_name}")
        except ValueError as e:
            messagebox.showerror("Error", str(e))
    
    def show_history(self):
        transactions = self.current_user.get_transactions()
        if transactions:
            history_str = f"Transaction History for {self.current_user.user_name}:\n\n"
            for transaction in transactions:
                if transaction[2] == 'Sent':
                    history_str += f"Transaction ID: {transaction[0]}, Type: {transaction[2]}, Amount: Rs{transaction[3]}, To: {transaction[4]}\n"
                else:
                    serial_number_str = transaction[1] if transaction[2] != 'Received' or self.current_user.user_name != transaction[4] else 'Hidden'
                    history_str += f"Transaction ID: {transaction[0]}, Serial Number: {serial_number_str}, Type: {transaction[2]}, Amount: Rs{transaction[3]}\n"
            messagebox.showinfo("Transaction History", history_str)
        else:
            messagebox.showinfo("Transaction History", "No transactions yet.")
    
    def show_serial_numbers(self):
        transactions = self.current_user.get_transactions()
        if transactions:
            serial_numbers_str = f"Serial Numbers for {self.current_user.user_name}:\n\n"
            for transaction in transactions:
                serial_number_str = transaction[1] if transaction[2] != 'Received' or self.current_user.user_name != transaction[4] else 'Hidden'
                serial_numbers_str += f"Serial Number: {serial_number_str}, Amount: Rs{transaction[3]}\n"
            messagebox.showinfo("Transaction Serial Numbers", serial_numbers_str)
        else:
            messagebox.showinfo("Transaction Serial Numbers", "No transactions yet.")

    def update_balance(self):
        self.balance_value.config(text=f"Rs{self.current_user.get_balance()}")

if __name__ == "__main__":
    root = tk.Tk()
    app = WalletApp(root)
    root.mainloop()
