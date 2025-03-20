import asyncio
from collections.abc import AsyncGenerator
from pathlib import Path
import secrets
from typing import Any
from unittest.mock import AsyncMock, Mock

import httpx
from pyfakefs.fake_filesystem import FakeFilesystem
import pytest
from pytest_mock import MockerFixture

from isubrip.data_structures import Episode, Movie, SubtitlesData
from isubrip.scrapers.scraper import Scraper

# Constants
TEST_DATA_DIR = Path(__file__).parent / "test_data"


# Auto-Use Fixtures
@pytest.fixture(autouse=True)
def reset_singletons() -> None:
    """Resets singleton instances between tests."""
    Scraper.reset_instances()

@pytest.fixture(autouse=True)
async def reset_event_loop() -> AsyncGenerator:
    """Provides event loop for async tests."""
    import isubrip.constants

    loop = asyncio.new_event_loop()
    isubrip.constants.EVENT_LOOP = loop
    yield
    loop.close()

# General Fixtures
@pytest.fixture
def temp_dir(fs: FakeFilesystem) -> Path:
    """Creates a temporary directory in the fake filesystem."""
    dir_path = Path(f"/tmp/{secrets.token_hex(5)}")
    fs.create_dir(dir_path)
    return dir_path

# HTTP and Network Mocking
@pytest.fixture
async def mock_http_client(mocker: MockerFixture) -> AsyncMock:
    """Mocks HTTP client for network requests."""
    mock_client = AsyncMock(spec=httpx.AsyncClient)
    mocker.patch("httpx.AsyncClient", return_value=mock_client)
    return mock_client

@pytest.fixture
def mock_session(mocker: MockerFixture) -> Mock:
    """Provides mocked HTTP session."""
    return mocker.patch("httpx.AsyncClient")

# Data Sample Fixtures
@pytest.fixture
def sample_movie() -> Movie:
    """Provides sample Movie instance."""
    return Movie(
        id="123",
        title="Test Movie",
        year=2023,
        language="en",
    )

@pytest.fixture
def sample_episode() -> Episode:
    """Provides sample Episode instance."""
    return Episode(
        id="456",
        show_title="Test Show",
        season=1,
        episode=1,
        title="Pilot",
        language="en",
    )

@pytest.fixture
def sample_subtitles() -> SubtitlesData:
    """Provides sample subtitles data."""
    # TODO: Load from test_data/sample_subtitles.srt
    return SubtitlesData(
        content="1\n00:00:01,000 --> 00:00:02,000\nTest subtitle\n",
        language="en",
        format="srt",
    )

# Utility Functions
def load_test_data(file_name: str, sub_directory: str | None = None) -> bytes:
    """Loads test data from file."""
    file_path = TEST_DATA_DIR / (sub_directory or "") / file_name
    # TODO: Add test data files
    with open(file_path, "rb") as f:
        return f.read()

def mock_external_api_call(mocker: MockerFixture, url: str, response_data: dict[str, Any],
                          status_code: int = 200) -> Mock:
    """Helper to mock external API calls."""
    mock_response = Mock()
    mock_response.status_code = status_code
    mock_response.json.return_value = response_data
    mock_get = mocker.patch("httpx.AsyncClient.get", return_value=mock_response)
    return mock_get
