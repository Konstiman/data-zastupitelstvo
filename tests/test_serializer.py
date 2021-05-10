import json
import unittest

from src.models.Option import Option
from src.models.Poll import Poll
from src.models.PollDetails import PollDetails
from src.models.PollParty import PollParty
from src.models.PollPartyDetails import PollPartyDetails
from src.models.Result import Result
from src.models.Vote import Vote
from src.Serializer import Serializer


class SerializingTest(unittest.TestCase):

    def test_serialize_z8_25_24(self):
        serializer = Serializer()

        metadata = {
            "last_update": "2021-05-10 13:47:00"
        }

        actual_json = serializer.get_json([self.get_poll_z8_25_24()], metadata)
        actual_dict = json.loads(actual_json)

        expected_dict = self.get_dict_z8_25_24()

        self.assertEqual(actual_dict, expected_dict)

    def get_dict_z8_25_24(self):
        data = {}
        with open('tests/outputs/20210323-24-32825.json') as json_file:
            data = json.load(json_file)

        return data

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
                         Option(None, "yes", "Ano")),
                    Vote(None, "Pavel Dvořák", "nepřít.", None),
                    Vote(None, "Jiří Faltýnek", "nepřít.", None),
                    Vote(None, "Šárka Korkešová", "Ano",
                         Option(None, "yes", "Ano")),
                    Vote(None, "Iva Kremitovská", "nepřít. (VK)", None),
                    Vote(None, "Lucie Pokorná", "Ano",
                         Option(None, "yes", "Ano")),
                ]),
                PollParty(None, "ČSSD", PollPartyDetails(4, 0, 0), [
                    Vote(None, "Jiří Ides", "nepřít.", None),
                    Vote(None, "Jiří Oliva", "Ano",
                         Option(None, "yes", "Ano")),
                    Vote(None, "Jiří Novotný", "Ano",
                         Option(None, "yes", "Ano")),
                    Vote(None, "Pavel Sázavský", "Ano",
                         Option(None, "yes", "Ano")),
                    Vote(None, "Marek Viskot", "Ano",
                         Option(None, "yes", "Ano")),
                ]),
                PollParty(None, "KDU-ČSL", PollPartyDetails(8, 0, 0), [
                    Vote(None, "Vít Beran", "Ano", Option(None, "yes", "Ano")),
                    Vote(None, "Antonín Crha", "Ano",
                         Option(None, "yes", "Ano")),
                    Vote(None, "Petr Hladík", "Ano",
                         Option(None, "yes", "Ano")),
                    Vote(None, "Filip Chvátal", "Ano",
                         Option(None, "yes", "Ano")),
                    Vote(None, "Jitka Ivičičová", "Ano",
                         Option(None, "yes", "Ano")),
                    Vote(None, "Filip Leder", "Ano",
                         Option(None, "yes", "Ano")),
                    Vote(None, "Jiří Mihola", "Ano",
                         Option(None, "yes", "Ano")),
                    Vote(None, "Jaroslav Suchý", "Ano",
                         Option(None, "yes", "Ano")),
                ]),
                PollParty(None, "ODS", PollPartyDetails(13, 0, 0), [
                    Vote(None, "Jana Bohuňovská", "Ano",
                         Option(None, "yes", "Ano")),
                    Vote(None, "David Grund", "Ano",
                         Option(None, "yes", "Ano")),
                    Vote(None, "Jiří Herman", "Ano",
                         Option(None, "yes", "Ano")),
                    Vote(None, "Michal Chládek", "Ano",
                         Option(None, "yes", "Ano")),
                    Vote(None, "Pavel Jankůj", "Ano (VK)",
                         Option(None, "yes", "Ano")),
                    Vote(None, "Ludvík Kadlec", "Ano",
                         Option(None, "yes", "Ano")),
                    Vote(None, "Robert Kerndl", "Ano",
                         Option(None, "yes", "Ano")),
                    Vote(None, "Petr Kratochvíl", "Ano",
                         Option(None, "yes", "Ano")),
                    Vote(None, "Andrea Pazderová", "Ano",
                         Option(None, "yes", "Ano")),
                    Vote(None, "David Pokorný", "Ano",
                         Option(None, "yes", "Ano")),
                    Vote(None, "Martin Příborský", "nepřít.", None),
                    Vote(None, "Kristýna Černá", "Ano (VK)",
                         Option(None, "yes", "Ano")),
                    Vote(None, "David Trllo", "Ano",
                         Option(None, "yes", "Ano")),
                    Vote(None, "Markéta Vaňková", "Ano",
                         Option(None, "yes", "Ano")),
                ]),
                PollParty(None, "Piráti", PollPartyDetails(6, 0, 0), [
                    Vote(None, "Róbert Čuma", "Ano (VK)",
                         Option(None, "yes", "Ano")),
                    Vote(None, "Marek Fišer", "Ano (VK)",
                         Option(None, "yes", "Ano")),
                    Vote(None, "Alena Pavlasová", "Ano",
                         Option(None, "yes", "Ano")),
                    Vote(None, "Tomáš Koláčný", "Ano",
                         Option(None, "yes", "Ano")),
                    Vote(None, "Ondřej Kotas", "Ano (VK)",
                         Option(None, "yes", "Ano")),
                    Vote(None, "Lukáš Mamula", "Ano",
                         Option(None, "yes", "Ano")),
                ]),
                PollParty(None, "SPD", PollPartyDetails(0, 1, 1), [
                    Vote(None, "Ivan Fencl", "Zdržel se",
                         Option(None, "abstained", "Zdržel se")),
                    Vote(None, "Jiří Kment", "Ne",
                         Option(None, "no", "Ne")),
                    Vote(None, "Jana Přikrylová", "nepřít.", None),
                    Vote(None, "Lucie Šafránková", "nepřít.", None),
                ]),
                PollParty(None, "Nezávislí", PollPartyDetails(5, 0, 0), [
                    Vote(None, "Petr Bořecký", "nepřít.", None),
                    Vote(None, "René Černý", "nepřít.", None),
                    Vote(None, "Marek Janíček", "nepřít.", None),
                    Vote(None, "Kateřina Jarošová", "nepřít.", None),
                    Vote(None, "Karel Kalivoda", "Ano",
                         Option(None, "yes", "Ano")),
                    Vote(None, "Karin Karasová", "nepřít.", None),
                    Vote(None, "Richard Mrázek", "Ano",
                         Option(None, "yes", "Ano")),
                    Vote(None, "René Novotný", "Ano",
                         Option(None, "yes", "Ano")),
                    Vote(None, "Vít Prýgl", "nepřít.", None),
                    Vote(None, "Petr Souček", "Ano",
                         Option(None, "yes", "Ano")),
                    Vote(None, "Pavel Staněk", "Ano",
                         Option(None, "yes", "Ano")),
                    Vote(None, "Petr Vokřál", "nepřít.", None),
                ]),
            ]
        )
        

if __name__ == '__main__':
    unittest.main()
