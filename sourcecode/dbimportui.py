import streamlit as st
import pandas as pd
import pymysql
import traceback
import sys

# ====================== 설정 ======================
# NOTE: 실제 운영 환경에서는 st.secrets를 사용하여 민감 정보를 관리하는 것이 좋습니다.
# DB_CONFIG = st.secrets["database"]
DB_CONFIG = dict(
    host="127.0.0.1",
    user="root",
    password="0000",
    db="soloDB",
    charset="utf8mb4",
    autocommit=False,
)
DEFAULT_TARGET_TABLE = "company"
READ_CSV_KW = dict(encoding="utf-8-sig")

# ==================================================

# 제목 및 소개
st.title("CSV 데이터 MySQL 임포터")
st.info("CSV 파일을 업로드하고, 데이터베이스에 삽입할 테이블을 지정하세요.")

# 사이드바에 데이터베이스 설정
with st.sidebar:
    st.header("데이터베이스 설정")
    db_host = st.text_input("Host", value=DB_CONFIG["host"])
    db_user = st.text_input("User", value=DB_CONFIG["user"])
    db_password = st.text_input("Password", type="password", value=DB_CONFIG["password"])
    db_name = st.text_input("Database", value=DB_CONFIG["db"])
    target_table = st.text_input("타겟 테이블", value=DEFAULT_TARGET_TABLE)

# 파일 업로드
uploaded_file = st.file_uploader("CSV 파일 선택", type=["csv"])

# --- 데이터 임포트 함수 ---
def import_data(df, conn, target_table_name):
    """
    Pandas DataFrame을 MySQL 테이블에 임포트하는 핵심 로직
    """
    total_rows = len(df)
    if total_rows == 0:
        st.warning("CSV에 데이터가 없습니다.")
        return 0, 0, None

    try:
        with conn.cursor() as cur:
            st.info("테이블 컬럼 확인 중...")
            cur.execute(f"DESCRIBE `{target_table_name}`;")
            table_desc = cur.fetchall()
            table_columns = [row[0] for row in table_desc]

            # CSV 컬럼과 테이블 컬럼의 교집합만 사용
            use_cols = [c for c in df.columns if c in table_columns]
            if not use_cols:
                st.error(f"CSV 컬럼({list(df.columns)}) 중 테이블({target_table_name})과 일치하는 컬럼이 없습니다.")
                return 0, 0, None

            # INSERT 문 동적 생성
            cols_sql = ", ".join(f"`{c}`" for c in use_cols)
            placeholders = ", ".join(["%s"] * len(use_cols))
            sql = f"INSERT INTO `{target_table_name}` ({cols_sql}) VALUES ({placeholders})"
            
            # 데이터 삽입
            st.info(f"데이터 입력 중... 총 {total_rows}개 행")
            inserted = 0
            errors = 0
            
            # 진행률 표시
            progress_bar = st.progress(0)
            status_text = st.empty()

            for i, (_, row) in enumerate(df[use_cols].iterrows(), start=1):
                values = [None if (pd.isna(v)) else v for v in row.tolist()]
                
                try:
                    cur.execute(sql, values)
                    inserted += 1
                except Exception as e:
                    errors += 1
                    # 오류는 로그에만 기록하고 계속 진행
                    st.error(f"행 {i} 삽입 실패: {e}")
                    traceback.print_exc(file=sys.stdout)
                
                progress_bar.progress(i / total_rows)
                status_text.text(f"진행 중: {i}/{total_rows}")
                
            conn.commit()
            return inserted, errors, table_desc

    except pymysql.err.OperationalError as e:
        st.error(f"DB 연결/권한 오류: {e}")
        return 0, 0, None
    except pymysql.err.IntegrityError as e:
        st.error(f"데이터 무결성 오류: {e}")
        return 0, 0, None
    except Exception as e:
        st.error(f"예상치 못한 오류: {e}")
        traceback.print_exc(file=sys.stdout)
        return 0, 0, None

