import json
import os
import shutil
import time
from datetime import datetime
from pprint import pprint
from unittest.mock import Mock

import pytest
import requests
from dotenv import load_dotenv
from tenacity import RetryError

from otterai.otterai import OtterAI, OtterAIException

load_dotenv(dotenv_path=".env")

TEST_SPEECH_OTID = os.getenv("TEST_OTTERAI_SPEECH_OTID")
assert TEST_SPEECH_OTID is not None, "TEST_OTTERAI_SPEECH_OTID is not set in .env"

DOWNLOAD_DIR = "test_downloads"


@pytest.fixture(scope="module", autouse=True)
def setup_download_dir():
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    yield

    # shutil.rmtree(DOWNLOAD_DIR)


@pytest.fixture
def otterai_instance():
    return OtterAI()


@pytest.fixture
def authenticated_otterai_instance():
    otter = OtterAI()
    username = os.getenv("OTTERAI_USERNAME")
    password = os.getenv("OTTERAI_PASSWORD")

    assert username is not None, "OTTERAI_USERNAME is not set in .env"
    assert password is not None, "OTTERAI_PASSWORD is not set in .env"

    response = otter.login(username, password)
    assert response["status"] == requests.codes.ok, "Failed to log in"

    return otter


# Login Tests
def test_login(otterai_instance):
    username = os.getenv("OTTERAI_USERNAME")
    password = os.getenv("OTTERAI_PASSWORD")
    assert username is not None, "OTTERAI_USERNAME is not set in .env"
    assert password is not None, "OTTERAI_PASSWORD is not set in .env"

    response = otterai_instance.login(username, password)
    assert response["status"] == requests.codes.ok


def test_login_invalid_username(otterai_instance):
    response = otterai_instance.login("invalid_username", os.getenv("OTTERAI_PASSWORD"))
    assert response["status"] != requests.codes.ok


def test_login_invalid_password(otterai_instance):
    response = otterai_instance.login(os.getenv("OTTERAI_USERNAME"), "invalid_password")
    assert response["status"] != requests.codes.ok


def test_login_invalid_credentials(otterai_instance):
    response = otterai_instance.login("invalid_username", "invalid_password")
    assert response["status"] != requests.codes.ok


def test_login_already_logged_in(authenticated_otterai_instance, capsys):
    assert (
        authenticated_otterai_instance._userid is not None
    ), "User should already be logged in"

    response = authenticated_otterai_instance.login(
        os.getenv("OTTERAI_USERNAME"), os.getenv("OTTERAI_PASSWORD")
    )

    assert response["status"] == requests.codes.ok
    assert response["data"]["userid"] == authenticated_otterai_instance._userid


# User ID Validation Tests
def test_is_userid_none(otterai_instance):
    assert otterai_instance._is_userid_invalid() is True


def test_is_userid_empty(otterai_instance):
    otterai_instance._userid = ""
    assert otterai_instance._is_userid_invalid() is True


def test_is_userid_valid(otterai_instance):
    otterai_instance._userid = "123456"
    assert otterai_instance._is_userid_invalid() is False


# Response Handling Tests
def test_handle_response_json(otterai_instance):
    mock_response = Mock()
    mock_response.status_code = requests.codes.ok
    mock_response.json.return_value = {"key": "value"}

    result = otterai_instance._handle_response(mock_response)
    assert result["status"] == requests.codes.ok
    assert result["data"] == {"key": "value"}


def test_handle_response_no_json(otterai_instance):
    mock_response = Mock()
    mock_response.status_code = requests.codes.ok
    mock_response.json.side_effect = ValueError  # Simulate no JSON
    mock_response.text = "Some plain text"

    result = otterai_instance._handle_response(mock_response)
    assert result["status"] == requests.codes.ok
    assert result["data"] == {}


def test_handle_response_with_data(otterai_instance):
    mock_response = Mock()
    mock_response.status_code = 201
    additional_data = {"extra": "info"}

    result = otterai_instance._handle_response(mock_response, data=additional_data)
    assert result["status"] == 201
    assert result["data"] == additional_data


# Authenticated Tests


def test_get_user(authenticated_otterai_instance):
    response = authenticated_otterai_instance.get_user()
    assert response["status"] == requests.codes.ok


def test_set_speech_title(authenticated_otterai_instance):
    otid = TEST_SPEECH_OTID

    response = authenticated_otterai_instance.get_speech(otid)

    title_after = f"Hello, World! {datetime.now()}"

    response = authenticated_otterai_instance.set_speech_title(
        otid=otid,
        title=title_after,
    )

    response = authenticated_otterai_instance.get_speech(otid)
    assert response["data"]["speech"]["title"] == title_after


