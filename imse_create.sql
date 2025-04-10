DROP DATABASE IF EXISTS db;
CREATE DATABASE db;
USE db;


CREATE TABLE adresse (
    adresse_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    land VARCHAR(50) NOT NULL,
    stadt VARCHAR(50) NOT NULL,
    strasse VARCHAR(50) NOT NULL,
    haus_nr VARCHAR(50) NOT NULL, -- use string in case of stiege / tuer, etc.
    UNIQUE (land, stadt, strasse, haus_nr)  -- keine duplicate adressen
);

CREATE TABLE bestellung (
    bestell_nr INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    datum DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    liefer_adresse_id INT UNSIGNED NOT NULL,
    FOREIGN KEY (liefer_adresse_id) REFERENCES adresse(adresse_id)
);

CREATE TABLE lager (
  lager_nr INT UNSIGNED PRIMARY KEY, 
  lager_adresse_id INT UNSIGNED UNIQUE,
  raum_anzahl INT UNSIGNED NOT NULL, 
  FOREIGN KEY (lager_adresse_id) REFERENCES adresse(adresse_id)
);

CREATE TABLE raum (
  raum_nr INT UNSIGNED NOT NULL, -- raum nummern sind unique pro lager. etage ist nur eine Zusatzinfo.
  etage INT UNSIGNED NOT NULL, 
  groesse INT UNSIGNED NOT NULL, -- todo: oe?? bessere bezeichnung?
  lager_nr INT UNSIGNED NOT NULL,  -- lager in dem sich der raum befindet
  PRIMARY KEY (raum_nr, lager_nr),  -- pk der weak entity, nur in kombination mit lager
  FOREIGN KEY (lager_nr) REFERENCES lager(lager_nr) ON DELETE CASCADE 
);

CREATE TABLE artikel (
    artikel_nr INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    bezeichnung VARCHAR(50) NOT NULL,
    preis_cent INT UNSIGNED NOT NULL,
    datum DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE artikel_raum (
    raum_nr INT UNSIGNED,
    lager_nr INT UNSIGNED,
    artikel_nr INT UNSIGNED,
    anzahl INT UNSIGNED,
    FOREIGN KEY (raum_nr) REFERENCES raum(raum_nr),
    FOREIGN KEY (lager_nr) REFERENCES lager(lager_nr)
    FOREIGN KEY (artikel_nr) REFERENCES artikel(artikel_nr)
    PRIMARY KEY (artikel_nr, raum_nr, lager_nr),  -- zussammengesetzter pk
);

CREATE TABLE bestellung_artikel (
    bestellung_artikel_nr INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    bestell_nr INT UNSIGNED,
    artikel_nr INT UNSIGNED,
    FOREIGN KEY (bestell_nr) REFERENCES bestellung(bestell_nr),
    FOREIGN KEY (artikel_nr) REFERENCES artikel(artikel_nr)
);

CREATE TABLE kategorie (
    kategorie_nr INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    ueber_kategorie INT UNSIGNED,
    bezeichnung VARCHAR(50) NOT NULL,
    color_code VARCHAR(50),
    FOREIGN KEY (ueber_kategorie) REFERENCES kategorie(kategorie_nr)
);

CREATE TABLE kunde (
  kunde_nr INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  datum DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  rechnungs_adresse_id INT UNSIGNED, -- todo: required? then need to save address first, or use lieferaddr as default??
  firmen_kunde BOOLEAN NOT NULL DEFAULT FALSE, -- to make queries for eg. name easier based on kunde_nr
  status_vip BOOLEAN NOT NULL DEFAULT FALSE, -- todo: could rm, used only because of 3 attributes requirement
  FOREIGN KEY (rechnungs_adresse_id) REFERENCES adresse(adresse_id)
);

CREATE TABLE privatkunde (
  kunde_nr INT UNSIGNED PRIMARY KEY,  -- referenziert kunde_nr in kunde tabelle
  vorname VARCHAR(50) NOT NULL,
  nachname VARCHAR(50) NOT NULL,
  FOREIGN KEY (kunde_nr) REFERENCES kunde(kunde_nr) ON DELETE CASCADE
);

CREATE TABLE firmenkunde (
  kunde_nr INT UNSIGNED PRIMARY KEY,  -- referenziert kunde_nr in kunde tabelle
  steuer_nr VARCHAR(20) UNIQUE, -- tin, atu?? some string i'd say
  firmen_name VARCHAR(50) NOT NULL,
  FOREIGN KEY (kunde_nr) REFERENCES kunde(kunde_nr) ON DELETE CASCADE
);

-- docker cp ./12134101_SCHORT_create.sql mariadb-container:/tmp/create1.sql
