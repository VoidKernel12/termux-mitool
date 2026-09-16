import os
import time
import subprocess
import sys

# Terminal Color Codes
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RESET = "\033[0m"

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def check_dependencies():
    """Check if adb and fastboot are installed in Termux."""
    missing = []
    for tool in ['adb', 'fastboot']:
        res = subprocess.run(['which', tool], capture_output=True, text=True)
        if res.returncode != 0:
            missing.append(tool)
    
    if missing:
        clear_screen()
        print(f"{RED}[!] Error: Required tools missing: {', '.join(missing)}{RESET}")
        print(f"{YELLOW}[*] Please install them in Termux using: {CYAN}pkg install android-tools{RESET}\n")
        return False
    return True

def show_main_menu():
    clear_screen()
    print(f"{CYAN}==================================================")
    print(" SMART XIAOMI TERMUX TOOLKIT (PRO MAX v1.2 FIXED) ")
    print(f"=================================================={RESET}")
    print(f" {GREEN}[1]{RESET} Unlock Bootloader (MIUI)")
    print(f" {GREEN}[2]{RESET} Unlock Bootloader (HyperOS)")
    print(f" {GREEN}[3]{RESET} Flash ROM (Auto-Detect & Smart Safe)")
    print(f" {GREEN}[4]{RESET} Mi Assistant (Advanced)")
    print(f" {RED}[5]{RESET} Exit")
    print(f"{CYAN}=================================================={RESET}")

def show_sub_menu(title, options):
    clear_screen()
    print(f"{CYAN}==================================================")
    print(f" {title.upper()} ")
    print(f"=================================================={RESET}")
    for idx, opt in enumerate(options, 1):
        print(f" {GREEN}[{idx}]{RESET} {opt}")
    print(f"{CYAN}=================================================={RESET}")

def check_fastboot_connected():
    """Verify if a device is connected in fastboot mode."""
    try:
        res = subprocess.run(['fastboot', 'devices'], capture_output=True, text=True, timeout=5)
        devices = res.stdout.strip()
        if not devices:
            print(f"{RED}[-] No fastboot device found! Check your OTG cable & phone mode.{RESET}")
            return False
        print(f"{GREEN}[+] Device found:\n{devices}{RESET}")
        return True
    except Exception as e:
        print(f"{RED}[-] Error checking fastboot: {e}{RESET}")
        return False

def smart_unlock_device():
    """Safe unlock attempt with connection validation."""
    if not check_fastboot_connected():
        return False

    print(f"\n{YELLOW}[*] Testing 'fastboot flashing unlock' support...{RESET}")
    try:
        res = subprocess.run(['fastboot', 'flashing', 'unlock'], capture_output=True, text=True, timeout=15)
        output = (res.stdout + res.stderr).lower()

        if res.returncode == 0 or "okay" in output:
            print(f"{GREEN}[+] 'flashing unlock' command accepted! Check phone screen.{RESET}")
            return True

        print(f"{YELLOW}[!] 'flashing unlock' not accepted. Trying 'oem unlock'...{RESET}")
        res_oem = subprocess.run(['fastboot', 'oem', 'unlock'], capture_output=True, text=True, timeout=15)
        oem_output = (res_oem.stdout + res_oem.stderr).lower()

        if res_oem.returncode == 0 or "okay" in oem_output:
            print(f"{GREEN}[+] 'oem unlock' command accepted! Check phone screen.{RESET}")
            return True

        print(f"\n{RED}[-] Unlock failed. Modern Xiaomi/HyperOS devices require official Mi Unlock PC tool / Token.{RESET}")
        return False
    except Exception as e:
        print(f"{RED}[-] Error during smart unlock: {e}{RESET}")
        return False

