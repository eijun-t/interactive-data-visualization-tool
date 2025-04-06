# 売上データ分析ダッシュボード

このアプリケーションは、売上データを分析・可視化するStreamlitアプリケーションです。

## 機能

- 日付、製品、地域によるデータのフィルタリング
- 日ごとの売上を棒グラフで表示
- 製品ごとの売上を棒グラフで表示
- 売上の時系列推移を折れ線グラフで表示
- 地域ごとの売上比率をパイチャートで表示
- 売上に関する基本統計情報の表示

## 必要条件

- Python 3.7以上
- 必要なPythonパッケージ（requirements.txtに記載）

## セットアップと実行方法

1. リポジトリをクローンまたはダウンロードします。
2. 必要なパッケージをインストールします。
   ```
   pip install -r requirements.txt
   ```
3. Streamlitアプリを実行します。
   ```
   streamlit run main.py
   ```
4. ブラウザで以下のURLにアクセスします：http://localhost:8501

## データについて

アプリケーションは`sales_data.csv`から売上データを読み込みます。このファイルには以下の情報が含まれています：

- 日付 (Date)
- 製品名 (Product)
- 売上 (Sales)
- 地域 (Region)

画像１
<img width="1512" alt="image" src="https://github.com/user-attachments/assets/60df994d-b52a-411f-ac48-bcdcde45bbd9" />
画像２
<img width="1512" alt="image" src="https://github.com/user-attachments/assets/ea006f00-6468-4fc2-86d1-ba98e208bd63" />
画像３
<img width="1492" alt="image" src="https://github.com/user-attachments/assets/b2248cd8-369a-44e2-b793-7fab374ca95c" />