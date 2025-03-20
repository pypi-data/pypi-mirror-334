from pathlib import Path

import yaml
from pydantic.dataclasses import dataclass as pydantic_dataclass

__all__ = ['load_args_for_reaction_exploration']


@pydantic_dataclass
class MleKindDict:
    metal: str
    leaving: str
    entering: str


@pydantic_dataclass
class YamlDict:
    mle_kinds: list[MleKindDict]


def load_args_for_reaction_exploration(
        filepath: str | Path
        ) -> list[tuple[str, str, str]]:
    """Parse the input file for `translate_to_graph`."""
    filepath = Path(filepath)
    with filepath.open('r') as f:
        data = yaml.safe_load(f)

    return [
        (mle_kind['metal'], mle_kind['leaving'], mle_kind['entering'])
        for mle_kind in data['mle_kinds']]
