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