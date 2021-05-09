import typing

from src.models.Option import Option


class Vote:
    def __init__(self, id: int, voter: str, text: str, option: Option):
        # id z databaze
        self.id = id
        # jmeno hlasujiciho
        self.voter = voter
        # puvodni text hlasu
        self.text = text
        # zvolena moznost
        self.option = option

    def to_dict(self):
        return {
            "voter": self.voter,
            "text": self.text,
            "option": self.option.name if self.option else None
        }
