import pandas as pd
from pyvis.network import Network

# ------------------------------
# LOAD ALL DATASETS
# ------------------------------
df_main = pd.read_csv("data/clean_drug_network.csv")
df_disease = pd.read_csv("data/drug_disease.csv")
df_organ = pd.read_csv("data/drug_organ_effects.csv")

# ------------------------------
# FUNCTION: BUILD GRAPH FOR ANY DRUG
# ------------------------------
def build_drug_graph(drug_name):

    # Filter rows for the chosen drug
    row = df_main[df_main["drug_name"].str.lower() == drug_name.lower()].iloc[0]

    net = Network(height="700px", width="100%", bgcolor="#000000", font_color="white")
    net.barnes_hut()

    # ------------------------------
    # DRUG NODE (CENTER)
    ------------------------------
    net.add_node(drug_name, label=drug_name, color="#4DA6FF", shape="ellipse", size=45)

    # ------------------------------
    # TARGET GENES
    ------------------------------
    if pd.notna(row["target_full_names"]):
        genes = [g.strip() for g in row["target_full_names"].split(",")]
        for g in genes:
            net.add_node(g, label=g, color="#FF8C00", shape="dot", size=22)
            net.add_edge(drug_name, g, color="#FF8C00")

    # ------------------------------
    # DISEASES
    ------------------------------
    df_d = df_disease[df_disease["drug_name"].str.lower() == drug_name.lower()]
    for _, d in df_d.iterrows():
        disease = d["disease"]
        net.add_node(disease, label=disease, color="#A64DFF", shape="box", size=20)
        net.add_edge(drug_name, disease, color="#A64DFF")

    # ------------------------------
    # ORGAN EFFECTS
    ------------------------------
    df_o = df_organ[df_organ["drug_name"].str.lower() == drug_name.lower()]
    for _, o in df_o.iterrows():
        organ = o["organ"]
        effect = o["effect"]
        
        label = f"{organ} ({effect})"
        
        net.add_node(label, label=label, color="#FF4D4D", shape="diamond", size=22)
        net.add_edge(drug_name, label, color="#FF4D4D")

    # ------------------------------
    # SIDE EFFECTS
    ------------------------------
    if pd.notna(row["side_effects"]):
        side_effects = [s.strip() for s in row["side_effects"].split(",")]
        for s in side_effects:
            net.add_node(s, label=s, color="#32CD32", shape="triangle", size=18)
            net.add_edge(drug_name, s, color="#32CD32")

    # ------------------------------
    # OUTPUT GRAPH
    ------------------------------
    net.show("drug_graph.html")
    print("Graph generated successfully! → drug_graph.html")


# ------------------------------
# EXAMPLE: Generate graph for Crocin
# ------------------------------
build_drug_graph("Crocin")
