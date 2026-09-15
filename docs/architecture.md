# RouteGuard AI - Architecture

## 1. Architecture Overview

RouteGuard AI is a modular Python and Streamlit application designed as a supply-chain decision-support system.

The architecture separates:

- User interface
- Data loading
- Shipment risk analysis
- Route optimization
- Fleet optimization
- Cold-chain monitoring
- AI-assisted recommendations

The application uses synthetic CSV datasets as its primary demonstration data source.

---

## 2. High-Level Architecture

```text
                         ┌──────────────────────┐
                         │    Streamlit UI      │
                         │      app.py          │
                         └──────────┬───────────┘
                                    │
                 ┌──────────────────┼──────────────────┐
                 │                  │                  │
                 ▼                  ▼                  ▼
        ┌────────────────┐ ┌────────────────┐ ┌────────────────┐
        │  Risk Engine   │ │ Route Optimizer│ │ Fleet Optimizer│
        │ risk_engine.py │ │route_optimizer │ │fleet_optimizer │
        └───────┬────────┘ └───────┬────────┘ └───────┬────────┘
                │                  │                  │
                └──────────────────┼──────────────────┘
                                   │
                                   ▼
                         ┌────────────────────┐
                         │  Cold Chain Module │
                         │   cold_chain.py    │
                         └──────────┬─────────┘
                                    │
                                    ▼
                         ┌────────────────────┐
                         │    AI Copilot      │
                         │   ai_copilot.py    │
                         └──────────┬─────────┘
                                    │
                                    ▼
                         ┌────────────────────┐
                         │   IBM watsonx.ai   │
                         └────────────────────┘