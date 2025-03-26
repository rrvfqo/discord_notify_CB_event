'''
查詢公告快易查網站，關鍵字為"轉換公司債"，並將新公告發送通知
'''

import requests
import json
from datetime import datetime, timedelta
# import os



# 台灣證券交易所公告網址
announcement_url = "https://mopsov.twse.com.tw/mops/web/ezsearch_query"

# # 紀錄已發送的公告檔案路徑
# sent_announcements_file = "sent_announcements.json"
# # 紀錄上次檢查日期的檔案路徑
# last_checked_date_file = "last_checked_date.txt"

# def load_sent_announcements():
#     if os.path.exists(sent_announcements_file):
#         with open(sent_announcements_file, "r", encoding="utf-8") as file:
#             content = file.read().strip()
#             if content:
#                 return set(json.loads(content))
#     return set()

# def save_sent_announcements(sent_announcements):
#     with open(sent_announcements_file, "w", encoding="utf-8") as file:
#         json.dump(list(sent_announcements), file, ensure_ascii=False, indent=4)

# def load_last_checked_date():
#     if os.path.exists(last_checked_date_file):
#         with open(last_checked_date_file, "r", encoding="utf-8") as file:
#             return file.read().strip()
#     return None

# def save_last_checked_date(date):
#     with open(last_checked_date_file, "w", encoding="utf-8") as file:
#         file.write(date)

# # 紀錄已發送的公告
# sent_announcements = load_sent_announcements()
# # 紀錄上次檢查日期
# last_checked_date = load_last_checked_date()


def get_sii_announcement():
    today = datetime.now().strftime('%Y%m%d')

    # 上市公司公告參數
    announcement_body = f'step=00&RADIO_CM=1&TYPEK=sii&CO_MARKET=&CO_ID=&PRO_ITEM=&SUBJECT=%E8%BD%89%E6%8F%9B%E5%85%AC%E5%8F%B8%E5%82%B5&SDATE={today}&EDATE=&lang=TW&AN='

    # 取得公告資訊
    response = requests.post(announcement_url, data=announcement_body)

    if response.status_code == 200:
        # 移除 UTF-8 BOM
        json_data = response.text.lstrip('\ufeff')
        # 將 JSON 資料轉換為 Python dict
        response_dict = json.loads(json_data)

        # 篩選出 'ctime' 與現在時間相差一小時以內的資料
        one_hour_ago = datetime.now() - timedelta(hours=1)
        print(f"SII one_hour_ago = {one_hour_ago}")
        filtered_data = []
        for announcement in response_dict.get("data", []):
            print(f"SII announcement = {announcement}")
            # 將當天日期補充到 CTIME 中
            full_ctime = f"{datetime.now().strftime('%Y-%m-%d')} {announcement['CTIME']}"
            try:
                announcement_time = datetime.strptime(full_ctime, '%Y-%m-%d %H:%M:%S')
                print(f"SII announcement_time = {announcement_time}") 
                if announcement_time >= one_hour_ago:
                    filtered_data.append(announcement)
                    print(f"SII announcement = {announcement}")
            except ValueError:
                # 如果時間格式不正確，跳過該公告
                print("時間格式不正確")
                continue

        response_dict["data"] = filtered_data
        return response_dict
    return {"data": [], "message": ["查無公告資料"], "status": "fail"}

def get_otc_announcement():
    today = datetime.now().strftime('%Y%m%d')

    # 上櫃公司公告參數
    announcement_body = f'step=00&RADIO_CM=1&TYPEK=otc&CO_MARKET=&CO_ID=&PRO_ITEM=&SUBJECT=%E8%BD%89%E6%8F%9B%E5%85%AC%E5%8F%B8%E5%82%B5&SDATE={today}&EDATE=&lang=TW&AN='

    # 取得公告資訊
    response = requests.post(announcement_url, data=announcement_body)

    if response.status_code == 200:
        # 移除 UTF-8 BOM
        json_data = response.text.lstrip('\ufeff')
        # 將 JSON 資料轉換為 Python dict
        response_dict = json.loads(json_data)

        # 篩選出 'ctime' 與現在時間相差一小時以內的資料
        one_hour_ago = datetime.now() - timedelta(hours=1)
        print(f"OTC one_hour_ago = {one_hour_ago}")
        filtered_data = []
        for announcement in response_dict.get("data", []):
            print(f"OTC announcement = {announcement}")
            # 將當天日期補充到 CTIME 中
            full_ctime = f"{datetime.now().strftime('%Y-%m-%d')} {announcement['CTIME']}"
            try:
                announcement_time = datetime.strptime(full_ctime, '%Y-%m-%d %H:%M:%S')
                print(f"OTC announcement_time = {announcement_time}")   
                if announcement_time >= one_hour_ago:
                    filtered_data.append(announcement)
                    print(f"OTC announcement = {announcement}")
            except ValueError:
                # 如果時間格式不正確，跳過該公告
                print("時間格式不正確")
                continue

        response_dict["data"] = filtered_data
        return response_dict
    return {"data": [], "message": ["查無公告資料"], "status": "fail"}

def check_new_announcements():
    # global last_checked_date
    # today = datetime.now().strftime('%Y%m%d')
    
    # # 如果跨日，清空 sent_announcements 並更新 last_checked_date
    # if last_checked_date is None or today != last_checked_date:
    #     sent_announcements.clear()
    #     save_sent_announcements(sent_announcements)
    #     last_checked_date = today
    #     save_last_checked_date(today)

    sii_response_dict = get_sii_announcement()
    otc_response_dict = get_otc_announcement()

    print(f"sii_response_dict = {sii_response_dict}")
    print(f"otc_response_dict = {otc_response_dict}")

    new_announcements = sii_response_dict["data"] + otc_response_dict["data"]

    if new_announcements:
        print("有新的公告：")
        for announcement in new_announcements:
            announcement_details = f"{announcement['ctime']}\n{announcement['COMPANY_ID']}{announcement['COMPANY_NAME']}\n{announcement['SUBJECT']}\n{announcement['HYPERLINK']}"
            print(announcement_details)
        # save_sent_announcements(sent_announcements)  # 儲存已發送的公告
    else:
        print("沒有新的公告")

    return new_announcements


if __name__ == "__main__":
    check_new_announcements()




