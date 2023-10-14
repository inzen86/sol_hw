insert into orders (id, status, discount, paid, returns)
values ('d4df8b90-8f4e-4fd5-bbf2-4dd6f366bb86', 'PAID', 0.0, 0.0, 0.0);

insert into order_products (id, order_id, product_id, quantity)
values ('4bacc3dd-30b7-4193-bc77-16d046804d54', 'd4df8b90-8f4e-4fd5-bbf2-4dd6f366bb86', 123, 2),
       ('0248dfb0-d50c-4e37-a8b6-4d2d29d53a4d', 'd4df8b90-8f4e-4fd5-bbf2-4dd6f366bb86', 456, 6),
       ('1d277343-0b0a-48db-b668-aa518b0bbc30', 'd4df8b90-8f4e-4fd5-bbf2-4dd6f366bb86', 879, 4);

insert into order_products (id, order_id, product_id, quantity)
values ('91941753-3f45-4742-89d4-755438a2a01f', 'd4df8b90-8f4e-4fd5-bbf2-4dd6f366bb86', 999, 1);
insert into replacements (id, original_id, product_id, quantity)
values ('5de14f8a-c49e-4dcd-b3b4-fe7ab9c6daa8', '91941753-3f45-4742-89d4-755438a2a01f', 456, 3);