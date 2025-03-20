from typing import Dict, List, Optional, Any, Union
from pydantic import BaseModel, Field, model_validator


class ChatMetadata(BaseModel):
    mode: Optional[str] = Field(None, description="Chat mode: 'chat' or 'business_analyst'")
    agent_id: Optional[str] = Field(None, alias="agentId")
    thoughts: Optional[str] = None
    reasoning: Optional[str] = None
    actions: Optional[List[Dict[str, str]]] = None
    follow_up_question: Optional[str] = Field(None, alias="followUpQuestion")


class ChatMessage(BaseModel):
    role: str = Field(..., description="Message role: 'user', 'assistant', or 'system'")
    content: str = Field(..., description="Message content")
    metadata: Optional[ChatMetadata] = None
    timestamp: Optional[int] = None


class ChatPayload(BaseModel):
    message: str = Field(..., description="The message to send")
    chat_history: Optional[List[ChatMessage]] = Field(None, alias="chatHistory")
    conversation_id: Optional[str] = Field(None, alias="conversationId")
    model: Optional[str] = None
    integrations: Optional[List[str]] = None
    use_all_integrations: Optional[bool] = Field(None, alias="useAllIntegrations")
    mode: Optional[str] = Field("business_analyst", description="Chat mode")
    agent_id: Optional[str] = Field(None, alias="agentId")
    external_user_identifier: Optional[str] = Field(None, alias="externalUserIdentifier")
    privacy_mode: Optional[bool] = Field(None, alias="privacyMode")
    passthrough_mode: Optional[bool] = Field(False, alias="passthroughMode")
    sources_enabled: Optional[str] = Field(None, alias="sourcesEnabled")
    
    @model_validator(mode='after')
    def validate_external_user_identifier(self) -> 'ChatPayload':
        """Validate that external_user_identifier is provided when passthrough_mode is True."""
        if self.passthrough_mode and not self.external_user_identifier:
            raise ValueError("external_user_identifier is required when passthrough_mode is True")
        return self


class ReasoningInfo(BaseModel):
    conclusions: List[str]
    recommendations: List[str]
    risks: List[str]
    confidence: float


class SupervisorState(BaseModel):
    current_phase: str = Field(..., alias="currentPhase")
    phase_history: List[str] = Field(..., alias="phaseHistory")
    reasoning: str


class WebSearchResult(BaseModel):
    title: str
    snippet: str
    url: Optional[str] = None


class IntegrationInfo(BaseModel):
    type: str
    relevance: float
    reason: str


class DataRetrievalMetadata(BaseModel):
    freshness: float
    completeness: float
    data_types: List[str] = Field(..., alias="dataTypes")
    sources: List[str]
    applied_filters: Optional[Dict[str, Any]] = Field(None, alias="appliedFilters")
    explanation: Optional[str] = None


class DataRetrieval(BaseModel):
    historical_data: List[Any] = Field(..., alias="historicalData")
    metadata: DataRetrievalMetadata


class Analysis(BaseModel):
    metrics: Dict[str, Any]
    trends: List[str]
    insights: List[str]


class SuadaResponse(BaseModel):
    answer: str
    thoughts: Optional[str] = None
    actions: Optional[List[Dict[str, str]]] = None
    follow_up_question: Optional[str] = Field(None, alias="followUpQuestion")
    reasoning: Optional[ReasoningInfo] = None
    supervisor_state: Optional[SupervisorState] = Field(None, alias="supervisorState")
    web_search_results: Optional[List[WebSearchResult]] = Field(None, alias="webSearchResults")
    integration_analysis: Optional[Dict[str, List[IntegrationInfo]]] = Field(None, alias="integrationAnalysis")
    data_retrieval: Optional[DataRetrieval] = Field(None, alias="dataRetrieval")
    analysis: Optional[Analysis] = None
    conversation_id: Optional[str] = Field(None, alias="conversationId")
    timestamp: int


class SuadaConfig(BaseModel):
    api_key: str = Field(..., alias="apiKey")
    base_url: Optional[str] = Field("https://suada.ai/api/public", alias="baseUrl") 