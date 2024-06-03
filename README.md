# make-link-list
## 概要
戸塚区の行政関係情報のURLを取得するスクリプト。

### get_from_kurenkai.py
[定例会の日程・配布資料／事業計画・予算について【戸塚区連会】](https://rarea.events/event/97066)の
令和6年度、令和5年度の各月のページのリンクからjson,markdownファイルを生成する。
出力ファイルは、
- [kurenkai.json](https://github.com/katonobu/make-link-list/blob/main/kurenkai.json)
- [kurenkai.md](https://github.com/katonobu/make-link-list/blob/main/kurenkai.md)

### get_sakuradayori.py
[横浜市上倉田地域ケアプラザ ブログ](http://www.hirakukaicp.or.jp/kamikurata-blog)の広報さくらだより、のリンクページから、
対象ページ、各ページの画像データへのリンクを抽出しjson,markdownファイルを生成する。
出力ファイルは、
- [sakuradayori.json](https://github.com/katonobu/make-link-list/blob/main/sakuradayori.json)
- [sakuradayori.md](https://github.com/katonobu/make-link-list/blob/main/sakuradayori.md)

### get_from_chiku_center.py
[地区センター  地区センターだより](https://totsuka.chiiki-support.jp/centerdayori.html)のページから、
最新版pdfとバックナンバーのイメージファイルのリンクを抽出し、json,markdownファイルを生成する。
出力ファイルは、
- [chiku_center.json](https://github.com/katonobu/make-link-list/blob/main/chiku_center.json)
- [chiku_center.md](https://github.com/katonobu/make-link-list/blob/main/chiku_center.md)

### get_flat_station.py
[フラットステーション・とつか 情報誌『わくわくだより』](https://furatto-totsuka.com/wp/news-letter/)のページから、
最新版pdfのdownloadリンク(1-4P,2-3P,イベント予定表)を抽出し、json,markdownファイルを生成する。
出力ファイルは、
- [flat_station.json](https://github.com/katonobu/make-link-list/blob/main/flat_station.json)
- [flat_station.md](https://github.com/katonobu/make-link-list/blob/main/flat_station.md)

### get_kurashi_navi.py
[横浜市消費生活総合センター くらしナビ(最新号)](https://www.yokohama-consumer.or.jp/publish/lifenavi/index.html)、および、下部のバックナンバーから、
最新号pdfのリンクと、バックナンバーのリンク一式を抽出し、
json,markdownファイルを生成する。
出力ファイルは、
- [kurashi_navi.json](https://github.com/katonobu/make-link-list/blob/main/kurashi_navi.json)
- [kurashi_navi.md](https://github.com/katonobu/make-link-list/blob/main/kurashi_navi.md)

## 実行方法
### windows
- pythonがインストールされてる前提
- `01_setup.bat` を実行し、仮想環境を作り必要なライブラリをインストールする。
- `02_run_all.bat`を実行し、上記スクリプトを実行する。

### code space
- githubでcode spacesで実行する。
  - code spacesでpython環境+ライブラリインストールする設定済。
  - code spacesが立ち上がったら、ターミナルで `./run_all.sh`とすれば、スクリプトが走ってくれる。

## 課題
### 区連会
- リンク先のpdfは前半に説明ページがついている。
  - ダウンロードして必要なページのみを抽出する必要あり。
### さくらだより
- 画像がpngあるいはgif
  - pdfを置いてもらえると嬉しい。

### 地区センター
- pdfは最新版しかない。
  - 最低月一回ローカルにダウンロードしておく必要あり。

### フラットステーション・とつか
- downloadリンクにクエリが含まれてるが、問題ない?
- pdfが見開きになっているのが残念。
- pdfは最新版しかない。
  - 最低月一回ローカルにダウンロードしておく必要あり。

### くらしナビ
- 各自治会毎に1部しか来ていなかったため、回覧非対象ったが、結構内容濃いので追加。
- 凝ってるのでpdfファイルサイズがでかいのが残念。
