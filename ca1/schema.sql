DROP TABLE IF EXISTS users;

CREATE TABLE users
(
    user_id PRIMARY KEY,
    password TEXT NOT NULL
);

DROP TABLE IF EXISTS jewellery;

CREATE TABLE jewellery
(
    jewellery_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price REAL NOT NULL,
    description TEXT NOT NULL
);

INSERT INTO jewellery(name,price,description) 
VALUES ('Butterfly necklace',10.50,'A shiny silver necklace with a butterfly pendant'),
        ('Gold chain necklace',19.99,'A shiny gold necklace, for both men and women'),
        ('Layered gold necklace',24,'A shiny gold necklace with multiple layers'),
        ('Diamond bracelet',25,'A shiny silver bracelet embellished in diamonds'),
        ('Diamond stud earrings',10,'shiny diamond earring'),
        ('Gold hoop earrings',10.99,'shiny small gold hoop earrings'),
        ('Silver ring set',12.20,'a set of three silver rings'),
        ('Heart jewel ring',8.99,'a lovely heart jewel ring');

DROP TABLE IF EXISTS reviews;

CREATE TABLE reviews
(
    review_number INTEGER PRIMARY KEY AUTOINCREMENT,
    name_of_product TEXT NOT NULL,
    review TEXT NOT NULL
);

INSERT INTO reviews(name_of_product,review)
VALUES ('Butterfly necklace','Very pretty and a good price');

DROP TABLE IF EXISTS emails;

CREATE TABLE emails
(
    email PRIMARY KEY
);
