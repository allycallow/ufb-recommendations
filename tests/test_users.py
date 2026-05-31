from unittest.mock import patch

import pytest

USER_ID = "user123"
BASE_URL = f"/users/{USER_ID}"

ENDPOINTS = [
    f"{BASE_URL}/explore",
    f"{BASE_URL}/recommendations",
    f"{BASE_URL}/more-like-release",
    f"{BASE_URL}/more-like-artist",
    f"{BASE_URL}/top-picks",
]


@pytest.mark.parametrize("endpoint", ENDPOINTS)
def test_missing_api_key_returns_403(client, endpoint):
    response = client.get(endpoint)
    assert response.status_code == 403


@pytest.mark.parametrize("endpoint", ENDPOINTS)
def test_invalid_api_key_returns_401(client, endpoint):
    response = client.get(endpoint, headers={"X-API-Key": "wrong-key"})
    assert response.status_code == 401
    data = response.json()
    assert data["success"] is False
    assert data["statusCode"] == 401


def test_explore_empty(client, auth_headers):
    with patch("app.db.get_explore", return_value=[]) as mock_db:
        response = client.get(f"{BASE_URL}/explore", headers=auth_headers)
        mock_db.assert_called_once_with(USER_ID)
    assert response.status_code == 200
    assert response.json() == {"success": True, "items": []}


def test_explore_with_data(client, auth_headers):
    mock_data = [
        {"PK": f"USER#{USER_ID}", "SK": "RECOMMENDATION#release:abc", "is_hero": 1},
        {"PK": f"USER#{USER_ID}", "SK": "RECOMMENDATION#release:xyz", "is_hero": 0},
    ]
    with patch("app.db.get_explore", return_value=mock_data):
        response = client.get(f"{BASE_URL}/explore", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert len(data["items"]) == 2
    # sorted by is_hero descending
    assert data["items"][0]["id"] == "Recommendation:release:abc"
    assert data["items"][0]["is_hero"] == 1
    assert data["items"][1]["id"] == "Recommendation:release:xyz"


def test_recommendations_empty(client, auth_headers):
    with patch("app.db.get_recommendations", return_value=[]) as mock_db:
        response = client.get(f"{BASE_URL}/recommendations", headers=auth_headers)
        mock_db.assert_called_once_with(USER_ID)
    assert response.status_code == 200
    assert response.json() == {"success": True, "items": []}


def test_recommendations_with_data(client, auth_headers):
    mock_data = [
        {"PK": f"USER#{USER_ID}", "SK": "RECOMMENDATION#artist:abc", "is_hero": 0},
    ]
    with patch("app.db.get_recommendations", return_value=mock_data):
        response = client.get(f"{BASE_URL}/recommendations", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["items"][0]["id"] == "Recommendation:artist:abc"


def test_more_like_release_empty(client, auth_headers):
    with patch("app.db.get_more_like_release", return_value=[]) as mock_db:
        response = client.get(f"{BASE_URL}/more-like-release", headers=auth_headers)
        mock_db.assert_called_once_with(USER_ID)
    assert response.status_code == 200
    assert response.json() == {"success": True, "items": []}


def test_more_like_release_with_data(client, auth_headers):
    items = [{"id": "release:abc"}, {"id": "release:xyz"}]
    mock_data = [{"items": items}]
    with patch("app.db.get_more_like_release", return_value=mock_data):
        response = client.get(f"{BASE_URL}/more-like-release", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["items"] == items


def test_more_like_artist_empty(client, auth_headers):
    with patch("app.db.get_more_like_artist", return_value=[]) as mock_db:
        response = client.get(f"{BASE_URL}/more-like-artist", headers=auth_headers)
        mock_db.assert_called_once_with(USER_ID)
    assert response.status_code == 200
    assert response.json() == {"success": True, "items": []}


def test_more_like_artist_with_data(client, auth_headers):
    items = [{"id": "artist:abc"}, {"id": "artist:xyz"}]
    mock_data = [{"items": items}]
    with patch("app.db.get_more_like_artist", return_value=mock_data):
        response = client.get(f"{BASE_URL}/more-like-artist", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["items"] == items


def test_top_picks_empty(client, auth_headers):
    with patch("app.db.get_top_picks", return_value=[]) as mock_db:
        response = client.get(f"{BASE_URL}/top-picks", headers=auth_headers)
        mock_db.assert_called_once_with(USER_ID)
    assert response.status_code == 200
    assert response.json() == {"success": True, "items": []}


def test_top_picks_with_data(client, auth_headers):
    items = [{"id": "release:abc"}, {"id": "release:xyz"}]
    mock_data = [{"items": items}]
    with patch("app.db.get_top_picks", return_value=mock_data):
        response = client.get(f"{BASE_URL}/top-picks", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["items"] == items
