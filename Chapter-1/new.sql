\c postgres
DROP TABLE IF EXISTS comments CASCADE;
DROP TABLE IF EXISTS submissions CASCADE;
DROP TABLE IF EXISTS subreddits CASCADE;
DROP TABLE IF EXISTS authors CASCADE;

CREATE TABLE subreddits(

    banner_background_image TEXT,
    created_utc integer,
    description TEXT,
    display_name TEXT UNIQUE,
    header_img TEXT,
    hide_ads BOOLEAN,
    id TEXT UNIQUE,
    over_18 BOOLEAN,
    public_description TEXT,
    retrieved_utc INTEGER,
    name TEXT UNIQUE,
    subreddit_type TEXT,
    subscribers INTEGER,
    title TEXT,
    whitelist_status TEXT,
    PRIMARY KEY (id)
);

CREATE TABLE authors(

    id TEXT UNIQUE,
    retrieved_on integer,
    name TEXT UNIQUE,
    created_utc integer,
    link_karma integer,
    comment_karma integer,
    profile_img TEXT,
    profile_color TEXT,
    profile_over_18 TEXT,
    
    PRIMARY KEY (id, name)
    
);


CREATE TABLE submissions
(
    downs integer,
    url TEXT,
    id TEXT UNIQUE,
    edited BOOLEAN,
    num_reports integer,
    created_utc integer,
    name TEXT UNIQUE,
    title TEXT,
    author TEXT,
    permalink TEXT,
    num_comments integer,
    likes BOOLEAN,
    subreddit_id TEXT,
    ups integer,
    PRIMARY KEY (id),
    FOREIGN KEY(author) REFERENCES authors(name),
    FOREIGN KEY(subreddit_id) REFERENCES subreddits(name)
);

CREATE TABLE comments
(
    distinguished TEXT,
    downs integer,
    created_utc integer,
    controversiality INTEGER,
    edited BOOLEAN,
    gilded INTEGER,
    author_flair_css_class TEXT,
    id TEXT UNIQUE,
    author TEXT,
    retrieved_on integer,
    score_hidden BOOLEAN,
    subreddit_id TEXT,
    score integer,
    name TEXT UNIQUE,
    author_flair_text TEXT,
    link_id TEXT,
    archived BOOLEAN,
    ups integer,
    parent_id TEXT,
    subreddit TEXT,
    body TEXT,
    
    PRIMARY KEY (id),
    FOREIGN KEY(author) REFERENCES authors(name),
    FOREIGN KEY(subreddit_id) REFERENCES subreddits(name),
    FOREIGN KEY(subreddit) REFERENCES subreddits(display_name)
);

CREATE extension IF NOT EXISTS pg_bulkload;

