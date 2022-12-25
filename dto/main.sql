/*
 Source Server         : animedatabase
 Source Server Type    : SQLite
 Source Server Version : 3035005
 Source Schema         : main

 Target Server Type    : SQLite
 Target Server Version : 3035005
 File Encoding         : 65001

*/

PRAGMA foreign_keys = false;

-- ----------------------------
-- Table structure for categoryMap
-- ----------------------------
CREATE TABLE "categoryMap" (
  "id" INTEGER NOT NULL,
  "Anime" integer NOT NULL ON CONFLICT REPLACE DEFAULT 0,
  CONSTRAINT "id" PRIMARY KEY ("id"),
  CONSTRAINT "fk_id" FOREIGN KEY ("id") REFERENCES "nameTable" ("id") ON DELETE CASCADE ON UPDATE CASCADE
);

-- ----------------------------
-- Table structure for downloadTable
-- ----------------------------
CREATE TABLE "downloadTable" (
  "id" integer NOT NULL ON CONFLICT ABORT,
  "source" text,
  "directory" text,
  "filter_name" text,
  "related_table" text,
  CONSTRAINT "id" PRIMARY KEY ("id") ON CONFLICT ABORT,
  CONSTRAINT "fk_id" FOREIGN KEY ("id") REFERENCES "nameTable" ("id") ON DELETE CASCADE ON UPDATE CASCADE
);

-- ----------------------------
-- Table structure for metadataTable
-- ----------------------------
CREATE TABLE "metadataTable" (
  "id" integer NOT NULL ON CONFLICT ABORT COLLATE BINARY,
  "img" text DEFAULT "/config/assets/default.jpg",
  "info" text DEFAULT "no info",
  "AnimeDBid" text(10),
  CONSTRAINT "id" PRIMARY KEY ("id") ON CONFLICT ABORT,
  CONSTRAINT "fk_id" FOREIGN KEY ("id") REFERENCES "nameTable" ("id") ON DELETE CASCADE ON UPDATE CASCADE
);

-- ----------------------------
-- Table structure for nameTable
-- ----------------------------
CREATE TABLE "nameTable" (
  "id" integer NOT NULL ON CONFLICT ABORT COLLATE BINARY PRIMARY KEY AUTOINCREMENT,
  "name" text NOT NULL ON CONFLICT ABORT DEFAULT "new Series",
  "user_level" integer NOT NULL ON CONFLICT ABORT DEFAULT 4,
  CONSTRAINT "user_level_check" CHECK (user_level>0 and user_level<5)
);

-- ----------------------------
-- Table structure for sqlite_sequence
-- ----------------------------
DROP TABLE IF EXISTS "sqlite_sequence";
CREATE TABLE sqlite_sequence(name,seq);

-- ----------------------------
-- Table structure for subscriptionTable
-- ----------------------------
DROP TABLE IF EXISTS "subscriptionTable";
CREATE TABLE "subscriptionTable" (
  "id" integer NOT NULL ON CONFLICT ABORT COLLATE BINARY,
  "starttime" text DEFAULT (datetime('now','localtime')),
  "totalEpisodes" integer NOT NULL ON CONFLICT ABORT DEFAULT 0,
  "lastUpdateTime" text NOT NULL ON CONFLICT ABORT DEFAULT (datetime('now','localtime')),
  "lastUpdateEP" integer NOT NULL ON CONFLICT ABORT DEFAULT 0,
  "nextUpdateTime" text NOT NULL ON CONFLICT ABORT DEFAULT (datetime('now','localtime')),
  "nextUpdateEP" integer NOT NULL DEFAULT 1,
  "span" integer NOT NULL ON CONFLICT ABORT DEFAULT 168,
  "type" text NOT NULL ON CONFLICT ABORT DEFAULT jackett,
  PRIMARY KEY ("id") ON CONFLICT ABORT,
  CONSTRAINT "fk_id" FOREIGN KEY ("id") REFERENCES "nameTable" ("id") ON DELETE CASCADE ON UPDATE CASCADE
);

-- ----------------------------
-- Table structure for userTable
-- ----------------------------
DROP TABLE IF EXISTS "userTable";
CREATE TABLE "userTable" (
  "user_level" integer NOT NULL ON CONFLICT ABORT DEFAULT 4,
  "username" text NOT NULL ON CONFLICT ABORT,
  "passwd" text NOT NULL,
  "session" text,
  CONSTRAINT "username" PRIMARY KEY ("username") ON CONFLICT ABORT,
  CONSTRAINT "session_unique" UNIQUE ("session") ON CONFLICT REPLACE,
  CONSTRAINT "level" CHECK (user_level>0 and user_level<5)
);

-- ----------------------------
-- View structure for DownloadItem
-- ----------------------------
DROP VIEW IF EXISTS "DownloadItem";
CREATE VIEW "DownloadItem" AS SELECT
	nameTable.id, 
	nameTable.name, 
	subscriptionTable.lastUpdateTime, 
	subscriptionTable.lastUpdateEP, 
	subscriptionTable.nextUpdateTime, 
	subscriptionTable.nextUpdateEP, 
	subscriptionTable.span, 
	subscriptionTable.type, 
	downloadTable.source, 
	downloadTable.directory, 
	downloadTable.filter_name, 
	downloadTable.related_table
FROM
	subscriptionTable
	INNER JOIN
	nameTable
	ON 
		subscriptionTable.id = nameTable.id
	INNER JOIN
	downloadTable
	ON 
		nameTable.id = downloadTable.id
GROUP BY
	nameTable.id
HAVING
	subscriptionTable.lastUpdateEP < subscriptionTable.totalEpisodes
ORDER BY
	datetime(subscriptionTable.nextUpdateTime) ASC;

-- ----------------------------
-- View structure for SubscriptionItem
-- ----------------------------
DROP VIEW IF EXISTS "SubscriptionItem";
CREATE VIEW "SubscriptionItem" AS SELECT
	nameTable.id, 
	nameTable.name, 
	subscriptionTable.starttime, 
	subscriptionTable.totalEpisodes, 
	subscriptionTable.lastUpdateTime, 
	subscriptionTable.lastUpdateEP, 
	subscriptionTable.nextUpdateTime, 
	subscriptionTable.nextUpdateEP, 
	subscriptionTable.span, 
	subscriptionTable.type
FROM
	nameTable
	INNER JOIN
	subscriptionTable
	ON 
		nameTable.id = subscriptionTable.id
ORDER BY
	nameTable.id ASC;

-- ----------------------------
-- View structure for metadataItem
-- ----------------------------
DROP VIEW IF EXISTS "metadataItem";
CREATE VIEW "metadataItem" AS SELECT
	nameTable.id, 
	nameTable.name, 
	metadataTable.img, 
	metadataTable.info, 
	metadataTable.AnimeDBid
FROM
	nameTable
	INNER JOIN
	metadataTable
	ON 
		nameTable.id = metadataTable.id
ORDER BY
	nameTable.id ASC;

-- ----------------------------
-- Auto increment value for nameTable
-- ----------------------------
UPDATE "main"."sqlite_sequence" SET seq = 1 WHERE name = 'nameTable';

PRAGMA foreign_keys = true;
