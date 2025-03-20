import xml.etree.ElementTree as ET

import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder
from tenacity import retry, retry_if_exception, stop_after_attempt, wait_exponential


class OtterAIException(Exception):
    pass


class OtterAI:
    API_BASE_URL = "https://otter.ai/forward/api/v1/"
    S3_BASE_URL = "https://s3.us-west-2.amazonaws.com/"

    def __init__(self):
        self._session = requests.Session()
        self._userid = None
        self._cookies = None

    def _is_userid_invalid(self):
        return not self._userid

    def _handle_response(self, response, data=None):
        if data:
            return {"status": response.status_code, "data": data}
        try:
            return {"status": response.status_code, "data": response.json()}
        except ValueError:
            return {"status": response.status_code, "data": {}}

    def is_retryable_exception(exception):
        """Defines which exceptions should trigger a retry"""
        if isinstance(exception, requests.exceptions.RequestException):
            return True
        if hasattr(exception, "response") and exception.response is not None:
            return exception.response.status_code in [429, 500, 502, 503, 504]
        return False

    @retry(
        retry=retry_if_exception(is_retryable_exception),
        wait=wait_exponential(multiplier=2, min=2, max=60),  # Increased wait time
        stop=stop_after_attempt(7),  # More retry attempts
    )
    def _make_request(self, method, url, **kwargs):
        """Handles API requests with retries"""
        try:
            response = self._session.request(method, url, **kwargs)

            if response.status_code == 429:  # Handle rate limits dynamically
                retry_after = response.headers.get("Retry-After")
                if retry_after:
                    wait_time = int(retry_after) + 1  # Convert to int and add buffer
                    print(f"Rate limited. Retrying in {wait_time} seconds...")
                    time.sleep(wait_time)
                else:
                    print(f"Rate limited. Applying exponential backoff...")
                response.raise_for_status()

            elif response.status_code in [500, 502, 503, 504]:
                print(f"Retrying {url} due to status {response.status_code}")
                response.raise_for_status()

            return response

        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}, URL: {url}")
            raise

    def login(self, username, password):
        # Avoid logging in again if already authenticated
        if self._userid:
            print("Already logged in, skipping login request.")
            return {"status": requests.codes.ok, "data": {"userid": self._userid}}

        auth_url = OtterAI.API_BASE_URL + "login"
        payload = {"username": username}
        self._session.auth = (username, password)

        try:
            response = self._make_request("GET", auth_url, params=payload)

            if response.status_code == requests.codes.ok:
                self._userid = response.json().get("userid")
                self._cookies = response.cookies.get_dict()
                print("Login successful!")
            else:
                print(
                    f"Login failed with status {response.status_code}: {response.text}"
                )

            return self._handle_response(response)

        except requests.exceptions.RequestException as e:
            print(f"Login failed due to request exception: {e}")
            return {"status": 500, "data": {"error": str(e)}}

    def get_user(self):
        user_url = OtterAI.API_BASE_URL + "user"
        response = self._make_request("GET", user_url)
        return self._handle_response(response)

    def get_speakers(self):
        speakers_url = OtterAI.API_BASE_URL + "speakers"
        if self._is_userid_invalid():
            raise OtterAIException("userid is invalid")
        payload = {"userid": self._userid}
        response = self._make_request("GET", speakers_url, params=payload)

        return self._handle_response(response)

    def get_speeches(self, folder=0, page_size=45, source="owned"):
        speeches_url = OtterAI.API_BASE_URL + "speeches"
        if self._is_userid_invalid():
            raise OtterAIException("userid is invalid")
        payload = {
            "userid": self._userid,
            "folder": folder,
            "page_size": page_size,
            "source": source,
        }
        response = self._make_request("GET", speeches_url, params=payload)

        return self._handle_response(response)

    def get_speech(self, otid):
        speech_url = OtterAI.API_BASE_URL + "speech"
        if self._is_userid_invalid():
            raise OtterAIException("userid is invalid")
        payload = {"userid": self._userid, "otid": otid}
        response = self._make_request("GET", speech_url, params=payload)

        return self._handle_response(response)

    def query_speech(self, query, otid, size=500):
        query_speech_url = OtterAI.API_BASE_URL + "advanced_search"
        payload = {"query": query, "size": size, "otid": otid}
        response = self._make_request("GET", query_speech_url, params=payload)

        return self._handle_response(response)

    def upload_speech(self, file_name, content_type="audio/mp4"):
        speech_upload_params_url = OtterAI.API_BASE_URL + "speech_upload_params"
        speech_upload_prod_url = OtterAI.S3_BASE_URL + "speech-upload-prod"
        finish_speech_upload = OtterAI.API_BASE_URL + "finish_speech_upload"

        if self._is_userid_invalid():
            raise OtterAIException("userid is invalid")

        # First grab upload params (aws data)
        payload = {"userid": self._userid}
        response = self._make_request("GET", speech_upload_params_url, params=payload)

        if response.status_code != requests.codes.ok:
            return self._handle_response(response)

        response_json = response.json()
        params_data = response_json["data"]

        # Send options (precondition) request
        prep_req = requests.Request("OPTIONS", speech_upload_prod_url).prepare()
        prep_req.headers["Accept"] = "*/*"
        prep_req.headers["Connection"] = "keep-alive"
        prep_req.headers["Origin"] = "https://otter.ai"
        prep_req.headers["Referer"] = "https://otter.ai/"
        prep_req.headers["Access-Control-Request-Method"] = "POST"
        self._session.send(prep_req)

        # TODO: test for large files (this should stream)
        fields = {}
        params_data["success_action_status"] = str(params_data["success_action_status"])
        del params_data["form_action"]
        fields.update(params_data)
        fields["file"] = (file_name, open(file_name, mode="rb"), content_type)
        multipart_data = MultipartEncoder(fields=fields)
        response = self._make_request(
            "POST",
            speech_upload_prod_url,
            data=multipart_data,
            headers={"Content-Type": multipart_data.content_type},
        )

        if response.status_code != 201:
            return self._handle_response(response)

        # Parse XML response
        xmltree = ET.ElementTree(ET.fromstring(response.text))
        xmlroot = xmltree.getroot()
        location = xmlroot[0].text
        bucket = xmlroot[1].text
        key = xmlroot[2].text

        # Call finish API
        payload = {
            "bucket": bucket,
            "key": key,
            "language": "en",
            "country": "us",
            "userid": self._userid,
        }
        response = self._make_request("GET", finish_speech_upload, params=payload)

        return self._handle_response(response)

    def download_speech(self, otid, name=None, fileformat="txt,pdf,mp3,docx,srt"):
        download_speech_url = OtterAI.API_BASE_URL + "bulk_export"
        if self._is_userid_invalid():
            raise OtterAIException("userid is invalid")
        payload = {"userid": self._userid}
        data = {"formats": fileformat, "speech_otid_list": [otid]}
        headers = {
            "x-csrftoken": self._cookies["csrftoken"],
            "referer": "https://otter.ai/",
        }
        response = self._make_request(
            "POST", download_speech_url, params=payload, headers=headers, data=data
        )
        filename = (
            (name if not name == None else otid)
            + "."
            + ("zip" if "," in fileformat else fileformat)
        )
        if response.ok:
            with open(filename, "wb") as f:
                f.write(response.content)
        else:
            raise OtterAIException(
                f"Got response status {response.status_code} when attempting to download {otid}"
            )
        return self._handle_response(response, data={"filename": filename})

    def move_to_trash_bin(self, otid):
        move_to_trash_bin_url = OtterAI.API_BASE_URL + "move_to_trash_bin"
        if self._is_userid_invalid():
            raise OtterAIException("userid is invalid")
        payload = {"userid": self._userid}
        data = {"otid": otid}
        headers = {"x-csrftoken": self._cookies["csrftoken"]}
        response = self._make_request(
            "POST", move_to_trash_bin_url, params=payload, headers=headers, data=data
        )

        return self._handle_response(response)

    def create_speaker(self, speaker_name):
        create_speaker_url = OtterAI.API_BASE_URL + "create_speaker"
        if self._is_userid_invalid():
            raise OtterAIException("userid is invalid")
        payload = {"userid": self._userid}
        data = {"speaker_name": speaker_name}
        headers = {"x-csrftoken": self._cookies["csrftoken"]}
        response = self._make_request(
            "POST", create_speaker_url, params=payload, headers=headers, data=data
        )

        return self._handle_response(response)

    def get_notification_settings(self):
        notification_settings_url = OtterAI.API_BASE_URL + "get_notification_settings"
        response = self._make_request("GET", notification_settings_url)

        return self._handle_response(response)

    def list_groups(self):
        list_groups_url = OtterAI.API_BASE_URL + "list_groups"
        if self._is_userid_invalid():
            raise OtterAIException("userid is invalid")
        payload = {"userid": self._userid}
        response = self._make_request("GET", list_groups_url, params=payload)

        return self._handle_response(response)

    def get_folders(self):
        folders_url = OtterAI.API_BASE_URL + "folders"
        if self._is_userid_invalid():
            raise OtterAIException("userid is invalid")
        payload = {"userid": self._userid}
        response = self._make_request("GET", folders_url, params=payload)

        return self._handle_response(response)

    def speech_start(self):
        speech_start_uel = OtterAI.API_BASE_URL + "speech_start"
        ### TODO
        # In the browser a websocket session is opened
        # wss://ws.aisense.com/api/v2/client/speech?token=ey...
        # The speech_start endpoint returns the JWT token

    def stop_speech(self):
        speech_finish_url = OtterAI.API_BASE_URL + "speech_finish"

    def set_speech_title(self, otid, title):
        set_speech_title_url = OtterAI.API_BASE_URL + "set_speech_title"
        if self._is_userid_invalid():
            raise OtterAIException("userid is invalid")
        payload = {"userid": self._userid, "otid": otid, "title": title}
        response = self._make_request("GET", set_speech_title_url, params=payload)

        return self._handle_response(response)
