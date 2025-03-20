"""Tests for validation in the Suada client module."""
import pytest
from pydantic import ValidationError
from suada.client import Suada
from suada.types import SuadaConfig, ChatPayload

def test_external_user_identifier_validation_in_payload():
    """Test that external_user_identifier validation works in ChatPayload."""
    # Valid case: No external_user_identifier is fine when passthrough_mode is False
    payload = ChatPayload(message="Test message")
    assert payload.external_user_identifier is None
    assert payload.passthrough_mode is False

    # Valid case: With external_user_identifier and passthrough_mode
    payload = ChatPayload(
        message="Test message",
        externalUserIdentifier="user-123",
        passthroughMode=True,
        sourcesEnabled="external"
    )
    assert payload.external_user_identifier == "user-123"
    assert payload.passthrough_mode is True
    assert payload.sources_enabled == "external"

    # Invalid case: passthrough_mode True without external_user_identifier
    with pytest.raises(ValidationError) as exc_info:
        ChatPayload(
            message="Test message",
            passthroughMode=True
        )
    assert "external_user_identifier is required when passthrough_mode is True" in str(exc_info.value)

def test_external_user_identifier_validation_in_tool():
    """Test that external_user_identifier validation works in create_tool."""
    client = Suada(SuadaConfig(apiKey="fake-key"))
    
    # Valid case: With external_user_identifier
    tool = client.create_tool(
        external_user_identifier="user-123"  # passthrough_mode defaults to True
    )
    assert tool.user_id == "user-123"
    assert tool.is_passthrough_mode is True

    # Valid case: With passthrough_mode False
    tool = client.create_tool(
        passthrough_mode=False
    )
    assert tool.user_id is None
    assert tool.is_passthrough_mode is False

    # Invalid case: passthrough_mode True (default) without external_user_identifier
    with pytest.raises(ValueError) as exc_info:
        client.create_tool()  # passthrough_mode defaults to True
    assert "external_user_identifier is required when passthrough_mode is True" in str(exc_info.value)