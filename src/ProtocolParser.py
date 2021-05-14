#!/usr/bin/env python
# coding=utf-8

import AdvancedHTMLParser
import datetime
import re

from src.models.Option import Option
from src.models.Poll import Poll
from src.models.PollDetails import PollDetails
from src.models.PollParty import PollParty
from src.models.PollPartyDetails import PollPartyDetails
from src.models.Result import Result
from src.models.Vote import Vote


# TODO add types
# TODO remove camelCase


class ProtocolParser:
    def __init__(self):
        self.__parser = AdvancedHTMLParser.AdvancedHTMLParser()

    def parse_file(self, filename):
        html = self.__loadFile(filename)
        self.__parser.parseStr(html)

        tables = self.__parser.getElementsByTagName('table')

        title = self.__getValueByClassName(tables[0], 'title')
        subtitle = self.__getValueByTagName(tables[0], 'p', 1)
        subject = re.sub(
            r'\s+', ' ', self.__getValueByClassName(tables[0], 'subject'))

        result = self.__getPollResult(tables[1].textContent.strip())

        code = self.__parseCode(title)
        number = self.__parseNumber(subtitle)
        datetime = self.__parseDatetime(title)
        details = self.__parseSubresults(tables[3].textContent.split("\n"))
        parties = self.__parsePartyResults(tables)

        return Poll(None, code, number, datetime, subject, result, details, parties)

    def __loadFile(self, filename):
        with open(filename, 'rb') as f:
            return f.read().decode("windows-1250").encode('utf-8').decode('utf-8')

    def __getValueByClassName(self, root, className, index=0):
        return root.getElementsByClassName(className)[index].textContent.strip()

    def __getValueByTagName(self, root, tagName, index=0):
        return self.__parser.getElementsByTagName(tagName, root)[index].textContent.strip()

    def __parseValue(self, regex, string):
        m = regex.match(string)
        if (m):
            return m.group(1)
        return ""

    def __parseCode(self, title):
        p = re.compile(r'^\s*Zastupitelstvo města Brna č\. ([^\s]+)')
        return self.__parseValue(p, title)

    def __parseDatetime(self, title):
        p = re.compile(r'^\s*Zastupitelstvo města Brna č\. [^\s]+\s+(.*?)\s*$')
        raw_datetime = self.__parseValue(p, title)
        obj_datetime = datetime.datetime.strptime(raw_datetime, '%d.%m.%Y - %H:%M:%S')
        return obj_datetime.replace(tzinfo=datetime.timezone.utc).isoformat()

    def __parseNumber(self, subtitle):
        p = re.compile(r'^\s*Hlasování č\. (\d+)$')
        return int(self.__parseValue(p, subtitle))

    def __parseSubresultNumber(self, string):
        p = re.compile(r'^.*?:\s+(\d+)$')
        return int(self.__parseValue(p, string))

    def __parseSubresults(self, array):
        subresults = []
        for i in range(len(array)):
            subr = re.sub(r'\s+', ' ', array[i].strip())
            if (subr):
                subresults.append(subr)

        return PollDetails(
            self.__parseSubresultNumber(subresults[0]),
            self.__parseSubresultNumber(subresults[1]),
            self.__parseSubresultNumber(subresults[2]),
            self.__parseSubresultNumber(subresults[3]),
            self.__parseSubresultNumber(subresults[4]) if len(
                subresults) > 4 else None
        )

    def __parsePartyResults(self, tables):
        partiesCount = (len(tables) - 4) // 3
        partiesArray = []
        for i in range(1, partiesCount + 1):
            infoTable = tables[2 + i * 3]

            name = self.__getValueByTagName(infoTable, 'th', 0)

            results = self.__getValueByTagName(infoTable, 'th', 1)
            details = self.__parsePartyDetailedResults(results)

            votesTable = tables[3 + i * 3]
            votesRows = self.__parser.getElementsByTagName('tr', votesTable)
            votesTuples = self.__parsePartyVotes(votesRows)
            votes = self.__groupPartyVotes(votesTuples)

            partiesArray.append(PollParty(None, name, details, votes))

        return partiesArray

    def __parsePartyDetailedResults(self, results):
        p1 = re.compile(r'\(Ano:\s+(\d+)')
        yes = int(self.__parseValue(p1, results))

        p2 = re.compile(r'.*Ne:\s+(\d+)')
        no = int(self.__parseValue(p2, results))

        p3 = re.compile(r'.*Zdržel se:\s+(\d+)')
        abstained = int(self.__parseValue(p3, results))

        return PollPartyDetails(yes, no, abstained)

    def __parsePartyVotes(self, rows):
        entries = []
        for i in range(len(rows)):
            content = rows[i].textContent
            splitter = "\n"
            if ("\r" in content):
                splitter = "\r\n"
            subentries = content.split(splitter)
            for j in range(1, len(subentries) - 1):
                entries.append(subentries[j].strip())
        return entries

    def __groupPartyVotes(self, entries):
        votes = []
        for i in range(0, len(entries), 2):
            name = entries[i][:-1]
            text = entries[i + 1]
            # remove 'text' from the condition if you want to accept empty results
            if (name and text and name != "&nbsp;" and text != "&nbsp;"):
                votes.append(Vote(None, name, text, self.__getVoteOption(text)))

        return votes

    def __getPollResult(self, text):
        # it might be better to load options from db
        if ("Přijato" in text):
            return Result(1, "accepted", "Přijato")
        if ("Nepřijato" in text):
            return Result(2, "declined", "Nepřijato")

        return None

    def __getVoteOption(self, text):
        # it might be better to load options from db
        if ("Ano" in text):
            return Option(1, "yes", "Ano")
        if ("Ne" in text and not "Nepř" in text and not "Nehlasoval" in text):
            return Option(2, "no", "Ne")
        if ("Zdržel se" in text):
            return Option(3, "abstained", "Zdržel se")

        return None
