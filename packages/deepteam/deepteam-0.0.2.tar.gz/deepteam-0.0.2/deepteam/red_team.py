from typing import List

from deepeval.utils import get_or_create_event_loop

from deepteam.vulnerabilities import BaseVulnerability
from deepteam.attacks import BaseAttack
from deepteam.attacks.multi_turn.types import CallbackType
from deepteam.red_teamer import RedTeamer


def red_team(
    model_callback: CallbackType,
    vulnerabilities: List[BaseVulnerability],
    attacks: List[BaseAttack],
    attacks_per_vulnerability_type: int = 1,
    ignore_errors: bool = False,
    run_async: bool = True,
    max_concurrent: int = 10,
):
    red_teamer = RedTeamer(
        async_mode=run_async,
        max_concurrent=max_concurrent,
    )
    if run_async:
        loop = get_or_create_event_loop()
        loop.run_until_complete(
            red_teamer.a_red_team(
                model_callback=model_callback,
                vulnerabilities=vulnerabilities,
                attacks=attacks,
                attacks_per_vulnerability_type=attacks_per_vulnerability_type,
                ignore_errors=ignore_errors,
            )
        )
        risk_assessment = red_teamer.risk_assessment
    else:
        risk_assessment = red_teamer.red_team(
            model_callback=model_callback,
            vulnerabilities=vulnerabilities,
            attacks=attacks,
            attacks_per_vulnerability_type=attacks_per_vulnerability_type,
            ignore_errors=ignore_errors,
        )
    return risk_assessment
