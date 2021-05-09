CREATE TABLE "polls" (
    "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "code" TEXT,
    "number" INTEGER,
    "datetime" TEXT,
    "subject" TEXT,
    "result" INTEGER,
    "present" INTEGER,
    "yes" INTEGER,
    "no" INTEGER,
    "abstained" INTEGER,
    "did_not_vote" INTEGER,
    FOREIGN KEY("result") REFERENCES result_options("id")
);
CREATE TABLE "poll_parties" (
    "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "poll" INTEGER NOT NULL,
    "name" TEXT NOT NULL,
    "yes" INTEGER,
    "no" INTEGER,
    "abstained" INTEGER,
    FOREIGN KEY("poll") REFERENCES polls("id")
);
CREATE TABLE "votes" (
    "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "poll_party" INTEGER NOT NULL,
    "voter" TEXT NOT NULL,
    "option" INTEGER,
    "text" TEXT NOT NULL,
    FOREIGN KEY("option") REFERENCES vote_options("id"),
    FOREIGN KEY("poll_party") REFERENCES poll_parties("id")
);
CREATE TABLE "vote_options" (
    "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "sysid" TEXT NOT NULL,
    "name" TEXT NOT NULL
);
CREATE TABLE "result_options" (
    "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "sysid" TEXT NOT NULL,
    "name" TEXT NOT NULL
);
CREATE TABLE "processed_files" (
    "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "name" TEXT NOT NULL,
    "datetime" TEXT NOT NULL
);
INSERT INTO "result_options" ("sysid", "name")
VALUES ("accepted", "Přijato"),
    ("declined", "Zamítnuto");
INSERT INTO "vote_options" ("sysid", "name")
VALUES ("yes", "Ano"),
    ("no", "Ne"),
    ("abstained", "Zdržel se");
INSERT INTO "polls" (
        "code",
        "number",
        "datetime",
        "subject",
        "result",
        "present",
        "yes",
        "no",
        "abstained",
        "did_not_vote"
    )
VALUES (
        "Z8/18",
        24,
        "2021-03-21 09:07:05",
        "Test otevřených dat",
        1,
        42,
        22,
        18,
        1,
        1
    );
INSERT INTO "poll_parties" ("poll", "name", "yes", "no", "abstained")
VALUES (1, "ANO 2011", 1, 1, 1),
    (1, "ČSSD", 1, 1, 1);
INSERT INTO "votes" ("poll_party", "voter", "option", "text")
VALUES (1, "David Aleš", 1, "Ano"),
    (1, "Pavel Dvořák", NULL, "nepřít."),
    (2, "Jiří Ides", 3, "Zdržel se"),
    (2, "Jiří Oliva", 2, "Ne");