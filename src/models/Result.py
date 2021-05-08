import typing


class Result:
    def __init__(self, id: int, sysid: str, name: str):
        # id z databaze
        self.id = id
        # systemovy identifikator
        self.sysid = sysid
        # textova reprezentace vysledku
        self.name = name

    def to_json(self):
        return "TODO"
