# 🧬 BioNet Intelligence Explorer
> **Advanced Social Network Analysis (SNA) of Pharmaceutical Data**

BioNet Intelligence Explorer is an interactive web-based platform designed to map, visualize, and analyze complex networks of drug-symptom interactions, target proteins, disease treatments, and drug-drug interactions. By combining network science (NetworkX & PyVis) with interactive visuals (Plotly) and generative AI (Llama 3.3 via Groq), the system offers clinical-grade insights into pharmacology data.

---

## ✨ Features

### 1. 💊 Drug Profile & Pharmacopoeia
- **Searchable Database**: Detailed profile lookup for generic names, drug classes, and underlying mechanism of action.
- **Biomarker Mapping**: Lists targeted proteins and contraindications.
- **Organ-Level Analysis**: Interactive dashboards graphing the impact levels on major body organs and the disease treatment spectrum.

### 2. 🤢 Symptom & Toxicity Explorer
- **Symptom Clustered Network**: Interactive force-directed PyVis subgraph displaying which drugs trigger specific side effects.
- **5-Graph Analytics Dashboard**:
  - **Most Common Side Effects**: horizontal frequency bar charts.
  - **Drug Toxicity Score**: identifying high-risk drugs by total side effect counts.
  - **Symptom Load by Class**: pie chart profiling class-level side effect density.
  - **Connectivity Spread**: violin plot mapping network density.
  - **Drug-to-Symptom Balance**: ratio distribution bar charts.

### 3. 🩺 Disease Treatment Landscape
- **Approved Treatment Finder**: Map conditions and diseases to approved clinical therapeutics.
- **Drug Class Analysis**: Profiling and graphing the primary drug classes used to treat selected diseases.

### 4. 🔮 Drug Interaction Simulator
- **Biological Target Aggregator**: Combine target proteins across multiple selected drugs.
- **Predictive Interaction Engine**: Projects and ranks potential side-effect risks based on overlapping protein target profiles.

### 5. 🤖 AI Drug Assistant (Grounded Chatbot)
- **Knowledge-Grounded LLM**: Powered by **Llama 3.3** via Groq, automatically injected with local database context dynamically parsed from queries.
- **Medical Inquiry Assistant**: Ask detailed questions about mechanisms, clinical targets, and contraindications.

---

## 🛠️ Technology Stack
- **Frontend / UX**: [Streamlit](https://streamlit.io/) with a custom Glassmorphic Dark-Mode UI theme (custom HTML/CSS injection + Poppins Google Font).
- **Background Effects**: [Vanta.js](https://www.vantajs.com/) (Fog canvas animation) and [Lottie Animations](https://lottiefiles.com/).
- **Network Science**: [NetworkX](https://networkx.org/) (subgraph rendering and metrics calculations) and [PyVis](https://pyvis.readthedocs.io/) (interactive physics-based HTML graph rendering).
- **Data Analytics**: [Pandas](https://pandas.pydata.org/) & [Plotly](https://plotly.com/).
- **AI Agent**: [Groq SDK](https://github.com/groq/groq-python) with `llama-3.3-70b-versatile`.

---🚀 Getting Started
1. Prerequisites
Ensure you have Python 3.10+ installed on your system.

2. Setup Virtual Environment
Run the following commands in your terminal:

powershell


# Create environment
python -m venv .venv
# Activate environment (Windows PowerShell)
.venv\Scripts\Activate.ps1
# Install dependencies
pip install -r requirements.txt
3. Add API Keys
Create a .streamlit/secrets.toml file in the project root:

toml


GROQ_API_KEY = "your-groq-api-key-here"
(Make sure to replace this with your actual Groq key. You can generate a free key at console.groq.com)

4. Run the Application
Start the Streamlit development server:

bash


streamlit run app.py
Open http://localhost:8501 in your web browser.

## 📂 Repository Structure
```text
SNA_FINAL_PROJ/
│
├── .streamlit/
│   ├── config.toml           # Theme styling (Lavender/Plum accents)
│   └── secrets.toml          # Groq API keys (git-ignored)
│
├── data/                     # Raw & processed CSV databases
│   ├── clean_drug_network.csv
│   ├── drug_disease.csv
│   └── drug_organ_effects.csv
│
├── pages/
│   ├── 2_Network_Graph.py    # Symptom network & PyVis simulation
│   └── 3_AI_Chatbot.py       # Grounded LLM Assistant
│
├── app.py                    # Main app entry (Profile/Simulator tabs)
├── requirements.txt          # Python dependency list
├── .gitignore                # File exclusion setup for Git
└── README.md                 # Project documentation
