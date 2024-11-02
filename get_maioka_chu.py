import json
from get_gakko_dayori import get_gakko_dayori

if __name__ == "__main__":
    results = get_gakko_dayori("https://www.edu.city.yokohama.lg.jp/school/jhs/maioka/index.cfm/1,0,52,html")
    with open("maioka_chu.json", "w", encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    ols = []
    ols.append("# 舞岡中学校 学校だより")
    ols.append(f"## 最新号")
    item = results[0]
    ols.append(f"- [{item['pdf_title']}]({'https://www.edu.city.yokohama.lg.jp' + item['pdf_url']}) {item['update_at']}更新")

    ols.append(f"## バックナンバー")
    for item in results[1:]:
        ols.append(f"- [{item['pdf_title']}]({'https://www.edu.city.yokohama.lg.jp' + item['pdf_url']}) {item['update_at']}更新")

    with open("maioka_chu.md", "w", encoding='utf-8') as f:
        f.writelines('\n'.join(ols))


