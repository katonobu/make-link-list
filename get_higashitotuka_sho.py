import json
from get_gakko_dayori import get_gakko_dayori

if __name__ == "__main__":
    nendo_objs = [
        {
            "nendo_str":"令和６年度",
            "url":"https://www.edu.city.yokohama.lg.jp/school/es/higashitotsuka/index.cfm/1,0,52,267,html"
        },
        {
            "nendo_str":"令和５年度",
            "url":"https://www.edu.city.yokohama.lg.jp/school/es/higashitotsuka/index.cfm/1,0,52,260,html"
        }
    ]
    for nendo_obj in nendo_objs:
        results = get_gakko_dayori(nendo_obj["url"])
        nendo_obj.update({
            "results":results
        })
    with open("higashi_totsuka_sho.json", "w", encoding='utf-8') as f:
        json.dump(nendo_objs, f, indent=2, ensure_ascii=False)

    ols = []
    ols.append("# 東戸塚小学校 学校だより")
    ols.append(f"## 最新号")
    item = nendo_objs[0]["results"][0]
    ols.append(f"- [{item['pdf_title']}]({'https://www.edu.city.yokohama.lg.jp' + item['pdf_url']}) {item['update_at']}更新")

    ols.append(f"## バックナンバー")
    for nendo_obj in nendo_objs:
        ols.append(f'### {nendo_obj["nendo_str"]}')
        for item in nendo_obj["results"]:
            ols.append(f"- [{item['pdf_title']}]({'https://www.edu.city.yokohama.lg.jp' + item['pdf_url']}) {item['update_at']}更新")

    with open("higashi_totsuka_sho.md", "w", encoding='utf-8') as f:
        f.writelines('\n'.join(ols))


