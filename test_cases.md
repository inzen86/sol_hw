## GET /api/products

- [x] GET /api/products
- [x] GET /api/produ
- [x] GET /api/products/asd
- [X] GET /api
- [x] GET /ap
- [x] POST /api/products
- [x] POST /api/produ
- [x] POST /api/products/asd
- [x] POST /api
- [x] POST /ap

## POST /api/orders

- [x] POST /api/orders
- [x] POST /api/order
- [x] POST /api/orders/asd
- [x] GET /api/orders
- [x] GET /api/order
- [x] GET /api/orders/asd

## GET /api/orders/:order_id

- [x] GET /api/orders/62c4f7bf-9484-4c4b-83af-e749fb8246d2
    - new untouched order
- [x] GET /api/orders/62c4f7bf-9484-4c4b-83af-e749fb8246d
    - wrong order id
- [x] POST /api/orders/62c4f7bf-9484-4c4b-83af-e749fb8246d2
    - wrong method

## PATCH /api/orders/:order_id

- [x] PATCH /api/orders/62c4f7bf-9484-4c4b-83af-e749fb8246d2
    - header Content-Type: application/json
    - body {"status": "PAID"}
        1. uus order
        2. muuda status PAID
- [x] PATCH /api/orders/
    - header Content-Type: application/json
    - body {"status": "PAID"}
    - No order id
- [x] PATCH /api/orders/orders/4c189c70-2ef3-405d-9511-a1a8c6645181
    - header Content-Type: application/json
    - body {"status": "PAID"}
    - Invalid json
- [x] PATCH /api/orders/orders/4c189c70-2ef3-405d-9511-a1a8c6645181
    - header Content-Type: application/json
    - body {"status": "PAID"}
    - order on juba PAID

## GET /api/orders/:order_id/products

- [x] GET /api/orders/:order_id/products
    - tühi tellimus
- [x] GET /api/orders/:order_id/products
    - tootega
- [x] GET /api/orders/:order_id/products
    - tellimust ei ole
- [x] GET /api/orders/:order_id/products/asdf
    - tellimus on olemas

## POST /api/orders/:order_id/products

- [x] POST /api/orders/:order_id/products
    - headers - Content-Type: application/json
    - body - [123]
    - status: NEW
    - tellimus on olemas
- [x] POST /api/orders/:order_id/products
    - headers - Content-Type: application/json
    - body - [123]
    - status: PAID
    - tellimus on olemas
- [x] POST /api/orders/:order_id/products
    - headers - Content-Type: application/json
    - body - [123]
    - tellimust pole olemas
- [x] POST /api/orders/:order_id/products
    - headers - Content-Type: application/json
    - body - [123m,./]
    - status: NEW
    - tellimus on olemas
    - vigane json
- [x] POST /api/orders/:order_id/products
    - headers - Content-Type: application/json
    - body - []
    - status: NEW
    - tellimus on olemas
    - tühi list json
- [x] POST /api/orders/:order_id/products
    - headers - Content-Type: application/json
    - body -
    - status: NEW
    - tellimus on olemas
    - tühi body

## PATCH /api/orders/:order_id/products/:product_id  quantity
- [x] PATCH /api/orders/:order_id/products/:product_id
    - header - Content-Type: application/json
    - body - {"quantity": 33}
    - status: NEW
    - toode on
- [x] PATCH /api/orders/:order_id/products/:product_id
    - header - Content-Type: application/json
    - body - {"quantity": 33}
    - status: PAID
    - toode on
- [x] PATCH /api/orders/:order_id/products/:product_id
    - header - Content-Type: application/json
    - body - {"quantity": 33}
    - tellimus on
    - toodet pole olemas
- [x] PATCH /api/orders/:order_id/products/:product_id
    - header - Content-Type: application/json
    - body - {"quantity": 33}
    - tellimust ega toodet pole olemas
- [x] PATCH /api/orders/:order_id/products/:product_id
    - header - Content-Type: application/json
    - body - {"quantity": 33},./
    - vigane json
- [x] PATCH /api/orders/:order_id/products/:product_id
    - header - Content-Type: application/json
    - body - {}
    - tühi objekt
- [x] PATCH /api/orders/:order_id/products/:product_id
    - header - Content-Type: application/json
    - body -
    - tühi body

## PATCH /api/orders/:order_id/products/:product_id  replaced_with
- [x] PATCH /api/orders/:order_id/products/:product_id
  - header - Content-Type: application/json
  - body - {"replaced_with": {"product_id": 123, "quantity": 6}}
  - status: NEW
  - toode on
- [x] PATCH /api/orders/:order_id/products/:product_id
  - header - Content-Type: application/json
  - body - {"replaced_with": {"product_id": 123, "quantity": 6}}
  - status: PAID
  - toode on
- [x] PATCH /api/orders/:order_id/products/:product_id
  - header - Content-Type: application/json
  - body - {"replaced_with": {"product_id": 123, "quantity": 6}}
  - tellimus on
  - toodet pole olemas
- [x] PATCH /api/orders/:order_id/products/:product_id
  - header - Content-Type: application/json
  - body - {"replaced_with": {"product_id": 123, "quantity": 6}}
  - tellimust ega toodet pole olemas
- [x] PATCH /api/orders/:order_id/products/:product_id
  - header - Content-Type: application/json
  - body - {"replaced_with": {"product_id": 123, "quantity": 6}}
  - vigane json
- [x] PATCH /api/orders/:order_id/products/:product_id
  - header - Content-Type: application/json
  - body - {"replaced_with": {"product_id": 123, "quantity": "ASD"}}
  - vigane json
- [x] PATCH /api/orders/:order_id/products/:product_id
  - header - Content-Type: application/json
  - body - {"replaced_with": {"product_id": "asd, "quantity": 6}}
  - vigane json
- [x] PATCH /api/orders/:order_id/products/:product_id
  - header - Content-Type: application/json
  - body - {"replaced_with": {"product_id": "asd, "quantity": 6}}
  - asenda sama tootega




Kui mul on aega üle

- arvuta total ja paid kui status muudetakse PAID olekusse, muuda get() nii, et NEW statusega arvutab total summa ja
  PAID statusega võtab tabelist