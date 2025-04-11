SET @filter_date = '2025-04-01';

SELECT
    b.bestell_nr, 
    b.datum,
    k.kunde_nr,
    -- Kundenname (Firmenkunde oder Privatkunde)
    IF(fk.firmen_name IS NOT NULL, fk.firmen_name, CONCAT(pk.vorname, ' ', pk.nachname)) AS kunde_name,
    -- Stadt der Lieferadresse
    liefer_adresse.stadt AS liefer_stadt,
    a.artikel_nr,
    a.bezeichnung AS artikel_bezeichnung,
    kategorie.bezeichnung AS kategorie
FROM bestellung b
    -- Join Kundendaten
    JOIN kunde k ON b.kunde_nr = k.kunde_nr
    LEFT JOIN privatkunde pk ON k.kunde_nr = pk.kunde_nr
    LEFT JOIN firmenkunde fk ON k.kunde_nr = fk.kunde_nr
    -- Join Lieferadresse der Bestellung
    JOIN adresse liefer_adresse ON b.liefer_adresse_id = liefer_adresse.adresse_id
    -- Join Bestellartikeln (mix table)
    JOIN bestellung_artikel ba ON b.bestell_nr = ba.bestell_nr
    JOIN artikel a ON ba.artikel_nr = a.artikel_nr
    -- Join Kategorie
    LEFT JOIN kategorie kategorie ON a.kategorie_nr = kategorie.kategorie_nr
WHERE b.datum >= @filter_date
ORDER BY b.datum DESC, b.bestell_nr;
