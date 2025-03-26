
import sys
import requests


from get_new_CB_announcement import check_new_announcements  # 匯入函式


def notify_discord_webhook(msg):
    url = 'https://discord.com/api/webhooks/1326821713266081864/gEH_ld99DB2qGdF8a3vk80mDW-Pc3H1kzFzYSNG1gqDxzdFcgArcKLP-fn0LKoUT85cw'
    headers = {"Content-Type": "application/json"}
    data = {"content": msg, "username": "公告-可轉債"}
    res = requests.post(url, headers = headers, json = data) 
    if res.status_code in (200, 204):
            print(f"Request fulfilled with response: {res.text}")
    else:
            print(f"Request failed with response: {res.status_code}-{res.text}")


def generate_msg():
    new_announcements = check_new_announcements()  # 呼叫函式取得新公告
    if new_announcements:
        msg = '\n\n'.join(
            f"{announcement['CDATE']}{announcement['CTIME']}\n{announcement['COMPANY_ID']} {announcement['COMPANY_NAME']}\n{announcement['SUBJECT']}\n{announcement['HYPERLINK']}"
            for announcement in new_announcements
        )
        return msg
    return None

def job():
    msg = generate_msg()
    if msg:
        notify_discord_webhook(msg)


def signal_handler(sig, frame):
    global running
    print('Stopping the scheduler...')
    running = False
    sys.exit(0)

if __name__ == "__main__":

    job()  # 立即執行一次
    
