DROP TABLE IF EXISTS blanked;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS soldier;
DROP TABLE IF EXISTS platoon;







SELECT * from Platoon

SELECT Count(*) as cnt, p.name
FROM platoon as p
JOIN soldier as s on s.platoon_id = p.index
GROUP BY p.name



SELECT * from soldier
WHERE platoon_id = 1

SELECT * from orders
SELECT * from blanked
