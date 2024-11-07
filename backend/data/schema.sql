-- Vytvoření tabulek

-- Tabulka správné řešení
CREATE TABLE Correct_solution (
     correct_solution_id VARCHAR(20) PRIMARY KEY,
     correct_solution_text VARCHAR(100) NOT NULL,
     case_sensitive BOOLEAN NOT NULL DEFAULT 0,
     question_id INTEGER NOT NULL,
     FOREIGN KEY (question_id) REFERENCES Question (question_id)
         ON DELETE NO ACTION
         ON UPDATE NO ACTION
);

-- Tabulka vyplněná otázka
CREATE TABLE Filled_question (
     question_id INTEGER,
     solution VARCHAR(100),
     is_correct BOOLEAN NOT NULL DEFAULT 0,
     filled_test_id INTEGER,
     PRIMARY KEY (question_id, filled_test_id),
     FOREIGN KEY (question_id) REFERENCES Question (question_id)
         ON DELETE NO ACTION
         ON UPDATE NO ACTION,
     FOREIGN KEY (filled_test_id) REFERENCES Filled_test (filled_test_id)
         ON DELETE NO ACTION
         ON UPDATE NO ACTION
);

-- Tabulka Vyplněný test
CREATE TABLE Filled_test (
     filled_test_id INTEGER PRIMARY KEY AUTOINCREMENT,
     test_id INTEGER,
     user_id INTEGER,
     date_time_beginning DATETIME NOT NULL DEFAULT (datetime('now')),
     date_time_end DATETIME,
     FOREIGN KEY (test_id) REFERENCES Test (test_id)
         ON DELETE NO ACTION
         ON UPDATE NO ACTION,
     FOREIGN KEY (user_id) REFERENCES Profile (user_id)
         ON DELETE SET NULL
         ON UPDATE NO ACTION
);

-- Tabulka Otázka
CREATE TABLE Question (
     question_id INTEGER PRIMARY KEY AUTOINCREMENT,
     title VARCHAR(35) NOT NULL,
     task VARCHAR(100) NOT NULL,
     help VARCHAR(100),
     test_id INTEGER,
     FOREIGN KEY (test_id) REFERENCES Test (test_id)
         ON DELETE NO ACTION
         ON UPDATE NO ACTION
);

-- Tabulka Test
CREATE TABLE Test (
     test_id INTEGER PRIMARY KEY AUTOINCREMENT,
     title VARCHAR(30) NOT NULL,
     description VARCHAR(30) NOT NULL,
     subject VARCHAR(25) NOT NULL,
     datetime DATETIME NOT NULL DEFAULT (datetime('now')),
     sequence BOOLEAN NOT NULL DEFAULT 0,
     max_time TIME,
     user_id INTEGER,
     FOREIGN KEY (user_id) REFERENCES Profile (user_id)
         ON DELETE SET NULL
         ON UPDATE NO ACTION
);

-- Tabulka Uživatelský profil
CREATE TABLE Profile (
     user_id INTEGER PRIMARY KEY AUTOINCREMENT,
     name VARCHAR(20) NOT NULL,
     surname VARCHAR(20) NOT NULL,
     email VARCHAR(25) NOT NULL,
     password VARCHAR(25) NOT NULL,
     user_type VARCHAR(1) NOT NULL DEFAULT 'P',
     last_logged_in DATETIME,
     CHECK (user_type IN ('A', 'P', 'T')),
     CHECK (email LIKE '%@%.%')
);

CREATE TABLE Tokens (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    token VARCHAR(255) NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Profile(user_id)
        ON DELETE CASCADE
        ON UPDATE NO ACTION
);