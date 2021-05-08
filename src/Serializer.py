import json
import typing

from src.models.Poll import Poll


class Serializer:
    def getJson(self, poll: Poll) -> str:
        return json.dumps(poll, ensure_ascii=False)
