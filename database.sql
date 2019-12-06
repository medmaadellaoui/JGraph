CREATE TABLE package (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    package_name TEXT NOT NULL UNIQUE,
    absolute_path TEXT NOT NULL
);

CREATE TABLE class (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    class_name TEXT NOT NULL UNIQUE,
    absolute_path TEXT NOT NULL,
    package_id INTEGER NOT NULL,
    FOREIGN KEY(package_id) REFERENCES package(id)
);

CREATE TABLE link (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    class_src INTEGER NOT NULL,
    class_dst INTEGER NOT NULL,
    FOREIGN KEY(class_src) REFERENCES class(id),
    FOREIGN KEY(class_dst) REFERENCES class(id)
    CONSTRAINT unq UNIQUE (class_src, class_dst)
);