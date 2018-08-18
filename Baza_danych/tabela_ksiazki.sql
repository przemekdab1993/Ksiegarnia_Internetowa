CREATE table ksiazki(
	id_ksiazki int(12) auto_increment primary key not null,
    tytul text not null,
    gatunek varchar(32) not null,
    imie_autora varchar(32) not null,
    nazwisko_autora varchar(32) not null,
    wydawnictwo text not null,
    rok_wydania year not null,
    cena float not null 
    );
    