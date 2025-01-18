import os
import pytest
from unittest.mock import patch, MagicMock
from app.aws_setup import upload_file_to_s3

@pytest.fixture
def mock_s3_client():
    with patch("app.aws_setup.s3_client") as mock:
        yield mock

def test_upload_file_to_s3_success(mock_s3_client):
    mock_s3_client.upload_file.return_value = None
    file_path = "test_file.txt"
    bucket_name = "test_bucket"
    s3_file_name = "test_file_s3.txt"

    with open(file_path, "w") as f:
        f.write("test content")

    result = upload_file_to_s3(file_path, bucket_name, s3_file_name)
    assert result == f"https://{bucket_name}.s3.amazonaws.com/{s3_file_name}"

    os.remove(file_path)

def test_upload_file_to_s3_file_not_found(mock_s3_client):
    mock_s3_client.upload_file.side_effect = FileNotFoundError
    file_path = "non_existent_file.txt"
    bucket_name = "test_bucket"
    s3_file_name = "test_file_s3.txt"

    with pytest.raises(FileNotFoundError):
        upload_file_to_s3(file_path, bucket_name, s3_file_name)

def test_upload_file_to_s3_no_credentials(mock_s3_client):
    mock_s3_client.upload_file.side_effect = Exception("NoCredentialsError")
    file_path = "test_file.txt"
    bucket_name = "test_bucket"
    s3_file_name = "test_file_s3.txt"

    with open(file_path, "w") as f:
        f.write("test content")

    with pytest.raises(Exception, match="NoCredentialsError"):
        upload_file_to_s3(file_path, bucket_name, s3_file_name)

    os.remove(file_path)

def test_upload_file_to_s3_client_error(mock_s3_client):
    mock_s3_client.upload_file.side_effect = Exception("ClientError")
    file_path = "test_file.txt"
    bucket_name = "test_bucket"
    s3_file_name = "test_file_s3.txt"

    with open(file_path, "w") as f:
        f.write("test content")

    with pytest.raises(Exception, match="ClientError"):
        upload_file_to_s3(file_path, bucket_name, s3_file_name)

    os.remove(file_path)

def test_upload_file_to_s3_unexpected_error(mock_s3_client):
    mock_s3_client.upload_file.side_effect = Exception("UnexpectedError")
    file_path = "test_file.txt"
    bucket_name = "test_bucket"
    s3_file_name = "test_file_s3.txt"

    with open(file_path, "w") as f:
        f.write("test content")

    with pytest.raises(Exception, match="UnexpectedError"):
        upload_file_to_s3(file_path, bucket_name, s3_file_name)

    os.remove(file_path)
