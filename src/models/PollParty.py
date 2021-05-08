import typing

from src.models.PollPartyDetails import PollPartyDetails
from src.models.Vote import Vote


class PollParty:
    def __init__(self, id: int, name: str, details: PollPartyDetails, votes: [Vote]):
        # id z databaze
        self.id = id
        # nazev politicke strany
        self.name = name
        # detaily hlasovani
        self.details = details
        # seznam hlasu
        self.votes = votes

    def to_json(self):
        return "TODO"
