create table order_items
(
	order_id int null,
	item_id int null,
	quantity int not null,
	purchase_unit_price float not null,
	constraint orders_items_pk
		unique (order_id, item_id)
);
