-- usecase 1: is-A relation:
-- neuer Firmenkunden registriert sich und führt Bestellung aus:

-- satisfy precondition: Artikel mit dependencies anlegen:
START TRANSACTION;

-- Adresse für Lager:
INSERT INTO adresse (land, stadt, strasse, haus_nr)
VALUES ('Österreich', 'Wien', 'Karlplatz', '22');
SET @adresse_id1 = LAST_INSERT_ID();

-- Lager:
INSERT INTO lager (lager_nr, lager_adresse_id, raum_anzahl)
VALUES (NULL, @adresse_id1, 20);
SET @lager_nr = LAST_INSERT_ID();

-- Raum:
INSERT INTO raum (raum_nr, lager_nr, etage, groesse)
VALUES (1, @lager_nr, 1, 20);
SET @raum_nr = 1;
COMMIT;

START TRANSACTION;
-- Kategorie:
INSERT INTO kategorie (ueber_kategorie, bezeichnung, color_code)
VALUES (NULL, 'Testkategorie', '#FF0000');
SET @kategorie_id = LAST_INSERT_ID();

-- Artikel:
INSERT INTO artikel (kategorie_nr, bezeichnung, preis_cent)
VALUES (@kategorie_id, 'Testartikel', 2500);
SET @artikel_nr = LAST_INSERT_ID();

-- Lagerbestand:
INSERT INTO artikel_raum (raum_nr, lager_nr, artikel_nr, anzahl)
VALUES (@raum_nr, @lager_nr, @artikel_nr, 10); -- 10 Stück Testartikel sind in Raum 1 lagernd
COMMIT;


-- usecase 1:
-- neuer Firmenkunden registriert sich und führt Bestellung aus:
START TRANSACTION;
-- Rechnungsadresse:
INSERT INTO adresse (land, stadt, strasse, haus_nr)
VALUES ('Österreich', 'Wien', 'Teststraße', '11C');
SET @adresse_id2 = LAST_INSERT_ID();

-- Kunde:
INSERT INTO kunde (rechnungs_adresse_id, firmen_kunde, status_vip)
VALUES (@adresse_id2, TRUE, FALSE);
SET @kunde_nr = LAST_INSERT_ID();

-- Firmenkunde:
INSERT INTO firmenkunde (kunde_nr, steuer_nr, firmen_name)
VALUES (@kunde_nr, 'ATU122345578', 'Test GmbH');

-- Bestellung
INSERT INTO bestellung (kunde_nr, liefer_adresse_id)
VALUES (@kunde_nr, @adresse_id1);
SET @bestell_nr = LAST_INSERT_ID();

-- bestellung_artikel
INSERT INTO bestellung_artikel (bestell_nr, artikel_nr)
VALUES (@bestell_nr, @artikel_nr);
COMMIT;