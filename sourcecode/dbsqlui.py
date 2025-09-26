# app.py  ── streamlit run app.py
import streamlit as st
import pandas as pd
import pymysql

st.set_page_config(page_title="완전한 GUI 응용 프로그램 (Streamlit)", layout="wide")

# ===== DB 설정 =====
DB_CONFIG = dict(
    host="127.0.0.1",
    user="root",
    password="0000",
    db="soloDB",
    charset="utf8mb4",
    autocommit=False,
)

TABLE = "userTable"   # (id, userName, email, birthYear) 순서라고 가정

# ===== DB 유틸 =====
def exec_write(sql: str, params: tuple | list = ()):
    """INSERT/DELETE 등 쓰기 쿼리 (트랜잭션 1회)."""
    try:
        conn = pymysql.connect(**DB_CONFIG)
        with conn:
            with conn.cursor() as cur:
                cur.execute(sql, params)
            conn.commit()
        return True, None
    except Exception as e:
        return False, str(e)

@st.cache_data(ttl=60)  # 60초 캐시
def fetch_users(prefix: str | None):
    """사용자 목록 조회 (옵션: 이름 prefix)."""
    conn = pymysql.connect(**DB_CONFIG)
    try:
        with conn.cursor() as cur:
            if prefix:
                cur.execute(f"SELECT id, userName, email, birthYear FROM {TABLE} "
                            "WHERE userName LIKE %s ORDER BY id",
                            (prefix + "%",))
            else:
                cur.execute(f"SELECT id, userName, email, birthYear FROM {TABLE} ORDER BY id")
            rows = cur.fetchall()
            df = pd.DataFrame(rows, columns=["ID", "Name", "eMail", "Birth Year"])
            return df
    finally:
        conn.close()

def insert_user(id_: str, name: str, email: str, birth_year: int):
    sql = f"INSERT INTO {TABLE}(id, userName, email, birthYear) VALUES (%s, %s, %s, %s)"
    return exec_write(sql, (id_, name, email, birth_year))

def delete_users(ids: list[str]):
    if not ids:
        return True, None
    # 안전하게 IN 절 구성
    placeholders = ",".join(["%s"] * len(ids))
    sql = f"DELETE FROM {TABLE} WHERE id IN ({placeholders})"
    return exec_write(sql, ids)

# ===== UI =====
st.title("완전한 GUI 응용 프로그램 (Streamlit)")

col_form, col_query = st.columns([1, 1])

with col_form:
    st.subheader("입력")
    with st.form("insert_form", clear_on_submit=True):
        id_ = st.text_input("ID", max_chars=32)
        name = st.text_input("이름", max_chars=50)
        email = st.text_input("이메일", max_chars=100)
        birth = st.number_input("출생연도", min_value=1900, max_value=2100, value=1999, step=1)
        submitted = st.form_submit_button("입력")
    if submitted:
        if not id_ or not name or not email:
            st.error("ID/이름/이메일은 필수입니다.")
        else:
            ok, err = insert_user(id_, name, email, int(birth))
            if ok:
                st.success("데이터 입력 성공")
                fetch_users.clear()  # 캐시 무효화
            else:
                st.error(f"데이터 입력 오류: {err}")

with col_query:
    st.subheader("조회")
    name_prefix = st.text_input("이름 (start with)")
    do_search = st.button("조회")

# 첫 진입/조회 버튼 시 목록 갱신
df = fetch_users(name_prefix if do_search or name_prefix else None)

st.markdown("#### 목록")
if df.empty:
    st.info("데이터가 없습니다.")
else:
    # 선택 컬럼(체크박스)을 추가해 삭제 대상 지정
    df_show = df.copy()
    df_show["선택"] = False

    edited = st.data_editor(
        df_show,
        column_config={
            "선택": st.column_config.CheckboxColumn(required=False),
        },
        disabled=["ID", "Name", "eMail", "Birth Year"],  # 읽기 전용
        use_container_width=True,
        key="grid_users",
    )

    sel_rows = edited[edited["선택"]]
    col_del, col_info = st.columns([1, 3])
    with col_del:
        if st.button("선택 삭제", type="primary", disabled=sel_rows.empty):
            ids = sel_rows["ID"].tolist()
            ok, err = delete_users(ids)
            if ok:
                st.success(f"{len(ids)}건 삭제 완료")
                fetch_users.clear()  # 캐시 무효화
                st.rerun()
            else:
                st.error(f"삭제 오류: {err}")
    with col_info:
        st.caption(f"총 {len(df)}건")
