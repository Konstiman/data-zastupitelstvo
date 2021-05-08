import typing


class Option:
    def __init__(self, id: int, sysid: str, name: str):
        # id z databaze
        self.id = id
        # systemovy identifikator
        self.sysid = sysid
        # textova reprezentace volby
        self.name = name

    def to_json(self):
        return "TODO"