# --- 메인 실행 로직 ---
if uploaded_file is not None:
    # CSV 미리보기
    try:
        df = pd.read_csv(uploaded_file, **READ_CSV_KW)
        st.subheader("업로드된 CSV 데이터 미리보기")
        
        # 첫 번째 컬럼 제외 및 컬럼명 정리
        df_processed = df.iloc[:, 1:]
        df_processed.columns = [c.strip() for c in df_processed.columns]
        
        # 테이블 열과 매칭되는 컬럼을 하이라이트
        db_cols = []
        try:
            conn = pymysql.connect(
                host=db_host, user=db_user, password=db_password, db=db_name, autocommit=False
            )
            with conn.cursor() as cur:
                cur.execute(f"DESCRIBE `{target_table}`;")
                db_cols = [row[0] for row in cur.fetchall()]
        except Exception as e:
            st.warning(f"DB 연결 오류로 컬럼 매칭을 확인할 수 없습니다: {e}")
        
        def highlight_matching(s, db_cols):
            return ['background-color: #21618C' if col in db_cols else '' for col in s]
        
        st.dataframe(df_processed.head(10).style.apply(highlight_matching, db_cols=db_cols), use_container_width=True)
        st.caption("메모리 사용량을 줄이기 위해 상위 10개 행만 미리보기로 표시됩니다.")
        st.caption("파란색으로 강조된 컬럼이 데이터베이스 테이블에 매칭됩니다.")

        # --- 데이터 통찰 및 분석 섹션 (새로 추가) ---
        st.subheader("데이터 통찰 (Import 전)")
        
        # 1. 기술 통계
        st.info("숫자 데이터에 대한 기술 통계")
        numerical_df = df_processed.select_dtypes(include=['number'])
        if not numerical_df.empty:
            st.dataframe(numerical_df.describe().T)
        else:
            st.warning("분석할 숫자형 데이터가 없습니다.")

        # 2. 범주형 데이터 시각화
        st.info("범주형 데이터 분포 시각화")
        categorical_cols = df_processed.select_dtypes(include=['object', 'category']).columns.tolist()
        
        if len(categorical_cols) > 0:
            selected_col = st.selectbox("시각화할 범주형 컬럼 선택:", categorical_cols)
            
            value_counts = df_processed[selected_col].value_counts().reset_index()
            value_counts.columns = [selected_col, "count"]
            
            if len(value_counts) > 1:
                # 상위 10개만 시각화
                top_10 = value_counts.head(10)
                st.write(f"**'{selected_col}'** 컬럼의 상위 10개 값")
                st.bar_chart(top_10, x=selected_col, y="count")
            else:
                st.warning(f"선택한 컬럼 '{selected_col}'에는 단일 값만 포함되어 있어 시각화하기에 적합하지 않습니다.")
        else:
            st.warning("분석할 범주형 데이터가 없습니다.")
        
        # --- 추가된 분석 섹션 끝 ---

    except pd.errors.EmptyDataError:
        st.error("업로드된 파일이 비어 있습니다.")
    except Exception as e:
        st.error(f"파일을 읽는 중 오류가 발생했습니다: {e}")

    # 임포트 버튼
    if st.button("MySQL로 데이터 임포트 시작"):
        if not target_table:
            st.error("테이블 이름을 입력하세요.")
        else:
            with st.spinner("데이터베이스 연결 중..."):
                try:
                    conn = pymysql.connect(
                        host=db_host, user=db_user, password=db_password, db=db_name, autocommit=False
                    )
                    
                    df_processed = df.iloc[:, 1:]
                    df_processed.columns = [c.strip() for c in df_processed.columns]

                    inserted, errors, table_desc = import_data(df_processed, conn, target_table)

                    st.success("임포트 완료!")
                    
                    # --- 통계 및 시각화 ---
                    st.subheader("임포트 결과 요약")
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric(label="총 CSV 행", value=len(df_processed))
                        st.metric(label="성공적으로 삽입된 행", value=inserted)
                    with col2:
                        st.metric(label="실패한 행", value=errors)

                    # 성공/실패율 차트
                    st.subheader("성공/실패율")
                    import_results = pd.DataFrame({
                        "결과": ["성공", "실패"],
                        "수": [inserted, errors]
                    })
                    st.bar_chart(import_results, x="결과", y="수", color="결과")

                    # 데이터베이스 테이블 정보 출력
                    st.subheader(f"MySQL '{target_table}' 테이블 정보")
                    
                    if table_desc:
                        desc_df = pd.DataFrame(table_desc, columns=["Field", "Type", "Null", "Key", "Default", "Extra"])
                        st.dataframe(desc_df, use_container_width=True)
                    
                    try:
                        with conn.cursor() as cur:
                            cur.execute(f"SELECT COUNT(*) FROM `{target_table}`;")
                            db_row_cnt = cur.fetchone()[0]
                            st.metric("현재 테이블의 총 행 수", db_row_cnt)
                            
                            st.subheader(f"데이터베이스에 저장된 데이터 미리보기 (상위 10개)")
                            cur.execute(f"SELECT * FROM `{target_table}` LIMIT 10;")
                            db_data = cur.fetchall()
                            db_columns = [col[0] for col in cur.description]
                            db_df = pd.DataFrame(db_data, columns=db_columns)
                            st.dataframe(db_df, use_container_width=True)
                    except Exception as e:
                        st.error(f"테이블 정보 조회 중 오류: {e}")
                    finally:
                        conn.close()

                except Exception as e:
                    st.error(f"데이터베이스 연결 오류: {e}")
                    traceback.print_exc()
