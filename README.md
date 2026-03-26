



# 🏭 Vimko Inventory & Order Management App

## Overview

**Vimko App** is a Django + DRF project for managing products, dealers, inventory, and orders.
It handles **all business rules and edge cases**, including stock validation, order flow, and admin-only actions.

**Key Features:**

* Product management (create/list)
* Dealer management
* Inventory management (add/update)
* Order management (Draft → Confirm → Deliver)
* Stock deduction on order confirmation
* Admin-only inventory update
* API-ready with JSON responses

---

## 🔗 API Endpoints & Usage (With All Edge Cases)

---

### 1️⃣ Product API

* **Create Product**

```http
POST /api/products/
```

**Normal Case:**

```json
{
  "name": "Brake Pad",
  "price": 500
}
```

**Edge Cases:**

1. Missing `name`

```json
{
  "price": 500
}
```

❌ Fail → `400 Bad Request`

2. Negative `price`

```json
{
  "name": "Brake Pad",
  "price": -100
}
```

❌ Fail → `400 Bad Request`

3. Duplicate name (if unique constraint)

```json
{
  "name": "Brake Pad",
  "price": 600
}
```

❌ Fail → `400 Bad Request`

* **List Products**

```http
GET /api/products/
```

---

### 2️⃣ Dealer API

* **Create Dealer**

```http
POST /api/dealers/
```

**Normal Case:**

```json
{
  "name": "ABC Dealer",
  "email": "abc@gmail.com",
  "phone": "9876543210",
  "address": "Delhi"
}
```

**Edge Cases:**

1. Invalid email

```json
{
  "name": "ABC",
  "email": "wrong",
  "phone": "123",
  "address": "Delhi"
}
```

❌ Fail → `400 Bad Request`

2. Missing phone

```json
{
  "name": "XYZ Dealer",
  "email": "xyz@gmail.com",
  "address": "Mumbai"
}
```

❌ Fail → `400 Bad Request`

* **List Dealers**

```http
GET /api/dealers/
```

---

### 3️⃣ Inventory API

* **Add Inventory**

```http
POST /api/inventory/add/
```

**Normal Case:**

```json
{
  "product": 1,
  "quantity": 100
}
```

**Edge Cases:**

1. Product does not exist

```json
{
  "product": 999,
  "quantity": 50
}
```

❌ Fail → `404 Not Found`

2. Negative quantity

```json
{
  "product": 1,
  "quantity": -10
}
```

❌ Fail → `400 Bad Request`

3. Zero quantity

```json
{
  "product": 1,
  "quantity": 0
}
```

❌ Fail → `400 Bad Request`

* **Check Inventory**

```http
GET /api/inventory/
```

* **Admin Update Inventory**

```http
PUT /api/inventory/1/
```

**Body:**

```json
{
  "quantity": 200
}
```

**Edge Cases:**

1. Without admin → `403 Forbidden`
2. Wrong product ID → `404 Not Found`
3. Negative quantity → `400 Bad Request`

---

### 4️⃣ Orders API

* **Create Order (Draft)**

```http
POST /api/orders/
```

**Normal Case:**

```json
{
  "dealer": 1,
  "items": [{"product": 1, "quantity": 10}]
}
```

**Edge Cases:**

1. Zero quantity

```json
{
  "dealer": 1,
  "items": [{"product":1, "quantity":0}]
}
```

❌ Fail → `400 Bad Request`

2. Negative quantity

```json
{
  "dealer": 1,
  "items": [{"product":1, "quantity":-5}]
}
```

❌ Fail → `400 Bad Request`

3. Product does not exist

```json
{
  "dealer": 1,
  "items": [{"product":999, "quantity":5}]
}
```

❌ Fail → `404 Not Found`

4. Dealer does not exist

```json
{
  "dealer": 999,
  "items": [{"product":1, "quantity":5}]
}
```

❌ Fail → `404 Not Found`

5. Empty items

```json
{
  "dealer": 1,
  "items": []
}
```

❌ Fail → `400 Bad Request`

* **Confirm Order**

```http
POST /api/orders/1/confirm/
```

✔ Stock is deducted automatically

**Edge Cases:**

1. Already confirmed

```http
POST /api/orders/1/confirm/
```

❌ Fail → `400 Bad Request`

2. Insufficient stock (if order quantity > available)

```json
{
  "error": "Insufficient stock"
}
```

3. Non-existent order

```http
POST /api/orders/999/confirm/
```

❌ Fail → `404 Not Found`

* **Deliver Order**

```http
POST /api/orders/1/deliver/
```

✔ Status = Delivered

**Edge Cases:**

1. Deliver without confirm

```http
POST /api/orders/2/deliver/
```

❌ Fail → `400 Bad Request`

2. Already delivered

```http
POST /api/orders/1/deliver/
```

❌ Fail → `400 Bad Request`

3. Non-existent order

```http
POST /api/orders/999/deliver/
```

❌ Fail → `404 Not Found`

---

## 🧠 Business Logic Flow

1. Product → Dealer → Inventory → Order Draft → Confirm → Deliver
2. Stock deducted **only on confirm**
3. Admin-only inventory updates
4. All endpoints validate **missing/negative fields, existence, and permissions**

---

## ✅ Postman Testing Sequence

1. Create Product (normal + edge)
2. Create Dealer (normal + edge)
3. Add Inventory (normal + edge)
4. Create Order (Draft) (normal + edge)
5. Confirm Order → check stock deduction
6. Deliver Order
7. Admin updates inventory if needed

---

## 📝 Run Locally

```bash
# Clone repo
git clone <repo-url>
cd vimko_project

# Install dependencies
pip install -r requirements.txt

# Migrate database
python manage.py migrate

# Create superuser (admin)
python manage.py createsuperuser

# Run server
python manage.py runserver
```

**Visit:** `http://127.0.0.1:8000/`

---


