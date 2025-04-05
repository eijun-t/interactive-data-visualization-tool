import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from datetime import datetime

# アプリのタイトルを設定
st.title("売上データ分析ダッシュボード")
st.write("このアプリでは、製品と地域ごとの売上データを分析できます。")

# データの読み込み（キャッシュを使用してパフォーマンスを向上）
@st.cache_data
def load_data():
    """
    CSVファイルからデータを読み込み、日付を日時形式に変換します
    """
    df = pd.read_csv("sales_data.csv")
    df["Date"] = pd.to_datetime(df["Date"])
    return df

# データの読み込み
df = load_data()

# サイドバーの作成
st.sidebar.header("フィルター設定")

# 日付フィルター
min_date = df["Date"].min().date()
max_date = df["Date"].max().date()

# 日付選択ウィジェット
start_date = st.sidebar.date_input(
    "開始日",
    min_date,
    min_value=min_date,
    max_value=max_date
)
end_date = st.sidebar.date_input(
    "終了日",
    max_date,
    min_value=min_date,
    max_value=max_date
)

# 日付を文字列からdatetime形式に変換して比較できるようにする
start_date = datetime.combine(start_date, datetime.min.time())
end_date = datetime.combine(end_date, datetime.max.time())

# 製品選択
all_products = df["Product"].unique().tolist()
selected_products = st.sidebar.multiselect(
    "製品を選択",
    options=all_products,
    default=all_products
)

# 地域選択
all_regions = df["Region"].unique().tolist()
selected_regions = st.sidebar.multiselect(
    "地域を選択",
    options=all_regions,
    default=all_regions
)

# フィルタリング処理
filtered_df = df.copy()

# 日付でフィルタリング
filtered_df = filtered_df[(filtered_df["Date"] >= start_date) & (filtered_df["Date"] <= end_date)]

# 製品でフィルタリング
filtered_df = filtered_df[filtered_df["Product"].isin(selected_products)]

# 地域でフィルタリング（選択された地域が存在する場合のみ）
if selected_regions:
    filtered_df = filtered_df[filtered_df["Region"].isin(selected_regions)]

# フィルタリングの概要を表示
st.write(f"**選択された期間**: {start_date.date()} から {end_date.date()}")
st.write(f"**選択された製品**: {', '.join(selected_products)}")
st.write(f"**選択された地域**: {', '.join(selected_regions)}")

# フィルタリングされたデータの表示（折りたたみ可能なセクションに）
with st.expander("フィルタリングされたデータを表示"):
    st.dataframe(filtered_df)

# 1. サマリーボード（統計情報）
st.subheader("サマリーボード")
total_sales = filtered_df["Sales"].sum()
avg_sales = filtered_df["Sales"].mean()
max_sales = filtered_df["Sales"].max()
min_sales = filtered_df["Sales"].min()

# 4つのカラムに統計情報を表示
stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)
with stat_col1:
    st.metric(label="総売上", value=f"{total_sales}")
with stat_col2:
    st.metric(label="平均売上/日", value=f"{avg_sales}")
with stat_col3:
    st.metric(label="最大売上", value=f"{max_sales}")
with stat_col4:
    st.metric(label="最小売上", value=f"{min_sales}")

# 2行目: 日次推移グラフと製品別売上分布
row2_col1, row2_col2 = st.columns(2)

with row2_col1:
    st.write("### 日次推移グラフ（折れ線グラフ）")
    
    # 日付と製品ごとのデータを集計
    product_daily_sales = filtered_df.groupby(["Date", "Product"])["Sales"].sum().reset_index()
    
    # 製品ごとに別々の折れ線で表示
    fig1 = px.line(
        product_daily_sales,
        x="Date",
        y="Sales",
        color="Product",  # 製品で色分け
        title="製品別の日次売上推移",
        labels={"Sales": "売上高", "Date": "日付", "Product": "製品"},
        markers=True,     # データポイントにマーカーを表示
        template="plotly_white"
    )
    
    # グラフの見た目を調整
    fig1.update_layout(
        legend=dict(
            orientation="h",    # 凡例を水平に
            yanchor="bottom",
            y=1.02,            # グラフの上に配置
            xanchor="right",
            x=1
        )
    )
    
    st.plotly_chart(fig1, use_container_width=True)

with row2_col2:
    st.write("### 製品別売上分布（スタック棒グラフ）")
    
    # 日付と製品ごとのデータを準備
    date_product_sales = filtered_df.groupby(["Date", "Product"])["Sales"].sum().reset_index()
    
    # スタック棒グラフを作成
    fig2 = px.bar(
        date_product_sales,
        x="Date",
        y="Sales",
        color="Product",
        title="製品別の日次売上分布",
        labels={"Sales": "売上高", "Date": "日付", "Product": "製品"},
        template="plotly_white",
        barmode="stack"  # スタック表示
    )
    st.plotly_chart(fig2, use_container_width=True)

# 3行目: 地域別売上割合とクロス集計表
row3_col1, row3_col2 = st.columns(2)

with row3_col1:
    st.write("### 地域別売上割合（円グラフ）")
    
    # 地域ごとの売上を集計
    region_sales = filtered_df.groupby("Region")["Sales"].sum().reset_index()
    
    # 円グラフを作成
    fig3 = px.pie(
        region_sales,
        values="Sales",
        names="Region",
        title="地域ごとの売上比率",
        hole=0.4,  # ドーナツグラフにする
        template="plotly_white"
    )
    st.plotly_chart(fig3, use_container_width=True)

with row3_col2:
    st.write("### クロス集計表（ピボットテーブル）")
    
    # ピボットテーブルを作成
    pivot_table = pd.pivot_table(
        filtered_df,
        values="Sales",
        index=["Product"],
        columns=["Region"],
        aggfunc="sum",
        fill_value=0
    )
    
    # 合計行と合計列を追加
    pivot_table.loc["合計"] = pivot_table.sum()
    pivot_table["合計"] = pivot_table.sum(axis=1)
    
    # 表示（スタイリングを適用して見やすく）
    st.dataframe(pivot_table.style.highlight_max(axis=0), use_container_width=True)
