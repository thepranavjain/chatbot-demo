import pytest
from fastapi import HTTPException, Request
from unittest.mock import patch, MagicMock
from firebase_admin.auth import UserRecord
from dependencies.auth import firebase_auth_dependency


@pytest.fixture
def mock_request():
    return MagicMock(spec=Request)


@patch("firebase_admin.auth.verify_id_token")
@patch("firebase_admin.auth.get_user")
def test_firebase_auth_dependency_success(
    mock_get_user, mock_verify_id_token, mock_request
):
    mock_request.headers.get.return_value = "Bearer valid_token"

    mock_decoded_token = {"uid": "test_uid"}
    mock_user_record = MagicMock(spec=UserRecord)

    mock_verify_id_token.return_value = mock_decoded_token
    mock_get_user.return_value = mock_user_record

    user_record = firebase_auth_dependency(mock_request)
    assert mock_get_user.called_once_with("test_uid")
    assert user_record == mock_user_record


def test_firebase_auth_dependency_missing_header(mock_request):
    mock_request.headers.get.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        firebase_auth_dependency(mock_request)
    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Missing or invalid Authorization header"


def test_firebase_auth_dependency_invalid_header(mock_request):
    mock_request.headers.get.return_value = "Invalid token"

    with pytest.raises(HTTPException) as exc_info:
        firebase_auth_dependency(mock_request)
    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Missing or invalid Authorization header"


@patch("firebase_admin.auth.verify_id_token", side_effect=Exception("Invalid token"))
def test_firebase_auth_dependency_invalid_token(mock_verify_id_token, mock_request):
    mock_request.headers.get.return_value = "Bearer invalid_token"

    with pytest.raises(HTTPException) as exc_info:
        firebase_auth_dependency(mock_request)
    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Authentication failed: Invalid token"
