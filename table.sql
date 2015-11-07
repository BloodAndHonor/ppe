create table device_info (
	number varchar(15) primary key not null,
	name varchar(20),
	category_number varchar(10),
	model varchar(50),
	specification varchar(50),
	price varchar(10),
	vender varchar(50),
	buy_date timestamp,
	status varchar(15),
	funds_category varchar(15),
	use_direction varchar(15),
	device_source varchar(15),
	use_person varchar(10),
	handby_person varchar(10),
	record_person varchar(10),
	input_person varchar(10),
	in_date timestamp,
	document_number varchar(20),
	location varchar(20),
	remarks varchar(50),
	funds_card varchar(50),
	user varchar(50)
);

create table device_change_log (
	log_date timestamp,
	name varchar(20),
	number varchar(15) not null,
	count int,
	unit varchar(5),
	old_location varchar(20),
	new_location varchar(20),
	old_user varchar(10),
	new_user varchar(10)
);
