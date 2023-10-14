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
    status text not null default 'NEW', -- [NEW, PAID], could use separate table of possible statuses with many to one relation
    discount real default 0,
    paid real default 0,
    returns real default 0
    -- total will be calculated on the fly for simplicity and consistency,
    -- this could be saved later if performance is an issue
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
    original_id references order_products(id),
    product_id references products(id),
    quantity integer
)