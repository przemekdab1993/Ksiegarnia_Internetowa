CREATE table user(
	id_user smallint auto_increment not null primary key,
    user_name varchar(32) not null,
    password varchar(16) not null,
    email varchar(128) not null,
    cash decimal(12,2) default 0,
    data_registration timestamp default current_timestamp
    );
    