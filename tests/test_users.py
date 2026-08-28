from unittest.mock import patch

import pytest

USER_ID = "user123"
BASE_URL = f"/v1/users/{USER_ID}"

ENDPOINTS = [
    f"{BASE_URL}/explore",
    f"{BASE_URL}/recommendations",
    f"{BASE_URL}/more-like-release",
    f"{BASE_URL}/more-like-artist",
    f"{BASE_URL}/top-picks",
    f"{BASE_URL}/home",
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


RECOMMENDATION_ITEM = {
    "title": "Top Picks",
    "items": [{"id": "Release:abc"}, {"id": "Release:xyz"}],
    "meta": {"types": ["RELEASE"], "next_update_date": "2024-02-02"},
}


def test_explore_with_data(client, auth_headers):
    mock_data = [
        {
            "PK": f"USER#{USER_ID}",
            "SK": "RECOMMENDATION#release:abc",
            "is_hero": 1,
            **RECOMMENDATION_ITEM,
        },
        {
            "PK": f"USER#{USER_ID}",
            "SK": "RECOMMENDATION#release:xyz",
            "is_hero": 0,
            **RECOMMENDATION_ITEM,
        },
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
        {
            "PK": f"USER#{USER_ID}",
            "SK": "RECOMMENDATION#artist:abc",
            "is_hero": 0,
            **RECOMMENDATION_ITEM,
        },
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
    mock_data = [
        {
            "id": "6a2d9cd4-35b8-4fbf-903c-367a569ad535",
            "target_id": "release:abc",
            "type": "MORE_LIKE_RELEASE",
            "recommendations": ["release:1", "release:2"],
            "processed_at": "2026-07-25T09:23:43.618795+00:00",
        },
        {
            "id": "1a6b208b-31d1-42aa-b6ca-24bba6e84b8a",
            "target_id": "release:xyz",
            "type": "MORE_LIKE_RELEASE",
            "recommendations": ["release:3"],
            "processed_at": "2026-07-25T09:23:43.618795+00:00",
        },
    ]
    with patch("app.db.get_more_like_release", return_value=mock_data):
        response = client.get(f"{BASE_URL}/more-like-release", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["items"] == [
        {
            "id": "6a2d9cd4-35b8-4fbf-903c-367a569ad535",
            "target_id": "release:abc",
            "recommendations": ["release:1", "release:2"],
        },
        {
            "id": "1a6b208b-31d1-42aa-b6ca-24bba6e84b8a",
            "target_id": "release:xyz",
            "recommendations": ["release:3"],
        },
    ]


def test_more_like_artist_empty(client, auth_headers):
    with patch("app.db.get_more_like_artist", return_value=[]) as mock_db:
        response = client.get(f"{BASE_URL}/more-like-artist", headers=auth_headers)
        mock_db.assert_called_once_with(USER_ID)
    assert response.status_code == 200
    assert response.json() == {"success": True, "items": []}


def test_more_like_artist_with_data(client, auth_headers):
    mock_data = [
        {
            "id": "6a2d9cd4-35b8-4fbf-903c-367a569ad535",
            "target_id": "artist:abc",
            "type": "MORE_LIKE_ARTIST",
            "recommendations": ["release:1", "release:2"],
            "processed_at": "2026-07-25T09:23:43.618795+00:00",
        },
        {
            "id": "1a6b208b-31d1-42aa-b6ca-24bba6e84b8a",
            "target_id": "artist:xyz",
            "type": "MORE_LIKE_ARTIST",
            "recommendations": ["release:3"],
            "processed_at": "2026-07-25T09:23:43.618795+00:00",
        },
    ]
    with patch("app.db.get_more_like_artist", return_value=mock_data):
        response = client.get(f"{BASE_URL}/more-like-artist", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["items"] == [
        {
            "id": "6a2d9cd4-35b8-4fbf-903c-367a569ad535",
            "target_id": "artist:abc",
            "recommendations": ["release:1", "release:2"],
        },
        {
            "id": "1a6b208b-31d1-42aa-b6ca-24bba6e84b8a",
            "target_id": "artist:xyz",
            "recommendations": ["release:3"],
        },
    ]


def test_home_empty(client, auth_headers):
    with (
        patch("app.db.get_home_feed", return_value=[]) as mock_home_feed,
        patch("app.db.get_more_like_release", return_value=[]) as mock_release,
        patch("app.db.get_more_like_artist", return_value=[]) as mock_artist,
    ):
        response = client.get(f"{BASE_URL}/home", headers=auth_headers)
        mock_home_feed.assert_called_once_with(USER_ID)
        mock_release.assert_called_once_with(USER_ID)
        mock_artist.assert_called_once_with(USER_ID)
    assert response.status_code == 200
    assert response.json() == {"success": True, "items": []}


def test_home_with_data(client, auth_headers):
    home_feed = [
        {
            "id": "home-feed-hero",
            "target_id": "home-feed-hero",
            "type": "release",
            "title": "Latest Release",
            "subtitle": "Check out the latest release from our artists",
            "items": ["release:hero"],
        },
    ]
    more_like_release = [
        {
            "id": "6a2d9cd4-35b8-4fbf-903c-367a569ad535",
            "target_id": "release:abc",
            "type": "MORE_LIKE_RELEASE",
            "recommendations": ["release:1"],
        },
    ]
    more_like_artist = [
        {
            "id": "1a6b208b-31d1-42aa-b6ca-24bba6e84b8a",
            "target_id": "artist:xyz",
            "type": "MORE_LIKE_ARTIST",
            "recommendations": ["release:2"],
        },
    ]
    with (
        patch("app.db.get_home_feed", return_value=home_feed),
        patch("app.db.get_more_like_release", return_value=more_like_release),
        patch("app.db.get_more_like_artist", return_value=more_like_artist),
    ):
        response = client.get(f"{BASE_URL}/home", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True

    # The home-feed section is curated and must stay first; the more-like
    # sections are shuffled after it, so only their relative order is fixed.
    assert data["items"][0] == {
        "id": "home-feed-hero",
        "target_id": "home-feed-hero",
        "type": "release",
        "title": "Latest Release",
        "subtitle": "Check out the latest release from our artists",
        "items": ["release:hero"],
    }
    assert sorted(data["items"][1:], key=lambda item: item["id"]) == [
        {
            "id": "1a6b208b-31d1-42aa-b6ca-24bba6e84b8a",
            "target_id": "artist:xyz",
            "type": "MORE_LIKE_ARTIST",
            "title": None,
            "subtitle": "More Like",
            "items": ["release:2"],
        },
        {
            "id": "6a2d9cd4-35b8-4fbf-903c-367a569ad535",
            "target_id": "release:abc",
            "type": "MORE_LIKE_RELEASE",
            "title": None,
            "subtitle": "More Like",
            "items": ["release:1"],
        },
    ]


def test_top_picks_empty(client, auth_headers):
    with patch("app.db.get_top_picks", return_value=[]) as mock_db:
        response = client.get(f"{BASE_URL}/top-picks", headers=auth_headers)
        mock_db.assert_called_once_with(USER_ID)
    assert response.status_code == 200
    assert response.json() == {"success": True, "items": []}


def test_top_picks_with_data(client, auth_headers):
    items = [
        {"type": "release", "id": "release:abc"},
        {"type": "release", "id": "release:xyz"},
    ]
    mock_data = [{"items": items}]
    with patch("app.db.get_top_picks", return_value=mock_data):
        response = client.get(f"{BASE_URL}/top-picks", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["items"] == items
