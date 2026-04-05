import requests
from bs4 import BeautifulSoup
from datetime import datetime,timedelta
import pandas as pd
import os
from dotenv import load_dotenv
from linebot import LineBotApi
from linebot.models import TextSendMessage

#載入設定
load_dotenv()

class LineNotifier:
    '''負責處理通知邏輯'''
    def __init__(self):
        self.token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
        self.user_id = os.getenv("LINE_USER_ID")
        self.line_bot_api = LineBotApi(self.token)

    def send_line_message(self,message):
        try:
            self.line_bot_api.push_message(self.user_id,TextSendMessage(text = message))
            print("LINE 訊息已成功推播")
        except Exception as e:
            print(f"發送失敗:{e}")

class PTTScraper:
    '''負責處理爬蟲邏輯'''
    def __init__(self,board,days):
        self.board = board
        self.days = days
        self.target_date = datetime.now() - timedelta(days = days)
        self.base_url = "https://www.ptt.cc"
        #PTT抓取有的版需要滿１８歲以上
        self.headers = {'cookie': 'over18=1', 'User-Agent': 'Mozilla/5.0'}

    def get_post_within_days(self):
        url = f"{self.base_url}/bbs/{board}/index.html"
        all_matched_posts = []
        keep_crawling = True

        print(f"--- 開始抓取 {self.board} 版最近 {self.days} 天的文章 ---")

        while url and keep_crawling:
            print(f"正在處理頁面: {url}")
            resp = requests.get(url,headers=self.headers)
            if resp.status_code != 200:
                break

            #解析html
            soup = BeautifulSoup(resp.text,'html.parser')

            sep = soup.find('div',class_='r-list-sep')

            # 1. 抓取當前頁面的文章(置頂公告不抓)
            if sep:
                post_entries = sep.find_all_previous('div',class_= 'r-ent')
            else:
                post_entries = reversed(soup.find_all('div',class_= 'r-ent'))

            for entry in post_entries:
                title_tag = entry.find('div',class_='title').find('a')
                date_str = entry.find('div',class_='date').text.strip()
                if not title_tag: continue

                #處理跨年問題,若文章時間大於現在時間,判定為去年
                article_date = datetime.strptime(f"{datetime.now().year}/{date_str}","%Y/%m/%d")
                if article_date > datetime.now():
                    article_date = article_date.replace(year=article_date.year -1)

                # 判斷是否停止
                if article_date < self.target_date:
                    keep_crawling = False
                    break

                all_matched_posts.append({
                    'title':title_tag.text,
                    'date':article_date.strftime("%Y/%m/%d"),
                    'link':self.base_url + title_tag['href']
                })
            
            # 2. 取得上一頁連結，準備下一次迴圈
            prev_url = soup.find('a',string ="‹ 上頁")
            url = self.base_url + prev_url['href'] if prev_url else None

        return all_matched_posts
    
class Save_To_Csv:
   def __init__(self):
        pass
   
   def save_to_csv(self,posts_list,filename):
        if not posts_list:
            print("沒有資料可以儲存!")
            return
        
        #將List轉換成DataFrome,並排序
        df = pd.DataFrame(posts_list)
        df.sort_values(by='date',ascending=False)

        # 存成CSV
        # index=False 代表不要存 Pandas 自動產生的數字編號
        # encoding='utf-8-sig' 是為了讓 Excel 開啟時不會亂碼 (對 Mac/Windows 友善)
        df.to_csv(filename,index=False,encoding='utf-8-sig')
        print(f"成功儲存{len(df)}筆資料至{filename}")



# --- Main Code---
if __name__ == "__main__":
    #---設定---
    keywords=["Lakers","Warriors","BOX"]
    days = 5
    board = "NBA"

    # 1.初始化
    scraper = PTTScraper(board,days)
    notifer = LineNotifier()
    toCsv = Save_To_Csv()

    # 2.執行爬蟲動作
    print(f"開始執行{board}爬蟲任務")
    results = scraper.get_post_within_days()
    
    # 3.關鍵字篩選
    matched = [p for p in results if any(kw.lower() in p['title'].lower() for kw in keywords)]

    # 4.儲存至csv
    toCsv.save_to_csv(matched,filename="ppt_output.csv")

    # 5.發送結果
    if matched:
        msg = f"\n發現 {len(matched)} 筆資料：\n" + "\n".join([f"- {p['title']}\n{p['link']}" for p in matched])
        notifer.send_line_message(msg)
    else:
        notifer.send_line_message("今天沒有符合的文章")
    


    
