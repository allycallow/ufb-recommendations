from unittest.mock import patch

LABEL_ID = "label123"
BASE_URL = f"/labels/{LABEL_ID}"


def test_missing_api_key_returns_403(client):
    response = client.get(f"{BASE_URL}/related-artists")
    assert response.status_code == 403


def test_invalid_api_key_returns_401(client):
    response = client.get(f"{BASE_URL}/related-artists", headers={"X-API-Key": "wrong-key"})
    assert response.status_code == 401
    data = response.json()
    assert data["success"] is False
    assert data["statusCode"] == 401


def test_related_artists_empty(client, auth_headers):
    with patch("app.db.get_label_related_artists", return_value=[]) as mock_db:
        response = client.get(f"{BASE_URL}/related-artists", headers=auth_headers)
        mock_db.assert_called_once_with(LABEL_ID)
    assert response.status_code == 200
    assert response.json() == {"success": True, "items": []}


def test_related_artists_with_data(client, auth_headers):
    items = [{"id": "artist:abc"}, {"id": "artist:xyz"}]
    mock_data = [{"items": items}]
    with patch("app.db.get_label_related_artists", return_value=mock_data) as mock_db:
        response = client.get(f"{BASE_URL}/related-artists", headers=auth_headers)
        mock_db.assert_called_once_with(LABEL_ID)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["items"] == ["artist:abc", "artist:xyz"]
