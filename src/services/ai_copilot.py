import os
import requests
from dotenv import load_dotenv

load_dotenv()

def _local_answer(question: str, context: str) -> str:
    q = question.lower()
    if "critical" in q or "urgent" in q:
        return (
            "Start with the highest-risk shipments shown in the dashboard. "
            "Prioritise shipments marked Critical, then review active disruptions, "
            "route alternatives and cold-chain excursions before redeploying available assets."
        )
    if "cold" in q or "temperature" in q:
        return (
            "The cold-chain panel identifies readings outside the 2–8°C operating range. "
            "Minor, Major and Critical severity are assigned from the size of the excursion. "
            "Investigate Critical readings before delivery."
        )
    if "fleet" in q or "vehicle" in q:
        return (
            "Use the fleet recommendations table to identify available assets with low utilisation. "
            "Redeploy an idle asset toward the highest-risk shipment when capacity and location make sense."
        )
    if "route" in q or "reroute" in q:
        return (
            "Compare route alternatives using the optimizer score. The recommendation favours lower "
            "disruption risk first, then travel time and cost."
        )
    return (
        "RouteGuard AI combines disruption impact, shipment risk, route ranking, fleet utilisation "
        "and cold-chain severity. Ask about critical shipments, routes, fleet or temperature excursions."
    )

def _get_token(api_key: str) -> str:
    response = requests.post(
        "https://iam.cloud.ibm.com/oidc/token",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={
            "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
            "apikey": api_key,
        },
        timeout=20,
    )
    response.raise_for_status()
    return response.json()["access_token"]

def watsonx_answer(question: str, context: str) -> tuple[str, bool]:
    enabled = os.getenv("WATSONX_ENABLED", "false").lower() == "true"
    api_key = os.getenv("WATSONX_APIKEY", "")
    project_id = os.getenv("WATSONX_PROJECT_ID", "")
    base_url = os.getenv("WATSONX_URL", "https://us-south.ml.cloud.ibm.com").rstrip("/")
    version = os.getenv("WATSONX_API_VERSION", "2025-10-25")
    model_id = os.getenv("WATSONX_MODEL_ID", "ibm/granite-4-0-h-small")

    if not enabled or not api_key or not project_id:
        return _local_answer(question, context), False

    try:
        token = _get_token(api_key)
        url = f"{base_url}/ml/v1/text/chat?version={version}"
        system = (
            "You are RouteGuard AI, a logistics operations copilot. "
            "Use only the supplied application context. Do not invent shipment IDs, costs, "
            "routes or sensor values. Explain recommendations briefly and clearly. "
            "When uncertainty exists, say what should be checked by an operator."
        )
        payload = {
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": f"APPLICATION CONTEXT:\n{context}\n\nQUESTION:\n{question}"},
            ],
            "project_id": project_id,
            "model_id": model_id,
            "max_completion_tokens": 500,
            "temperature": 0,
        }
        response = requests.post(
            url,
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}",
            },
            json=payload,
            timeout=45,
        )
        response.raise_for_status()
        data = response.json()
        text = data["choices"][0]["message"]["content"]
        return text.strip(), True
    except Exception as exc:
        return (
            "watsonx.ai could not be reached, so RouteGuard used its local fallback. "
            f"Check your WATSONX settings. Technical detail: {type(exc).__name__}."
        ), False
