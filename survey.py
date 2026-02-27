import streamlit as st
import pandas as pd
from datetime import datetime
import os
import time

# =========================
# 設定
# =========================

FILE_NAME = "results.xlsx"

COLUMNS = [
    "回答ID",
    "送信日時",
    "名前",
    "年齢",
    "満足度",
    "回答時間(秒)"
]

# =========================
# 開始時間記録
# =========================

if "start_time" not in st.session_state:
    st.session_state.start_time = time.time()

# =========================
# フォームUI
# =========================

st.title("アンケート")

name = st.text_input("名前")
age = st.number_input("年齢", min_value=0, max_value=120, step=1)
satisfaction = st.selectbox(
    "満足度",
    ["とても満足", "満足", "普通", "不満", "とても不満"]
)

# =========================
# 送信ボタン
# =========================

if st.button("送信"):

    end_time = time.time()
    response_time = round(end_time - st.session_state.start_time, 2)

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # =========================
    # Excel読み込み or 新規作成
    # =========================

    if os.path.exists(FILE_NAME):
        df = pd.read_excel(FILE_NAME)
    else:
        df = pd.DataFrame(columns=COLUMNS)

    # =========================
    # 回答ID 自動付番
    # =========================

    if len(df) == 0:
        new_id = 1
    else:
        new_id = df["回答ID"].max() + 1

    # =========================
    # 新しい回答
    # =========================

    new_data = pd.DataFrame([{
        "回答ID": new_id,
        "送信日時": now,
        "名前": name,
        "年齢": age,
        "満足度": satisfaction,
        "回答時間(秒)": response_time
    }])

    df = pd.concat([df, new_data], ignore_index=True)

    # =========================
    # Excel保存
    # =========================

    df.to_excel(FILE_NAME, index=False)

    st.success(f"回答ありがとうございました！（回答ID: {new_id}）")

    # 次の回答者用に時間リセット
    st.session_state.start_time = time.time()
