CREATE TABLE nauczyciele
    (
	ID              INT(4)          NOT NULL AUTO_INCREMENT,
	imie		    VARCHAR(40)		NOT NULL,
    nazwisko	    VARCHAR(40)		NOT NULL,
    PESEL           BIGINT          NOT NULL,
    adres   	    VARCHAR(30)		NOT NULL,
    email   		VARCHAR(40)		NOT NULL,
    numer_telefonu  VARCHAR(13)     NOT NULL,
    PRIMARY KEY (ID)
    );
    
ALTER TABLE nauczyciele AUTO_INCREMENT = 1001;

CREATE TABLE klasy
	(
	ID              VARCHAR(10)     NOT NULL,
	nazwa           VARCHAR(10)     NOT NULL,
	opis            VARCHAR(30)     NULL,
	ID_wychowawcy   INT             NULL,
	rocznik         INT             NOT NULL,
    PRIMARY KEY (ID),
    FOREIGN KEY (ID_wychowawcy) REFERENCES nauczyciele(ID)
    );
    
CREATE TABLE uczniowie
	(
	ID              INT(6)          NOT NULL AUTO_INCREMENT,
    PESEL		    BIGINT			NOT NULL,
    imie		    VARCHAR(40)		NOT NULL,
    nazwisko	    VARCHAR(40)		NOT NULL,
    data_urodzenia	VARCHAR(11)		NOT NULL,
    adres   	    VARCHAR(30)		NOT NULL,
    email   		VARCHAR(40)		NOT NULL,
    klasa           VARCHAR(10)     NULL,
    PRIMARY KEY (ID)
    );
    
ALTER TABLE uczniowie AUTO_INCREMENT = 100001;


INSERT INTO uczniowie(PESEL, imie, nazwisko, data_urodzenia, adres, email)
			VALUES(98011405079, 'Piotr', 'Rosa', '98-01-14', 'Mieczysławka 9B', 'rosapiotr@o2.pl');
INSERT INTO uczniowie(PESEL, imie, nazwisko, data_urodzenia, adres, email)
			VALUES(98011405079, 'Piotr', 'Rosa', '98-01-14', 'Mieczysławka 9B', 'rosapiotr@o2.pl');
			
CREATE TABLE przedmioty
	(
	ID              INT(5)          NOT NULL AUTO_INCREMENT,
    nazwa		    VARCHAR(40)		NOT NULL,
    ID_nauczyciela  INT(4)          NULL,
    PRIMARY KEY (ID),
    FOREIGN KEY (ID_nauczyciela) REFERENCES nauczyciele(ID)
    );
    
CREATE TABLE oceny
	(
	ID_ucznia       INT(6)          NOT NULL,
    ID_przedmiotu   INT(5)          NOT NULL,
    ocena           VARCHAR(3)      NOT NULL,
    waga            INT(1)          NOT NULL,
    wynik           VARCHAR(100)    NULL,
    FOREIGN KEY (ID_ucznia) REFERENCES uczniowie(ID),
    FOREIGN KEY (ID_przedmiotu) REFERENCES przedmioty(ID)
    );
    
CREATE TABLE ogloszenia
	(
	ID              INT             NOT NULL AUTO_INCREMENT,
    ID_nauczyciela  INT(4)          NOT NULL,
    ID_przedmiotu   INT(5)          NOT NULL,
    tresc           VARCHAR(1000)    NOT NULL,
    PRIMARY KEY (ID),
    FOREIGN KEY (ID_nauczyciela) REFERENCES nauczyciele(ID),
    FOREIGN KEY (ID_przedmiotu) REFERENCES przedmioty(ID)
    );
    
CREATE TABLE zajecia
	(
	ID              INT             NOT NULL AUTO_INCREMENT,
    ID_przedmiotu   INT(5)          NOT NULL,
    ID_klasy        VARCHAR(10)     NOT NULL,
    dzien           VARCHAR(13)     NULL,
    godzina         TIME            NULL,
    sala            VARCHAR(5)      NULL,
    PRIMARY KEY (ID),
    FOREIGN KEY (ID_przedmiotu) REFERENCES przedmioty(ID),
    FOREIGN KEY (ID_klasy) REFERENCES klasy(ID)
    );

