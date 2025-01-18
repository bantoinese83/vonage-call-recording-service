# Vonage Call Recording Service

A simple call recording service using the Vonage Voice API, FastAPI, and SQLModel. This service allows users to answer calls, handle call events, record calls, and manage recordings. It also includes user authentication and a dashboard for viewing call statistics.

## Features

- User authentication (sign up, login, get current user)
- Answer incoming calls and return NCCO actions
- Handle call events and update call states
- Record calls and store recordings
- Retrieve a list of recordings with search, pagination, and limit parameters
- Dashboard to view call statistics (total duration, total recordings, success rate, average duration)

## Requirements

- Python 3.8+
- FastAPI
- SQLModel
- SQLAlchemy
- Vonage
- Loguru
- Halo
- Googletrans
- SpeechRecognition
- Boto3
- Pydantic
- Uvicorn

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/bantoinese83/vonage-call-recording-service.git
    cd vonage-call-recording-service
    ```

2. Create a virtual environment and activate it:

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Set up environment variables:

    Create a `.env` file in the root directory and add the following variables:

    ```env
    VONAGE_API_KEY=your_vonage_api_key
    VONAGE_API_SECRET=your_vonage_api_secret
    VONAGE_NUMBER=your_vonage_number
    AWS_ACCESS_KEY=your_aws_access_key
    AWS_SECRET_KEY=your_aws_secret_key
    AWS_BUCKET_NAME=your_aws_bucket_name
    ```

5. Initialize the database:

    ```bash
    python -m app.database
    ```

## Running the Application

1. Start the FastAPI application:

    ```bash
    uvicorn main:app --reload
    ```

2. The application will be available at `http://127.0.0.1:8000`.

## API Endpoints

### Authentication

- **Sign Up**: `POST /api/v1/auth/signup`
- **Login**: `POST /api/v1/auth/login`
- **Get Current User**: `GET /api/v1/auth/user`

### Calls

- **Answer Call**: `POST /api/v1/calls/answer`
- **Handle Call Event**: `POST /api/v1/calls/events`
- **Handle Recording Event**: `POST /api/v1/calls/recordings`

### Recordings

- **Get Recordings**: `GET /api/v1/recordings/list`
- **Create Recording**: `POST /api/v1/recordings/create`

### Dashboard

- **Get Dashboard Data**: `GET /api/v1/dashboard/data`

## Testing

1. Run the tests using pytest:

    ```bash
    pytest
    ```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.