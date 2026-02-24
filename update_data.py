import requests
from bs4 import BeautifulSoup
import json
import datetime
import os
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Yahoo Finance JP ranking URLs
URLS = {
    "値上がり率": "https://finance.yahoo.co.jp/stocks/ranking/up",
    "値下がり率": "https://finance.yahoo.co.jp/stocks/ranking/down",
    "出来高": "https://finance.yahoo.co.jp/stocks/ranking/volume",
    "売買代金": "https://finance.yahoo.co.jp/stocks/ranking/tradingValueHigh",
    "配当利回り": "https://finance.yahoo.co.jp/stocks/ranking/dividendYield",
    "高PER": "https://finance.yahoo.co.jp/stocks/ranking/highPer?market=all&term=daily",
    "低PER": "https://finance.yahoo.co.jp/stocks/ranking/lowPer?market=all&term=daily",
    "高PBR": "https://finance.yahoo.co.jp/stocks/ranking/highPbr?market=all&term=daily",
    "低PBR": "https://finance.yahoo.co.jp/stocks/ranking/lowPbr?market=all&term=daily"
}

def fetch_ranking(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    all_data = []
    # Fetch up to 2 pages (50 items per page = 100 items)
    for page in range(1, 3):
        paged_url = f"{url}?page={page}"
        response = requests.get(paged_url, headers=headers, verify=False)
        if response.status_code != 200:
            print(f"Failed to fetch {paged_url}")
            break
            
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table')
        if not table:
            break
            
        rows = table.find_all('tr')[1:] # Skip header
        for row in rows:
            th = row.find(['th', 'td'])
            if not th: continue
            rank = th.text.strip()
            
            tds = row.find_all('td')
            if len(tds) < 3: continue
            
            # Column 1 (tds[0] or tds[1] depending on if th is a td)
            # Based on subagent, th is a separate element, and tds starts after th.
            # But BeautifulSoup find_all('td') might include th if it's a td.
            # In Yahoo Finance, rank is a <th>.
            
            name_cell = tds[0]
            name_a = name_cell.find('a')
            name = name_a.text.strip() if name_a else name_cell.text.strip().split('\n')[0]
            
            code_li = name_cell.find('li')
            code = code_li.text.strip() if code_li else ""
            if not code:
                import re
                code_match = re.search(r'\d{4}', name_cell.text)
                code = code_match.group(0) if code_match else ""

            # More precise price extraction
            price_span = tds[1].find('span')
            price = price_span.text.strip().replace(',', '') if price_span else tds[1].text.strip().split('\n')[0].replace(',', '')
            
            # More precise change_pct extraction
            spans = tds[2].find_all('span')
            if len(spans) >= 2:
                # Usually it's in the last span or the one with %
                change_pct = "-"
                for s in spans:
                    if '%' in s.text:
                        change_pct = s.text.strip()
                        break
            else:
                change_pct = tds[2].text.strip().replace('\n', ' ').split(' ')[-1]
            
            # Volume/Trading Value
            volume_span = tds[3].find('span')
            volume = volume_span.text.strip().replace(',', '').replace('株', '') if volume_span else tds[3].text.strip().replace(',', '').replace('株', '')
            
            data = {
                "rank": rank,
                "code": code,
                "name": name,
                "price": price,
                "change_pct": change_pct,
                "volume": volume,
                "per": "-",
                "pbr": "-",
                "yield": "-"
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
        
    # Write as JSON file
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(output['rankings'], f, ensure_ascii=False, indent=2)
        
    print("Successfully updated data.js and data.json")

if __name__ == "__main__":
    main()