def run_unlock(is_hyperos=False):
    clear_screen()
    print(f"{YELLOW}==================================================")
    print(" SMART BOOTLOADER UNLOCK AUTOMATION ")
    print(f"=================================================={RESET}")

    if is_hyperos:
        print(f"{RED}[!] WARNING: HyperOS requires account binding + wait time + PC Mi Unlock!{RESET}")
        print(f"{RED}[!] Fastboot commands alone cannot bypass Xiaomi server lock.{RESET}\n")
        cont = input(f"{CYAN}Still want to try fastboot command? (y/n): {RESET}").strip().lower()
        if cont != 'y': 
            return
    else:
        print(f"{RED}[!] WARNING: Unlocking will wipe all user data!{RESET}")

    action = input(f"\n{CYAN}Press Enter to start or 'q' to cancel: {RESET}").strip()
    if action.lower() == 'q': 
        return

    print(f"\n{YELLOW}[*] Running Smart Unlock Sequence...{RESET}")
    smart_unlock_device()
    input(f"\n{CYAN}Press Enter to return...{RESET}")

def handle_unlock(name, is_hyperos=False):
    while True:
        options = ["Open Login Portal & Unlock Setup", "Back"]
        show_sub_menu(name, options)
        choice = input(f"{CYAN}Select (1-2): {RESET}").strip()

        if choice == '1':
            clear_screen()
            print(f"{YELLOW}Opening Xiaomi Account Portal...{RESET}")
            try:
                subprocess.run(['termux-open-url', 'https://account.xiaomi.com'])
            except Exception:
                try:
                    subprocess.run(['am', 'start', '-a', 'android.intent.action.VIEW', '-d', 'https://account.xiaomi.com'])
                except Exception:
                    print(f"{RED}[-] Please open https://account.xiaomi.com manually in your browser.{RESET}")

            print(f"\n{CYAN}Instructions:{RESET}")
            print("1. Login & Bind account on target device")
            print("2. Wait required time (if prompted)")
            print("3. Return here and type 'done'")

            while True:
                ans = input(f"\n{CYAN}Type {GREEN}'done'{CYAN} when finished (or {RED}'back'{CYAN}): {RESET}").strip().lower()
                if ans == 'done' or ans == '':
                    run_unlock(is_hyperos)
                    break
                elif ans == 'back':
                    break
                else:
                    print(f"{RED}Invalid input. Type 'done' or 'back'.{RESET}")
            break
        elif choice == '2':
            break

def handle_rom():
    while True:
        options = ["Check Fastboot Devices", "Flash Fastboot ROM (Safe Mode)", "Back"]
        show_sub_menu("Flash ROM", options)
        choice = input(f"{CYAN}Select (1-3): {RESET}").strip()

        if choice == '1':
            clear_screen()
            check_fastboot_connected()
            input(f"\n{CYAN}Press Enter to return...{RESET}")

        elif choice == '2':
            clear_screen()
            if not check_fastboot_connected():
                input(f"\n{CYAN}Press Enter to return...{RESET}")
                continue

            print(f"{YELLOW}[i] ROM ফোল্ডারটির পুরো সঠিক পাথ (Path) লিখুন{RESET}")
            path = input(f"{CYAN}Enter extracted ROM folder path: {RESET}").strip()
            
            if os.path.isdir(path):
                flash_script = os.path.join(path, 'flash_all.sh')

                if os.path.exists(flash_script):
                    print(f"{YELLOW}[*] Executing flash_all.sh using bash...{RESET}")
                    try:
                        subprocess.run(['bash', flash_script])
                        print(f"\n{GREEN}[+] Flash script finished!{RESET}")
                    except Exception as e:
                        print(f"{RED}[-] Failed to run flash_all.sh: {e}{RESET}")
                else:
                    print(f"\n{YELLOW}[!] Safe Flash Mode: flash_all.sh পাওয়া যায়নি!{RESET}")
                    print(f"{YELLOW}[!] রেন্ডম ফাইল ফ্ল্যাশ না করে প্রয়োজনীয় নির্দিষ্ট ফাইল পারমিশন চাওয়া হচ্ছে:{RESET}\n")
                    
                    critical_imgs = ['boot.img', 'init_boot.img', 'recovery.img', 'vendor_boot.img']
                    found_any = False

                    for img in critical_imgs:
                        img_path = os.path.join(path, img)
                        if os.path.exists(img_path):
                            found_any = True
                            part_name = os.path.splitext(img)[0]
                            confirm = input(f"{CYAN}Flash '{img}' to partition '{part_name}'? (y/n): {RESET}").strip().lower()
                            if confirm == 'y':
                                print(f"{YELLOW}[*] Flashing {part_name}...{RESET}")
                                subprocess.run(['fastboot', 'flash', part_name, img_path])

                    if not found_any:
                        print(f"{RED}[-] No basic flashable images (boot, recovery) found in this folder.{RESET}")
                    else:
                        print(f"\n{GREEN}[+] Flashing process completed!{RESET}")
            else:
                print(f"{RED}[-] Invalid directory path!{RESET}")
            input(f"\n{CYAN}Press Enter to return...{RESET}")

        elif choice == '3':
            break

