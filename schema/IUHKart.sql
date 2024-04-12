CREATE TABLE "order" (
  "order_id" int PRIMARY KEY NOT NULL,
  "order_number" varchar(255),
  "shipping_date" date,
  "order_date" date,
  "order_amount" float,
  "order_status" varchar(255),
  "customer_id" int NOT NULL,
  "address_id" int
);

CREATE TABLE "order_product" (
  "order_product_id" int PRIMARY KEY NOT NULL,
  "product_id" int NOT NULL,
  "order_id" int NOT NULL,
  "price" float,
  "quantity" int
);

CREATE TABLE "product" (
  "product_id" int PRIMARY KEY NOT NULL,
  "product_name" varchar(255),
  "vendor_id" int NOT NULL,
  "category_id" int NOT NULL,
  "original_price" float,
  "stock" int,
  "brand" varchar(255)
);

CREATE TABLE "product_image" (
  "product_img_id" int PRIMARY KEY,
  "product_id" int,
  "product_img_url" varchar
);

CREATE TABLE "discount" (
  "discount_id" int PRIMARY KEY,
  "percentage" float
);

CREATE TABLE "product_discount" (
  "product_discount_id" int PRIMARY KEY,
  "product_id" int,
  "discount_id" int,
  "start_date" timestamp,
  "end_date" timestamp,
  "price_after_discount" float,
  "invoice_id" int
);

CREATE TABLE "payment" (
  "payment_id" int PRIMARY KEY NOT NULL,
  "order_id" int NOT NULL,
  "payment_mode" varchar(255),
  "customer_id" int NOT NULL,
  "date_of_payment" date
);

CREATE TABLE "address" (
  "address_id" int PRIMARY KEY NOT NULL,
  "city_province" varchar(100),
  "address_detail" varchar(200)
);

CREATE TABLE "cart" (
  "cart_id" int PRIMARY KEY NOT NULL,
  "product_id" int NOT NULL,
  "customer_id" int UNIQUE NOT NULL,
  "grand_total" float,
  "items_total" int
);

CREATE TABLE "review" (
  "review_id" int PRIMARY KEY NOT NULL,
  "description" text,
  "ratings" varchar(255),
  "product_id" int NOT NULL,
  "customer_id" int NOT NULL
);

CREATE TABLE "vendor" (
  "vendor_id" int PRIMARY KEY NOT NULL,
  "address_id" int,
  "name" varchar(255),
  "phone" varchar(20),
  "email" varchar(50),
  "description" text
);

CREATE TABLE "category" (
  "category_id" int PRIMARY KEY NOT NULL,
  "category_name" varchar(255),
  "slug" varchar(255),
  "category_img_url" varchar(255)
);

CREATE TABLE "category_product" (
  "category_product_id" int PRIMARY KEY,
  "category_id" int,
  "product_id" int
);

CREATE TABLE "customer" (
  "customer_id" int PRIMARY KEY,
  "address_id" int,
  "fullname" varchar(30),
  "email" varchar(50),
  "date_of_birth" date,
  "phone" varchar(20),
  "age" smallint,
  "avatar_url" varchar(200)
);

CREATE TABLE "invoice" (
  "invoice_id" int PRIMARY KEY,
  "order_id" int UNIQUE,
  "payment_id" int UNIQUE,
  "total_money" float
);

ALTER TABLE "category_product" ADD FOREIGN KEY ("category_id") REFERENCES "category" ("category_id");

ALTER TABLE "category_product" ADD FOREIGN KEY ("product_id") REFERENCES "product" ("product_id");

ALTER TABLE "product_discount" ADD FOREIGN KEY ("invoice_id") REFERENCES "invoice" ("invoice_id");

ALTER TABLE "payment" ADD FOREIGN KEY ("payment_id") REFERENCES "invoice" ("payment_id");

ALTER TABLE "order" ADD FOREIGN KEY ("order_id") REFERENCES "invoice" ("order_id");

ALTER TABLE "product_discount" ADD FOREIGN KEY ("discount_id") REFERENCES "discount" ("discount_id");

ALTER TABLE "product_discount" ADD FOREIGN KEY ("product_id") REFERENCES "product" ("product_id");

ALTER TABLE "order" ADD FOREIGN KEY ("customer_id") REFERENCES "customer" ("customer_id");

ALTER TABLE "order_product" ADD FOREIGN KEY ("order_id") REFERENCES "order" ("order_id");

ALTER TABLE "order_product" ADD FOREIGN KEY ("product_id") REFERENCES "product" ("product_id");

ALTER TABLE "product" ADD FOREIGN KEY ("vendor_id") REFERENCES "vendor" ("vendor_id");

ALTER TABLE "product" ADD FOREIGN KEY ("category_id") REFERENCES "category" ("category_id");

ALTER TABLE "payment" ADD FOREIGN KEY ("customer_id") REFERENCES "customer" ("customer_id");

ALTER TABLE "customer" ADD FOREIGN KEY ("address_id") REFERENCES "address" ("address_id");

ALTER TABLE "vendor" ADD FOREIGN KEY ("address_id") REFERENCES "address" ("address_id");

ALTER TABLE "order" ADD FOREIGN KEY ("address_id") REFERENCES "address" ("address_id");

ALTER TABLE "customer" ADD FOREIGN KEY ("customer_id") REFERENCES "cart" ("customer_id");

ALTER TABLE "cart" ADD FOREIGN KEY ("product_id") REFERENCES "product" ("product_id");

ALTER TABLE "review" ADD FOREIGN KEY ("customer_id") REFERENCES "customer" ("customer_id");

ALTER TABLE "review" ADD FOREIGN KEY ("product_id") REFERENCES "product" ("product_id");

ALTER TABLE "product_image" ADD FOREIGN KEY ("product_id") REFERENCES "product" ("product_id");
