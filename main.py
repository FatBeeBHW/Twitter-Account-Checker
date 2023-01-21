from colorama import Fore, init
from configparser import ConfigParser
from time import sleep, perf_counter
import httpx
import os
import pyfiglet
import threading
from const import *

# file paths
invalid_path = "output/invalid.txt"
valid_path = "output/valid.txt"
flagged_path = "output/flagged.txt"

# Clear Files
open(invalid_path, 'w').close()
open(flagged_path, 'w').close()
open(valid_path, 'w').close()


# Read config.ini file
config_object = ConfigParser()
config_object.read("config.ini")
settings = config_object["SETTINGS"]
sproxy = settings["proxy"]
checkflag = settings["checkflag"]
addct0 = settings["addct0"]
saveastoken = settings["saveastoken"]

# Fuck you python
if "True" in checkflag:
    checkflag = True
else:
    checkflag = False

if "True" in addct0:
    addct0 = True
else:
    addct0 = False

if "True" in saveastoken:
    saveastoken = True
else:
    saveastoken = False

# Dynamic Clear Console
def cls():
    os.system('cls' if os.name == 'nt' else 'clear')


# Initial Stuff & Banner
init(autoreset=True)
os.system("title FatBee's Account Checker")
cls()
ascii_banner = pyfiglet.figlet_format("FatBee's Checker")
print(f"{Fore.YELLOW}{ascii_banner}")
print(f"{Fore.WHITE}🐝 Made by {Fore.LIGHTYELLOW_EX}FatBee{Fore.WHITE}  |  💬 Telegram: {Fore.LIGHTBLUE_EX}@fatbeebhw{Fore.WHITE}  |  💬 Telegram Group: {Fore.LIGHTBLUE_EX}@twitteropensource{Fore.WHITE}  |  Version: {Fore.LIGHTGREEN_EX}{VERSION}")

proxy = sproxy
proxies = {"all://": f"http://{proxy}"}

noct0 = False
isonlytoken = False

# Load Tokens
tokens = open("accounts.txt", "r").read().splitlines()
if len(tokens) == 0:
    print(f"{Fore.YELLOW}\n[!] Accounts File is Empty.\n")
    exit()
else:
    print(
        f"{Fore.YELLOW}\n[!] Loaded {Fore.CYAN}{len(tokens)} {Fore.YELLOW}Accounts")

# Format Detection
if len(tokens[1]) < 60:
    print(f"{Fore.YELLOW}[!] Token Only Format Detected.")
    isonlytoken = True
elif len(tokens[1]) > 60 and len(tokens[1]) < 200:
    print(f"{Fore.YELLOW}[!] No ct0 Format detected.")
    noct0 = True
elif len(tokens[1]) > 240:
    print(f"{Fore.YELLOW}[!] Standard Format detected.")

if noct0 == True and isonlytoken == False and addct0 == True:
    print(f"{Fore.YELLOW}[!] ct0 will be added in the output.")

if saveastoken == True and isonlytoken == False:
    print(f"{Fore.YELLOW}[!] Export will be done in Token Only Format.")

# Data Usage
initialdatausage = len(tokens) * 2.6
expecteddu = initialdatausage / 1000
expecteddu = round(expecteddu, 3)
print(f"{Fore.YELLOW}[!] Expected Data Usage is less than {Fore.CYAN}{expecteddu} MB")

# Expected Time to complete
initialtime = len(tokens) * 0.45
mmf, ssf = divmod(initialtime, 60)
mmrf = round(mmf)
ssrf = round(ssf)
print(f"{Fore.YELLOW}[!] Expected Run Time: {Fore.CYAN}{mmrf} Minute(s) {ssrf} Second(s)\n")
print(f"{Fore.YELLOW}========== {Fore.CYAN}Initializing Threads {Fore.YELLOW}========== \n\n")

# % Calc
def get_percentage_difference(num_a, num_b):
    return (abs(num_a - num_b) / num_b) * 100

# Update Title
def titleupdate():
    with open(invalid_path, "r") as deadacc:
        deadcount = len(deadacc.readlines())

    with open(valid_path, "r") as validcc:
        validacc = len(validcc.readlines())

    if checkflag == True and isonlytoken == False:
        with open(flagged_path, "r") as flagacc:
            flagcount = len(flagacc.readlines())
        os.system(("title Valid: %s / Invalid: %s / Flagged: %s" %
                  (validacc, deadcount, flagcount)))
    else:
        os.system(("title Valid: %s / Invalid: %s" % (validacc, deadcount)))


