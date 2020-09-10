DROP TABLE IF EXISTS sections;
DROP TABLE IF EXISTS pages;

CREATE TABLE sections (
    section_id TEXT PRIMARY KEY,
    title TEXT UNIQUE NOT NULL
);

CREATE TABLE pages (
    page_id INTEGER PRIMARY KEY AUTOINCREMENT,
    section_id TEXT NOT NULL,
    title TEXT UNIQUE NOT NULL,
    contentUrl TEXT NOT NULL,
    lastModifiedDateTime TEXT NOT NULL,
    FOREIGN KEY (section_id) REFERENCES sections (section_id)
);
