import typing

from src.models.PollParty import PollParty
from src.models.PollDetails import PollDetails
from src.models.Result import Result


class Poll:
    def __init__(self, id: int, code: str, number: int, datetime: str, subject: str, result: Result, details: PollDetails, parties: [PollParty]):
        # id z databaze
        self.id = id
        # cislo schuze zastupitelstva - napr. Z8/25
        self.code = code
        # cislo hlasovani v ramci schuze
        self.number = number
        # datum a cas hlasovani
        self.datetime = datetime
        # predmet hlasovani
        self.subject = subject
        # vysledek hlasovani
        self.result = result
        # detaily hlasovani
        self.details = details
        # seznam hlasujicich stran
        self.parties = parties

    def to_dict(self):
        return {
            "code": self.code,
            "number": self.number,
            "datetime": self.datetime,
            "subject": self.subject,
            "result": self.result.name,
            "details": self.details.to_dict(),
            "parties": list(map((lambda party: party.to_dict()), self.parties))
        }
