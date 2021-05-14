import sqlite3
from typing import List

from src.models.Option import Option
from src.models.Poll import Poll
from src.models.PollDetails import PollDetails
from src.models.PollParty import PollParty
from src.models.PollPartyDetails import PollPartyDetails
from src.models.Result import Result
from src.models.Vote import Vote


def __is_int(val):
    try:
        int(val)
        return True
    except ValueError:
        return False


supported_get_params = {
    # system could support also 'where' param: https://gis.brno.cz/ags1/sdk/rest/index.html#//02ss0000002r000000
    # "where": {
    #    "validator": "",
    #    "help": ""
    # },
    "sort": {
        "validator": lambda p: p in ["newest", "oldest"],
        "help": "Supported values: 'newest', 'oldest'."
    },
    "limit": {
        "validator": lambda p: __is_int(p),
        "help": "Supported values: non-negative integers."
    },
    "offset": {
        "validator": lambda p: __is_int(p),
        "help": "Supported values: non-negative integers."
    }
}


# behaves like a context manager https://book.pythontips.com/en/latest/context_managers.html
class DatabaseManager(object):
    def __init__(self, db_path: str):
        self.connection = sqlite3.connect(db_path)
        self.connection.row_factory = sqlite3.Row

        self.results = self.__load_results()
        self.options = self.__load_options()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.connection.close()

    def close(self):
        self.connection.close()

    def get_polls(self, params: dict) -> List[Poll]:
        poll_query = self.__build_query(params)

        cur = self.connection.cursor()
        cur.execute(poll_query)

        polls = cur.fetchall()

        parties_dict = self.__get_poll_parties(poll_query)

        results = []
        for poll in polls:
            result = None
            if (poll["result"] and poll["result"] in self.results):
                result = self.results[poll["result"]]

            parties = []
            if (poll["id"] in parties_dict):
                parties = parties_dict[poll["id"]]

            results.append(
                Poll(
                    poll["id"],
                    poll["code"],
                    poll["number"],
                    poll["datetime"],
                    poll["subject"],
                    result,
                    PollDetails(poll["present"], poll["yes"], poll["no"],
                                poll["abstained"], poll["did_not_vote"]),
                    parties
                )
            )

        return results

    def save_poll(self, poll: Poll):
        sql = 'INSERT INTO "polls" ("code", "number", "datetime", "subject", "result", "present", "yes", "no", "abstained", "did_not_vote") VALUES (?,?,?,?,?,?,?,?,?,?);'

        cur = self.connection.cursor()
        cur.execute(sql, (poll.code, poll.number, poll.datetime, poll.subject, poll.result.id, poll.details.present,
                          poll.details.yes, poll.details.no, poll.details.abstained, poll.details.did_not_vote))
        self.connection.commit()

        poll.id = cur.lastrowid

        for party in poll.parties:
            self.__save_poll_party(poll.id, party)

    def get_processed_filenames(self) -> List[str]:
        query = "SELECT name FROM processed_files"

        cur = self.connection.cursor()
        cur.execute(query)

        files = cur.fetchall()
        output = []
        for file in files:
            output.append(file["name"])

        return output

    def save_processed_file(self, name, datetime):
        sql = 'INSERT INTO "processed_files" ("name", "datetime") VALUES (?,?);'

        cur = self.connection.cursor()
        cur.execute(sql, (name, datetime))
        self.connection.commit()

    def get_last_update(self) -> str:
        query = "SELECT MAX(datetime) AS datetime FROM processed_files"

        cur = self.connection.cursor()
        cur.execute(query)

        entry = cur.fetchone()
        if entry:
            return entry["datetime"]

        return ""

    def __build_query(self, params: dict) -> str:
        for key in params.keys():
            if (not key in supported_get_params.keys()):
                raise Exception('invalid parameter "' + key + '" (unsupported)')
            if (not supported_get_params[key]["validator"](params[key])):
                raise Exception('invalid parameter "' + key + '" value', supported_get_params[key]["help"])

        poll_query = "SELECT * FROM polls"

        ordering = "DESC"
        if ("sort" in params and params["sort"] == "oldest"):
            ordering = "ASC"

        poll_query += " ORDER BY datetime " + ordering

        limit = -1
        if ("limit" in params):
            limit = int(params["limit"])
        offset = 0
        if ("offset" in params):
            offset = int(params["offset"])
        
        poll_query = "SELECT * FROM (" + poll_query + ") LIMIT " + str(limit) + " OFFSET " + str(offset)

        return poll_query

    def __save_poll_party(self, poll_id: int, party: PollParty):
        sql = 'INSERT INTO "poll_parties" ("poll", "name", "yes", "no", "abstained") VALUES (?,?,?,?,?);'

        cur = self.connection.cursor()
        cur.execute(sql, (poll_id, party.name, party.details.yes,
                          party.details.no, party.details.abstained))
        self.connection.commit()

        party.id = cur.lastrowid

        for vote in party.votes:
            self.__save_party_vote(party.id, vote)

    def __save_party_vote(self, party_id: int, vote: Vote):
        sql = 'INSERT INTO "votes" ("poll_party", "voter", "option", "text") VALUES (?,?,?,?);'

        option_id = None
        if (vote.option):
            option_id = vote.option.id

        cur = self.connection.cursor()
        cur.execute(sql, (party_id, vote.voter, option_id, vote.text))
        self.connection.commit()

        vote.id = cur.lastrowid

    def __get_poll_parties(self, poll_query):
        parties_query = "SELECT * FROM poll_parties WHERE poll IN (SELECT id FROM (" + \
            poll_query + "))"

        cur = self.connection.cursor()
        cur.execute(parties_query)

        parties = cur.fetchall()

        votes_dict = self.__get_party_votes(parties_query)

        result = {}
        for party in parties:
            if (not party["poll"] in result):
                result[party["poll"]] = []

            votes = []
            if (party["id"] in votes_dict):
                votes = votes_dict[party["id"]]

            result[party["poll"]].append(
                PollParty(
                    party["id"],
                    party["name"],
                    PollPartyDetails(
                        party["yes"], party["no"], party["abstained"]),
                    votes))

        return result

    def __get_party_votes(self, parties_query):
        votes_query = "SELECT * FROM votes WHERE poll_party IN (SELECT id FROM (" + \
            parties_query + "))"

        cur = self.connection.cursor()
        cur.execute(votes_query)

        votes = cur.fetchall()

        result = {}
        for vote in votes:
            if (not vote["poll_party"] in result):
                result[vote["poll_party"]] = []

            option = None
            if (vote["option"] and vote["option"] in self.options):
                option = self.options[vote["option"]]

            result[vote["poll_party"]].append(
                Vote(vote["id"], vote["voter"], vote["text"], option))

        return result

    def __load_results(self):
        results_query = "SELECT * FROM result_options"

        cur = self.connection.cursor()
        cur.execute(results_query)

        rows = cur.fetchall()

        result = {}
        for row in rows:
            result[row["id"]] = Result(row["id"], row["sysid"], row["name"])

        return result

    def __load_options(self):
        options_query = "SELECT * FROM vote_options"

        cur = self.connection.cursor()
        cur.execute(options_query)

        rows = cur.fetchall()

        result = {}
        for row in rows:
            result[row["id"]] = Option(row["id"], row["sysid"], row["name"])

        return result
