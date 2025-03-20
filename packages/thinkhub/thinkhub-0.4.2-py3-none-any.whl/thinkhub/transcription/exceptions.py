"""
Define custom exception classes specific to the transcription service.

These exceptions handle various error scenarios, such as missing credentials,
invalid file paths, and client initialization failures, providing a structured
way to manage errors in the transcription process.
"""

from thinkhub.exceptions import BaseServiceError


class TranscriptionServiceError(BaseServiceError):
    """Base exception for transcription service related errors."""

    pass


class MissingGoogleCredentialsError(TranscriptionServiceError):
    """
    Raised when the GOOGLE_APPLICATION_CREDENTIALS environment variable is missing.

    This environment variable is required to authenticate with the Google Speech API.
    """

    pass


class InvalidGoogleCredentialsPathError(TranscriptionServiceError):
    """
    Raised when the file specified by GOOGLE_APPLICATION_CREDENTIALS does not exist.

    This could be due to a typo in the path or the file being deleted.
    """

    pass


class ClientInitializationError(TranscriptionServiceError):
    """Raised when the Google Speech client fails to initialize."""

    pass


class AudioFileNotFoundError(TranscriptionServiceError):
    """Raised when the audio file to transcribe is not found."""

    pass


class TranscriptionJobError(TranscriptionServiceError):
    """Raised for errors that occur during the transcription job."""

    pass


class MissingAPIKeyError(TranscriptionServiceError):
    """Raised when the API KEY environment variable is missing."""

    pass
