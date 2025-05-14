import streamlit as st
import pandas as pd
import plotly.express as px

# ---- データの読み込み（CSV形式想定） ----
@st.cache_data
def load_data():
    # CSVファイルの形式：Chain,Category,Project,KOL,Posts,Impressions
    return pd.read_csv("sample_kol_data.csv")

df = load_data()

# ---- ヒートマップ用に集計 ----
heatmap_data = df.groupby(["Chain", "Category"])\
                   .agg({"Impressions": "sum"})\
                   .reset_index()
heatmap_pivot = heatmap_data.pivot(index="Chain", columns="Category", values="Impressions")

# ---- ヒートマップ描画 ----
st.title("XFlow Community: カテゴリ×チェーン インプレッションマップ")
st.caption("クリックで該当プロジェクトとKOL一覧を表示")

fig = px.imshow(
    heatmap_pivot,
    text_auto=True,
    color_continuous_scale='YlOrRd',
    labels=dict(color="Imp合計")
)
fig.update_layout(height=500)

selected = st.plotly_chart(fig, use_container_width=True)

# ---- クリックイベント処理（仮: セレクタ使用） ----
# Streamlitでヒートマップセルクリック検知は難しいため、Dropdownで模擬する
st.subheader("チェーンとカテゴリを選んで詳細表示")
chain = st.selectbox("チェーンを選択", sorted(df["Chain"].unique()))
category = st.selectbox("カテゴリを選択", sorted(df["Category"].unique()))

filtered = df[(df["Chain"] == chain) & (df["Category"] == category)]

st.markdown(f"### 🔍 {chain} × {category} の該当プロジェクトとKOL")
if not filtered.empty:
    for project in filtered["Project"].unique():
        st.markdown(f"#### 🚀 プロジェクト: {project}")
        kol_data = filtered[filtered["Project"] == project]
        for _, row in kol_data.iterrows():
            st.markdown(f"- @{row['KOL']}: {row['Posts']} posts, {row['Impressions']} Imps")
else:
    st.info("該当データがありません")
