from unittest.mock import patch
import pandas as pd


_sample_forecast = pd.DataFrame(
    {
        "ds": pd.date_range("2025-01-06", periods=3, freq="D"),
        "yhat": [6, 7, 8],
        "yhat_lower": [5, 6, 7],
        "yhat_upper": [7, 8, 9],
        "model_used": ["linear"] * 3,
        "low_confidence": [False, False, False],
    }
)


def test_forecast_success(client):
    payload = {
        "data": [
            {"ds": "2025-01-01", "y": 1},
            {"ds": "2025-01-02", "y": 2},
            {"ds": "2025-01-03", "y": 3},
        ]
    }
    with patch("DataScience.forecast.run_forecast", return_value=_sample_forecast):
        resp = client.post("/forecast", json=payload)
    assert resp.status_code == 200
    body = resp.get_json()
    assert set(body.keys()) == {"forecast", "low_confidence"}
    assert isinstance(body["forecast"], list)
    assert isinstance(body["low_confidence"], bool)


def test_forecast_missing_data(client):
    resp = client.post("/forecast", json={})
    assert resp.status_code == 400


def test_forecast_wrong_columns(client):
    bad_payload = {"data": [{"date": "2025-01-01", "value": 1}]}
    with patch("DataScience.forecast.run_forecast", return_value=_sample_forecast):
        resp = client.post("/forecast", json=bad_payload)
    assert resp.status_code == 400