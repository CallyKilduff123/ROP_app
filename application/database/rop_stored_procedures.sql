USE rop_baby_db;

-- PROCEDURE 1: DETERMINE POSTMENSTRUAL AGE AND POSTNATAL AGE AND FIRST SCREEN DATE:


DELIMITER //

CREATE PROCEDURE CalculatePMAandPNAandFirstScreenDate()
BEGIN
    SELECT 
        baby_id,
        firstname,
        lastname,
		date_of_birth,
        gestational_age_at_birth_weeks,
        gestational_age_at_birth_days,
        DATEDIFF(CURDATE(), date_of_birth) DIV 7 AS postnatal_age_weeks, -- PNA in weeks
        DATEDIFF(CURDATE(), date_of_birth) MOD 7 AS postnatal_age_days,  -- PNA in days
        gestational_age_at_birth_weeks + (DATEDIFF(CURDATE(), date_of_birth) DIV 7) AS pma_weeks, -- PMA in weeks
        (gestational_age_at_birth_days + DATEDIFF(CURDATE(), date_of_birth)) MOD 7 AS pma_days, -- PMA in days
        CASE 
            WHEN gestational_age_at_birth_weeks < 31 THEN 
                IF(DATE_ADD(date_of_birth, INTERVAL 31 - gestational_age_at_birth_weeks WEEK) > DATE_ADD(date_of_birth, INTERVAL 4 WEEK),
                   DATE_ADD(date_of_birth, INTERVAL 31 - gestational_age_at_birth_weeks WEEK),
                   DATE_ADD(date_of_birth, INTERVAL 4 WEEK))
            ELSE
                IF(DATE_ADD(date_of_birth, INTERVAL 36 - gestational_age_at_birth_weeks WEEK) < DATE_ADD(date_of_birth, INTERVAL 4 WEEK),
                   DATE_ADD(date_of_birth, INTERVAL 36 - gestational_age_at_birth_weeks WEEK),
                   DATE_ADD(date_of_birth, INTERVAL 4 WEEK))
        END AS first_screen_date
    FROM 
        baby;
END //

DELIMITER ;

call CalculatePMAandPNAandFirstScreenDate()