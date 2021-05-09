import os
import tempfile
import unittest

from src.models.Option import Option
from src.models.Poll import Poll
from src.models.PollDetails import PollDetails
from src.models.PollParty import PollParty
from src.models.PollPartyDetails import PollPartyDetails
from src.models.Result import Result
from src.models.Vote import Vote
from src.DatabaseManager import DatabaseManager

from utils import compare_polls


class DatabaseManagerSavingTest(unittest.TestCase):

    def setUp(self):
        self.test_dir = tempfile.TemporaryDirectory()

        self.db_full = self.test_dir.name + "/db_full.sqlite"
        os.system("sqlite3 " + self.db_full + " < database/example_data.sql")

        self.db_empty = self.test_dir.name + "/db_empty.sqlite"
        os.system("sqlite3 " + self.db_empty + " < database/create.sql")

    def tearDown(self):
        self.test_dir.cleanup()

    def test_get_poll(self):
        expected_polls = [self.get_poll_test_saved()]

        with DatabaseManager(self.db_full) as db_manager:
            actual_polls = db_manager.get_polls("")

        self.assertEqual(len(actual_polls), len(expected_polls))
        compare_polls(self, actual_polls[0], expected_polls[0])

    def test_save_poll(self):
        poll_to_save = self.get_poll_z8_25_24_fresh()

        with DatabaseManager(self.db_empty) as db_manager:
            db_manager.save_poll(poll_to_save)

        actual_polls = []
        expected_polls = [self.get_poll_z8_25_24_saved()]
        with DatabaseManager(self.db_empty) as db_manager:
            actual_polls = db_manager.get_polls("")

        self.assertEqual(len(actual_polls), len(expected_polls))
        compare_polls(self, actual_polls[0], expected_polls[0])

    def get_poll_test_saved(self):
        return Poll(
            1,
            "Z8/18",
            24,
            "2021-03-21 09:07:05",
            "Test otevřených dat",
            Result(1, "accepted", "Přijato"),
            PollDetails(42, 22, 18, 1, 1),
            [
                PollParty(1, "ANO 2011", PollPartyDetails(1, 1, 1), [
                    Vote(1, "David Aleš", "Ano", Option(1, "yes", "Ano")),
                    Vote(2, "Pavel Dvořák", "nepřít.", None),
                ]),
                PollParty(2, "ČSSD", PollPartyDetails(1, 1, 1), [
                    Vote(3, "Jiří Ides", "Zdržel se",
                         Option(3, "abstained", "Zdržel se")),
                    Vote(4, "Jiří Oliva", "Ne", Option(2, "no", "Ne")),
                ]),
            ]
        )

    def get_poll_z8_25_24_fresh(self):
        return Poll(
            None,
            "Z8/25",
            24,
            "2021-03-23 09:07:05",
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

    def get_poll_z8_25_24_saved(self):
        return Poll(
            1,
            "Z8/25",
            24,
            "2021-03-23 09:07:05",
            "21. Návrh na poskytnutí individuální investiční dotace Moravskému zemskému muzeu na realizaci projektu „Mendelova stezka Brnem“ – návrh rozpočtového opatření",
            Result(1, "accepted", "Přijato"),
            PollDetails(41, 39, 1, 1, None),
            [
                PollParty(1, "Nezávislí pro Brno", PollPartyDetails(3, 0, 0), [
                    Vote(1, "David Aleš", "Ano",
                         Option(1, "yes", "Ano")),
                    Vote(2, "Pavel Dvořák", "nepřít.", None),
                    Vote(3, "Jiří Faltýnek", "nepřít.", None),
                    Vote(4, "Šárka Korkešová", "Ano",
                         Option(1, "yes", "Ano")),
                    Vote(5, "Iva Kremitovská", "nepřít. (VK)", None),
                    Vote(6, "Lucie Pokorná", "Ano",
                         Option(1, "yes", "Ano")),
                ]),
                PollParty(2, "ČSSD", PollPartyDetails(4, 0, 0), [
                    Vote(7, "Jiří Ides", "nepřít.", None),
                    Vote(8, "Jiří Oliva", "Ano",
                         Option(1, "yes", "Ano")),
                    Vote(9, "Jiří Novotný", "Ano",
                         Option(1, "yes", "Ano")),
                    Vote(10, "Pavel Sázavský", "Ano",
                         Option(1, "yes", "Ano")),
                    Vote(11, "Marek Viskot", "Ano",
                         Option(1, "yes", "Ano")),
                ]),
                PollParty(3, "KDU-ČSL", PollPartyDetails(8, 0, 0), [
                    Vote(12, "Vít Beran", "Ano", Option(1, "yes", "Ano")),
                    Vote(13, "Antonín Crha", "Ano",
                         Option(1, "yes", "Ano")),
                    Vote(14, "Petr Hladík", "Ano",
                         Option(1, "yes", "Ano")),
                    Vote(15, "Filip Chvátal", "Ano",
                         Option(1, "yes", "Ano")),
                    Vote(16, "Jitka Ivičičová", "Ano",
                         Option(1, "yes", "Ano")),
                    Vote(17, "Filip Leder", "Ano",
                         Option(1, "yes", "Ano")),
                    Vote(18, "Jiří Mihola", "Ano",
                         Option(1, "yes", "Ano")),
                    Vote(19, "Jaroslav Suchý", "Ano",
                         Option(1, "yes", "Ano")),
                ]),
                PollParty(4, "ODS", PollPartyDetails(13, 0, 0), [
                    Vote(20, "Jana Bohuňovská", "Ano",
                         Option(1, "yes", "Ano")),
                    Vote(21, "David Grund", "Ano",
                         Option(1, "yes", "Ano")),
                    Vote(22, "Jiří Herman", "Ano",
                         Option(1, "yes", "Ano")),
                    Vote(23, "Michal Chládek", "Ano",
                         Option(1, "yes", "Ano")),
                    Vote(24, "Pavel Jankůj", "Ano (VK)",
                         Option(1, "yes", "Ano")),
                    Vote(25, "Ludvík Kadlec", "Ano",
                         Option(1, "yes", "Ano")),
                    Vote(26, "Robert Kerndl", "Ano",
                         Option(1, "yes", "Ano")),
                    Vote(27, "Petr Kratochvíl", "Ano",
                         Option(1, "yes", "Ano")),
                    Vote(28, "Andrea Pazderová", "Ano",
                         Option(1, "yes", "Ano")),
                    Vote(29, "David Pokorný", "Ano",
                         Option(1, "yes", "Ano")),
                    Vote(30, "Martin Příborský", "nepřít.", None),
                    Vote(31, "Kristýna Černá", "Ano (VK)",
                         Option(1, "yes", "Ano")),
                    Vote(32, "David Trllo", "Ano",
                         Option(1, "yes", "Ano")),
                    Vote(33, "Markéta Vaňková", "Ano",
                         Option(1, "yes", "Ano")),
                ]),
                PollParty(5, "Piráti", PollPartyDetails(6, 0, 0), [
                    Vote(34, "Róbert Čuma", "Ano (VK)",
                         Option(1, "yes", "Ano")),
                    Vote(35, "Marek Fišer", "Ano (VK)",
                         Option(1, "yes", "Ano")),
                    Vote(36, "Alena Pavlasová", "Ano",
                         Option(1, "yes", "Ano")),
                    Vote(37, "Tomáš Koláčný", "Ano",
                         Option(1, "yes", "Ano")),
                    Vote(38, "Ondřej Kotas", "Ano (VK)",
                         Option(1, "yes", "Ano")),
                    Vote(39, "Lukáš Mamula", "Ano",
                         Option(1, "yes", "Ano")),
                ]),
                PollParty(6, "SPD", PollPartyDetails(0, 1, 1), [
                    Vote(40, "Ivan Fencl", "Zdržel se",
                         Option(3, "abstained", "Zdržel se")),
                    Vote(41, "Jiří Kment", "Ne",
                         Option(2, "no", "Ne")),
                    Vote(42, "Jana Přikrylová", "nepřít.", None),
                    Vote(43, "Lucie Šafránková", "nepřít.", None),
                ]),
                PollParty(7, "Nezávislí", PollPartyDetails(5, 0, 0), [
                    Vote(44, "Petr Bořecký", "nepřít.", None),
                    Vote(45, "René Černý", "nepřít.", None),
                    Vote(46, "Marek Janíček", "nepřít.", None),
                    Vote(47, "Kateřina Jarošová", "nepřít.", None),
                    Vote(48, "Karel Kalivoda", "Ano",
                         Option(1, "yes", "Ano")),
                    Vote(49, "Karin Karasová", "nepřít.", None),
                    Vote(50, "Richard Mrázek", "Ano",
                         Option(1, "yes", "Ano")),
                    Vote(51, "René Novotný", "Ano",
                         Option(1, "yes", "Ano")),
                    Vote(52, "Vít Prýgl", "nepřít.", None),
                    Vote(53, "Petr Souček", "Ano",
                         Option(1, "yes", "Ano")),
                    Vote(54, "Pavel Staněk", "Ano",
                         Option(1, "yes", "Ano")),
                    Vote(55, "Petr Vokřál", "nepřít.", None),
                ]),
            ]
        )


if __name__ == '__main__':
    unittest.main()
