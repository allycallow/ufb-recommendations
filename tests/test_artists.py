from unittest.mock import patch

ARTIST_ID = "artist123"
BASE_URL = f"/artists/{ARTIST_ID}"
TRENDING_URL = "/artists/trending"


def test_missing_api_key_returns_403(client):
    response = client.get(f"{BASE_URL}/related-artists")
    assert response.status_code == 403


def test_invalid_api_key_returns_401(client):
    response = client.get(
        f"{BASE_URL}/related-artists", headers={"X-API-Key": "wrong-key"}
    )
    assert response.status_code == 401
    data = response.json()
    assert data["success"] is False
    assert data["statusCode"] == 401


def test_related_artists_empty(client, auth_headers):
    with patch("app.db.get_artist_related_artists", return_value=[]) as mock_db:
        response = client.get(f"{BASE_URL}/related-artists", headers=auth_headers)
        mock_db.assert_called_once_with(ARTIST_ID)
    assert response.status_code == 200
    assert response.json() == {"success": True, "items": []}


def test_related_artists_with_data(client, auth_headers):
    mock_data = [{"id": "artist:abc"}, {"id": "artist:xyz"}]
    with patch("app.db.get_artist_related_artists", return_value=mock_data) as mock_db:
        response = client.get(f"{BASE_URL}/related-artists", headers=auth_headers)
        mock_db.assert_called_once_with(ARTIST_ID)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["items"] == ["artist:abc", "artist:xyz"]


def test_trending_artists_missing_api_key_returns_403(client):
    response = client.get(TRENDING_URL)
    assert response.status_code == 403


def test_trending_artists_invalid_api_key_returns_401(client):
    response = client.get(TRENDING_URL, headers={"X-API-Key": "wrong-key"})
    assert response.status_code == 401
    data = response.json()
    assert data["success"] is False
    assert data["statusCode"] == 401


def test_trending_artists_empty(client, auth_headers):
    with patch("app.db.get_trending_artists", return_value=[]) as mock_db:
        response = client.get(TRENDING_URL, headers=auth_headers)
        mock_db.assert_called_once()
    assert response.status_code == 200
    assert response.json() == {"success": True, "items": []}


def test_trending_artists_with_data(client, auth_headers):
    artist_ids = [
        "a4517d13-8371-4e28-b07f-8f47c56b561c",
        "41e5a14a-40ce-482d-8b2c-84f013b40f1e",
    ]
    with patch("app.db.get_trending_artists", return_value=artist_ids) as mock_db:
        response = client.get(TRENDING_URL, headers=auth_headers)
        mock_db.assert_called_once()
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["items"] == artist_ids
