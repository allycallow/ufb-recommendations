from unittest.mock import patch

RELEASE_ID = "release123"
BASE_URL = f"/releases/{RELEASE_ID}"


def test_missing_api_key_returns_403(client):
    response = client.get(f"{BASE_URL}/recommendations")
    assert response.status_code == 403


def test_invalid_api_key_returns_401(client):
    response = client.get(
        f"{BASE_URL}/recommendations", headers={"X-API-Key": "wrong-key"}
    )
    assert response.status_code == 401
    data = response.json()
    assert data["success"] is False
    assert data["statusCode"] == 401


def test_recommendations_empty(client, auth_headers):
    with patch("app.db.get_release_recommendations", return_value=[]) as mock_db:
        response = client.get(f"{BASE_URL}/recommendations", headers=auth_headers)
        mock_db.assert_called_once_with(RELEASE_ID)
    assert response.status_code == 200
    assert response.json() == {"success": True, "items": []}


def test_recommendations_with_data(client, auth_headers):
    release_ids = ["release:abc", "release:xyz"]
    mock_data = [{"items": {"SS": release_ids}}]
    with patch("app.db.get_release_recommendations", return_value=mock_data) as mock_db:
        response = client.get(f"{BASE_URL}/recommendations", headers=auth_headers)
        mock_db.assert_called_once_with(RELEASE_ID)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["items"] == release_ids