def handle_mi_assistant():
    while True:
        options = [
            "ADB Sideload (Flash Zip)",
            "Reboot System",
            "Reboot to Fastboot",
            "Wipe Data (Fastboot -w)",
            "Check ADB Device",
            "Back"
        ]
        show_sub_menu("Mi Assistant (Advanced)", options)
        choice = input(f"{CYAN}Select (1-6): {RESET}").strip()

        if choice == '1':
            clear_screen()
            print(f"{YELLOW}[*] Make sure phone is in Recovery Sideload mode!{RESET}")
            zpath = input(f"{CYAN}Enter Recovery Zip file path: {RESET}").strip()
            if os.path.exists(zpath) and zpath.endswith('.zip'):
                print(f"{YELLOW}[*] Starting ADB Sideload...{RESET}")
                res = subprocess.run(['adb', 'sideload', zpath])
                if res.returncode == 0:
                    print(f"{GREEN}[+] Sideload Done!{RESET}")
                else:
                    print(f"{RED}[-] Sideload process failed.{RESET}")
            else:
                print(f"{RED}[-] Invalid zip file path!{RESET}")
            input(f"\n{CYAN}Press Enter to return...{RESET}")

        elif choice == '2':
            print(f"{YELLOW}[*] Rebooting system...{RESET}")
            subprocess.run(['adb', 'reboot'])
            input(f"\n{CYAN}Press Enter to return...{RESET}")

        elif choice == '3':
            print(f"{YELLOW}[*] Rebooting to Fastboot...{RESET}")
            subprocess.run(['adb', 'reboot', 'bootloader'])
            input(f"\n{CYAN}Press Enter to return...{RESET}")

        elif choice == '4':
            clear_screen()
            if check_fastboot_connected():
                print(f"{RED}[!] WARNING: This will WIPE ALL DATA on device!{RESET}")
                confirm = input(f"{CYAN}Type 'yes' to confirm data wipe: {RESET}").strip().lower()
                if confirm == 'yes':
                    print(f"{YELLOW}[*] Executing 'fastboot -w'...{RESET}")
                    res = subprocess.run(['fastboot', '-w'])
                    if res.returncode == 0:
                        print(f"{GREEN}[+] Data wipe successful!{RESET}")
                    else:
                        print(f"{RED}[-] Wipe failed.{RESET}")
            input(f"\n{CYAN}Press Enter to return...{RESET}")

        elif choice == '5':
            clear_screen()
            try:
                res = subprocess.run(['adb', 'devices'], capture_output=True, text=True, timeout=5)
                print(f"{GREEN}{res.stdout.strip() if res.stdout.strip() else 'No ADB device found.'}{RESET}")
            except Exception as e:
                print(f"{RED}[-] Error: {e}{RESET}")
            input(f"\n{CYAN}Press Enter to return...{RESET}")

        elif choice == '6':
            break

def main():
    if not check_dependencies():
        sys.exit(1)

    while True:
        show_main_menu()
        choice = input(f"{CYAN}Select (1-5): {RESET}").strip()
        if choice == '1':
            handle_unlock("Unlock Bootloader (MIUI)", False)
        elif choice == '2':
            handle_unlock("Unlock Bootloader (HyperOS)", True)
        elif choice == '3':
            handle_rom()
        elif choice == '4':
            handle_mi_assistant()
        elif choice == '5':
            print(f"{GREEN}Goodbye!{RESET}")
            break
        else:
            print(f"{RED}Invalid choice!{RESET}")
            time.sleep(1)

if __name__ == "__main__":
    main()
