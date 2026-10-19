"""Verify the customer API uses Gemini through the app's review-generation flow."""

from app import ai_service
from app.config import settings
from tests.conftest import sample_business


def test_generate_review_uses_gemini(client, auth, monkeypatch):
    monkeypatch.setattr(settings, "GEMINI_API_KEY", "test-gemini-key")
    calls = []

    def fake_gemini(prompt, regenerate):
        calls.append((prompt, regenerate))
        return '{"review": "I liked the Food Quality and thought the Service was good."}'

    monkeypatch.setattr(ai_service, "_call_gemini", fake_gemini)

    created = client.post("/api/admin/businesses", json=sample_business(), headers=auth)
    assert created.status_code == 201
    business = created.json()

    response = client.post(
        f"/api/public/business/{business['id']}/generate-review",
        json={
            "answers": [
                {"category_id": business["categories"][0]["id"], "rating": "Excellent"},
                {"category_id": business["categories"][1]["id"], "rating": "Good"},
            ],
            "comment": "",
        },
    )

    assert response.status_code == 200
    result = response.json()
    assert result["source"] == "ai"
    assert result["fallback_reason"] is None
    assert result["review"] == "I liked the Food Quality and thought the Service was good."
    assert len(calls) == 1
    assert '"business_name": "Bluebird Cafe"' in calls[0][0]
    assert calls[0][1] is False
