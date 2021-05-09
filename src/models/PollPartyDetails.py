import typing


class PollPartyDetails:
    def __init__(self, yes: int, no: int, abstained: int):
        # pocet hlasujicich pro
        self.yes = yes
        # pocet hlasujicich proti
        self.no = no
        # pocet zdrzivsich se hlasovani
        self.abstained = abstained

    def to_dict(self):
        return {
            "yes": self.yes,
            "no": self.no,
            "abstained": self.abstained
        }
