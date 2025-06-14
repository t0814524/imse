START TRANSACTION;
-- Lager 1:
INSERT INTO adresse (land, stadt, strasse, haus_nr)
VALUES ('Österreich', 'Wien', 'Karlplatz', '20');
SET @lager_addr1 = LAST_INSERT_ID();

INSERT INTO lager (lager_nr, lager_adresse_id, raum_anzahl)
VALUES (1, @lager_addr1, 4);

INSERT INTO raum (raum_nr, lager_nr, etage, groesse)
VALUES (1, 1, 1, 30),
       (2, 1, 2, 40);

-- Lager 2:
INSERT INTO adresse (land, stadt, strasse, haus_nr)
VALUES ('Österreich', 'Graz', 'Hauptstraße', '15');
SET @lager_addr2 = LAST_INSERT_ID();

INSERT INTO lager (lager_nr, lager_adresse_id, raum_anzahl)
VALUES (2, @lager_addr2, 3);

INSERT INTO raum (raum_nr, lager_nr, etage, groesse)
VALUES (1, 2, 1, 25),
       (2, 2, 2, 35);

-- Lager 3:
INSERT INTO adresse (land, stadt, strasse, haus_nr)
VALUES ('Österreich', 'Linz', 'Bahnhofstraße', '5');
SET @lager_addr3 = LAST_INSERT_ID();

INSERT INTO lager (lager_nr, lager_adresse_id, raum_anzahl)
VALUES (3, @lager_addr3, 5);

INSERT INTO raum (raum_nr, lager_nr, etage, groesse)
VALUES (1, 3, 1, 50),
       (2, 3, 2, 60);
COMMIT;

-- kategorien, artikel und links zwischen artikel und raum.
START TRANSACTION;
-- 3 kategorien:
INSERT INTO kategorie (ueber_kategorie, bezeichnung, color_code)
VALUES (NULL, 'Elektronik', '#FF0000');
SET @cat1 = LAST_INSERT_ID();

INSERT INTO kategorie (ueber_kategorie, bezeichnung, color_code)
VALUES (NULL, 'Bücher', '#00FF00');
SET @cat2 = LAST_INSERT_ID();

INSERT INTO kategorie (ueber_kategorie, bezeichnung, color_code)
VALUES (NULL, 'Kleidung', '#0000FF');
SET @cat3 = LAST_INSERT_ID();

-- Ketegorie 1 (Elektronik): 2 artikel einfuegen:
INSERT INTO artikel (kategorie_nr, bezeichnung, preis_cent)
VALUES (@cat1, 'Smartphone', 50000);
SET @art1 = LAST_INSERT_ID();

INSERT INTO artikel (kategorie_nr, bezeichnung, preis_cent)
VALUES (@cat1, 'Laptop', 80000);
SET @art2 = LAST_INSERT_ID();

-- Kategorie 2 (Bücher), 2 artikel einfuegen:
INSERT INTO artikel (kategorie_nr, bezeichnung, preis_cent)
VALUES (@cat2, 'Database Design', 3500);
SET @art3 = LAST_INSERT_ID();

INSERT INTO artikel (kategorie_nr, bezeichnung, preis_cent)
VALUES (@cat2, 'Learning SQL', 2500);
SET @art4 = LAST_INSERT_ID();

-- Kategorie 3 (Kleidung),  2 artikel einfuegen:
INSERT INTO artikel (kategorie_nr, bezeichnung, preis_cent)
VALUES (@cat3, 'T-Shirt', 1500);
SET @art5 = LAST_INSERT_ID();

INSERT INTO artikel (kategorie_nr, bezeichnung, preis_cent)
VALUES (@cat3, 'Jeans', 3000);
SET @art6 = LAST_INSERT_ID();

-- artikel mit raum verbinden:
INSERT INTO artikel_raum (raum_nr, lager_nr, artikel_nr, anzahl)
VALUES (1, 1, @art1, 15),
       (2, 1, @art2, 10),
       (1, 2, @art3, 20),
       (2, 2, @art4, 25),
       (1, 3, @art5, 50),
       (2, 3, @art6, 40);
COMMIT;

-- Kunde, Bestellung, Bestellung_Artikel.
START TRANSACTION;
-- 3 Rechnungsadressen:
INSERT INTO adresse (land, stadt, strasse, haus_nr)
VALUES ('Österreich', 'Wien', 'Teststraße', '1B');
SET @cust_addr1 = LAST_INSERT_ID();

INSERT INTO adresse (land, stadt, strasse, haus_nr)
VALUES ('Österreich', 'Graz', 'Marktplatz', '3B');
SET @cust_addr2 = LAST_INSERT_ID();

INSERT INTO adresse (land, stadt, strasse, haus_nr)
VALUES ('Österreich', 'Linz', 'Rathausplatz', '7');
SET @cust_addr3 = LAST_INSERT_ID();

-- 3 Kunden:
-- Kunde 1 (Firmenkunde)
INSERT INTO kunde (rechnungs_adresse_id, firmen_kunde, status_vip)
VALUES (@cust_addr1, TRUE, TRUE);
SET @kunde1 = LAST_INSERT_ID();
INSERT INTO firmenkunde (kunde_nr, steuer_nr, firmen_name)
VALUES (@kunde1, 'ATU123456789', 'Firma Eins');

-- Kunde 2 (Firmenkunde)
INSERT INTO kunde (rechnungs_adresse_id, firmen_kunde, status_vip)
VALUES (@cust_addr2, TRUE, FALSE);
SET @kunde2 = LAST_INSERT_ID();
INSERT INTO firmenkunde (kunde_nr, steuer_nr, firmen_name)
VALUES (@kunde2, 'ATU987654321', 'Firma Zwei');

-- Kunde 3 (Privatkunde)
INSERT INTO kunde (rechnungs_adresse_id, firmen_kunde, status_vip)
VALUES (@cust_addr3, FALSE, FALSE);
SET @kunde3 = LAST_INSERT_ID();
INSERT INTO privatkunde (kunde_nr, vorname, nachname)
VALUES (@kunde3, 'Max', 'Mustermann');

-- Bestellungen:
-- Kunde 1:
INSERT INTO bestellung (kunde_nr, liefer_adresse_id)
VALUES (@kunde1, @lager_addr1); 
SET @bestell1 = LAST_INSERT_ID();
INSERT INTO bestellung_artikel (bestell_nr, artikel_nr)
VALUES (@bestell1, @art1),
       (@bestell1, @art3);

-- Kunde 2:
INSERT INTO bestellung (kunde_nr, liefer_adresse_id)
VALUES (@kunde2, @lager_addr2);
SET @bestell2 = LAST_INSERT_ID();
INSERT INTO bestellung_artikel (bestell_nr, artikel_nr)
VALUES (@bestell2, @art5);

-- Kunde 3:
INSERT INTO bestellung (kunde_nr, liefer_adresse_id)
VALUES (@kunde3, @lager_addr3);
SET @bestell3 = LAST_INSERT_ID();
INSERT INTO bestellung_artikel (bestell_nr, artikel_nr)
VALUES (@bestell3, @art2), (@bestell3, @art4),(@bestell3, @art6);

COMMIT;