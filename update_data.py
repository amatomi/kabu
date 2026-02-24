import requests
from bs4 import BeautifulSoup
import json
import datetime
import os

# Yahoo Finance JP ranking URLs
URLS = {
    "値上がり率": "https://finance.yahoo.co.jp/stocks/ranking/up",
    "値下がり率": "https://finance.yahoo.co.jp/stocks/ranking/down",
    "出来高": "https://finance.yahoo.co.jp/stocks/ranking/volume",
    "売買代金": "https://finance.yahoo.co.jp/stocks/ranking/tradingValue",
    "値上がり幅": "https://finance.yahoo.co.jp/stocks/ranking/upWidth",
    "値下がり幅": "https://finance.yahoo.co.jp/stocks/ranking/downWidth",
    "配当利回り": "https://finance.yahoo.co.jp/stocks/ranking/yield",
    "高PER": "https://finance.yahoo.co.jp/stocks/ranking/perHigh",
    "低PER": "https://finance.yahoo.co.jp/stocks/ranking/perLow",
    "高PBR": "https://finance.yahoo.co.jp/stocks/ranking/pbrHigh",
    "低PBR": "https://finance.yahoo.co.jp/stocks/ranking/pbrLow"
}

def fetch_ranking(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    all_data = []
    # Fetch up to 2 pages (50 items per page = 100 items)
    for page in range(1, 3):
        paged_url = f"{url}?page={page}"
        response = requests.get(paged_url, headers=headers)
        if response.status_code != 200:
            print(f"Failed to fetch {paged_url}")
            break
            
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table')
        if not table:
            break
            
        rows = table.find_all('tr')[1:] # Skip header
        for row in rows:
            cols = row.find_all('td')
            if len(cols) < 5:
                continue
                
            # Basic mapping (may need adjustment based on specific ranking page structure)
            data = {
                "rank": cols[0].text.strip(),
                "code": cols[1].text.strip(),
                "name": cols[3].text.strip(),
                "price": cols[5].text.strip(),
                "change_pct": cols[6].text.strip() if len(cols) > 6 else "-",
                "volume": cols[7].text.strip() if len(cols) > 7 else "-",
                "per": cols[8].text.strip() if len(cols) > 8 else "-",
                "pbr": cols[9].text.strip() if len(cols) > 9 else "-",
                "yield": cols[10].text.strip() if len(cols) > 10 else "-"
            }
            all_data.append(data)
            
    return all_data

def main():
    results = {}
    for theme, url in URLS.items():
        print(f"Fetching {theme}...")
        results[theme] = fetch_ranking(url)
        
    retrieval_time = datetime.datetime.now().strftime("%Y/%m/%d %H:%M")
    
    output = {
        "retrieval_time": retrieval_time,
        "rankings": results
    }
    
    # Write as JavaScript variable
    with open('data.js', 'w', encoding='utf-8') as f:
        f.write(f"const STOCK_DATA = {json.dumps(output, ensure_ascii=False, indent=4)};")
        
    print("Successfully updated data.js")

if __name__ == "__main__":
    main()
