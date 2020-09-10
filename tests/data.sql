INSERT INTO sections (section_id, title)
VALUES
    ('test_id', 'test_title');

INSERT INTO pages (section_id, title, contentUrl, lastModifiedDateTime)
VALUES
    ('test_id', 'page_title', 'page_contentUrl', 'page_lastModifiedDateTime');