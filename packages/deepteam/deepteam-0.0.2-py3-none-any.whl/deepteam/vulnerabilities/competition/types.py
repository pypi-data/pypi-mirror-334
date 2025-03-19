from enum import Enum
from typing import Literal


class CompetitionType(Enum):
    COMPETITORS_MENTION = "competitors mention"
    MARKET_MANIPULATION = "market manipulation"
    DISCREDITATION = "discreditation"
    CONFIDENTIAL_STRATEGIES = "confidential strategies"


CompetitionTypes = Literal[
    CompetitionType.COMPETITORS_MENTION.value,
    CompetitionType.MARKET_MANIPULATION.value,
    CompetitionType.DISCREDITATION.value,
    CompetitionType.CONFIDENTIAL_STRATEGIES.value,
]