delimiter //
CREATE PROCEDURE dodajnauczyciela
	(
	imie		    VARCHAR(40),
    nazwisko	    VARCHAR(40),
    PESEL           BIGINT,
    adres   	    VARCHAR(30),
    email   		VARCHAR(40),
    numer_telefonu  VARCHAR(13)
    )
BEGIN
    IF NOT EXISTS
		(SELECT * FROM nauczyciele n 
		    WHERE n.PESEL = PESEL)
	    THEN
            INSERT INTO nauczyciele(imie, nazwisko, PESEL, adres, email, numer_telefonu)
                VALUES(imie, nazwisko, PESEL, adres, email, numer_telefonu);
    END IF;
END;
//

//
CREATE PROCEDURE dodajklase
    (
	nazwa           VARCHAR(10),
	ID_wychowawcy   INT,
	opis            VARCHAR(30),
	rocznik         INT
	)
BEGIN
    INSERT INTO klasy(ID, nazwa, ID_wychowawcy, opis, rocznik)
        VALUES(CONCAT(rocznik, "-", nazwa), nazwa, ID_wychowawcy, opis, rocznik);
END;
//

//
CREATE PROCEDURE dodajogloszenie
    (
    ID_nauczyciela  INT(4),
    ID_przedmiotu   INT(5),
    tresc           VARCHAR(1000)
    )
BEGIN
    INSERT INTO ogloszenia(ID_nauczyciela, ID_przedmiotu, tresc)
        VALUES(ID_nauczyciela, ID_przedmiotu, tresc);
END;
//

//
CREATE PROCEDURE dodajucznia
	(
	PESEL		    BIGINT,
    imie		    VARCHAR(40),
    nazwisko	    VARCHAR(40),
    data_urodzenia	VARCHAR(11),
    adres   	    VARCHAR(30),
    email   		VARCHAR(40),
    klasa           INT
    )
BEGIN
    IF NOT EXISTS
		(SELECT * FROM uczniowie u
		    WHERE u.PESEL = PESEL)
	    THEN
            INSERT INTO uczniowie(PESEL, imie, nazwisko, data_urodzenia, adres, email, klasa)
                VALUES(PESEL, imie, nazwisko, data_urodzenia, adres, email, klasa);
    END IF;
END;
//

//
CREATE PROCEDURE zmienklase
    (
    ID_ucznia       INT(6),
    ID_klasy        VARCHAR(10)
    )
BEGIN
    UPDATE uczniowie
    SET klasa = ID_klasy
    WHERE ID=ID_ucznia;
END;
//

//
CREATE PROCEDURE dodajprzedmiot
    (
    nazwa		    VARCHAR(40),
    ID_nauczyciela  INT(4)
    )
BEGIN
    INSERT INTO przedmioty(nazwa, ID_nauczyciela)
        VALUES(nazwa, ID_nauczyciela);
END;
//

//
CREATE PROCEDURE dodajocene
    (
	ID_ucznia       INT(6),
    ID_przedmiotu   INT(5),
    ocena           VARCHAR(3),
    waga            INT(1),
    wynik           VARCHAR(100)
    )
BEGIN
    INSERT INTO oceny(ID_ucznia, ID_przedmiotu, ocena, waga, wynik)
        VALUES(ID_ucznia, ID_przedmiotu, ocena, waga, wynik);
END;
//

//
CREATE PROCEDURE dodajzajecia
    (
    ID_przedmiotu   INT(5),
    ID_klasy        VARCHAR(10),
    dzien           VARCHAR(13),
    godzina         TIME,
    sala            VARCHAR(5)
    )
