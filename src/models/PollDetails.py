import typing


class PollDetails:
    def __init__(self, present: int, yes: int, no: int, abstained: int, did_not_vote: int):
        # pocet pritomnych
        self.present = present
        # pocet hlasujicich pro
        self.yes = yes
        # pocet hlasujicich proti
        self.no = no
        # pocet zdrzivsich se hlasovani
        self.abstained = abstained
        # pocet nepritomnych
        self.did_not_vote = did_not_vote

    def to_json(self):
        return "TODO"
