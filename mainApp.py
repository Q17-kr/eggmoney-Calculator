import streamlit as st
import pandas as pd
# import pyperclip as pc

if "data" not in st.session_state:
    origin_data = pd.DataFrame(columns=["code", "account"], index=list(range(10)))
    origin_data["code"] = [""] * 10
    origin_data["account"] = [0] * 10
    st.session_state.data = origin_data



file = st.container()
upload_file, download_file = file.columns([1, 1])

uploaded_file = upload_file.file_uploader("코드 데이터 파일 업로드", type=["csv"])
if uploaded_file is not None:
    st.session_state.data = pd.read_csv(uploaded_file, dtype={"code": str, "account": int}).fillna("")

data = st.session_state.data

download_file.download_button("데이터 저장", data.to_csv().encode("utf-8"), file_name="eggmoneyCodesData.csv", mime="text/csv", type="secondary", use_container_width=True)



input_code, get_code = st.columns([1, 1])

with input_code:
    header = st.container()
    col_code, col_account, col_delete = header.columns([3, 1, 1])
    col_code.markdown("코드")
    col_account.markdown("잔액")

for i in range(data.index.max() + 1):
    with input_code:
        row = st.container()
        col_code, col_account, col_delete = row.columns([3, 1, 1])

        prev_code = data.loc[i, "code"]
        prev_account = data.loc[i, "account"]

        new_code = col_code.text_input(f"code_{i}", value=prev_code, max_chars=20, label_visibility="collapsed")
        new_account = col_account.number_input(f"account_{i}", min_value=0, value=int(prev_account), step=1000, label_visibility="collapsed")

        if new_code != prev_code or new_account != prev_account:
            data.loc[i, "code"] = new_code
            data.loc[i, "account"] = new_account
            st.session_state.data = data

        if col_delete.button("삭제", key=f"del_{i}"):
            data.loc[i, "code"] = ""
            data.loc[i, "account"] = 0
            st.session_state.data = data


if input_code.button("", icon=":material/add:", use_container_width=True):
    data.loc[data.index.max() + 1] = ["", 0]
    st.session_state.data = data
    st.rerun()



with get_code:
    try:
        codelist = [i for i in data["code"].tolist() if len(i) > 19]
    except:
        codelist = []
    selected_code = st.selectbox("사용 코드", codelist, index=0 if codelist else None)

    if selected_code:
        codeFirst, codeSecond, codeThird, codeFourth = st.columns(4)
        # codeFirst.button(selected_code[:5], on_click=pc.copy, args=(selected_code[:5],), use_container_width=True)
        # codeSecond.button(selected_code[5:10], on_click=pc.copy, args=(selected_code[5:10],), use_container_width=True)
        # codeThird.button(selected_code[10:15], on_click=pc.copy, args=(selected_code[10:15],), use_container_width=True)
        # codeFourth.button(selected_code[15:], on_click=pc.copy, args=(selected_code[15:],), use_container_width=True)
        codeFirst.code(selected_code[:5], language="text")
        codeSecond.code(selected_code[5:10], language="text")
        codeThird.code(selected_code[10:15], language="text")
        codeFourth.code(selected_code[15:], language="text")
