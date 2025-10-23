
CREATE table employees (
	id INT AUTO_INCREMENT PRIMARY KEY,
	name varchar(100) NOT NULL,
    position VARCHAR(100),
    age INT,
    department varchar(100)    
);

INSERT INTO employees (name, position, salary)
VALUES
	('혜린', 'PM', 90000),
    ('은우', 'Frontend', 80000),
    ('가을', 'Backend', 92000),
    ('지수', 'Frontend', 7800),
    ('민혁', 'Frontend', 96000),
    ('하온', 'Backend', 130000);
    
SELECT name, salary
From employees
WHERE position = 'Frontend' AND salary <= 90000;

UPDATE employees
SET salary = salary * 1.1
WHERE position = 'PM';
SELECT name, position, salary
FROM employees
WHERE position = 'PM';

UPDATE employees
SET salary = salary * 1.05
WHERE position = 'Backend';

DELETE FROM employees
WHERE name = '민혁';

SELECT position, AVG(salary) AS average_salary
FROM employees
GROUP BY position;

DROP TABLE employees;