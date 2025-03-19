from enum import Enum
from typing import Literal


class MisinformationType(Enum):
    FACTUAL_ERRORS = "factual errors"
    UNSUPPORTED_CLAIMS = "unsupported claims"
    EXPERTISE_MISREPRESENTATION = "expertise misrepresentation"


MisinformationTypes = Literal[
    MisinformationType.FACTUAL_ERRORS.value,
    MisinformationType.UNSUPPORTED_CLAIMS.value,
    MisinformationType.EXPERTISE_MISREPRESENTATION.value,
]
