import streamlit as st
import os
from openpyxl import Workbook, load_workbook
from datetime import datetime

st.title("簡単アンケートフォーム")

name = st.text_input("お名前を入力してください")
age = st.number_input("年齢を入力してください", min_value=0, max_value=120)
satisfaction = st.radio(
    "満足度を教えてください",
    ("とても満足", "満足", "普通", "不満", "とても不満")
)

if st.button("送信"):

    file_name = "results.xlsx"

    # ファイルがなければ新規作成
    if not os.path.exists(file_name):
        wb = Workbook()
        ws = wb.active
        ws.append(["送信日時", "名前", "年齢", "満足度"])
        wb.save(file_name)

    # 既存ファイルを開く
    wb = load_workbook(file_name)
    ws = wb.active

    # データ追加
    ws.append([
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        name,
        age,
        satisfaction
    ])

    wb.save(file_name)

    st.success("回答ありがとうございました！Excelに保存されました！")
