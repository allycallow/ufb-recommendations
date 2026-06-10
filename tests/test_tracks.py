from unittest.mock import patch

BASE_URL = "/tracks"


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
    track_ids = ["track:abc", "track:xyz"]
    mock_data = [{"id": tid} for tid in track_ids]
    with patch("app.db.get_trending_tracks", return_value=mock_data) as mock_db:
        response = client.get(f"{BASE_URL}/trending", headers=auth_headers)
        mock_db.assert_called_once()
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["items"] == track_ids
