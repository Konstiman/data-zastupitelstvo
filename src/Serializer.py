import json
import typing

from src.models.Poll import Poll


class Serializer:
    def get_json(self, polls: [Poll], metadata: dict = {}) -> str:
        data_dict = metadata.copy()
        data_dict["data"] = []
        for poll in polls:
            data_dict["data"].append(poll.to_dict())

        return json.dumps(data_dict, ensure_ascii=False)
