-- usecase 1: is-A relation:
-- neuen Firmenkunden eintragen:
--    addresse anlegen:
INSERT INTO adresse (land, stadt, strasse, haus_nr) 
VALUES
('Österreich', 'Wien', 'Teststraße', '1A')

--    kunde anlegen:
INSERT INTO kunde (rechnungs_adresse_id, firmen_kunde, status_vip) 
VALUES
(1, TRUE, FALSE), -- rechnungs_adresse_id von zuvor eingetragenen Adresse verwenden





-- -- steuer_id anhand der kunden_nr abfragen: easy
-- SELECT fk.steuer_nr
-- FROM firmenkunde fk
-- JOIN kunde k ON fk.kunde_nr = k.kunde_nr
-- WHERE k.kunde_nr = ?;

-- -- addresse anhand der kunden_nr abfragen: mit extra table...
-- -- gibt es andere anforderungen ausser isa und weak entity?

-- -- usecase 2: weak entity:
-- -- Neues Produkt aufnehmen und einlagern: aufwendig