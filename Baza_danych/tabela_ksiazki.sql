CREATE table ksiazki(
	id_ksiazki smallint auto_increment primary key not null,
    tytul text not null,
    gatunek varchar(32) not null,
    imie_autora varchar(32) not null,
    nazwisko_autora varchar(32) not null,
    wydawnictwo text not null,
    rok_wydania year not null,
    cena numeric(8,2) not null, 
    liczba_ocen int,
    ocena decimal(6,6),
    data_dodania timestamp default current_timestamp
    );
    