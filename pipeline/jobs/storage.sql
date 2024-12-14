CREATE TABLE IF NOT EXISTS store (
	id int PRIMARY KEY NOT NULL,
	name varchar(255),
	user_id int NOT NULL
);

CREATE TABLE IF NOT EXISTS customer (
	id int PRIMARY KEY NOT NULL,
	name varchar(255),
	user_id int NOT NULL
);

CREATE TABLE IF NOT EXISTS users (
	id int PRIMARY KEY NOT NULL,
	address_id int
);

CREATE TABLE IF NOT EXISTS address (
	id int PRIMARY KEY NOT NULL,
	province_id int
);

CREATE TABLE IF NOT EXISTS province (
	id int PRIMARY KEY NOT NULL,
	province_name varchar(255)
);

CREATE TABLE IF NOT EXISTS promotion (
	id int PRIMARY KEY NOT NULL,
	name varchar(255),
	discount float
);

CREATE TABLE IF NOT EXISTS promotion_product (
	id int PRIMARY KEY NOT NULL,
	promotion_id int,
	product_id int
);

CREATE TABLE IF NOT EXISTS category (
	id int PRIMARY KEY NOT NULL,
	name varchar(255)
);

CREATE TABLE IF NOT EXISTS product (
	id int PRIMARY KEY NOT NULL,
	shop_id int,
	category_id int
);

CREATE TABLE IF NOT EXISTS orders (
	id int PRIMARY KEY NOT NULL,
	customer_id int
);

CREATE TABLE IF NOT EXISTS order_product (
	id int PRIMARY KEY NOT NULL,
	order_id int,
	product_id int
);

ALTER TABLE "store" ADD FOREIGN KEY ("user_id") REFERENCES "users" ("id");

ALTER TABLE "customer" ADD FOREIGN KEY ("user_id") REFERENCES "users" ("id");

ALTER TABLE "users" ADD FOREIGN KEY ("address_id") REFERENCES "address" ("id");

ALTER TABLE "address" ADD FOREIGN KEY ("province_id") REFERENCES "province" ("id");

ALTER TABLE "product" ADD FOREIGN KEY ("category_id") REFERENCES "category" ("id");

ALTER TABLE "product" ADD FOREIGN KEY ("shop_id") REFERENCES "store" ("id");

ALTER TABLE "promotion_product" ADD FOREIGN KEY ("promotion_id") REFERENCES "promotion" ("id");

ALTER TABLE "promotion_product" ADD FOREIGN KEY ("product_id") REFERENCES "product" ("id");

ALTER TABLE "orders" ADD FOREIGN KEY ("customer_id") REFERENCES "customer" ("id");

ALTER TABLE "order_product" ADD FOREIGN KEY ("order_id") REFERENCES "orders" ("id");

ALTER TABLE "order_product" ADD FOREIGN KEY ("product_id") REFERENCES "product" ("id");