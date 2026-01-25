#---------------------------------
# vi: sw=4 ts=4 expandtab
#---------------------------------

from dataclasses import dataclass, asdict
from typing import List
import json

@dataclass
class Rank:
    rank: int
    appid: int
    concurrent_in_game: int
    peak_in_game: int

@dataclass
class Response:
    last_update: int
    ranks: List[Rank]

    def __post_init__(self):
        self.ranks = [Rank(**rank) for rank in self.ranks]

@dataclass
class TopSteamGames:
    response: Response

    def __post_init__(self):
        self.response = Response(**self.response)

    def toJson(self):
        return json.dumps(asdict(self), indent=4)
