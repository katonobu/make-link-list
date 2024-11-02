import json
import requests
import datetime
import re
from bs4 import BeautifulSoup

def get_higashi_totsuka_sho():
    result = []
    rsp = requests.get("https://www.edu.city.yokohama.lg.jp/school/es/higashitotsuka/index.cfm/1,0,52,267,html", headers={'User-Agent': ''})

    trans = str.maketrans("１２３４５６７８９０","1234567890")
    if rsp.ok:
        soup = BeautifulSoup(rsp.content, "html.parser")
        for a_tag in soup.find_all('a'):
            if re.match(r"^[１２３４５６７８９０1234567890]+月号", a_tag.text):
                title = a_tag.text.strip()
                datetime_src_str = a_tag.get('href').split("/")[-1].replace(".pdf","")
                result.append({
                    'month':int(title.translate(trans).replace("月号",""), 10),
                    'update_at':str(datetime.datetime.strptime(datetime_src_str, "%Y%m%d-%H%M%S")),
                    'pdf_title':title,
                    'pdf_url':a_tag.get('href')
                })
            else:
                pass
                # print(a_tag.text.strip())
        result = sorted(result, key=lambda x:(x['month']+8)%12, reverse=True)
    return result

if __name__ == "__main__":
    results = get_higashi_totsuka_sho()
    with open("higashi_totsuka_sho.json", "w", encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    ols = []
    ols.append("# 東戸塚小学校 学校だより")
    ols.append(f"## 最新号")
    item = results[0]
    ols.append(f"- [{item['pdf_title']}]({'https://www.edu.city.yokohama.lg.jp' + item['pdf_url']}) {item['update_at']}更新")

    ols.append(f"## バックナンバー")
    for item in results[1:]:
        ols.append(f"- [{item['pdf_title']}]({'https://www.edu.city.yokohama.lg.jp' + item['pdf_url']}) {item['update_at']}更新")

    with open("higashi_totsuka_sho.md", "w", encoding='utf-8') as f:
        f.writelines('\n'.join(ols))


