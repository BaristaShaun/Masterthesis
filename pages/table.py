import streamlit as st
import pandas as pd

def app():
    st.title("📊 Fuel Variant별 Impact Category 총합 대시보드")

    # 📂 master.xlsx 파일 불러오기
    try:
        df = pd.read_excel("master.xlsx", sheet_name=0)
        df['Scenario'] = pd.to_numeric(df['Scenario'], errors='coerce')
        impact_categories = df.columns[4:]
        df[impact_categories] = df[impact_categories].apply(pd.to_numeric, errors='coerce')
    except FileNotFoundError:
        st.error("❌ master.xlsx 파일을 찾을 수 없습니다.")
        return

    # 🎯 16개 Fuel Variant 정의
    target_variants = {
        'STL1': {'Fuel': 'STL', 'Scenario': [0, 1]},
        'STL2': {'Fuel': 'STL', 'Scenario': [0, 2]},
        'STL3': {'Fuel': 'STL', 'Scenario': [0, 3]},
        'PTL1': {'Fuel': 'PTL', 'Scenario': [0, 1]},
        'PTL2': {'Fuel': 'PTL', 'Scenario': [0, 2]},
        'PTL3': {'Fuel': 'PTL', 'Scenario': [0, 3]},
        'PTL4': {'Fuel': 'PTL', 'Scenario': [0, 4]},
        'PBTL1': {'Fuel': 'PBTL', 'Scenario': [0, 1]},
        'PBTL2': {'Fuel': 'PBTL', 'Scenario': [0, 2]},
        'PBTL3': {'Fuel': 'PBTL', 'Scenario': [0, 3]},
        'PBTL4': {'Fuel': 'PBTL', 'Scenario': [0, 4]},
        'BTL': {'Fuel': 'BTL', 'Scenario': [0]},
        'HEFA1': {'Fuel': 'HEFA', 'Scenario': [0, 1]},
        'HEFA2': {'Fuel': 'HEFA', 'Scenario': [0, 2]},
        'HEFA3': {'Fuel': 'HEFA', 'Scenario': [0, 3]},
        'HEFA4': {'Fuel': 'HEFA', 'Scenario': [0, 4]}
    }

    # 📊 총합 계산
    summary_data = {}
    for label, rule in target_variants.items():
        temp_df = df[(df['Fuel'] == rule['Fuel']) & (df['Scenario'].isin(rule['Scenario']))]
        impact_sum = temp_df[impact_categories].sum()
        summary_data[label] = impact_sum

    result_df = pd.DataFrame(summary_data).T
    result_df.index.name = "Fuel Variant"
    result_df = result_df.reset_index()

    # 📊 인터랙티브 테이블 표시
    st.subheader("🔍 Fuel Variant별 Impact Category 총합")
    st.dataframe(result_df, use_container_width=True)

    # 📥 데이터 다운로드
    csv = result_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 CSV로 다운로드",
        data=csv,
        file_name='fueltype_impact_summary.csv',
        mime='text/csv',
    )
