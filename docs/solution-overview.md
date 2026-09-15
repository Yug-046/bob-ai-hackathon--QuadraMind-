# RouteGuard AI - Solution Overview

## 1. Solution Summary

RouteGuard AI is an interactive supply-chain decision-support application built with Python and Streamlit.

It brings shipment risk analysis, disruption-aware route optimization, fleet utilization analysis, cold-chain monitoring, and AI-assisted recommendations into a single operational dashboard.

The prototype uses synthetic logistics datasets to demonstrate how these capabilities can work together during supply-chain disruptions.

---

## 2. How the Solution Works

RouteGuard AI processes several operational datasets and presents the results through specialized modules.

```text
Synthetic Logistics Data
          │
          ▼
     Data Loading
          │
          ▼
   ┌──────┴───────┐
   │              │
   ▼              ▼
Risk Analysis   Disruption Analysis
   │              │
   └──────┬───────┘
          │
    ┌─────┼───────────────┐
    │     │               │
    ▼     ▼               ▼
 Route   Fleet       Cold Chain
Optimizer Optimizer   Monitoring
    │     │               │
    └─────┼───────────────┘
          │
          ▼
      AI Copilot
          │
          ▼
    IBM watsonx.ai