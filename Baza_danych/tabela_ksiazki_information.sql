CREATE table ksiazki_information (
	id_ksiazki smallint not null unique,
    img_src varchar(64) not null,
    info_1 text,
    info_2 text,
    info_3 text,

    foreign key (id_ksiazki) references ksiazki(id_ksiazki)
);