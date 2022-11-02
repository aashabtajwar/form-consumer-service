CREATE TABLE publishers (
    id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL
);


CREATE TABLE responders (
    id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    phone VARCHAR(255) NOT NULL
);

CREATE TABLE forms (
    id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    title VARCHAR(255) NOT NULL,
    description VARCHAR(255) NOT NULL,
    link VARCHAR(255) NOT NULL,
    sheet_name VARCHAR(255) NOT NULL,
    publisher_id INT,
    FOREIGN KEY (publisher_id) REFERENCES publishers(id) ON DELETE CASCADE

);

CREATE TABLE questions (
    id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    text VARCHAR(255) NOT NULL,
    field_name VARCHAR(255) NOT NULL,
    form_id INT,
    FOREIGN KEY (form_id) REFERENCES forms(id) ON DELETE CASCADE
);


CREATE TABLE responses (
    id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    text VARCHAR(255) NOT NULL,
    question_id INT,
    responder_id INT, 
    FOREIGN KEY (question_id) REFERENCES questions(id) ON DELETE CASCADE,
    FOREIGN KEY (responder_id) REFERENCES responders(id) ON DELETE CASCADE
);