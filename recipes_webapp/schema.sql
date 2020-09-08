DROP TABLE IF EXISTS sections;
DROP TABLE IF EXISTS page;

CREATE TABLE sections (
    section_id TEXT PRIMARY KEY,
    title TEXT UNIQUE NOT NULL
);

CREATE TABLE page (
    page_id INTEGER PRIMARY KEY AUTOINCREMENT,
    section_id TEXT NOT NULL,
    title TEXT UNIQUE NOT NULL,
    contentUrl TEXT NOT NULL,
    FOREIGN KEY (section_id) REFERENCES sections (section_id)
);
