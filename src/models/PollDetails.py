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

    def to_dict(self):
        return {
            "present": self.present,
            "yes": self.yes,
            "no": self.no,
            "abstained": self.abstained,
            "did_not_vote": self.did_not_vote
        }
