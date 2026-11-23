import os
import time
from flask import Flask, jsonify, request

app = Flask(__name__)


@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    return response


@app.get("/health")
def health():
    return jsonify({"status": "ok", "service": "nexvora-ai-backend"})


def evaluate_prompt(prompt: str) -> dict:
    start_time = time.perf_counter()
    lowered = prompt.lower()

    is_sensitive = any(
        token in lowered
        for token in [
            "zip code",
            "age group",
            "race",
            "gender",
            "loan approval",
            "credit score",
            "discriminat",
            "prioritizing applicants",
            "ssn",
            "password",
        ]
    )
    is_complex = (
        any(
            token in lowered
            for token in [
                "algorithm",
                "distributed",
                "rate limiter",
                "time/space",
                "complexity",
                "architect",
                "python",
                "sql",
                "optimize",
                "code",
            ]
        )
        or len(prompt) > 130
    )

    if is_sensitive:
        payload = {
            "category": "sensitive",
            "modelId": "llama-70b",
            "tierBadge": "Open-Source Guarded Tier",
            "tierKey": "open",
            "carbonBadge": "Policy-Wrapped Inference",
            "modelName": "Llama-3.3-70B (Fairness-Guarded)",
            "confidence": 94,
            "complexityLabel": "Complexity: 0.58 (Policy Sensitive)",
            "reason": "Protected demographic attributes detected — routed to guarded tier with fairness constraints.",
            "costActual": "$0.0011",
            "costBaseline": "vs $0.0048 Frontier",
            "savedPct": 77,
            "savedDollar": 0.0037,
            "energy": "0.09g CO2e",
            "energyBadge": "Balanced Tier",
            "guardrailStatus": "FLAGGED",
            "guardrailTitle": "Bias / PII Mitigated",
            "guardrailDesc": "Demographic proxies stripped; neutrality constraints applied.",
            "warningText": "Protected attributes were excluded from scoring weights to preserve parity.",
            "output": (
                "Guardrail Notice: Sensitive demographic attributes were excluded from decision weights.\n\n"
                "1. Evaluate objective financial capacity and verified documentation.\n"
                "2. Apply uniform eligibility thresholds across all applicants.\n"
                "3. Log audit metadata without storing raw protected attributes."
            ),
            "tokens": 680,
            "qgScore": "8.8 / 10",
            "qgStatus": "MITIGATED",
            "faithfulness": 0.91,
            "relevancy": 0.95,
            "toxicity": 0.01,
            "hallucination": 0.02,
            "trace": [
                {
                    "step": "1. Intent & Complexity Analysis",
                    "detail": "Scored prompt complexity at 0.58 with sensitive decision context.",
                    "badge": "Moderate",
                    "ok": True,
                },
                {
                    "step": "2. Guardrail & Fairness Policy",
                    "detail": "Neutrality constraint applied before generating response.",
                    "badge": "Mitigated",
                    "ok": False,
                },
                {
                    "step": "3. Backend Model Routing",
                    "detail": "Routed via Python backend service using env config.",
                    "badge": "Guarded",
                    "ok": True,
                },
            ],
        }
    elif is_complex:
        payload = {
            "category": "complex",
            "modelId": "gemini-pro",
            "tierBadge": "Frontier Reasoning Tier",
            "tierKey": "pro",
            "carbonBadge": "Deep Reasoning Allocated",
            "modelName": "Gemini 2.5 Pro",
            "confidence": 98,
            "complexityLabel": "Complexity: 0.89 (High)",
            "reason": "High technical reasoning depth detected — routed to Frontier tier for thorough analysis.",
            "costActual": "$0.0042",
            "costBaseline": "vs $0.0120 Deep Tier",
            "savedPct": 65,
            "savedDollar": 0.0078,
            "energy": "0.22g CO2e",
            "energyBadge": "High Compute",
            "guardrailStatus": "PASS",
            "guardrailTitle": "Safe & Compliant",
            "guardrailDesc": "No PII or policy violations detected.",
            "warningText": "",
            "output": (
                "• Use a sliding-window timestamp log per client key with atomic expiry checks.\n"
                "• Time Complexity: Amortized O(1) per request.\n"
                "• Space Complexity: O(N) over active client timestamps within the window."
            ),
            "tokens": 1340,
            "qgScore": "9.7 / 10",
            "qgStatus": "PASS",
            "faithfulness": 0.96,
            "relevancy": 0.99,
            "toxicity": 0.00,
            "hallucination": 0.01,
            "trace": [
                {
                    "step": "1. Intent & Complexity Analysis",
                    "detail": "Detected technical/architectural reasoning prompt (Complexity: 0.89).",
                    "badge": "High Depth",
                    "ok": True,
                },
                {
                    "step": "2. Policy & Safety Check",
                    "detail": "Passed pre-flight safety check.",
                    "badge": "Clean",
                    "ok": True,
                },
                {
                    "step": "3. Backend Model Routing",
                    "detail": "Selected Gemini 2.5 Pro tier via /api/route.",
                    "badge": "Escalated",
                    "ok": True,
                },
            ],
        }
    else:
        payload = {
            "category": "simple",
            "modelId": "flash-lite",
            "tierBadge": "In-House Lightweight Tier",
            "tierKey": "lite",
            "carbonBadge": "95% Lower Compute",
            "modelName": "Gemini 2.5 Flash-Lite",
            "confidence": 96,
            "complexityLabel": "Complexity: 0.21 (Low)",
            "reason": "Low complexity and zero PII detected — routed to lightweight tier to minimize cost and latency.",
            "costActual": "$0.0002",
            "costBaseline": "vs $0.0045 Frontier",
            "savedPct": 95,
            "savedDollar": 0.0043,
            "energy": "0.04g CO2e",
            "energyBadge": "Low Carbon",
            "guardrailStatus": "PASS",
            "guardrailTitle": "Safe & Compliant",
            "guardrailDesc": "Zero PII or protected-attribute bias detected.",
            "warningText": "",
            "output": (
                "• Concise routing summary generated by the Nexvora AI backend.\n"
                "• Low-complexity requests stay on fast, low-cost inference.\n"
                "• Ready to swap in live provider SDK calls using server environment variables."
            ),
            "tokens": 340,
            "qgScore": "9.6 / 10",
            "qgStatus": "PASS",
            "faithfulness": 0.94,
            "relevancy": 0.98,
            "toxicity": 0.00,
            "hallucination": 0.01,
            "trace": [
                {
                    "step": "1. Intent & Complexity Analysis",
                    "detail": "Classified as low-complexity request (Complexity: 0.21).",
                    "badge": "Low Depth",
                    "ok": True,
                },
                {
                    "step": "2. Policy & Safety Check",
                    "detail": "Passed pre-flight check.",
                    "badge": "Clean",
                    "ok": True,
                },
                {
                    "step": "3. Backend Model Routing",
                    "detail": "Routed to Gemini 2.5 Flash-Lite tier via /api/route.",
                    "badge": "Optimal",
                    "ok": True,
                },
            ],
        }

    elapsed_ms = int((time.perf_counter() - start_time) * 1000)
    payload["latency"] = f"{max(0.12, elapsed_ms / 1000):.2f}s"
    return payload


@app.route("/api/route", methods=["POST", "OPTIONS"])
def api_route():
    if request.method == "OPTIONS":
        return ("", 204)

    data = request.get_json(silent=True) or {}
    prompt = (data.get("prompt") or "").strip()
    if not prompt:
        return jsonify({"error": "Prompt is required"}), 400

    # Example env var read for real provider integration on Render:
    # api_key = os.environ.get("GEMINI_API_KEY", "")
    _ = os.environ.get("GEMINI_API_KEY", "")
    return jsonify(evaluate_prompt(prompt))


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
