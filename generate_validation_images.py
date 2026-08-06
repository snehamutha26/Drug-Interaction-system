
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import os

# Create output directory
os.makedirs("report_visuals", exist_ok=True)

# 1. Load Data
try:
    df_drugs = pd.read_csv("data/clean_drug_network.csv")
    df_disease = pd.read_csv("data/drug_disease.csv")
    df_organ = pd.read_csv("data/drug_organ_effects.csv")
    print("Datasets loaded successfully.")
except Exception as e:
    print(f"Error loading datasets: {e}")
    exit()

# Set style
plt.style.use('ggplot')

# ==========================================
# 1. Dataset Validation Summary
# ==========================================
print("Generating Dataset Validation Summary...")
plt.figure(figsize=(10, 6))

data_counts = {
    'Drugs': len(df_drugs),
    'Disease Associations': len(df_disease),
    'Organ Effects': len(df_organ)
}

# Create bar chart
bars = plt.bar(data_counts.keys(), data_counts.values(), color=['#8C4ADE', '#4A90E2', '#50E3C2'])
plt.title('Dataset Validation: Record Counts', fontsize=14)
plt.ylabel('Number of Records')
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Add value labels
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height,
             f'{height:,}',
             ha='center', va='bottom')

plt.tight_layout()
plt.savefig("report_visuals/1_dataset_validation.png", dpi=300)
plt.close()


# ==========================================
# Build Network for Analysis
# ==========================================
print("Building Network...")
G = nx.Graph()

# Add drug nodes and target nodes from drug df
# Assuming 'drug_name' and 'targets' columns based on app.py
for _, row in df_drugs.iterrows():
    drug = str(row['drug_name'])
    targets = str(row['targets']).split(',')
    
    G.add_node(drug, type='drug', color='#8C4ADE')
    
    for t in targets:
        t = t.strip()
        if t:
            G.add_node(t, type='target', color='#50E3C2')
            G.add_edge(drug, t)

print(f"Network built. Nodes: {G.number_of_nodes()}, Edges: {G.number_of_edges()}")

# ==========================================
# 2. Network Graph Structure (Sample)
# ==========================================
print("Generating Network Structure Visualization...")
# Subsample for visibility if too large
if G.number_of_nodes() > 500:
    # Take a subgraph of top degree nodes + neighbors
    degrees = dict(G.degree())
    top_nodes = sorted(degrees, key=degrees.get, reverse=True)[:50]
    nodes_to_draw = set(top_nodes)
    for n in top_nodes:
        nodes_to_draw.update(list(G.neighbors(n))[:2]) # Add a few neighbors
    H = G.subgraph(nodes_to_draw)
else:
    H = G

plt.figure(figsize=(12, 12))
pos = nx.spring_layout(H, k=0.15, iterations=20)

# Draw nodes by type
drugs = [n for n, d in H.nodes(data=True) if d.get('type') == 'drug']
targets = [n for n, d in H.nodes(data=True) if d.get('type') == 'target']

nx.draw_networkx_nodes(H, pos, nodelist=drugs, node_color='#8C4ADE', node_size=100, label='Drugs')
nx.draw_networkx_nodes(H, pos, nodelist=targets, node_color='#50E3C2', node_size=50, label='Targets')
nx.draw_networkx_edges(H, pos, alpha=0.2, edge_color='gray')

plt.title('Drug-Target Interaction Network (Sampled)', fontsize=16)
plt.legend()
plt.axis('off')
plt.tight_layout()
plt.savefig("report_visuals/2_network_structure.png", dpi=300)
plt.close()


# ==========================================
# 3. Centrality Analysis
# ==========================================
print("Generating Centrality Analysis...")
# Use the full graph G for metrics
degree_cent = nx.degree_centrality(G)
top_10 = sorted(degree_cent.items(), key=lambda x: x[1], reverse=True)[:10]

nodes = [x[0] for x in top_10]
scores = [x[1] for x in top_10]

plt.figure(figsize=(12, 6))
plt.barh(nodes[::-1], scores[::-1], color='#8C4ADE')
plt.title('Top 10 Most Influential Nodes (Degree Centrality)', fontsize=14)
plt.xlabel('Degree Centrality Score')
plt.tight_layout()
plt.savefig("report_visuals/3_centrality_analysis.png", dpi=300)
plt.close()


# ==========================================
# 4. Community Detection
# ==========================================
print("Generating Community Detection Visualization...")
from networkx.algorithms.community import greedy_modularity_communities

# Community detection on the sampled graph H for visualization speed
communities = list(greedy_modularity_communities(H))

# Create color map
color_map = []
community_colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEEAD', '#D4A5A5', '#9B59B6', '#3498DB']

node_community = {}
for i, comm in enumerate(communities):
    c_color = community_colors[i % len(community_colors)]
    for node in comm:
        node_community[node] = c_color

colors = [node_community.get(n, '#999999') for n in H.nodes()]

plt.figure(figsize=(12, 12))
pos_comm = nx.spring_layout(H, k=0.2, iterations=30)
nx.draw_networkx_nodes(H, pos_comm, node_size=80, node_color=colors)
nx.draw_networkx_edges(H, pos_comm, alpha=0.15)
plt.title('Community Detection (Modularity Class)', fontsize=16)
plt.axis('off')
plt.tight_layout()
plt.savefig("report_visuals/4_community_structure.png", dpi=300)
plt.close()

print("All visuals generated in 'report_visuals/' directory.")
