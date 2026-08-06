import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
from streamlit_lottie import st_lottie
import networkx as nx

# -------------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------------
st.set_page_config(page_title="BioNet Explorer", layout="wide", page_icon="🧬")

# -------------------------------------------------------
# ASSETS & STYLING
# -------------------------------------------------------
@st.cache_data(show_spinner=False)
def load_lottieurl(url: str):
    try:
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=2.0)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None

lottie_dna = load_lottieurl("https://lottie.host/8b7d6056-4299-4d6f-afe2-2f3495478465/xI8Xw4Kj6a.json")
lottie_molecule = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_9xRk2z.json")
lottie_health = load_lottieurl("https://assets9.lottiefiles.com/packages/lf20_5njp3vgg.json")

# Custom CSS for Fonts and Cards
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');

html, body, [class*="css"]  {
    font-family: 'Poppins', sans-serif;
}

.glass-card {
    background: rgba(255, 255, 255, 0.7);
    backdrop-filter: blur(10px);
    border-radius: 15px;
    padding: 20px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    margin-bottom: 20px;
    border: 1px solid rgba(255,255,255,0.2);
}

h1, h2, h3 {
    color: #2c3e50;
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------
# VANTA BACKGROUND
# -------------------------------------------------------
# Use direct script injection for reliability
# Use direct script injection for reliability
vanta_code = """
<style>
#vanta-canvas {
    position: fixed; 
    top: 0; 
    left: 0; 
    width: 100vw; 
    height: 100vh; 
    z-index: -1; 
}
.stApp, [data-testid="stAppViewContainer"], .main, header {
    background: transparent !important;
}
[data-testid="stSidebar"] {
    background: rgba(255, 255, 255, 0.85) !important;
    backdrop-filter: blur(10px);
}
</style>

<div id="vanta-canvas"></div>

<!-- Load Three.js and Vanta.fog from CDN -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r134/three.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/vanta/0.5.24/vanta.fog.min.js"></script>

<script>
window.addEventListener('DOMContentLoaded', () => {
    setTimeout(() => {
        if (window.VANTA) {
            VANTA.FOG({
                el: "#vanta-canvas",
                mouseControls: true, 
                touchControls: true, 
                gyroControls: false,
                minHeight: 200.00, 
                minWidth: 200.00, 
                highlightColor: 0xca2857,
                midtoneColor: 0xa40be3,
                lowlightColor: 0xe32f2f,
                baseColor: 0xede5e5,
                blurFactor: 0.58,
                speed: 2.60
            });
        }
    }, 1000); // 1s delay to ensure Three.js loads
});
</script>
"""
st.markdown(vanta_code, unsafe_allow_html=True)


# -------------------------------------------------------
# DATA LOADING
# -------------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("data/clean_drug_network.csv")
    df_disease = pd.read_csv("data/drug_disease.csv")
    df_organ = pd.read_csv("data/drug_organ_effects.csv")
    return df, df_disease, df_organ

df, df_disease, df_organ = load_data()

# -------------------------------------------------------
# MAIN HEADER
# -------------------------------------------------------
col1, col2 = st.columns([1, 4])
with col1:
    if lottie_dna:
        st_lottie(lottie_dna, height=100, key="dna_header")
    else:
        st.write("🧬") # Fallback emoji
with col2:
    st.markdown("<h1 style='padding-top: 20px;'>BioNet Intelligence Explorer</h1>", unsafe_allow_html=True)
    st.caption("Advanced Social Network Analysis of Pharmaceutical Data")

st.write("---")

# -------------------------------------------------------
# TABS
# -------------------------------------------------------
tab_drug, tab_target, tab_disease, tab_pred = st.tabs([
    "💊 Drug Profile", "🤢 Symptom Explorer", "🩺 Disease Analysis", "🔮 Drug Interaction AI"
])

# =======================================================
# TAB 1: DRUG PROFILE
# =======================================================
with tab_drug:
    c1, c2 = st.columns([3, 1])
    with c1:
        query = st.selectbox("Search Pharmacopoeia:", [""] + df["drug_name"].tolist())
    with c2:
        if lottie_molecule:
            st_lottie(lottie_molecule, height=80, key="mol_drug")
        else:
            st.write("🧪")

    if query:
        row = df[df["drug_name"] == query].iloc[0]
        st.markdown(f"""
        <div class="glass-card">
            <h2 style='color:#2980b9;'>{row['drug_name']} <small style='color:#7f8c8d;'>({row['generic_name']})</small></h2>
            <span style="background:#e0f7fa; padding:5px 10px; border-radius:15px; color:#006064; font-weight:bold;">{row['drug_class']}</span>
        </div>
        """, unsafe_allow_html=True)

        col_info1, col_info2 = st.columns(2)
        with col_info1:
            st.markdown(f'<div class="glass-card"><h3>🧬 Mechanism</h3>{row["mechanism"]}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="glass-card"><h3>⚠️ Side Effects</h3>{row["side_effects"]}</div>', unsafe_allow_html=True) 
        with col_info2:
            st.markdown(f'<div class="glass-card"><h3>🎯 Target Proteins</h3>{row["targets"]}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="glass-card"><h3>⛔ Contraindications</h3>{row["contraindications"]}</div>', unsafe_allow_html=True)

        # Analytics for Drug
        st.subheader("📊 Analytics Dashboard")
        ac1, ac2 = st.columns(2)
        with ac1:
            org_data = df_organ[df_organ["drug_id"] == row["drug_id"]]
            if not org_data.empty:
                fig = px.bar(org_data, x="organ", y="effect", title="Organ Impact Analysis", color="organ")
                st.plotly_chart(fig, use_container_width=True)
        with ac2:
            dis_data = df_disease[df_disease["drug_id"] == row["drug_id"]]
            if not dis_data.empty:
                fig = px.pie(dis_data, names="disease", title="Disease Treatment Spectrum", hole=0.4)
                st.plotly_chart(fig, use_container_width=True)

# =======================================================
# TAB 2: SYMPTOM EXPLORER (NEW)
# =======================================================
with tab_target: # Renamed visually to Symptom Explorer
    st.markdown("### 🤢 Symptom & Side Effect Explorer")
    all_symptoms = set()
    for s_str in df["side_effects"].dropna():
        for s in s_str.split(","):
            if s.strip(): all_symptoms.add(s.strip())
    
    sym_query = st.selectbox("Search for a Side Effect:", sorted(list(all_symptoms)))
    
    if sym_query:
        # Find drugs causing this symptom
        culprits = df[df["side_effects"].apply(lambda x: sym_query in str(x))]
        st.error(f"⚠️ Found **{len(culprits)}** drugs known to cause **{sym_query}**")
        
        tc1, tc2 = st.columns([1, 2])
        with tc1:
            st.dataframe(culprits[["drug_name", "drug_class"]], hide_index=True)
        with tc2:
            # Network Subgraph: Symptom -> Drugs
            G = nx.Graph()
            G.add_node(sym_query, color='red', size=25, label=sym_query)
            for d in culprits["drug_name"]:
                G.add_node(d, color='blue', size=15)
                G.add_edge(sym_query, d)
            
            pos = nx.spring_layout(G)
            edge_x, edge_y = [], []
            for edge in G.edges():
                x0, y0 = pos[edge[0]]
                x1, y1 = pos[edge[1]]
                edge_x.extend([x0, x1, None])
                edge_y.extend([y0, y1, None])

            edge_trace = go.Scatter(x=edge_x, y=edge_y, line=dict(width=0.5, color='#888'), mode='lines')
            node_x, node_y, node_text, node_color = [], [], [], []
            for node in G.nodes():
                x, y = pos[node]
                node_x.append(x); node_y.append(y)
                node_text.append(node)
                node_color.append(G.nodes[node]['color'])

            node_trace = go.Scatter(x=node_x, y=node_y, mode='markers+text', text=node_text, textposition="top center",
                                    marker=dict(color=node_color, size=15))
            
            fig_net = go.Figure(data=[edge_trace, node_trace], layout=go.Layout(
                title=f"Cluster: Drugs causing {sym_query}", showlegend=False, margin=dict(b=0,l=0,r=0,t=40),
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
            )
            st.plotly_chart(fig_net, use_container_width=True)

# =======================================================
# TAB 3: DISEASE ANALYSIS (RESTORED)
# =======================================================
with tab_disease:
    st.markdown("### 🩺 Disease Treatment Landscape")
    all_diseases = sorted(df_disease["disease"].unique())
    dis_query = st.selectbox("Select Disease/Condition:", all_diseases)
    
    if dis_query:
        treatments = df_disease[df_disease["disease"] == dis_query]["drug_id"].unique()
        drug_infos = df[df["drug_id"].isin(treatments)]
        
        st.info(f"**{len(drug_infos)}** Approved Treatments Found")
        st.table(drug_infos[["drug_name", "drug_class", "mechanism"]])
        
        # Stats
        fig_class = px.bar(drug_infos["drug_class"].value_counts().reset_index(), 
                           x="drug_class", y="count", color="drug_class", title="Drug Classes Used")
        st.plotly_chart(fig_class, use_container_width=True)

# =======================================================
# TAB 4: PREDICTIVE AI
# =======================================================
with tab_pred:
    st.markdown("### 🔮 Drug Interaction Simulator")
    st.write("Select multiple drugs to simulate potential side effects based on their combined biological targets.")
    
    if lottie_health:
        st_lottie(lottie_health, height=150, key="ai_robot")
    else:
        st.write("🤖")
    
    # 1. Input: Select Drugs
    selected_drugs = st.multiselect("Select Drugs to Combine:", sorted(df["drug_name"].unique()))
    
    if selected_drugs:
        # 2. Extract Targets from Selected Drugs
        combined_targets = set()
        for d in selected_drugs:
            t_str = df[df["drug_name"] == d]["targets"].values[0]
            for t in str(t_str).split(","):
                if t.strip(): combined_targets.add(t.strip())
        
        st.info(f"🧬 **Bio-Simulation Profile**: Aggregated **{len(combined_targets)}** protein targets from {', '.join(selected_drugs)}.")
        
        with st.expander("View Underlying Biological Targets"):
            st.write(sorted(list(combined_targets)))
            
        # 3. Predict / Infer Risks using these targets
        # Find *other* drugs that hit these targets to infer side effects
        matched = df[df["targets"].apply(lambda x: any(t in str(x) for t in combined_targets))]
        
        if not matched.empty:
            all_eff = [e.strip() for sublist in matched["side_effects"].dropna().str.split(",") for e in sublist]
            from collections import Counter
            counts = pd.DataFrame(Counter(all_eff).most_common(10), columns=["Effect", "Count"])
            
            st.subheader("⚠️ Predicted Interaction Risk Profile")
            fig = px.bar(counts, x="Count", y="Effect", orientation='h', color="Count", title="Projected Side Effects based on Target Overlap")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Insufficient data to predict interactions for this specific combination.")
