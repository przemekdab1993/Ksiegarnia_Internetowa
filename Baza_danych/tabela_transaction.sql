create table transactions(
	id_order int primary key auto_increment,
    id_ksiazki smallint,
    id_user smallint not null,
    name varchar(128) not null,
    data_order timestamp default current_timestamp,
    cost decimal(8,2) not null,
    
    foreign key (id_ksiazki) references ksiazki(id_ksiazki),
    foreign key (id_user) references user(id_user)
    );