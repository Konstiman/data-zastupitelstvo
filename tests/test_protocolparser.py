#!/usr/bin/env python
# coding=utf-8

import unittest

import typing

from src.models.Option import Option
from src.models.Poll import Poll
from src.models.PollDetails import PollDetails
from src.models.PollParty import PollParty
from src.models.PollPartyDetails import PollPartyDetails
from src.models.Result import Result
from src.models.Vote import Vote
from src.ProtocolParser import ProtocolParser

from utils import compare_polls


class ParsingProtocolsTest(unittest.TestCase):

    # tests section

    def test_protocol_z8_18_1(self):
        parser = ProtocolParser()

        parsed_poll = parser.parse_file('tests/protocols/20200616-1-29874.html')

        expected_poll = self.get_poll_z8_18_1()

        compare_polls(self, parsed_poll, expected_poll)

    def test_protocol_z8_25_24(self):
        parser = ProtocolParser()

        parsed_poll = parser.parse_file(
            'tests/protocols/20210323-24-32825.html')

        expected_poll = self.get_poll_z8_25_24()

        compare_polls(self, parsed_poll, expected_poll)

    # sample data section

    def get_poll_z8_18_1(self):
        return Poll(
            None,
            "Z8/18",
            1,
            "16.06.2020 - 8:17:54",
            "1. Technický bod (zapisovatelé, právní asistence, ověřovatelé zápisu, schválení programu zasedání ZMB) - ověřovatelé zápisu",
            Result(1, "accepted", "Přijato"),
            PollDetails(47, 46, 0, 0, 1),
            [
                PollParty(None, "ANO 2011", PollPartyDetails(12, 0, 0), [
                    Vote(None, "David Aleš", "Ano",
                         Option(1, "yes", "Ano")),
                    Vote(None, "Petr Bořecký", "Ano",
                         Option(1, "yes", "Ano")),
                    Vote(None, "René Černý", "Ano",
                         Option(1, "yes", "Ano")),
                    Vote(None, "Marek Janíček", "Ano",
                         Option(1, "yes", "Ano")),
                    Vote(None, "Kateřina Jarošová", "Ano",
                         Option(1, "yes", "Ano")),
                    Vote(None, "Karin Karasová", "Nehlasoval", None),
                    Vote(None, "Šárka Korkešová", "Ano",
                         Option(1, "yes", "Ano")),
                    Vote(None, "Iva Kremitovská", "Ano",
                         Option(1, "yes", "Ano")),
                    Vote(None, "Lucie Pokorná", "Ano",
                         Option(1, "yes", "Ano")),
                    Vote(None, "Vít Prýgl", "Ano", Option(1, "yes", "Ano")),
                    Vote(None, "Petr Souček", "Ano",
                         Option(1, "yes", "Ano")),
                    Vote(None, "Pavel Staněk", "Ano",
                         Option(1, "yes", "Ano")),
                    Vote(None, "Petr Vokřál", "Ano",
                         Option(1, "yes", "Ano")),
                ]),
                PollParty(None, "ČSSD", PollPartyDetails(5, 0, 0), [
                    Vote(None, "Jiří Ides", "Ano", Option(1, "yes", "Ano")),
                    Vote(None, "Jiří Oliva", "Ano",
                         Option(1, "yes", "Ano")),
                    Vote(None, "Jiří Novotný", "Ano",
                         Option(1, "yes", "Ano")),
                    Vote(None, "Pavel Sázavský", "Ano",
                         Option(1, "yes", "Ano")),
                    Vote(None, "Marek Viskot", "Ano",
                         Option(1, "yes", "Ano")),
                ]),
                PollParty(None, "KDU-ČSL", PollPartyDetails(8, 0, 0), [
                    Vote(None, "Vít Beran", "Ano", Option(1, "yes", "Ano")),
                    Vote(None, "Antonín Crha", "Ano",
                         Option(1, "yes", "Ano")),
                    Vote(None, "Petr Hladík", "Ano",
                         Option(1, "yes", "Ano")),
                    Vote(None, "Filip Chvátal", "Ano",
                         Option(1, "yes", "Ano")),
                    Vote(None, "Jitka Ivičičová", "Ano",
                         Option(1, "yes", "Ano")),
                    Vote(None, "Filip Leder", "Ano",
                         Option(1, "yes", "Ano")),
                    Vote(None, "Jiří Mihola", "Ano",
                         Option(1, "yes", "Ano")),
                    Vote(None, "Jaroslav Suchý", "Ano",
                         Option(1, "yes", "Ano")),
                ]),
                PollParty(None, "ODS", PollPartyDetails(12, 0, 0), [
                    Vote(None, "Jana Bohuňovská", "Ano",
                         Option(1, "yes", "Ano")),
                    Vote(None, "David Grund", "Ano",
                         Option(1, "yes", "Ano")),
                    Vote(None, "Michal Chládek", "Ano",
                         Option(1, "yes", "Ano")),
                    Vote(None, "Pavel Jankůj", "Ano",
                         Option(1, "yes", "Ano")),
                    Vote(None, "Robert Kerndl", "Ano",
                         Option(1, "yes", "Ano")),
                    Vote(None, "Petr Kratochvíl", "Ano",
                         Option(1, "yes", "Ano")),
                    Vote(None, "Andrea Pazderová", "Ano",
                         Option(1, "yes", "Ano")),
                    Vote(None, "David Pokorný", "Ano",
                         Option(1, "yes", "Ano")),
                    Vote(None, "Martin Příborský", "Ano",
                         Option(1, "yes", "Ano")),
                    Vote(None, "Kristýna Černá", "Ano",
                         Option(1, "yes", "Ano")),
                    Vote(None, "David Trllo", "Ano",
                         Option(1, "yes", "Ano")),
                    Vote(None, "Markéta Vaňková", "Ano",
                         Option(1, "yes", "Ano")),
                ]),
                PollParty(None, "Piráti", PollPartyDetails(5, 0, 0), [
                    Vote(None, "Róbert Čuma", "Ano",
                         Option(1, "yes", "Ano")),
                    Vote(None, "Marek Fišer", "Ano",
                         Option(1, "yes", "Ano")),
                    Vote(None, "Tomáš Koláčný", "Ano",
                         Option(1, "yes", "Ano")),
                    Vote(None, "Ondřej Kotas", "Ano",
                         Option(1, "yes", "Ano")),
                    Vote(None, "Lukáš Mamula", "Ano",
                         Option(1, "yes", "Ano")),
                ]),
                PollParty(None, "SPD", PollPartyDetails(4, 0, 0), [
                    Vote(None, "Ivan Fencl", "Ano",
                         Option(1, "yes", "Ano")),
                    Vote(None, "Jiří Kment", "Ano",
                         Option(1, "yes", "Ano")),
                    Vote(None, "Jana Přikrylová", "Ano",
                         Option(1, "yes", "Ano")),
                    Vote(None, "Lucie Šafránková", "Ano",
                         Option(1, "yes", "Ano")),
                ]),
            ]
        )

    def get_poll_z8_25_24(self):
        return Poll(
            None,
            "Z8/25",
            24,
            "23.03.2021 - 9:07:05",
            "21. Návrh na poskytnutí individuální investiční dotace Moravskému zemskému muzeu na realizaci projektu „Mendelova stezka Brnem“ – návrh rozpočtového opatření",
            Result(1, "accepted", "Přijato"),
            PollDetails(41, 39, 1, 1, None),
            [
                PollParty(None, "Nezávislí pro Brno", PollPartyDetails(3, 0, 0), [
                    Vote(None, "David Aleš", "Ano",
                         Option(1, "yes", "Ano")),
                    Vote(None, "Pavel Dvořák", "nepřít.", None),
                    Vote(None, "Jiří Faltýnek", "nepřít.", None),
                    Vote(None, "Šárka Korkešová", "Ano",
                         Option(1, "yes", "Ano")),
                    Vote(None, "Iva Kremitovská", "nepřít. (VK)", None),
                    Vote(None, "Lucie Pokorná", "Ano",
                         Option(1, "yes", "Ano")),
                ]),
                PollParty(None, "ČSSD", PollPartyDetails(4, 0, 0), [
                    Vote(None, "Jiří Ides", "nepřít.", None),
                    Vote(None, "Jiří Oliva", "Ano",
                         Option(1, "yes", "Ano")),
                    Vote(None, "Jiří Novotný", "Ano",
                         Option(1, "yes", "Ano")),
                    Vote(None, "Pavel Sázavský", "Ano",
                         Option(1, "yes", "Ano")),
                    Vote(None, "Marek Viskot", "Ano",
                         Option(1, "yes", "Ano")),
                ]),
                PollParty(None, "KDU-ČSL", PollPartyDetails(8, 0, 0), [
                    Vote(None, "Vít Beran", "Ano", Option(1, "yes", "Ano")),
                    Vote(None, "Antonín Crha", "Ano",
                         Option(1, "yes", "Ano")),
                    Vote(None, "Petr Hladík", "Ano",
                         Option(1, "yes", "Ano")),
                    Vote(None, "Filip Chvátal", "Ano",
                         Option(1, "yes", "Ano")),
                    Vote(None, "Jitka Ivičičová", "Ano",
                         Option(1, "yes", "Ano")),
                    Vote(None, "Filip Leder", "Ano",
                         Option(1, "yes", "Ano")),
                    Vote(None, "Jiří Mihola", "Ano",
                         Option(1, "yes", "Ano")),
                    Vote(None, "Jaroslav Suchý", "Ano",
                         Option(1, "yes", "Ano")),
                ]),
                PollParty(None, "ODS", PollPartyDetails(13, 0, 0), [
                    Vote(None, "Jana Bohuňovská", "Ano",
                         Option(1, "yes", "Ano")),
                    Vote(None, "David Grund", "Ano",
                         Option(1, "yes", "Ano")),
                    Vote(None, "Jiří Herman", "Ano",
                         Option(1, "yes", "Ano")),
                    Vote(None, "Michal Chládek", "Ano",
                         Option(1, "yes", "Ano")),
                    Vote(None, "Pavel Jankůj", "Ano (VK)",
                         Option(1, "yes", "Ano")),
                    Vote(None, "Ludvík Kadlec", "Ano",
                         Option(1, "yes", "Ano")),
                    Vote(None, "Robert Kerndl", "Ano",
                         Option(1, "yes", "Ano")),
                    Vote(None, "Petr Kratochvíl", "Ano",
                         Option(1, "yes", "Ano")),
                    Vote(None, "Andrea Pazderová", "Ano",
                         Option(1, "yes", "Ano")),
                    Vote(None, "David Pokorný", "Ano",
                         Option(1, "yes", "Ano")),
                    Vote(None, "Martin Příborský", "nepřít.", None),
                    Vote(None, "Kristýna Černá", "Ano (VK)",
                         Option(1, "yes", "Ano")),
                    Vote(None, "David Trllo", "Ano",
                         Option(1, "yes", "Ano")),
                    Vote(None, "Markéta Vaňková", "Ano",
                         Option(1, "yes", "Ano")),
                ]),
                PollParty(None, "Piráti", PollPartyDetails(6, 0, 0), [
                    Vote(None, "Róbert Čuma", "Ano (VK)",
                         Option(1, "yes", "Ano")),
                    Vote(None, "Marek Fišer", "Ano (VK)",
                         Option(1, "yes", "Ano")),
                    Vote(None, "Alena Pavlasová", "Ano",
                         Option(1, "yes", "Ano")),
                    Vote(None, "Tomáš Koláčný", "Ano",
                         Option(1, "yes", "Ano")),
                    Vote(None, "Ondřej Kotas", "Ano (VK)",
                         Option(1, "yes", "Ano")),
                    Vote(None, "Lukáš Mamula", "Ano",
                         Option(1, "yes", "Ano")),
                ]),
                PollParty(None, "SPD", PollPartyDetails(0, 1, 1), [
                    Vote(None, "Ivan Fencl", "Zdržel se",
                         Option(3, "abstained", "Zdržel se")),
                    Vote(None, "Jiří Kment", "Ne",
                         Option(2, "no", "Ne")),
                    Vote(None, "Jana Přikrylová", "nepřít.", None),
                    Vote(None, "Lucie Šafránková", "nepřít.", None),
                ]),
                PollParty(None, "Nezávislí", PollPartyDetails(5, 0, 0), [
                    Vote(None, "Petr Bořecký", "nepřít.", None),
                    Vote(None, "René Černý", "nepřít.", None),
                    Vote(None, "Marek Janíček", "nepřít.", None),
                    Vote(None, "Kateřina Jarošová", "nepřít.", None),
                    Vote(None, "Karel Kalivoda", "Ano",
                         Option(1, "yes", "Ano")),
                    Vote(None, "Karin Karasová", "nepřít.", None),
                    Vote(None, "Richard Mrázek", "Ano",
                         Option(1, "yes", "Ano")),
                    Vote(None, "René Novotný", "Ano",
                         Option(1, "yes", "Ano")),
                    Vote(None, "Vít Prýgl", "nepřít.", None),
                    Vote(None, "Petr Souček", "Ano",
                         Option(1, "yes", "Ano")),
                    Vote(None, "Pavel Staněk", "Ano",
                         Option(1, "yes", "Ano")),
                    Vote(None, "Petr Vokřál", "nepřít.", None),
                ]),
            ]
        )


if __name__ == '__main__':
    unittest.main()
