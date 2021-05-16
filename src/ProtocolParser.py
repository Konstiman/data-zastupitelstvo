#!/usr/bin/env python
# coding=utf-8

import AdvancedHTMLParser
import datetime
import re
import typing

from src.models.Option import Option
from src.models.Poll import Poll
from src.models.PollDetails import PollDetails
from src.models.PollParty import PollParty
from src.models.PollPartyDetails import PollPartyDetails
from src.models.Result import Result
from src.models.Vote import Vote


class ProtocolParser:
    def __init__(self):
        self.__parser = AdvancedHTMLParser.AdvancedHTMLParser()

    def parse_file(self, filename: str) -> Poll:
        html = self.__load_file(filename)
        self.__parser.parseStr(html)

        tables = self.__parser.getElementsByTagName('table')

        title = self.__get_title(tables[0])

        subtitle = self.__get_value_by_tag(tables[0], 'p', 1)
        subject = self.__get_subject(tables[0])

        result = self.__get_poll_result(tables[1].textContent.strip())

        code = self.__parse_code(title)
        number = self.__parse_number(subtitle)
        datetime = self.__parse_datetime(title)
        details = self.__parse_subresults(tables[3])
        parties = self.__parse_party_results(tables)

        return Poll(None, code, number, datetime, subject, result, details, parties)

    def __load_file(self, filename: str) -> str:
        with open(filename, 'rb') as f:
            return f.read().decode("windows-1250").encode('utf-8').decode('utf-8')

    def __get_title(self, title_tab):
        title = ""
        try:
            title = self.__get_value_by_class(title_tab, 'title')
        except:
            try:
                title = self.__get_value_by_class(title_tab, 'header')
            except:
                pass
        
        return title

    def __get_subject(self, subject_tab):
        subject = ""
        try:
            subject = self.__get_value_by_class(subject_tab, 'subject')
        except:
            subjectElems = self.__parser.getElementsByXPath("//center/b")
            if (len(subjectElems) > 0):
                subject = subjectElems[0].textContent.strip()

        return re.sub(r'\s+', ' ', subject)

    def __get_value_by_class(self, root, className, index=0):
        return root.getElementsByClassName(className)[index].textContent.strip()

    def __get_value_by_tag(self, root, tagName, index=0):
        return self.__parser.getElementsByTagName(tagName, root)[index].textContent.strip()

    def __parse_value(self, regex, string):
        m = regex.match(string)
        if (m):
            return m.group(1)
        return ""

    def __parse_code(self, title):
        p = re.compile(r'^\s*Zastupitelstvo města Brna č\. ([^\s]+)')
        return self.__parse_value(p, title)

    def __parse_datetime(self, title):
        p = re.compile(r'^\s*Zastupitelstvo města Brna č\. [^\s]+\s+(.*?)\s*$')
        raw_datetime = self.__parse_value(p, title)
        obj_datetime = None
        try:
            obj_datetime = datetime.datetime.strptime(
                raw_datetime, '%d.%m.%Y - %H:%M:%S')
        except:
            obj_datetime = datetime.datetime.strptime(
                raw_datetime, '%d.%m.%Y %H:%M.%S')

        return obj_datetime.replace(tzinfo=datetime.timezone.utc).isoformat()

    def __parse_number(self, subtitle):
        p = re.compile(r'^\s*Hlasování č\. (\d+)$')
        return int(self.__parse_value(p, subtitle))

    def __parse_subresult(self, string):
        p = re.compile(r'^.*?:\s+(\d+)$')
        return int(self.__parse_value(p, string))

    def __parse_subresults(self, table):
        cells = self.__parser.getElementsByTagName("td", table)
        subresults = []
        for i in range(len(cells)):
            subr = re.sub(r'\s+', ' ', cells[i].textContent.strip())
            if (subr):
                subresults.append(subr)

        return PollDetails(
            self.__parse_subresult(subresults[0]),
            self.__parse_subresult(subresults[1]),
            self.__parse_subresult(subresults[2]),
            self.__parse_subresult(subresults[3]),
            self.__parse_subresult(subresults[4]) if len(
                subresults) > 4 else None
        )

    def __parse_party_results(self, tables):
        partiesCount = (len(tables) - 4) // 3
        partiesArray = []
        for i in range(1, partiesCount + 1):
            infoTable = tables[2 + i * 3]

            name = self.__get_value_by_tag(infoTable, 'th', 0)

            results = self.__get_value_by_tag(infoTable, 'th', 1)
            details = self.__parse_party_details(results)

            votesTable = tables[3 + i * 3]
            votesRows = self.__parser.getElementsByTagName('tr', votesTable)
            votesTuples = self.__parse_party_votes(votesRows)
            votes = self.__group_party_votes(votesTuples)

            partiesArray.append(PollParty(None, name, details, votes))

        return partiesArray

    def __parse_party_details(self, results):
        p1 = re.compile(r'\(Ano:\s+(\d+)')
        yes = int(self.__parse_value(p1, results))

        p2 = re.compile(r'.*Ne:\s+(\d+)')
        no = int(self.__parse_value(p2, results))

        p3 = re.compile(r'.*Zdržel se:\s+(\d+)')
        abstained = int(self.__parse_value(p3, results))

        return PollPartyDetails(yes, no, abstained)

    def __parse_party_votes(self, rows):
        entries = []
        for i in range(len(rows)):
            cells = self.__parser.getElementsByTagName('td', rows[i])
            for j in range(0, len(cells)):
                val = re.sub(r'\s+', ' ', cells[j].textContent.strip())
                entries.append(val)
        return entries

    def __group_party_votes(self, entries):
        votes = []
        for i in range(0, len(entries), 2):
            name = entries[i][:-1]
            text = entries[i + 1]
            # remove 'text' from the condition if you want to accept empty results
            if (name and text and name != "&nbsp;" and text != "&nbsp;"):
                votes.append(
                    Vote(None, name, text, self.__get_vote_option(text)))

        return votes

    def __get_poll_result(self, text):
        # it might be better to load options from db
        if ("Přijato" in text):
            return Result(1, "accepted", "Přijato")
        if ("Nepřijato" in text):
            return Result(2, "declined", "Nepřijato")

        return None

    def __get_vote_option(self, text):
        # it might be better to load options from db
        if ("Ano" in text):
            return Option(1, "yes", "Ano")
        if ("Ne" in text and not "Nepř" in text and not "Nehlasoval" in text):
            return Option(2, "no", "Ne")
        if ("Zdržel se" in text):
            return Option(3, "abstained", "Zdržel se")

        return None
