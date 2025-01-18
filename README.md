# 📞 Vonage Call Recording Service 🎙️

[![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/bantoinese83/vonage-call-recording-service/blob/main/LICENSE)
[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat&logo=fastapi)](https://fastapi.tiangolo.com/)
[![SQLModel](https://img.shields.io/badge/SQLModel-9370DB?style=flat&logo=database)](https://sqlmodel.tiangolo.com/)
[![Vonage](https://img.shields.io/badge/Vonage-E34C26?style=flat&logo=vonage)](https://developer.vonage.com/)
[![GitHub Stars](https://img.shields.io/github/stars/bantoinese83/vonage-call-recording-service?style=social)](https://github.com/bantoinese83/vonage-call-recording-service/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/bantoinese83/vonage-call-recording-service?style=social)](https://github.com/bantoinese83/vonage-call-recording-service/network/members)
[![GitHub Issues](https://img.shields.io/github/issues/bantoinese83/vonage-call-recording-service)](https://github.com/bantoinese83/vonage-call-recording-service/issues)
[![GitHub Pull Requests](https://img.shields.io/github/pulls/bantoinese83/vonage-call-recording-service)](https://github.com/bantoinese83/vonage-call-recording-service/pulls)

A robust call recording service built with **Vonage Voice API**, **FastAPI**, and **SQLModel**. This service not only handles basic call functionalities like answering calls and tracking call events but also dives deep into recording and managing those recordings. It also features user authentication and a detailed dashboard for analytics.

<br>

## ✨ Features

- 🔑 **User Authentication**: Secure sign-up, login, and current user retrieval.
- 📞 **Call Handling**: Answer incoming calls using Vonage NCCOs.
- 🔄 **Event Tracking**: Manage and update call states based on Vonage call events.
- 💾 **Call Recording**: Record calls and store recordings.
- 🗂️ **Recording Management**: List recordings with search, pagination, and limit options.
- 📊 **Dashboard**: View key call statistics like total duration, total recordings, success rate, and average duration.
- 🌐 **Cloud Storage**: Seamless integration with AWS S3 for storing recordings.
- 💬 **Speech-to-Text** : Transcribe audio recordings using Googletrans and SpeechRecognition
- 📝 **Multi Language Support** : Supports various language using google translate

<br>

## 🛠️ Requirements

-   **Python**: 3.8+
-   **Frameworks**:
    -   [FastAPI](https://fastapi.tiangolo.com/)
    -   [SQLModel](https://sqlmodel.tiangolo.com/)
    -   [SQLAlchemy](https://www.sqlalchemy.org/)
-   **Vonage**: [Vonage Python SDK](https://github.com/Vonage/vonage-python-sdk)
-   **Logging**: [Loguru](https://loguru.readthedocs.io/en/stable/)
-  **Progress**: [Halo](https://github.com/manrajgrover/halo)
-  **Speech to Text**: [SpeechRecognition](https://github.com/Uberi/speech_recognition)
-  **Language Translation** : [Googletrans](https://github.com/ssut/py-googletrans)
-   **AWS SDK**: [Boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)
-   **Validation**: [Pydantic](https://pydantic-docs.helpmanual.io/)
-   **Server**: [Uvicorn](https://www.uvicorn.org/)

<br>

## 🚀 Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/bantoinese83/vonage-call-recording-service.git
    cd vonage-call-recording-service
    ```

2.  **Create a virtual environment and activate it:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up environment variables:**

    Create a `.env` file in the root directory and add the following variables:

    ```env
    VONAGE_API_KEY=your_vonage_api_key
    VONAGE_API_SECRET=your_vonage_api_secret
    VONAGE_NUMBER=your_vonage_number
    AWS_ACCESS_KEY=your_aws_access_key
    AWS_SECRET_KEY=your_aws_secret_key
    AWS_BUCKET_NAME=your_aws_bucket_name
    ```
    
    
    > **Note** : AWS credentials and bucket name are needed if you want to store the recordings in AWS S3 bucket.

5.  **Initialize the database:**

    ```bash
    python -m app.database
    ```

<br>

## 🏃 Running the Application

1.  **Start the FastAPI application:**

    ```bash
    uvicorn main:app --reload
    ```

2.  **Access the API:**

    The application will be available at `http://127.0.0.1:8000`.

<br>

## 🗂️ API Endpoints

### Authentication

-   **Sign Up**: `POST /api/v1/auth/signup`
-   **Login**: `POST /api/v1/auth/login`
-   **Get Current User**: `GET /api/v1/auth/user`

### Calls

-   **Answer Call**: `POST /api/v1/calls/answer`
-   **Handle Call Event**: `POST /api/v1/calls/events`
-  **Handle Recording Event** : `POST /api/v1/calls/recordings`

### Recordings

-   **Get Recordings**: `GET /api/v1/recordings/list`
- **Create Recording** : `POST /api/v1/recordings/create`

### Dashboard

-   **Get Dashboard Data**: `GET /api/v1/dashboard/data`

<br>

## 🧪 Testing

1.  **Run tests with pytest:**

    ```bash
    pytest
    ```

<br>

## 📜 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

<br>

---
Made with ❤️ by [bantoinese83](https://github.com/bantoinese83)