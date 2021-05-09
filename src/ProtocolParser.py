#!/usr/bin/env python
# coding=utf-8

import AdvancedHTMLParser
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

        # TODO choose one from db
        result = Result(None, None, tables[1].textContent.strip())

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
        return self.__parseValue(p, title)

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

    def __getVoteOption(self, text):
        # TODO use regex
        # TODO load options from db
        if ("Ano" in text):
            return Option(None, "yes", "Ano")
        if ("Ne" in text and not "Nepř" in text and not "Nehlasoval" in text):
            return Option(None, "no", "Ne")
        if ("Zdržel se" in text):
            return Option(None, "abstained", "Zdržel se")

        return None