BEGIN
    INSERT INTO zajecia(ID_przedmiotu, ID_klasy, dzien, godzina, sala)
        VALUES(ID_przedmiotu, ID_klasy, dzien, godzina, sala);
END;
//

//
CREATE PROCEDURE wyswietlzajecia
    (
    ID_klasy        VARCHAR(10)
    )
BEGIN
    SELECT * FROM zajecia z
        WHERE z.ID_klasy = ID_klasy;
END;
//

//
CREATE PROCEDURE wyswietlwszystkieoceny
    (
    ID_ucznia       INT(6)
    )
BEGIN
    SELECT * FROM oceny o
        WHERE o.ID_ucznia = ID_ucznia;
END;
//

//
CREATE PROCEDURE wyswietlocenyzprzedmiotu
    (
    ID_ucznia       INT(6),
    ID_przedmiotu   INT(5)
    )
BEGIN
    SELECT * FROM oceny o
        WHERE o.ID_ucznia = ID_ucznia
        AND o.ID_przedmiotu = ID_przedmiotu;
END;
//

//
CREATE PROCEDURE znajdznauczyciela
    (
    nazwisko        VARCHAR(40)
    )
BEGIN
    SELECT n.imie, n.nazwisko, n.email, n.numer_telefonu FROM nauczyciele n
        WHERE n.nazwisko LIKE CONCAT('%', nazwisko, '%');
END;
//

//
CREATE PROCEDURE wyswietlogloszenia
    (
    ID_przedmiotu   INT(5)
    )
BEGIN
    SELECT o.ID_przedmiotu, p.nazwa, o.tresc FROM ogloszenia o
        JOIN przedmioty p ON p.ID = o.ID_przedmiotu
        WHERE o.ID_przedmiotu = ID_przedmiotu;
END;
//

//
CREATE PROCEDURE wyswietlogloszeniaklasy
    (
    ID_klasy        VARCHAR(10)  
    )
BEGIN
    SELECT o.ID_przedmiotu, p.nazwa, o.tresc FROM zajecia z 
        JOIN przedmioty p ON p.ID = z.ID_przedmiotu
        JOIN ogloszenia o ON o.ID_przedmiotu = p.ID
        WHERE z.ID_klasy = ID_klasy;
END;
//

-- //
-- CREATE PROCEDURE zmienemail
--     (
    
--     )
-- Czy powinienem zmieniac wszystko osobno, czy moge zalatwic to jedna procedura, gdzie jesli bedzie null, to pobrac z bazy i wstawic stare, albo wiele if
-- //
CALL dodajnauczyciela('Piotr', 'Rosa', 98011405089, 'Lubartów 24', 'rosapiotr@o2.pl', '512504897');
CALL dodajklase("3B", 1001, "matematyczno-fizyczna", 2018);
CALL dodajucznia(98011405079, 'Piotr', 'Rosa', '98-01-14', 'Mieczysławka 9B', 'rosapiotr@o2.pl', NULL);
CALL zmienklase(100002, '2018-3B');
CALL dodajprzedmiot("Matematyka", 1001);
CALL dodajocene(100001, 1, '3-', 2, '56/100 pkt. Źle zadania 3 i 5');
CALL dodajzajecia(1, '2018-3B', 'Poniedziałek', '8:15', '153c');
CALL dodajogloszenie(1001, 1, 'Zajecia odwolane do odwolania');

-- CALL wyswietlogloszeniaklasy('2018-3B');
-- SELECT -1;
-- SELECT * from nauczyciele;
-- SELECT * from uczniowie;
-- SELECT * FROM klasy;
-- SELECT * FROM przedmioty;
-- SELECT * FROM oceny;
-- SELECT * FROM zajecia;
-- SELECT version();
-- CALL wyswietlzajecia('2018-3B');
-- CALL wyswietlwszystkieoceny(100001);
-- CALL wyswietlocenyzprzedmiotu(100001, 1);
-- CALL znajdznauczyciela('o');
-- CALL wyswietlogloszenia(1);
-- 5.7.28-0ubuntu0.18.04.4