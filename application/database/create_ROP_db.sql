CREATE DATABASE rop_baby_db;

USE rop_baby_db;

CREATE TABLE baby
(
baby_id INT AUTO_INCREMENT PRIMARY KEY,
firstname VARCHAR(50) NOT NULL DEFAULT "baby",
lastname VARCHAR(50) NOT NULL,
gender ENUM ("male", "female") NOT NULL,
date_of_birth DATE, 
gestational_age_at_birth_weeks INT NOT NULL,
gestational_age_at_birth_days INT NOT NULL DEFAULT 0,
birthweight_grams INT NOT NULL
);


CREATE TABLE fundus
(
fundus_id INT AUTO_INCREMENT PRIMARY KEY,
baby_ID INT, FOREIGN KEY (baby_id) REFERENCES baby(baby_id),
vessels_end ENUM("zone 1", "zone 2", "zone 3"),
is_ROP BOOLEAN DEFAULT FALSE NOT NULL
);


CREATE TABLE ROP
(
ROP_id INT AUTO_INCREMENT PRIMARY KEY,
fundus_id INT, FOREIGN KEY (fundus_id) REFERENCES fundus(fundus_id),
stage ENUM ("stage 1", "stage 2", "stage 3", "stage 4+"),
zone ENUM("zone 1", "zone 2", "zone 3"),
plus_disease ENUM("plus", "preplus")
);

CREATE TABLE screening
(
screening_id INT AUTO_INCREMENT PRIMARY KEY,
baby_ID INT, FOREIGN KEY (baby_id) REFERENCES baby(baby_id),
rop_id INT, FOREIGN KEY (rop_id) REFERENCES rop(rop_id),
first_screen DATE,
next_screen DATE,
screening_frequency ENUM("weekly", "Every 2 weeks"),
is_terminated BOOLEAN DEFAULT FALSE NOT NULL
);

CREATE TABLE treatment
(
treatment_id INT AUTO_INCREMENT PRIMARY KEY,
ROP_id INT, FOREIGN KEY (ROP_id) REFERENCES ROP(ROP_id),
requires_treatment BOOLEAN DEFAULT FALSE,
treatment_date DATE,
post_treatment_review DATE
);
