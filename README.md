# 🚀 RouteGuard AI
## Supply Chain Disruption & Fleet Utilisation Optimizer

RouteGuard AI is an AI-powered decision-support prototype designed to help logistics and supply-chain teams respond to disruptions, optimize transportation routes, improve fleet utilization, and protect cold-chain shipments.

---

## 👥 Team

| Field | Value |
|---|---|
| **Team Name** | QuadraMind |
| **Track** | AI |
| **Team Lead** | Patel Yug Bhaveshkumar – 24ee046@charusat.edu.in |
| **Member 2** | Nishil Niraj Patwa – 25ee043@charusat.edu.in |
| **Member 3** | Rishit Shailendrabhai Pitroda – d26dce142@charusat.edu.in |
| **Member 4** | Krishn Shaileshbhai Padhariya – 25ee028@charusat.edu.in |

---

## 🎯 Problem Statement

Supply-chain disruptions such as severe weather, port strikes, and geopolitical events can cascade across shipments, while fleet assets may remain idle as other routes become overloaded. Cold-chain shipments are especially vulnerable because temperature excursions can cause product loss and delivery risk.

Logistics teams need a centralized decision-support system that can identify affected shipments, prioritize risk, recommend safer alternatives, redeploy underutilized fleet assets, and monitor cold-chain conditions.

---

## 💡 Solution

RouteGuard AI is an interactive Streamlit application that combines shipment risk analysis, disruption-aware route optimization, fleet utilization analysis, cold-chain monitoring, and AI-assisted operational recommendations.

The system analyzes synthetic logistics data to identify high-risk shipments, recommend alternative routes based on disruption risk, identify underutilized fleet assets for possible redeployment, detect cold-chain temperature excursions, and provide natural-language recommendations through an IBM watsonx.ai powered Copilot.

---

## ✨ Key Features

- **Disruption-aware shipment risk prioritization**  
  Identifies shipments affected by active disruptions and prioritizes them according to operational risk.

- **Disruption-aware route optimization**  
  Compares available routes using factors such as disruption risk, travel time, and estimated cost to recommend safer alternatives.

- **Fleet utilization analysis**  
  Identifies underutilized fleet assets and recommends potential shipment assignments for redeployment.

- **Cold-chain monitoring**  
  Detects temperature excursions in cold-chain shipments and classifies their severity.

- **IBM watsonx.ai Copilot**  
  Provides natural-language operational recommendations based on the logistics scenarios presented in the application.

---

## 🖥️ Application Modules

### 1. Command Dashboard

Provides an overview of the current logistics situation, including:

- Active shipments
- High and critical risk shipments
- Disruption-affected shipments
- Operational risk indicators

### 2. Route Optimizer

Allows users to select an origin and destination and compare available routes.

The optimizer considers:

- Route distance
- Estimated travel time
- Base transportation cost
- Disruption risk
- Overall route score

The system recommends a route with a lower operational risk while considering time and cost.

### 3. Fleet Optimizer

Analyzes fleet utilization and identifies vehicles or vessels operating below the configured utilization threshold.

The module provides potential redeployment recommendations by matching underutilized assets with suitable shipments.

### 4. Cold Chain Monitor

Analyzes temperature sensor readings for cold-chain shipments.

The module provides:

- Temperature readings
- Allowed temperature range
- Temperature deviation
- Excursion detection
- Severity classification

### 5. AI Copilot

The AI Copilot uses IBM watsonx.ai to generate natural-language operational recommendations for supply-chain scenarios.

A local deterministic fallback is also available when the IBM watsonx.ai connection is not configured.

---

## 🛠️ Technology Stack

### Languages

- Python

### Frameworks & Libraries

- Streamlit
- Pandas
- NumPy
- Plotly
- NetworkX
- Requests

### IBM Technologies

- IBM watsonx.ai
- IBM Bob IDE

### Testing

- Pytest

### Data

- Synthetic CSV datasets

---

## 📁 Project Structure

```text
routeguard-ai/
├── src/
│   ├── app.py
│   ├── data_loader.py
│   ├── generate_data.py
│   ├── data/
│   │   ├── shipments.csv
│   │   ├── fleet.csv
│   │   ├── routes.csv
│   │   ├── disruptions.csv
│   │   ├── cold_chain.csv
│   │   └── README.md
│   └── services/
│       ├── risk_engine.py
│       ├── route_optimizer.py
│       ├── fleet_optimizer.py
│       ├── cold_chain.py
│       └── ai_copilot.py
│
├── tests/
│   └── test_engines.py
│
├── requirements.txt
└── README.md