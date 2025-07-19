import io
from unittest.mock import patch
import pandas as pd


# sample cleaned DataFrame returned by patched clean_csv()
_sample_df = pd.DataFrame(
    {"ds": pd.date_range("2025-01-01", periods=3, freq="D"), "y": [10, 12, 14]}
)


def test_clean_success(client):
    csv_bytes = b"dummy"  # content ignored because clean_csv is patched
    with patch("DataScience.preprocess.clean_csv", return_value=_sample_df):
        resp = client.post(
            "/clean",
            data={"file": (io.BytesIO(csv_bytes), "sales.csv")},
            content_type="multipart/form-data",
        )
    assert resp.status_code == 200
    body = resp.get_json()
    assert isinstance(body, list)
    assert body[0].keys() == {"ds", "y"}


def test_clean_missing_file(client):
    resp = client.post("/clean", data={}, content_type="multipart/form-data")
    assert resp.status_code == 400


def test_clean_wrong_extension(client):
    csv_bytes = b"dummy"
    with patch("DataScience.preprocess.clean_csv", return_value=_sample_df):
        resp = client.post(
            "/clean",
            data={"file": (io.BytesIO(csv_bytes), "sales.txt")},
            content_type="multipart/form-data",
        )
    assert resp.status_code == 400