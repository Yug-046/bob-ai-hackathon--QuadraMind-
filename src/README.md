# RouteGuard AI source

The application is intentionally split into small Python modules so the project is
easy for a student developer to understand, test and extend.

- `app.py` — Streamlit user interface.
- `data_loader.py` — CSV loading and validation.
- `services/risk_engine.py` — disruption impact and shipment risk scoring.
- `services/route_optimizer.py` — route ranking.
- `services/fleet_optimizer.py` — idle fleet and redeployment logic.
- `services/cold_chain.py` — temperature excursion and severity analysis.
- `services/ai_copilot.py` — IBM watsonx.ai integration with a local fallback.
- `generate_data.py` — deterministic synthetic dataset generator.

All data included in this project is synthetic and contains no personal or client data.
