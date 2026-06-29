from unittest.mock import patch

PLAYLIST_ID = "f10fda15-5b97-4ba3-b5aa-54f133bce41d"
BASE_URL = f"/playlists/{PLAYLIST_ID}"
SUGGESTED_TRACKS_URL = f"{BASE_URL}/suggested-tracks"


def test_missing_api_key_returns_403(client):
    response = client.get(SUGGESTED_TRACKS_URL)
    assert response.status_code == 403


def test_invalid_api_key_returns_401(client):
    response = client.get(SUGGESTED_TRACKS_URL, headers={"X-API-Key": "wrong-key"})
    assert response.status_code == 401
    data = response.json()
    assert data["success"] is False
    assert data["statusCode"] == 401


def test_suggested_tracks_empty(client, auth_headers):
    with patch("app.db.get_playlist_suggested_tracks", return_value=[]) as mock_db:
        response = client.get(SUGGESTED_TRACKS_URL, headers=auth_headers)
        mock_db.assert_called_once_with(PLAYLIST_ID)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["items"] == []
    assert data["page"] == 1
    assert data["page_size"] == 20
    assert data["total"] == 0


def test_suggested_tracks_with_data(client, auth_headers):
    track_ids = [
        "0e5cc41e-e6c5-4e8d-8f4b-d4e0843e81f6",
        "18e5a148-095e-4c77-a37e-c40d548260c2",
    ]
    with patch(
        "app.db.get_playlist_suggested_tracks", return_value=track_ids
    ) as mock_db:
        response = client.get(SUGGESTED_TRACKS_URL, headers=auth_headers)
        mock_db.assert_called_once_with(PLAYLIST_ID)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["items"] == track_ids
    assert data["page"] == 1
    assert data["page_size"] == 20
    assert data["total"] == 2


def test_suggested_tracks_pagination(client, auth_headers):
    track_ids = [f"track{i}" for i in range(5)]
    with patch(
        "app.db.get_playlist_suggested_tracks", return_value=track_ids
    ) as mock_db:
        response = client.get(
            SUGGESTED_TRACKS_URL,
            params={"page": 2, "page_size": 2},
            headers=auth_headers,
        )
        mock_db.assert_called_once_with(PLAYLIST_ID)
    assert response.status_code == 200
    data = response.json()
    assert data["items"] == ["track2", "track3"]
    assert data["page"] == 2
    assert data["page_size"] == 2
    assert data["total"] == 5


def test_suggested_tracks_page_beyond_data(client, auth_headers):
    track_ids = ["track1", "track2"]
    with patch(
        "app.db.get_playlist_suggested_tracks", return_value=track_ids
    ) as mock_db:
        response = client.get(
            SUGGESTED_TRACKS_URL,
            params={"page": 5, "page_size": 10},
            headers=auth_headers,
        )
        mock_db.assert_called_once_with(PLAYLIST_ID)
    assert response.status_code == 200
    data = response.json()
    assert data["items"] == []
    assert data["total"] == 2
