'''
查詢公告快易查網站，關鍵字為"轉換公司債"，並將新公告發送通知
'''

import requests
import json
from datetime import datetime, timedelta, timezone



# 台灣證券交易所公告網址
announcement_url = "https://mopsov.twse.com.tw/mops/web/ezsearch_query"



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

        # 篩選出 'CDATE' 和 'CTIME' 與現在時間相差一小時以內的資料
        one_hour_ago = datetime.now(timezone.utc) - timedelta(hours=1)
        print(f"SII one_hour_ago = {one_hour_ago}")
        filtered_data = []
        for announcement in response_dict.get("data", []):
            print(f"SII announcement = {announcement}")
            try:
                # 將 CDATE 轉換為西元年格式
                cdate_parts = announcement['CDATE'].split('/')
                year = int(cdate_parts[0]) + 1911  # 將民國年轉換為西元年
                month = cdate_parts[1]
                day = cdate_parts[2]
                converted_cdate = f"{year}-{month}-{day}"

                # 組合 'CDATE' 和 'CTIME' 成 full_time
                full_time = datetime.strptime(f"{converted_cdate} {announcement['CTIME']}", '%Y-%m-%d %H:%M:%S').replace(tzinfo=timezone.utc)
                print(f"SII full_time = {full_time}")
                if full_time >= one_hour_ago:
                    filtered_data.append(announcement)
                    print(f"一小時內的SII announcement = {announcement}")
            except ValueError as e:
                # 如果時間格式不正確，跳過該公告
                print(f"時間格式不正確: {e}")
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

        # 篩選出 'CDATE' 和 'CTIME' 與現在時間相差一小時以內的資料
        one_hour_ago = datetime.now(timezone.utc) - timedelta(hours=1)
        print(f"OTC one_hour_ago = {one_hour_ago}")
        filtered_data = []
        for announcement in response_dict.get("data", []):
            print(f"OTC announcement = {announcement}")
            try:
                # 將 CDATE 轉換為西元年格式
                cdate_parts = announcement['CDATE'].split('/')
                year = int(cdate_parts[0]) + 1911  # 將民國年轉換為西元年
                month = cdate_parts[1]
                day = cdate_parts[2]
                converted_cdate = f"{year}-{month}-{day}"

                # 組合 'CDATE' 和 'CTIME' 成 full_time
                full_time = datetime.strptime(f"{converted_cdate} {announcement['CTIME']}", '%Y-%m-%d %H:%M:%S').replace(tzinfo=timezone.utc)
                print(f"OTC full_time = {full_time}")
                if full_time >= one_hour_ago:
                    filtered_data.append(announcement)
                    print(f"一小時內的OTC announcement = {announcement}")
            except ValueError as e:
                # 如果時間格式不正確，跳過該公告
                print(f"時間格式不正確: {e}")
                continue

        response_dict["data"] = filtered_data
        return response_dict
    return {"data": [], "message": ["查無公告資料"], "status": "fail"}

def check_new_announcements():

    sii_response_dict = get_sii_announcement()
    otc_response_dict = get_otc_announcement()

    print(f"sii_response_dict = {sii_response_dict}")
    print(f"otc_response_dict = {otc_response_dict}")

    new_announcements = sii_response_dict["data"] + otc_response_dict["data"]

    if new_announcements:
        print("有新的公告：")
        for announcement in new_announcements:
            announcement_details = f"{announcement['CDATE']} {announcement['CTIME']}\n{announcement['COMPANY_ID']}{announcement['COMPANY_NAME']}\n{announcement['SUBJECT']}\n{announcement['HYPERLINK']}"
            print(announcement_details)
        # save_sent_announcements(sent_announcements)  # 儲存已發送的公告
    else:
        print("沒有新的公告")

    return new_announcements


if __name__ == "__main__":
    check_new_announcements()