def test_set_speech_title_invalid_userid(otterai_instance):
    otterai_instance._userid = None
    with pytest.raises(OtterAIException, match="userid is invalid"):
        otterai_instance.set_speech_title("otid", "New Title")


def test_get_speakers_success(authenticated_otterai_instance):
    result = authenticated_otterai_instance.get_speakers()
    assert result["status"] == requests.codes.ok
    assert "speakers" in result["data"]
    assert isinstance(result["data"]["speakers"], list)


def test_get_speakers_invalid_userid(otterai_instance):
    otterai_instance._userid = None
    with pytest.raises(OtterAIException, match="userid is invalid"):
        otterai_instance.get_speakers()


def test_get_speeches_invalid_userid(otterai_instance):
    otterai_instance._userid = None
    with pytest.raises(OtterAIException, match="userid is invalid"):
        otterai_instance.get_speeches()


def test_get_speeches_success(authenticated_otterai_instance):
    result = authenticated_otterai_instance.get_speeches()
    assert result["status"] == requests.codes.ok
    assert "speeches" in result["data"]
    assert isinstance(result["data"]["speeches"], list)


def test_get_speech_success(authenticated_otterai_instance):
    otid = TEST_SPEECH_OTID
    response = authenticated_otterai_instance.get_speech(otid)
    assert response["status"] == requests.codes.ok
    assert "speech" in response["data"]
    assert response["data"]["speech"]["otid"] == otid


def test_get_speech_invalid_userid(otterai_instance):
    otterai_instance._userid = None
    with pytest.raises(OtterAIException, match="userid is invalid"):
        otterai_instance.get_speech("invalid_otid")


def test_query_speech_success(authenticated_otterai_instance):
    otid = TEST_SPEECH_OTID
    query = "test query"
    response = authenticated_otterai_instance.query_speech(query, otid)
    assert response["status"] == requests.codes.ok
    assert "data" in response
    assert isinstance(response["data"], dict)


def test_get_notification_settings(authenticated_otterai_instance):
    response = authenticated_otterai_instance.get_notification_settings()
    assert response["status"] == requests.codes.ok
    assert "data" in response
    assert isinstance(response["data"], dict)


def test_list_groups_success(authenticated_otterai_instance):
    response = authenticated_otterai_instance.list_groups()
    assert response["status"] == requests.codes.ok
    assert "data" in response
    assert "groups" in response["data"]


def test_list_groups_invalid_userid(otterai_instance):
    otterai_instance._userid = None
    with pytest.raises(OtterAIException, match="userid is invalid"):
        otterai_instance.list_groups()


def test_get_folders_success(authenticated_otterai_instance):
    response = authenticated_otterai_instance.get_folders()
    assert "data" in response
    assert "folders" in response["data"]


def test_get_folders_invalid_userid(otterai_instance):
    otterai_instance._userid = None
    with pytest.raises(OtterAIException, match="userid is invalid"):
        otterai_instance.get_folders()


def test_download_speech_success(authenticated_otterai_instance):
    otid = TEST_SPEECH_OTID

    file_extension = "txt"

    file_base_name = os.path.join(DOWNLOAD_DIR, f"{otid}")
    file_full_name = f"{file_base_name}.{file_extension}"

    if os.path.exists(file_base_name):
        os.remove(file_base_name)

    response = authenticated_otterai_instance.download_speech(
        otid=otid,
        name=file_base_name,
        fileformat=file_extension,
    )

    print(f"Response: {response}")
    print(f"Expected file path: {file_base_name}")

    assert response["status"] == requests.codes.ok, "Download request failed"
    assert os.path.exists(file_full_name), "File not downloaded"

    os.remove(file_full_name)


def test_download_speech_invalid_userid(otterai_instance):
    otterai_instance._userid = None
    with pytest.raises(OtterAIException, match="userid is invalid"):
        otterai_instance.download_speech("invalid_otid", name="invalid_file")


def test_download_speech_failure(authenticated_otterai_instance, monkeypatch):
    otid = TEST_SPEECH_OTID
    file_extension = "txt"
    file_name = f"failed_download.{file_extension}"

    def mock_failed_request(*args, **kwargs):
        mock_response = Mock()
        mock_response.status_code = 500  # Simulate server error
        mock_response.ok = False
        return mock_response

    monkeypatch.setattr(
        authenticated_otterai_instance, "_make_request", mock_failed_request
    )

    with pytest.raises(
        OtterAIException,
        match=f"Got response status 500 when attempting to download {otid}",
    ):
        authenticated_otterai_instance.download_speech(
            otid=otid, name=file_name, fileformat=file_extension
        )
