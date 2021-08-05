# Author: Huveyscan Kamar

database_setup_statements = [
'''
CREATE DATABASE themoviedb;

use themoviedb;

create table IF NOT EXISTS TV_SERIES (
        ID INT PRIMARY KEY,
        Name varchar(50) NOT NULL,
        Overview varchar(1000) NOT NULL,
        Number_of_Seasons INT NOT NULL,
        Number_of_Episodes INT NOT NULL,
        Popularity FLOAT NOT NULL,
        Vote_Average FLOAT NOT NULL,
        Vote_Count INT NOT NULL,
        First_Air_Date date NOT NULL,
        Last_Air_Date date NOT NULL,
        Status varchar(50) NOT NULL
        );
	
	create table IF NOT EXISTS PERSON (
        ID INT PRIMARY KEY,
        Name varchar(50) NOT NULL,
        Gender INT NOT NULL,
        Known_For_Department varchar(50) NOT NULL,
        Popularity FLOAT NOT NULL
        );
		
	create table IF NOT EXISTS CAST (
        Series_ID INT NOT NULL,
        Person_ID INT NOT NULL,
        Type varchar(50) NOT NULL,
        Character_Name varchar(50),
        PRIMARY KEY (Series_ID,Person_ID),
        FOREIGN KEY (Series_ID) REFERENCES TV_SERIES(ID),
        FOREIGN KEY (Person_ID) REFERENCES PERSON(ID)
        );

#SELECT * from TV_SERIES;
#SELECT * from PERSON;
#SELECT * from CAST;

#DELETE from TV_SERIES where ID > 1;
#DELETE from PERSON where ID > 1;
#DELETE from CAST where Series_ID > 1;

#1
SELECT * FROM PERSON ORDER BY Popularity DESC  LIMIT 10;

#2
SET @row_number = 0;
SELECT 
	(@row_number:=@row_number + 1) AS 'Popularity Order',
	Name AS 'Actress/Actor Name', 
    CASE 
		WHEN GENDER = 1 THEN "Female" 
        ELSE "Male" 
	END AS Gender
 FROM PERSON ORDER BY Popularity DESC  LIMIT 10;
 
 
#3
SELECT p.Name, s.Name, c.Character_Name FROM PERSON p 
INNER JOIN CAST c ON c.Person_ID = p.ID
INNER JOIN TV_SERIES s ON s.ID = c.Series_ID
Where p.ID IN(
SELECT p.ID FROM PERSON p 
INNER JOIN CAST c ON c.Person_ID = p.ID
INNER JOIN TV_SERIES s ON s.ID = c.Series_ID
GROUP BY p.Name
HAVING Count(p.ID)>1);

#INSERT INTO CAST (Series_ID,Person_ID,Type,Character_Name) VALUES (4087,2692,'Cast','Huveyscan Kamar');

#4
SET @row_number = 0;
SELECT 
(SELECT (@row_number:=@row_number + 1)) AS 'Popularity Order',
(SELECT Name FROM PERSON WHERE Known_For_Department = 'Acting' ORDER BY Popularity DESC LIMIT 1) AS Acting,
(SELECT Name FROM PERSON WHERE Known_For_Department = 'Directing' ORDER BY Popularity DESC LIMIT 1) AS Directing,
(SELECT Name FROM PERSON WHERE Known_For_Department = 'Writing' ORDER BY Popularity DESC LIMIT 1) AS Writing
UNION
SELECT 
(SELECT (@row_number:=@row_number + 1)) AS 'Popularity Order',
(SELECT Name FROM PERSON WHERE Known_For_Department = 'Acting' ORDER BY Popularity DESC LIMIT 1,1) AS Acting,
(SELECT Name FROM PERSON WHERE Known_For_Department = 'Directing' ORDER BY Popularity DESC LIMIT 1,1) AS Directing,
(SELECT Name FROM PERSON WHERE Known_For_Department = 'Writing' ORDER BY Popularity DESC  LIMIT 1,1) AS Writing
UNION
SELECT 
(SELECT (@row_number:=@row_number + 1)) AS 'Popularity Order',
(SELECT Name FROM PERSON WHERE Known_For_Department = 'Acting' ORDER BY Popularity DESC LIMIT 2,1) AS Acting,
(SELECT Name FROM PERSON WHERE Known_For_Department = 'Directing' ORDER BY Popularity DESC LIMIT 2,1) AS Directing,
(SELECT Name FROM PERSON WHERE Known_For_Department = 'Writing' ORDER BY Popularity DESC  LIMIT 2,1) AS Writing;

'''
]

# Author: Huveyscan Kamar