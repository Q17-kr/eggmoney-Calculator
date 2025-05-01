import streamlit as st
import pandas as pd
import uuid

@st.cache_data
def load_csv(uploaded_file):
    return pd.read_csv(uploaded_file, dtype={"code": str, "account": int}).fillna("")



if "data" not in st.session_state:
    df = pd.DataFrame(columns=["code", "account"], index=range(5))
    df["code"] = ""
    df["account"] = 0
    st.session_state.data = df
    st.session_state.key = str(uuid.uuid4())



file_container = st.container()
upload_col, download_col = file_container.columns([1, 1])

uploaded_file = upload_col.file_uploader("코드 데이터 파일 업로드", type=["csv"], key=st.session_state.key)
if uploaded_file:
    st.session_state.data = load_csv(uploaded_file)
    st.session_state.key = str(uuid.uuid4())

data = st.session_state.data

csv = data.to_csv(index=False).encode("utf-8")
download_col.download_button("데이터 저장", data=csv, file_name="eggmoneyCodesData.csv", mime="text/csv")



input_col, get_code_col = st.columns([1, 1])

with input_col:
    header = st.container()
    col_code, col_account, _ = header.columns([3, 1, 1])
    col_code.markdown("코드")
    col_account.markdown("잔액")
    changed = False
    delete_index = None

    for i in range(len(data)):
        row = st.container()
        col_code, col_account, col_delete = row.columns([3, 1, 1])

        prev_code = data.loc[i, "code"]
        prev_account = data.loc[i, "account"]

        new_code = col_code.text_input(f"code_{i}", value=prev_code, max_chars=20, label_visibility="collapsed")
        new_account = col_account.number_input(f"account_{i}", min_value=0, value=int(prev_account), step=1000, label_visibility="collapsed")

        if new_code != prev_code or new_account != prev_account:
            data.loc[i] = [new_code, new_account]
            changed = True

        if col_delete.button("삭제", key=f"delete_{i}"):
            delete_index = i
    
    if delete_index is not None:
        data.drop(index=delete_index, inplace=True)
        data.reset_index(drop=True, inplace=True)
        st.session_state.data = data
        st.rerun()

    if st.button("", icon=":material/add:", use_container_width=True):
        data.loc[len(data)] = ["", 0]
        st.session_state.data = data
        st.rerun()

    if changed:
        st.session_state.data = data



with get_code_col:
    st.markdown("사용 코드")
    try:
        codelist = [code for code in data["code"] if len(code) > 19]
    except:
        codelist = []

    if codelist:
        selected_code = st.selectbox("사용 코드", codelist)

        codeFirst, codeSecond, codeThird, codeFourth = st.columns(4)
        codeFirst.code(selected_code[:5], language="text")
        codeSecond.code(selected_code[5:10], language="text")
        codeThird.code(selected_code[10:15], language="text")
        codeFourth.code(selected_code[15:], language="text")
