create table orders
(
	order_id int auto_increment,
	customer_id int not null,
	datetime_placed datetime not null,
	constraint orders_pk
		primary key (order_id)
);
