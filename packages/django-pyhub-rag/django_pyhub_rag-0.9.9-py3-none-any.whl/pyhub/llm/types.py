from dataclasses import dataclass, field
from decimal import Decimal
from typing import Any, Literal, TypeAlias, Union

from anthropic.types import ModelParam as AnthropicChatModel
from openai.types import ChatModel as OpenAIChatModel
from pydantic import BaseModel
from typing_extensions import Optional

#
# Embedding
#

OpenAIEmbeddingModel: TypeAlias = Literal[
    "text-embedding-ada-002",  # 1536 차원
    "text-embedding-3-small",  # 1536 차원
    "text-embedding-3-large",  # 3072 차원
]

# https://console.upstage.ai/docs/capabilities/embeddings
UpstageEmbeddingModel: TypeAlias = Literal[
    "embedding-query",  # 검색어 목적 (4096차원)
    "embedding-passage",  # 문서의 일부, 문장 또는 긴 텍스트 목적 (4096차원)
]


OllamaEmbeddingModel: TypeAlias = Union[
    Literal[
        "nomic-embed-text",  # 768 차원
        "avr/sfr-embedding-mistral",  # 4096 차원
    ],
    str,
]

# https://cloud.google.com/vertex-ai/generative-ai/docs/embeddings/get-text-embeddings?hl=ko
GoogleEmbeddingModel: TypeAlias = Literal["text-embedding-004"]  # 768 차원

LLMEmbeddingModel = Union[OpenAIEmbeddingModel, UpstageEmbeddingModel, OllamaEmbeddingModel, GoogleEmbeddingModel]


#
# Chat
#

OpenAIChatModel  # noqa

AnthropicChatModel  # noqa

# https://console.upstage.ai/docs/capabilities/chat
UpstageChatModel: TypeAlias = Union[
    Literal[
        "solar-pro",
        "solar-mini",
    ]
]

OllamaChatModel: TypeAlias = Union[
    Literal[
        # tools, 70b : https://ollama.com/library/llama3.3
        "llama3.3",
        # tools, 1b, 3b : https://ollama.com/library/llama3.2
        "llama3.2",
        # tools, 8b, 70b, 405b : https://ollama.com/library/llama3.1
        "llama3.1",
        # tools, 7b : https://ollama.com/library/mistral
        "mistral",
        # tools, 0.5b, 1.5b, 7b, 72b : https://ollama.com/library/qwen2
        "qwen2",
    ],
    str,
]

# https://ai.google.dev/gemini-api/docs/models/gemini?hl=ko
GoogleChatModel: TypeAlias = Union[
    Literal[
        "gemini-2.0-flash",
        "gemini-2.0-flash-lite",
        "gemini-1.5-flash",
        "gemini-1.5-flash-8b",
        "gemini-1.5-pro",
    ],
]


LLMChatModel: TypeAlias = Union[OpenAIChatModel, AnthropicChatModel, UpstageChatModel, GoogleChatModel]


#
# Groundedness Check
#

# https://console.upstage.ai/docs/capabilities/groundedness-check#available-models
UpstageGroundednessCheckModel: TypeAlias = Literal["groundedness-check",]


#
# Types
#


@dataclass
class GroundednessCheck:
    is_grounded: Optional[bool] = None  # grounded (True), notGrounded (False), notSure (None)
    usage: Optional["Usage"] = None

    def __bool__(self):
        return self.is_grounded


class Message(BaseModel):
    role: Literal["system", "user", "assistant", "function"]
    content: str


@dataclass
class Usage:
    input: int = 0
    output: int = 0

    def __add__(self, other):
        if isinstance(other, Usage):
            return Usage(input=self.input + other.input, output=self.output + other.output)
        return NotImplemented


@dataclass
class Price:
    input_usd: Optional[Decimal] = None
    output_usd: Optional[Decimal] = None
    usd: Optional[Decimal] = None
    krw: Optional[Decimal] = None
    rate_usd: int = 1500

    def __post_init__(self):
        self.input_usd = self.input_usd or Decimal("0")
        self.output_usd = self.output_usd or Decimal("0")

        if not isinstance(self.input_usd, Decimal):
            self.input_usd = Decimal(str(self.input_usd))
        if not isinstance(self.output_usd, Decimal):
            self.output_usd = Decimal(str(self.output_usd))
        if self.usd is not None and not isinstance(self.usd, Decimal):
            self.usd = Decimal(str(self.usd))
        if self.krw is not None and not isinstance(self.krw, Decimal):
            self.krw = Decimal(str(self.krw))

        if self.usd is None:
            self.usd = self.input_usd + self.output_usd

        if self.krw is None:
            self.krw = self.usd * Decimal(self.rate_usd)


@dataclass
class Reply:
    text: str = ""
    usage: Optional[Usage] = None

    def __str__(self) -> str:
        return self.text

    def __format__(self, format_spec: str) -> str:
        return format(self.text, format_spec)


@dataclass
class ChainReply:
    values: dict[str, Any] = field(default_factory=dict)
    reply_list: list[Reply] = field(default_factory=list)

    def __len__(self) -> int:
        return len(self.reply_list)

    @property
    def text(self) -> str:
        try:
            return self.reply_list[-1].text
        except IndexError:
            return ""

    @property
    def usage(self) -> Optional[Usage]:
        try:
            return self.reply_list[-1].usage
        except IndexError:
            return None

    def __getitem__(self, key) -> Any:
        return self.values.get(key)


@dataclass
class Embed:
    array: list[float]  # noqa
    usage: Optional[Usage] = None

    def __iter__(self):
        return iter(self.array)

    def __len__(self):
        return len(self.array)

    def __getitem__(self, index):
        return self.array[index]

    def __str__(self):
        return str(self.array)


@dataclass
class EmbedList:
    arrays: list[Embed]  # noqa
    usage: Optional[Usage] = None

    def __iter__(self):
        return iter(self.arrays)

    def __len__(self):
        return len(self.arrays)

    def __getitem__(self, index):
        return self.arrays[index]

    def __str__(self):
        return str(self.arrays)
