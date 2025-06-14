-- Cleanup (safe for foreign keys)
START TRANSACTION;
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
COMMIT;
