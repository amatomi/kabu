import requests
from bs4 import BeautifulSoup
import json
import datetime
import os
import urllib3
import re

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
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    all_data = []
    # Fetch up to 2 pages (50 items per page = 100 items)
    for page in range(1, 3):
        paged_url = f"{url}&page={page}" if "?" in url else f"{url}?page={page}"
        try:
            response = requests.get(paged_url, headers=headers, verify=False, timeout=10)
            if response.status_code != 200:
                print(f"Failed to fetch {paged_url}: Status {response.status_code}")
                break
        except Exception as e:
            print(f"Error fetching {paged_url}: {e}")
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
            
            # --- Name and Code ---
            name_cell = tds[0]
            name_a = name_cell.find('a')
            name = name_a.text.strip() if name_a else name_cell.text.strip().split('\n')[0]
            
            code_li = name_cell.find('li')
            code = code_li.text.strip() if code_li else ""
            if not code:
                code_match = re.search(r'\d{4}', name_cell.text)
                code = code_match.group(0) if code_match else ""

            # --- Price ---
            price_td = tds[1]
            # Price is usually in the first span that doesn't have a date-related class
            price_spans = price_td.find_all('span', recursive=False)
            if price_spans:
                price = price_spans[0].text.strip().replace(',', '')
            else:
                price = price_td.text.strip().split('\n')[0].replace(',', '')
            
            # --- Change and Change % ---
            change_td = tds[2]
            change_width = "-"
            change_pct = "-"
            
            # The change cell has a nested structure. We want the two deepest spans.
            # Example: <span><span>+50</span><span>+35.71%</span></span>
            all_spans = change_td.find_all('span')
            # Filter for spans that don't have other spans inside (leaf spans)
            leaf_spans = [s for s in all_spans if not s.find('span')]
            
            if len(leaf_spans) >= 2:
                # Usually first is absolute change (width), second is percentage
                change_width = leaf_spans[0].text.strip().replace(',', '')
                change_pct = leaf_spans[1].text.strip()
                if not change_pct.endswith('%'):
                    change_pct += '%'
            elif len(leaf_spans) == 1:
                text = leaf_spans[0].text.strip()
                if '%' in text:
                    change_pct = text
                else:
                    change_width = text.replace(',', '')

            # --- Volume ---
            volume_td = tds[3] if len(tds) > 3 else None
            volume = "-"
            if volume_td:
                vol_span = volume_td.find('span')
                volume = vol_span.text.strip() if vol_span else volume_td.text.strip()
                volume = volume.replace(',', '').replace('株', '').replace('円', '')
            
            data = {
                "rank": rank,
                "code": code,
                "name": name,
                "price": price,
                "change_width": change_width,
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
        
    # Standardize output for data.json
    # Derive "値上がり幅" and "値下がり幅" if possible
    if "値上がり率" in results:
        # Sort by absolute change value (descending)
        def sort_key(x):
            try:
                # Remove '+' and parse as float
                val_str = x['change_width'].replace('+', '').replace(',', '')
                return float(val_str)
            except:
                return -1.0
        
        sorted_width = sorted(results["値上がり率"], key=sort_key, reverse=True)
        width_data = []
        for i, item in enumerate(sorted_width[:100]):
            new_item = item.copy()
            new_item['rank'] = str(i + 1)
            width_data.append(new_item)
        results["値上がり幅"] = width_data

    if "値下がり率" in results:
        def sort_key_down(x):
            try:
                # Remove '-' and parse as float for relative magnitude
                # Or keep '-' to sort most negative at the top of "price drop width"
                val_str = x['change_width'].replace('-', '').replace(',', '')
                return float(val_str)
            except:
                return -1.0
        
        sorted_width_down = sorted(results["値下がり率"], key=sort_key_down, reverse=True)
        width_data_down = []
        for i, item in enumerate(sorted_width_down[:100]):
            new_item = item.copy()
            new_item['rank'] = str(i + 1)
            width_data_down.append(new_item)
        results["値下がり幅"] = width_data_down

    # Ensure all keys exist
    expected_keys = [
        "値上がり率", "値下がり率", "出来高", "売買代金", 
        "値上がり幅", "値下がり幅", "配当利回り", 
        "高PER", "低PER", "高PBR", "低PBR"
    ]
    for key in expected_keys:
        if key not in results:
            results[key] = []
            
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