# Final Stats
def check_completed():
    with open(invalid_path, "r") as deadacc:
        deadcount = len(deadacc.readlines())

    with open(flagged_path, "r") as flagacc:
        flagcount = len(flagacc.readlines())

    with open(valid_path, "r") as validcc:
        validacc = len(validcc.readlines())

    with open("accounts.txt", "r") as totalacc:
        totalcheck = len(totalacc.readlines())

    totalbad = deadcount + flagcount
    precent = get_percentage_difference(totalbad, totalcheck)
    precent = 100 - precent
    precent = round(precent, 3)
    t1_stop = perf_counter()
    finaltime = t1_stop-t1_start

    mm, ss = divmod(finaltime, 60)
    mmr = round(mm)
    ssr = round(ss)
    cls()
    ascii_banner = pyfiglet.figlet_format("FatBee's Checker")
    print(f"{Fore.YELLOW}{ascii_banner}")
    print(f"{Fore.WHITE}🐝 Made by {Fore.LIGHTYELLOW_EX}FatBee{Fore.WHITE}  |  💬 Telegram: {Fore.LIGHTBLUE_EX}@fatbeebhw{Fore.WHITE}  |  💬 Telegram Group: {Fore.LIGHTBLUE_EX}@twitteropensource{Fore.WHITE}  |  Version: {Fore.LIGHTGREEN_EX}{VERSION}")
    print("")
    print(f"{Fore.LIGHTYELLOW_EX}[*] {Fore.LIGHTWHITE_EX}Done in: {Fore.CYAN}{mmr} Minute(s) {ssr} Seconds")
    print(f"{Fore.LIGHTYELLOW_EX}[*] {Fore.LIGHTWHITE_EX}Accounts Checked: {Fore.LIGHTYELLOW_EX}{totalcheck}")
    print(f"{Fore.LIGHTYELLOW_EX}[*] {Fore.LIGHTWHITE_EX}Lock Rate: {Fore.RED}{precent}%")
    print(f"{Fore.LIGHTYELLOW_EX}[*] {Fore.LIGHTWHITE_EX}Valid Accounts: {Fore.LIGHTGREEN_EX}{validacc}")
    print(f"{Fore.LIGHTYELLOW_EX}[*] {Fore.LIGHTWHITE_EX}Invalid Accounts: {Fore.RED}{deadcount}")
    
    if checkflag == True and isonlytoken == False:
        print(f"{Fore.LIGHTYELLOW_EX}[*] {Fore.LIGHTWHITE_EX}Flagged Accounts: {Fore.LIGHTRED_EX}{flagcount}")
    else:
        print(f"{Fore.LIGHTYELLOW_EX}[*] {Fore.LIGHTWHITE_EX}No Flag Check was done or format is Token only.")
        
    print("")
    print("")
    print(f"{Fore.RED} ** RESTARTING THE CHECKER WILL DELETE ALL THE FILES IN OUTPUT FOLDER**")
    input(f"\n{Fore.WHITE}Press any key to exit..")


