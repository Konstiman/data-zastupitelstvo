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

    def to_dict(self):
        return {
            "name": self.name,
            "details": self.details.to_dict(),
            "votes": list(map((lambda vote: vote.to_dict()), self.votes))
        }
