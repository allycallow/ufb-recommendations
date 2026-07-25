from unittest.mock import patch

BASE_URL = "/v1/tracks"


def test_missing_api_key_returns_403(client):
    response = client.get(f"{BASE_URL}/trending")
    assert response.status_code == 403


def test_invalid_api_key_returns_401(client):
    response = client.get(f"{BASE_URL}/trending", headers={"X-API-Key": "wrong-key"})
    assert response.status_code == 401
    data = response.json()
    assert data["success"] is False
    assert data["statusCode"] == 401


def test_trending_tracks_empty(client, auth_headers):
    with patch("app.db.get_trending_tracks", return_value=[]) as mock_db:
        response = client.get(f"{BASE_URL}/trending", headers=auth_headers)
        mock_db.assert_called_once()
    assert response.status_code == 200
    assert response.json() == {"success": True, "items": []}


def test_trending_tracks_with_data(client, auth_headers):
    track_ids = [
        "a4517d13-8371-4e28-b07f-8f47c56b561c",
        "41e5a14a-40ce-482d-8b2c-84f013b40f1e",
    ]
    with patch("app.db.get_trending_tracks", return_value=track_ids) as mock_db:
        response = client.get(f"{BASE_URL}/trending", headers=auth_headers)
        mock_db.assert_called_once()
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["items"] == track_ids
