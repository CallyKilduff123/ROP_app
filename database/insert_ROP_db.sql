USE rop_baby_db;

INSERT INTO baby (firstname, lastname, gender, date_of_birth, gestational_age_at_birth_weeks, gestational_age_at_birth_days, birthweight_grams)
VALUES
('Baby', 'Garcia', 'female', '2024-03-04', 26, 0, 900),
('Baby', 'Rodriguez', 'male','2024-03-15', 24, 1, 1249),
('Lucas', 'Jones', 'male','2024-03-04', 33, 1, 1431),
('Charlotte', 'Davis', 'female', '2024-03-06', 40, 6, 1900),
('Ava', 'Jones', 'female', '2024-03-12',  32, 6, 1356),
('Elijah', 'Jones', 'male', '2024-03-03', 31, 3, 1698),
('Olivia', 'Smith', 'female','2024-03-14', 23, 1, 900),
('Henry', 'McGarmin', 'male', '2024-03-11', 30, 6, 2900),
('Harper', 'Johnson', 'male', '2024-03-02', 31, 5, 1899),
('Mia', 'Franklin', 'female', '2024-03-17', 30, 2, 1450);

SELECT * FROM baby;

INSERT INTO fundus (baby_id, vessels_end, is_ROP)
VALUES
(01, 'zone 1', FALSE),
(02, 'zone 2', FALSE), 
(03, 'zone 2', FALSE), 
(05, 'zone 1', FALSE), 
(06, 'zone 2', TRUE), 
(07, 'zone 2', FALSE),
(08, 'zone 2', TRUE), 
(09, 'zone 2', TRUE), 
(10, 'zone 1', TRUE);

SELECT * FROM fundus;


INSERT INTO ROP(fundus_id, stage, zone, plus_disease)
VALUES
(5, "stage 3", "zone 1", "preplus"),
(7, "stage 1", "zone 1", "plus"),
(8, "stage 1", "zone 2", "plus"),
(9, "stage 1", "zone 3", NULL);

SELECT * FROM ROP;


INSERT INTO screening(baby_id, rop_id, first_screen, next_screen, screening_frequency, is_terminated)
VALUES
(1, NULL, NULL, NULL,NULL, FALSE),
(2, NULL, NULL, NULL, NULL, FALSE),
(3, NULL, NULL, NULL, NULL, FALSE),
(5, NULL, NULL, NULL, NULL, FALSE),
(6, 1, NULL, NULL, NULL, FALSE),
(7, NULL, NULL, NULL, NULL, FALSE),
(8, 2, NULL, NULL, NULL, FALSE),
(9, 3, NULL, NULL, NULL, FALSE),
(10, 4, NULL, NULL, NULL, FALSE);

SELECT * FROM screening;


INSERT INTO treatment(ROP_id, requires_treatment, treatment_date, post_treatment_review)
VALUES
(1, NULL, NULL, NULL),
(2, NULL, NULL, NULL),
(3, NULL, NULL, NULL),
(4, NULL, NULL, NULL);

SELECT * FROM treatment;

