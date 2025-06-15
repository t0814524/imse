START TRANSACTION;

-- deleta all data
DELETE FROM artikel_raum;
DELETE FROM bestellung_artikel;
DELETE FROM bestellung;
DELETE FROM firmenkunde;
DELETE FROM privatkunde;
DELETE FROM kunde;
DELETE FROM artikel;
DELETE FROM kategorie;
DELETE FROM raum;
DELETE FROM lager;
DELETE FROM adresse;

-- reset auto increment to avoid that ids keep going up
ALTER TABLE artikel_raum AUTO_INCREMENT = 1;
ALTER TABLE bestellung_artikel AUTO_INCREMENT = 1;
ALTER TABLE bestellung AUTO_INCREMENT = 1;
ALTER TABLE firmenkunde AUTO_INCREMENT = 1;
ALTER TABLE privatkunde AUTO_INCREMENT = 1;
ALTER TABLE kunde AUTO_INCREMENT = 1;
ALTER TABLE artikel AUTO_INCREMENT = 1;
ALTER TABLE kategorie AUTO_INCREMENT = 1;
ALTER TABLE raum AUTO_INCREMENT = 1;
ALTER TABLE lager AUTO_INCREMENT = 1;
ALTER TABLE adresse AUTO_INCREMENT = 1;

COMMIT;
