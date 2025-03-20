# otterai-py

Unofficial Python API for [otter.ai](http://otter.ai)

**Note:** This project is a fork of [gmchad/otterai-api](https://github.com/gmchad/otterai-api), as the original repository appears to be abandoned. Improvements and updates will be maintained here.

## Contents

-   [Installation](#installation)
-   [Setup](#setup)
-   [APIs](#apis)
    -   [User](#user)
    -   [Speeches](#speeches)
    -   [Speakers](#speakers)
    -   [Folders](#folders)
    -   [Groups](#groups)
    -   [Notifications](#notifications)
-   [Exceptions](#exceptions)
-   [Contribution](#contribution)

## Installation

Install via pip:

```bash
pip install .[dev]
```

or in a virtual environment:

```bash
python3 -m venv env
source env/bin/activate
pip install .[dev]
```

## Setup

```python
from otterai import OtterAI
otter = OtterAI()
otter.login('USERNAME', 'PASSWORD')
```

## APIs

### User

Get user-specific data:

```python
otter.get_user()
```

### Speeches

Get all speeches.

**Optional parameters**: `folder`, `page_size`, `source`

```python
otter.get_speeches()
```

Get a speech by ID:

```python
otter.get_speech(OTID)
```

Query a speech:

```python
otter.query_speech(QUERY, OTID)
```

Upload a speech.

**Optional parameters**: `content_type` (default: `audio/mp4`)

```python
otter.upload_speech(FILE_NAME)
```

Download a speech.

**Optional parameters**: `filename` (default: `id`), `format` (default: all available formats (`txt,pdf,mp3,docx,srt`) as a zip file)

```python
otter.download_speech(OTID, FILE_NAME)
```

Move a speech to the trash:

```python
otter.move_to_trash_bin(OTID)
```

Set speech title:

```python
otter.set_speech_title(OTID, TITLE)
```

#### TODO

-   Start a live speech
-   Stop a live speech
-   Assign a speaker to a speech transcript

### Speakers

Get all speakers:

```python
otter.get_speakers()
```

Create a speaker:

```python
otter.create_speaker(SPEAKER_NAME)
```

### Folders

Get all folders:

```python
otter.get_folders()
```

### Groups

Get all groups:

```python
otter.list_groups()
```

### Notifications

Get notification settings:

```python
otter.get_notification_settings()
```

## Exceptions

```python
from otterai import OtterAIException

try:
    ...
except OtterAIException as e:
    ...
```

## Contribution

To contribute to this project, follow these steps:

1. Create a `.env` file in the root directory with the following content:

    ```plaintext
    OTTERAI_USERNAME=""
    OTTERAI_PASSWORD=""
    TEST_OTTERAI_SPEECH_OTID=""
    ```

    - Replace `OTTERAI_USERNAME` and `OTTERAI_PASSWORD` with your Otter.ai credentials.
    - Replace `TEST_OTTERAI_SPEECH_OTID` with the ID of a speech you create on Otter.ai. This is required for the tests to pass.

2. To run the tests and the `main.py` file, execute the `run.sh` script:

    ```bash
    ./run.sh
    ```

3. Ensure all tests pass and make necessary updates to the tests if you modify or add functionality.

4. Submit a pull request with a clear description of your changes.
