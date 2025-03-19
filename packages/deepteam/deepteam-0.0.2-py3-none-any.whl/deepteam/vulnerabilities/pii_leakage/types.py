from enum import Enum
from typing import Literal


class PIILeakageType(Enum):
    DATABASE_ACCESS = "api and database access"
    DIRECT = "direct pii disclosure"
    SESSION_LEAK = "session pii leak"
    SOCIAL_MANIPULATION = "social engineering pii disclosure"


PIILeakageTypes = Literal[
    PIILeakageType.DATABASE_ACCESS.value,
    PIILeakageType.DIRECT.value,
    PIILeakageType.SESSION_LEAK.value,
    PIILeakageType.SOCIAL_MANIPULATION.value,
]

PIILeakageLiteral = Literal[
    "api and database access",
    "direct pii disclosure",
    "session pii leak",
    "social engineering pii disclosure",
]
