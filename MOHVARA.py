import os
import subprocess
from art import text2art
from colorama import Fore, Style, init

# تهيئة colorama
init(autoreset=True)

def clear_screen():
    """مسح الشاشة"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_intro(name):
    """طباعة مقدمة الأداة"""
    clear_screen()
    print(Fore.GREEN + Style.BRIGHT + text2art(name, font='slant'))
    print(Fore.LIGHTYELLOW_EX + "=" * 80)
    print(Fore.LIGHTYELLOW_EX + "| " + "Codec By M0HVARA === www.facebook.com/mohvara".center(76) + " |")
    print(Fore.LIGHTYELLOW_EX + "=" * 80)
    print(Fore.RED + Style.BRIGHT + "\u2554" + "\u2550" * 77 + "\u2557")
    print(Fore.RED + Style.BRIGHT + "\u2551" + f' HOME PAGE! '.center(77) + "\u2551")
    print(Fore.RED + Style.BRIGHT + "\u255A" + "\u2550" * 77 + "\u255D")
    print("\n")
def main_menu():
    """عرض قائمة الاختيار الرئيسية"""
    clear_screen()
    print_intro("M0HVARA")
    print("\033[44m \033[22m \033[4m Choose the page to display: \n")
    print(Fore.RED + "-" * 26)
    print(Fore.MAGENTA + Style.BRIGHT + "01 - Instagram")
    print(Fore.CYAN + Style.BRIGHT + "02 - Facebook")
    print(Fore.RED + "-" * 26)

    choice = input( "\033[44m \033[22m \033[4m Enter your choice (1 or 2): \n" + Style.RESET_ALL).strip()

    if choice == "1":
        clear_screen()
        run_instagram_script()
    elif choice == "2":
        clear_screen()
        run_facebook_script()
    else:
        print(Fore.RED + "Invalid choice. Please select 1 or 2.")
        input("Press Enter to return to the menu...")
        main_menu()

def run_instagram_script():
    """تشغيل سكريبت إنستغرام"""
    script_path = os.path.join('Resources', 'instagram_script.py')
    try:
        subprocess.run(["python", script_path], check=True)
    except subprocess.CalledProcessError as e:
        print(Fore.RED + f"Error occurred: {e}")
    except Exception as e:
        print(Fore.RED + f"An unexpected error occurred: {e}")

def run_facebook_script():
    """تشغيل سكريبت فيسبوك"""
    script_path = os.path.join('Resources', 'facebook_script.py')
    try:
        subprocess.run(["python", script_path], check=True)
    except subprocess.CalledProcessError as e:
        print(Fore.RED + f"Error occurred: {e}")
    except Exception as e:
        print(Fore.RED + f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main_menu()