# Checking Process
t1_start = perf_counter()
def check(auth=None, screen_name=None, password=None, email_or_phone=None, ct0s=None):
    while True:
        retryme = 0
        try:
            session = httpx.Client(http2=False, proxies=proxies)

            if checkflag == True and screen_name != None:
                session.headers.update(
                    {"authorization": "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA"})
                resp = session.post(
                    "https://api.twitter.com/1.1/guest/activate.json", headers=ACTIVATE_HEADERS)
                guest_token = (resp.json())["guest_token"]
                checker_url = f"https://twitter.com/i/api/graphql/hVhfo_TquFTmgL7gYwf91Q/UserByScreenName?variables=%7B%22screen_name%22%3A%22{screen_name}%22%2C%22withSafetyModeUserFields%22%3Atrue%2C%22withSuperFollowsUserFields%22%3Atrue%7D&features=%7B%22responsive_web_twitter_blue_verified_badge_is_enabled%22%3Atrue%2C%22verified_phone_label_enabled%22%3Afalse%2C%22responsive_web_twitter_blue_new_verification_copy_is_enabled%22%3Atrue%2C%22responsive_web_graphql_timeline_navigation_enabled%22%3Atrue%7D"

                CHECK_HEADERS['referer'] = f"https://twitter.com/{screen_name}"
                CHECK_HEADERS['x-guest-token'] = guest_token
                resp = session.get(checker_url, headers=CHECK_HEADERS)

                isgood = resp.text
                if "fake_account" in isgood:
                    print(
                        f"{Fore.LIGHTRED_EX}[-]{Fore.RESET} {Fore.CYAN}{screen_name} {Fore.LIGHTWHITE_EX}({auth}){Fore.LIGHTRED_EX} is flagged as Fake Account.")
                    save = open(invalid_path, "a")
                    save.write(
                        f"{screen_name}:{password}:{email_or_phone}:{ct0s}:{auth}\n")
                    save.close()
                    titleupdate()
                    break
                elif "offensive_profile_content" in isgood:
                    print(
                        f"{Fore.LIGHTRED_EX}[-]{Fore.RESET} {Fore.CYAN}{screen_name} {Fore.LIGHTWHITE_EX}({auth}){Fore.LIGHTRED_EX} has Offensive Content.")
                    save = open(flagged_path, "a")
                    save.write(
                        f"{screen_name}:{password}:{email_or_phone}:{ct0s}:{auth}\n")
                    save.close()
                    titleupdate()
                    break
                elif "suspends" in isgood:
                    print(
                        f"{Fore.LIGHTRED_EX}[-]{Fore.RESET} {Fore.CYAN}{screen_name} {Fore.LIGHTWHITE_EX}({auth}){Fore.LIGHTRED_EX} is Suspended.")
                    save = open(invalid_path, "a")
                    save.write(
                        f"{screen_name}:{password}:{email_or_phone}:{ct0s}:{auth}\n")
                    save.close()
                    titleupdate()
                    break

            if isonlytoken == False:
                cookies = {
                    'auth_token': auth
                }

                if noct0 == False:
                    cookies['ct0'] = ct0s
                    STANDARD_HEADERS['x-csrf-token'] = ct0s
                    response = session.post(
                        PROFILE_UPDATE, cookies=cookies, headers=STANDARD_HEADERS)
                    if response.status_code == 200:
                        print(
                            f"{Fore.LIGHTGREEN_EX}[+]{Fore.RESET} {Fore.CYAN}{screen_name} {Fore.LIGHTWHITE_EX}({auth}){Fore.LIGHTGREEN_EX} is valid.")
                        if saveastoken == True:
                            save = open(valid_path, "a")
                            save.write(f"{auth}\n")
                            save.close()
                            titleupdate()
                            break
                        else:
                            save = open(valid_path, "a")
                            save.write(
                                f"{screen_name}:{password}:{email_or_phone}:{ct0s}:{auth}\n")
                            save.close()
                            titleupdate()
                            break
                    else:
                        print(
                            f"{Fore.LIGHTRED_EX}[-]{Fore.RESET} {Fore.CYAN}{screen_name} {Fore.LIGHTWHITE_EX}({auth}){Fore.LIGHTRED_EX} is invalid.")
                        save = open(invalid_path, "a")
                        save.write(
                            f"{screen_name}:{password}:{email_or_phone}:{ct0s}:{auth}\n")
                        save.close()
                        titleupdate()
                        break
                if noct0 == True:
                    ct0_response = session.post(
                        PROFILE_UPDATE, cookies=cookies, headers=STANDARD_HEADERS)
                    ct0 = ct0_response.cookies['ct0']
                    cookies['ct0'] = ct0
                    STANDARD_HEADERS['x-csrf-token'] = ct0
                    if ct0_response.status_code != 401:
                        response = session.post(
                            PROFILE_UPDATE, cookies=cookies, headers=STANDARD_HEADERS)
                        if response.status_code == 200:
                            print(
                                f"{Fore.LIGHTGREEN_EX}[+]{Fore.RESET} {Fore.CYAN}{screen_name} {Fore.LIGHTWHITE_EX}({auth}){Fore.LIGHTGREEN_EX} is valid.")
                            if saveastoken == True:
                                save = open(valid_path, "a")
                                save.write(f"{auth}\n")
                                save.close()
                                titleupdate()
                                break
                            elif addct0 == True and saveastoken == False:
                                save = open(valid_path, "a")
                                save.write(
                                    f"{screen_name}:{password}:{email_or_phone}:{ct0}:{auth}\n")
                                save.close()
                                titleupdate()
                                break
                            elif addct0 == False and saveastoken == False:
                                save = open(valid_path, "a")
                                save.write(
                                    f"{screen_name}:{password}:{email_or_phone}:{auth}\n")
                                save.close()
                                titleupdate()
                                break
                        else:
                            print(
                                f"{Fore.LIGHTRED_EX}[-]{Fore.RESET} {Fore.CYAN}{screen_name} {Fore.LIGHTWHITE_EX}({auth}){Fore.LIGHTRED_EX} is invalid.")
                            save = open(invalid_path, "a")
                            save.write(
                                f"{screen_name}:{password}:{email_or_phone}:{auth}\n")
                            save.close()
                            titleupdate()
                            break
                    else:
                        print(
                            f"{Fore.LIGHTRED_EX}[-]{Fore.RESET} {Fore.CYAN}{screen_name} {Fore.LIGHTWHITE_EX}({auth}){Fore.LIGHTRED_EX} is invalid.")
                        save = open(invalid_path, "a")
                        save.write(
                            f"{screen_name}:{password}:{email_or_phone}:{auth}\n")
                        save.close()
                        titleupdate()
                    break

            elif isonlytoken == True:

                cookies = {
                    'auth_token': auth
                }

            # fetch ct0 from cookies
            ct0_response = session.post(
                PROFILE_UPDATE, cookies=cookies, headers=STANDARD_HEADERS)
            
            ct0 = ct0_response.cookies['ct0']
            cookies['ct0'] = ct0
            STANDARD_HEADERS['x-csrf-token'] = ct0

            if ct0_response.status_code != 401:
                response = session.post(
                    PROFILE_UPDATE, cookies=cookies, headers=STANDARD_HEADERS)
                if response.status_code == 200:
                    print(
                        f"{Fore.LIGHTGREEN_EX}[+] {Fore.RESET}{Fore.LIGHTWHITE_EX}({auth}){Fore.LIGHTGREEN_EX} is valid.")
                    save = open(valid_path, "a")
                    save.write(f"{auth}\n")
                    save.close()
                    break
                else:
                    print(
                        f"{Fore.LIGHTRED_EX}[-] {Fore.RESET}{Fore.LIGHTWHITE_EX}({auth}){Fore.LIGHTRED_EX} is invalid.")
                    save = open(invalid_path, "a")
                    save.write(f"{auth}\n")
                    save.close()
                    titleupdate()
                    break
            else:
                print(
                    f"{Fore.LIGHTRED_EX}[-] {Fore.RESET}{Fore.LIGHTWHITE_EX}({auth}){Fore.LIGHTRED_EX} is invalid.")
                save = open(invalid_path, "a")
                save.write(f"{auth}\n")
                save.close()
                titleupdate()
            break

        except Exception as err:
            retryme += 1
            print(f"{Fore.LIGHTYELLOW_EX}[!] {err} | Retry: #{retryme}")
            continue


threads = []

for x in range(len(tokens)):
    try:
        if isonlytoken == False and noct0 == False:
            auth = tokens[x].split(':')[4]
            ct0s = tokens[x].split(':')[3]
            email_or_phone = tokens[x].split(':')[2]
            password = tokens[x].split(':')[1]
            screen_name = tokens[x].split(':')[0]
            t = threading.Thread(target=check, args=(
                auth, screen_name, password, email_or_phone, ct0s))
            t.daemon = True
            threads.append(t)

        elif isonlytoken == True:
            t = threading.Thread(target=check, args=(tokens[x],))
            t.daemon = True
            threads.append(t)

        elif noct0 == True:
            auth = tokens[x].split(':')[3]
            email_or_phone = tokens[x].split(':')[2]
            password = tokens[x].split(':')[1]
            screen_name = tokens[x].split(':')[0]
            t = threading.Thread(target=check, args=(
                auth, screen_name, password, email_or_phone))
            t.daemon = True
            threads.append(t)
    except Exception as e:
        print(e)


for x in range(len(tokens)):
    try:
        sleep(0.05)
        threads[x].start()
    except Exception as e:
        print(e)

for x in range(len(tokens)):
    threads[x].join()

check_completed()
