import requests
from bs4 import BeautifulSoup
from datetime import datetime,timedelta
import pandas as pd



def get_post_within_days(board,days):
    
    target_date = datetime.now() - timedelta(days = days)

    #PTT抓取有的版需要滿１８歲以上
    url = f"https://www.ptt.cc/bbs/{board}/index.html"
    headers = {'cookie': 'over18=1', 'User-Agent': 'Mozilla/5.0'}

    all_matched_posts = []
    keep_crawling = True

    print(f"--- 開始抓取 {board} 版最近 {days} 天的文章 ---")
    
    while keep_crawling and url:
        print(f"正在處理頁面: {url}")
        resp = requests.get(url, headers=headers)
        if resp.status_code != 200:
            break

        #解析html
        soup = BeautifulSoup(resp.text, 'html.parser')

        sep = soup.find('div',class_='r-list-sep')
      
        # 1. 抓取當前頁面的文章
        if sep:
            post_entries = soup.find_all_previous('div',class_= 'r-ent')
        else:
            post_entries = reversed(soup.find_all('div',class_= 'r-ent'))
        

        for entry in post_entries:
            title_tag = entry.find('div',class_='title').find('a')
            date_str = entry.find('div',class_= 'date').text.strip()

            if title_tag:
                #處理跨年問題,若文章時間大於現在時間,判定為去年
                article_date = datetime.strptime(f"{datetime.now().year}/{date_str}","%Y/%m/%d")
                if article_date > datetime.now():
                    article_date = article_date.replace(year= article_date.year - 1)

                # 判斷是否停止
                if article_date < target_date:
                    keep_crawling = False
                    break

                all_matched_posts.append({
                    'title':title_tag.text,
                    'date': article_date.strftime("%Y-%m-%d"),
                    'link': "https://www.ptt.cc" + title_tag['href'] 
                })
        
        # 2. 取得上一頁連結，準備下一次迴圈
        prev_url = soup.find('a',string ="‹ 上頁")
        url = "https://www.ptt.cc" + prev_url['href'] if prev_url else None
        print(url)
        
    return all_matched_posts


def save_to_csv(posts_list,filename):
    if not posts_list:
        print("沒有資料可以儲存!")
        return
    
    # 將List 轉換成 DataFrame
    df = pd.DataFrame(posts_list)

    # 進行排序
    df.sort_values(by='date',ascending=False)

    # 存成CSV
    # index=False 代表不要存 Pandas 自動產生的數字編號
    # encoding='utf-8-sig' 是為了讓 Excel 開啟時不會亂碼 (對 Mac/Windows 友善)
    df.to_csv(filename,index = False,encoding='utf-8-sig')
    print(f"成功儲存{len(df)}筆資料至{filename}")



# --- Main Code---
if __name__ == "__main__":

    # 抓取最近n天的文章
    days = 3
    board = "NBA"

    results = get_post_within_days(board,days)
    for r in results:
        print(f"[{r['date']}] {r['title']}")
    
    # 儲存至CSV
    #results_filte = [p for p in results if "[BOX ]" in p['title']]# filter
    save_to_csv(results,"ppt_csv.csv")

