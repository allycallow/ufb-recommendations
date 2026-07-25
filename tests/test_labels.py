from unittest.mock import patch

LABEL_ID = "label123"
BASE_URL = f"/v1/labels/{LABEL_ID}"
TOP_PICKS_URL = f"{BASE_URL}/top-picks"


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
    with patch("app.db.get_label_related_artists", return_value=[]) as mock_db:
        response = client.get(f"{BASE_URL}/related-artists", headers=auth_headers)
        mock_db.assert_called_once_with(LABEL_ID)
    assert response.status_code == 200
    assert response.json() == {"success": True, "items": []}


def test_related_artists_with_data(client, auth_headers):
    mock_data = [{"id": "artist:abc"}, {"id": "artist:xyz"}]
    with patch("app.db.get_label_related_artists", return_value=mock_data) as mock_db:
        response = client.get(f"{BASE_URL}/related-artists", headers=auth_headers)
        mock_db.assert_called_once_with(LABEL_ID)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["items"] == ["artist:abc", "artist:xyz"]


def test_top_picks_missing_api_key_returns_403(client):
    response = client.get(TOP_PICKS_URL)
    assert response.status_code == 403


def test_top_picks_invalid_api_key_returns_401(client):
    response = client.get(TOP_PICKS_URL, headers={"X-API-Key": "wrong-key"})
    assert response.status_code == 401
    data = response.json()
    assert data["success"] is False
    assert data["statusCode"] == 401


def test_top_picks_empty(client, auth_headers):
    with patch("app.db.get_label_top_picks", return_value=[]) as mock_db:
        response = client.get(TOP_PICKS_URL, headers=auth_headers)
        mock_db.assert_called_once_with(LABEL_ID)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["items"] == []
    assert data["page"] == 1
    assert data["page_size"] == 20
    assert data["total"] == 0


def test_top_picks_with_data(client, auth_headers):
    mock_items = ["track1", "track2", "track3"]
    with patch("app.db.get_label_top_picks", return_value=mock_items) as mock_db:
        response = client.get(TOP_PICKS_URL, headers=auth_headers)
        mock_db.assert_called_once_with(LABEL_ID)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["items"] == mock_items
    assert data["page"] == 1
    assert data["page_size"] == 20
    assert data["total"] == 3


def test_top_picks_pagination(client, auth_headers):
    mock_items = [f"track{i}" for i in range(5)]
    with patch("app.db.get_label_top_picks", return_value=mock_items) as mock_db:
        response = client.get(
            TOP_PICKS_URL, params={"page": 2, "page_size": 2}, headers=auth_headers
        )
        mock_db.assert_called_once_with(LABEL_ID)
    assert response.status_code == 200
    data = response.json()
    assert data["items"] == ["track2", "track3"]
    assert data["page"] == 2
    assert data["page_size"] == 2
    assert data["total"] == 5


def test_top_picks_page_beyond_data(client, auth_headers):
    mock_items = ["track1", "track2"]
    with patch("app.db.get_label_top_picks", return_value=mock_items) as mock_db:
        response = client.get(
            TOP_PICKS_URL, params={"page": 5, "page_size": 10}, headers=auth_headers
        )
        mock_db.assert_called_once_with(LABEL_ID)
    assert response.status_code == 200
    data = response.json()
    assert data["items"] == []
    assert data["total"] == 2
