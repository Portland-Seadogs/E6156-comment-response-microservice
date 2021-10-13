-- auto-generated definition
create table orders
(
    order_id        int auto_increment
        primary key,
    customer_id     int      not null,
    datetime_placed datetime not null
);

