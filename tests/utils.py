# helper test functions
from src.models.Option import Option
from src.models.Poll import Poll
from src.models.PollDetails import PollDetails
from src.models.PollParty import PollParty
from src.models.PollPartyDetails import PollPartyDetails
from src.models.Result import Result
from src.models.Vote import Vote


def compare_polls(test, actual: Poll, expected: Poll):
    print("testing poll " + expected.code + "-" + str(expected.number))
    test.assertEqual(actual.id, expected.id)
    test.assertEqual(actual.code, expected.code)
    test.assertEqual(actual.number, expected.number)
    test.assertEqual(actual.datetime,  expected.datetime)
    test.assertEqual(actual.subject, expected.subject)
    compare_parties(test, actual.parties, expected.parties)
    compare_poll_details(test, actual.details, expected.details)
    test.assertEqual(actual.result.name, expected.result.name)


def compare_poll_details(test, actual: PollDetails, expected: PollDetails):
    test.assertEqual(actual.present, expected.present)
    test.assertEqual(actual.yes, expected.yes)
    test.assertEqual(actual.no, expected.no)
    test.assertEqual(actual.abstained, expected.abstained)
    test.assertEqual(actual.did_not_vote, expected.did_not_vote)


def compare_parties(test, actual: [PollParty], expected: [PollParty]):
    test.assertEqual(len(actual), len(expected))

    for i in range(len(actual)):
        print("  testing party '" + expected[i].name + "'")
        test.assertEqual(actual[i].id, expected[i].id)
        test.assertEqual(actual[i].name, expected[i].name)
        compare_votes(test, actual[i].votes, expected[i].votes)
        compare_parties_details(test, actual[i].details, expected[i].details)


def compare_parties_details(test, actual: PollPartyDetails, expected: PollPartyDetails):
    test.assertEqual(actual.yes, expected.yes)
    test.assertEqual(actual.no, expected.no)
    test.assertEqual(actual.abstained, expected.abstained)


def compare_votes(test, actual: [Vote], expected: [Vote]):
    test.assertEqual(len(actual), len(expected))

    for i in range(len(actual)):
        test.assertEqual(actual[i].id, expected[i].id)
        test.assertEqual(actual[i].voter, expected[i].voter)
        test.assertEqual(actual[i].text, expected[i].text)
        test.assertEqual(actual[i].text, expected[i].text)
        compare_options(test, actual[i].option, expected[i].option)


def compare_options(test, actual: Option, expected: Option):
    if (actual == None or expected == None):
        test.assertEqual(actual, expected)
    else:
        test.assertEqual(actual.id, expected.id)
        test.assertEqual(actual.sysid, expected.sysid)
        test.assertEqual(actual.name, expected.name)
