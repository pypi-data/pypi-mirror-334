"""Tests for the Suada client module."""
import pytest
from suada.client import Suada
from suada.types import SuadaConfig

def test_client_initialization():
    """Test that the client can be initialized."""
    config = SuadaConfig(apiKey="test-key")
    client = Suada(config=config)
    assert isinstance(client, Suada)
    assert client.session.headers["Authorization"] == "Bearer test-key" 