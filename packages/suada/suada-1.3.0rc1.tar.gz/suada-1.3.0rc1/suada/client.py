from typing import Dict, Optional, Any
import requests
from langchain.tools import BaseTool

from .types import (
    ChatPayload,
    SuadaConfig,
    SuadaResponse,
)


class Suada:
    """
    Suada API client for Python.
    
    This client provides access to Suada's Business Analyst API, allowing you to
    integrate Suada's powerful business analysis capabilities into your applications.
    """

    def __init__(self, config: SuadaConfig):
        """
        Initialize the Suada client.

        Args:
            config: SuadaConfig object containing API key and optional base URL
        """
        self.base_url = config.base_url.rstrip("/")
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {config.api_key}",
            "Content-Type": "application/json",
        })

    def _format_response(self, response: SuadaResponse) -> str:
        """
        Format the API response into a string format that can be used by LangChain agents.

        Args:
            response: SuadaResponse object containing the API response

        Returns:
            Formatted string containing the response with XML-like tags
        """
        parts = []

        # Add metrics if available
        if response.analysis and response.analysis.metrics:
            metrics_str = "\n".join(f"{k}: {v}" for k, v in response.analysis.metrics.items())
            parts.append(f"<metrics>{metrics_str}</metrics>")

        # Add insights if available
        if response.analysis and response.analysis.insights:
            insights_str = "\n".join(response.analysis.insights)
            parts.append(f"<insights>{insights_str}</insights>")

        # Add recommendations if available
        if response.reasoning and response.reasoning.recommendations:
            recommendations_str = "\n".join(response.reasoning.recommendations)
            parts.append(f"<recommendations>{recommendations_str}</recommendations>")

        # Add risks if available
        if response.reasoning and response.reasoning.risks:
            risks_str = "\n".join(response.reasoning.risks)
            parts.append(f"<risks>{risks_str}</risks>")

        # Add reasoning if available
        if response.supervisor_state and response.supervisor_state.reasoning:
            parts.append(f"<reasoning>{response.supervisor_state.reasoning}</reasoning>")

        # Add the main response
        parts.append(f"<response>{response.answer}</response>")

        return "\n\n".join(parts)

    def chat(self, payload: ChatPayload) -> str:
        """
        Send a chat message to Suada's API.

        Args:
            payload: ChatPayload object containing the message and optional parameters

        Returns:
            Formatted string containing the response

        Raises:
            requests.exceptions.RequestException: If the API request fails
        """
        try:
            response = self.session.post(
                f"{self.base_url}/chat",
                json=payload.model_dump(by_alias=True)
            )
            response.raise_for_status()
            suada_response = SuadaResponse.model_validate(response.json())
            return self._format_response(suada_response)
        except requests.exceptions.RequestException as e:
            if hasattr(e.response, 'json'):
                error_data = e.response.json()
                error_message = error_data.get('error', str(e))
            else:
                error_message = str(e)
            raise Exception(f"Suada API Error: {error_message}") from e

    def create_tool(
        self,
        name: Optional[str] = None,
        description: Optional[str] = None,
        external_user_identifier: Optional[str] = None,
        passthrough_mode: bool = True,
        sources_enabled: Optional[str] = 'external'
    ) -> BaseTool:
        """
        Create a LangChain tool that can be used in agents.

        Args:
            name: Optional tool name
            description: Optional tool description
            external_user_identifier: Optional user identifier. Required if passthrough_mode is True.
            passthrough_mode: Whether to pass messages directly to the LLM. Defaults to False.
            sources_enabled: Optional sources to enable. Defaults to 'external'.
        Returns:
            LangChain BaseTool instance
            
        Raises:
            ValueError: If passthrough_mode is True and external_user_identifier is not provided
        """
        if passthrough_mode and not external_user_identifier:
            raise ValueError("external_user_identifier is required when passthrough_mode is True")

        tool_name = name or "suada"
        tool_description = description or "A tool to get business insights and analysis from Suada AI"

        class SuadaTool(BaseTool):
            name: str = tool_name
            description: str = tool_description
            client: Suada = self
            user_id: Optional[str] = external_user_identifier
            is_passthrough_mode: bool = passthrough_mode

            def _run(self, query: str) -> str:
                payload = ChatPayload(
                    message=query,
                    external_user_identifier=self.user_id,
                    mode="business_analyst",
                    passthrough_mode=self.is_passthrough_mode,
                    sources_enabled=sources_enabled
                )
                return self.client.chat(payload)

            async def _arun(self, query: str) -> str:
                return self._run(query)

        return SuadaTool() 