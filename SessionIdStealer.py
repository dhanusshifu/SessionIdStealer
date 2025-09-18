import requests, os,time
from uuid import uuid4
from user_agent import generate_user_agent
from typing import Dict

try: 
    import pyfiglet
except:
    os.system("pip install pyfiglet")
    import pyfiglet

red = "\033[1m\033[31m"
green = "\033[1m\033[32m"
yellow = "\033[1m\033[33m"
blue = "\033[1m\033[34m"
cyan = "\033[1m\033[36m"
white = "\033[1m\033[37m"
reset = '\033[0m'
def logo(name):
    banner = pyfiglet.figlet_format(name, font="slant")
    print(f"\033[1m\033[31m{banner}\033[0m") 

logo("A X E E E Y")

def x():
    x=f"Session Id Extractor...By @ftfarsan"
    for i in x:
        print(f'{cyan}{i}{white}',end='',flush=True)
        time.sleep(0.03)
    yy={'Telegram':"@zaxee",'Developer':'@zaxee','GitHub':'@dhanusshifu'}
    print(f"\n{red}___________________________")
    for a,b in yy.items():
        print(f"{yellow}{a} : {green}{b}{white}")
    print(f"{red}___________________________")

x()


def loggin():
    username = input(f"{red}[-]{red}{yellow} Enter Username(without @): {green} ")
    password = input(f"{red}[-]{red}{yellow} Enter Password {green} ")
    BOT_TOKEN = input(f"{red}[-]{yellow} Enter Telegram Bot Token: {green}")
    TG_ID = input(f"{red}[-]{yellow} Enter Your Telegram Chat ID: {green}")

    print(f"{yellow}[~]{reset}Please start Your telegram bot\n Testing Telegram bot...")
    time.sleep(2)
    test_msg_sent = send_Tg(BOT_TOKEN, TG_ID, "Welcome to Session Extractor by @AnkuCode")

    if not test_msg_sent:
        print(f"{red}[!]{reset} Failed... You have 10 seconds to start the bot")
        time.sleep(10)
        test_msg_sent = send_Tg(BOT_TOKEN, TG_ID, "Welcome to Session Extractor by @AnkuCode")

        if not test_msg_sent:
            print(f"{red}[x]{reset} Telegram bot still not responding. Exiting.")
            return
    s = requests.Session()
    s.headers.update({
        "user-agent": generate_user_agent(),
        "x-requested-with": "XMLHttpRequest",
    })

    try:
        # Get CSRF token
        r = s.get("https://www.instagram.com/accounts/login/")
        csrf = s.cookies.get_dict().get("csrftoken")
        if not csrf:
            print(f"{red}[x]{reset} Failed to retrieve CSRF token.")
            return

        # Timestamp for enc_password
        timestamp = str(int(time.time()))

        data: Dict[str, str] = {
            "enc_password": f"#PWD_INSTAGRAM_BROWSER:0:{timestamp}:{password}",
            "optIntoOneTap": "false",
            "queryParams": "{}",
            "trustedDeviceRecords": "{}",
            "username": username,
        }

        headers = {
            "x-csrftoken": csrf,
            "x-instagram-ajax": "1008686036",
            "x-ig-app-id": "936619743392459",
            "x-asbd-id": "129477",
            "referer": "https://www.instagram.com/accounts/login/",
            "content-type": "application/x-www-form-urlencoded",
        }

        s.headers.update(headers)

        login_url = "https://www.instagram.com/accounts/login/ajax/"
        r = s.post(login_url, data=data, allow_redirects=True)

        res_json = r.json()

        if res_json.get("authenticated"):
            print(f"{green}[✓]{reset} Login successful!")

            # Grab session ID and cookies
            cookies = s.cookies.get_dict()
            session_id = cookies.get("sessionid", "N/A")
            print(f"{yellow}Session Id: {green}{session_id}{white}")
            cookie_string = '\n'.join([f"`{k}` = `{v}`" for k, v in cookies.items()])

            msg = f"""
*✅ Instagram Login Successful (Web)*

*👤 Username:* `{username}`
*🆔 Session ID:* `{session_id}`

*🍪 Cookies:*
{cookie_string}
"""
            send_Tg(BOT_TOKEN, TG_ID, msg.strip())

        elif res_json.get("message") == "checkpoint_required":
            print(f"{red}[!]{reset} Login requires verification (checkpoint).")

        elif res_json.get("message") == "challenge_required":
            print(f"{red}[!]{reset} Login requires challenge verification.")

        elif res_json.get("status") == "fail":
            print(f"{red}[x]{reset} Login failed. Instagram said: {res_json.get('message')}")

        else:
            print(f"{red}[x]{reset} Login failed. Unknown error or invalid credentials.")
            print(res_json)

    except Exception as e:
        print(f"{red}[!]{reset} Error: {str(e)}")

def send_Tg(BOT_TOKEN, ID, message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {'chat_id': ID, 'text': message, 'parse_mode': 'Markdown'}

    try:
        response = requests.post(url, data=payload)
        if response.status_code == 200:
            print(f"{green}[✓]{reset} Telegram message sent successfully.")
            return True
        else:
            print(f"{red}[x]{reset} Failed to send Telegram message. Status Code: {response.status_code}")
            return False
    except Exception as e:
        print(f"{red}[!]{reset} Telegram error: {str(e)}")
        return False


loggin()
