drop table if exists products;
drop table if exists orders;
drop table if exists order_products;
drop table if exists replacements;

create table products (
    id integer primary key autoincrement,
    name text not null,
    price real not null
);

create table orders (
    id text primary key,
    status text not null default 'NEW' -- [NEW, PAID]
);

create table order_products (
    id text primary key, -- uuid from python side
    order_id references orders(id),
    product_id references products(id),
    quantity integer not null,
    unique (order_id, product_id)
);

create table replacements (
    id text primary key,
    order_id references orders(id),
    original_id references order_products(id),
    product_id references products(id),
    quantity integer,
    unique (order_id, original_id)  -- each product in an order can have one replacement
)