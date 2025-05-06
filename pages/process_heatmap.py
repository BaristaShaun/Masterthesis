import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.colors import hex_to_rgb

def app():
    # -----------------------
    # 📂 Load master.xlsx
    # -----------------------
    st.title("🛠️ Process Analysis Dashboard")
    try:
        df = pd.read_excel("master.xlsx", sheet_name=0)
        df['Scenario'] = pd.to_numeric(df['Scenario'], errors='coerce')
        impact_categories = df.columns[4:]
        df[impact_categories] = df[impact_categories].apply(pd.to_numeric, errors='coerce')
    except FileNotFoundError:
        st.error("Could not find **master.xlsx** file.")
        return

    # -----------------------
    # 🎯 Define Target Fuels
    # -----------------------
    st.subheader("📊 Full Environmental Impact – All Fuel Variants")
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

    impact_data_raw = {}
    process_annotations = {}

    # 🔄 Collect impact data per fuel
    for short_name, rule in target_variants.items():
        temp_df = df[(df['Fuel'] == rule['Fuel']) & (df['Scenario'].isin(rule['Scenario']))]
        impact_sum = temp_df[impact_categories].sum()
        impact_data_raw[short_name] = impact_sum

        for impact in impact_categories:
            process_grouped = temp_df.groupby("Process")[impact].sum().reset_index()
            if len(process_grouped) > 0:
                top_row = process_grouped.loc[process_grouped[impact].idxmax()]
                process_name = top_row['Process']
                process_annotations[(impact, short_name)] = process_name
            else:
                process_annotations[(impact, short_name)] = "N/A"

    # 📊 Create DataFrame & Normalize
    heatmap_df = pd.DataFrame(impact_data_raw)
    norm_df = (heatmap_df / heatmap_df.max(axis=1).values.reshape(-1, 1)) * 100
    norm_df = norm_df.loc[::-1]  # Reverse order for better visuals

    # 📊 Create DataFrame & Normalize
    heatmap_df = pd.DataFrame(impact_data_raw)
    norm_df = (heatmap_df / heatmap_df.max(axis=1).values.reshape(-1, 1)) * 100
    norm_df = norm_df.loc[::-1]  # Reverse order for better visuals

    # ✅ 단위 없는 라벨
    display_index = norm_df.index.str.replace(r"\s*\(.*\)", "", regex=True)

    # 🔥 Build Heatmap
    fig = go.Figure(data=go.Heatmap(
        z=norm_df.values,
        x=norm_df.columns,
        y=norm_df.index,
        colorscale='Reds',
        colorbar=dict(title="Relative Impact (%)"),
        hoverongaps=False
    ))

    # 🏷️ Annotate cells with top processes
    for i, impact in enumerate(norm_df.index):
        for j, fuel in enumerate(norm_df.columns):
            process = process_annotations.get((impact, fuel), "")
            value = norm_df.loc[impact, fuel]
            font_color = "white" if value > 60 else "black"
            fig.add_annotation(
                text=process,
                x=fuel,
                y=impact,
                showarrow=False,
                font=dict(color=font_color, size=10),
                xanchor="center",
                yanchor="middle"
            )

    # ✅ y축 라벨 단위 제거해서 적용
    fig.update_layout(
        xaxis=dict(showticklabels=False, side="top"),
        yaxis=dict(
            title="Impact Category",
            tickfont=dict(size=10),
            tickvals=list(norm_df.index),
            ticktext=list(display_index)
        ),
        title="🔧 Top-Contributing Process per Environmental Impact (Rotated)",
        height=1000,
        width=1000,
        margin=dict(l=180, r=40, t=80, b=100)
    )

    for fuel in norm_df.columns:
        fig.add_annotation(
            x=fuel,
            y=1.03,
            text=fuel,
            xref="x",
            yref="paper",
            showarrow=False,
            font=dict(color='black', size=12),
            xanchor="center",
            yanchor="middle"
        )
    st.plotly_chart(fig, use_container_width=True)
