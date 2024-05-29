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
  "created_by" int NOT NULL,
  "category_id" int NOT NULL,
  "original_price" float,
  "stock" int,
  "brand" varchar(255),
  "slug" varchar(255),
  "product_description" text,
  "customer" int
);

CREATE TABLE "product_image" (
  "product_img_id" int PRIMARY KEY,
  "product_id" int,
  "product_img_url" varchar,
  "is_main" bool
);

CREATE TABLE "discount" (
  "discount_id" int PRIMARY KEY,
  "name" varchar(100),
  "discount_percent" float
);

CREATE TABLE "product_discount" (
  "product_discount_id" int PRIMARY KEY,
  "product_id" int,
  "discount_id" int,
  "start_date" timestamp,
  "end_date" timestamp
);

CREATE TABLE "order_product_discount" (
  "order_product_discount" int PRIMARY KEY,
  "order_product_id" int,
  "discount_id" int
);

CREATE TABLE "payment" (
  "payment_id" int PRIMARY KEY NOT NULL,
  "order_id" int NOT NULL,
  "payment_mode" varchar(255),
  "customer_id" int NOT NULL,
  "date_of_payment" date
);

CREATE TABLE "cart" (
  "cart_id" int PRIMARY KEY NOT NULL,
  "grand_total" float,
  "items_total" int
);

CREATE TABLE "cart_product" (
  "cart_product_id" int PRIMARY KEY NOT NULL,
  "cart_id" int NOT NULL,
  "product_id" int NOT NULL,
  "quantity" int
);

CREATE TABLE "review" (
  "review_id" int PRIMARY KEY NOT NULL,
  "review_content" text,
  "review_rating" varchar(255),
  "review_date" timestamp,
  "product_id" int NOT NULL,
  "customer_id" int NOT NULL
);

CREATE TABLE "vendor" (
  "vendor_id" int PRIMARY KEY,
  "vendor_name" varchar(255),
  "description" text,
  "vendor_logo" varchar(200)
);

CREATE TABLE "customer" (
  "customer_id" int PRIMARY KEY,
  "cart_id" int,
  "fullname" varchar(30),
  "date_of_birth" date,
  "age" smallint,
  "avatar_url" varchar(200)
);

CREATE TABLE "user" (
  "user_id" int PRIMARY KEY,
  "address_id" int,
  "email" varchar(50),
  "phone" varchar(20)
);

CREATE TABLE "category" (
  "category_id" int PRIMARY KEY,
  "category_name" varchar(255),
  "slug" varchar(255),
  "category_img_url" varchar(255)
);

CREATE TABLE "transaction" (
  "transaction_id" int PRIMARY KEY,
  "order_id" int UNIQUE,
  "payment_id" int UNIQUE,
  "total_money" float
);

CREATE TABLE "address" (
  "address_id" int PRIMARY KEY NOT NULL,
  "province_id" int,
  "address_detail" varchar(200)
);

CREATE TABLE "province" (
  "province_id" int PRIMARY KEY,
  "province_name" varchar(50),
  "province_name_en" varchar(50),
  "type" varchar(10)
);

CREATE TABLE "district" (
  "district_id" int PRIMARY KEY,
  "province_id" int,
  "district_name" varchar(50),
  "district_name_en" varchar(50),
  "type" varchar(15)
);

CREATE TABLE "ward" (
  "ward_id" int PRIMARY KEY,
  "ward_name" varchar(50),
  "ward_name_en" varchar(50),
  "province_id" int,
  "district_id" int,
  "type" varchar(10)
);

ALTER TABLE "order_product_discount" ADD FOREIGN KEY ("discount_id") REFERENCES "discount" ("discount_id");

ALTER TABLE "order_product_discount" ADD FOREIGN KEY ("order_product_id") REFERENCES "order_product" ("order_product_id");

ALTER TABLE "cart_product" ADD FOREIGN KEY ("cart_id") REFERENCES "cart" ("cart_id");

ALTER TABLE "cart_product" ADD FOREIGN KEY ("product_id") REFERENCES "product" ("product_id");

ALTER TABLE "address" ADD FOREIGN KEY ("province_id") REFERENCES "province" ("province_id");

ALTER TABLE "district" ADD FOREIGN KEY ("province_id") REFERENCES "province" ("province_id");

ALTER TABLE "ward" ADD FOREIGN KEY ("district_id") REFERENCES "district" ("district_id");

ALTER TABLE "ward" ADD FOREIGN KEY ("province_id") REFERENCES "province" ("province_id");

ALTER TABLE "vendor" ADD FOREIGN KEY ("vendor_id") REFERENCES "user" ("user_id");

ALTER TABLE "customer" ADD FOREIGN KEY ("customer_id") REFERENCES "user" ("user_id");

ALTER TABLE "payment" ADD FOREIGN KEY ("payment_id") REFERENCES "transaction" ("payment_id");

ALTER TABLE "order" ADD FOREIGN KEY ("order_id") REFERENCES "transaction" ("order_id");

ALTER TABLE "product_discount" ADD FOREIGN KEY ("discount_id") REFERENCES "discount" ("discount_id");

ALTER TABLE "product_discount" ADD FOREIGN KEY ("product_id") REFERENCES "product" ("product_id");

ALTER TABLE "order" ADD FOREIGN KEY ("customer_id") REFERENCES "customer" ("customer_id");

ALTER TABLE "order_product" ADD FOREIGN KEY ("order_id") REFERENCES "order" ("order_id");

ALTER TABLE "order_product" ADD FOREIGN KEY ("product_id") REFERENCES "product" ("product_id");

ALTER TABLE "product" ADD FOREIGN KEY ("created_by") REFERENCES "vendor" ("vendor_id");

ALTER TABLE "product" ADD FOREIGN KEY ("category_id") REFERENCES "category" ("category_id");

ALTER TABLE "payment" ADD FOREIGN KEY ("customer_id") REFERENCES "customer" ("customer_id");

ALTER TABLE "user" ADD FOREIGN KEY ("address_id") REFERENCES "address" ("address_id");

ALTER TABLE "order" ADD FOREIGN KEY ("address_id") REFERENCES "address" ("address_id");

ALTER TABLE "customer" ADD FOREIGN KEY ("cart_id") REFERENCES "cart" ("cart_id");

ALTER TABLE "review" ADD FOREIGN KEY ("customer_id") REFERENCES "customer" ("customer_id");

ALTER TABLE "review" ADD FOREIGN KEY ("product_id") REFERENCES "product" ("product_id");

ALTER TABLE "product_image" ADD FOREIGN KEY ("product_id") REFERENCES "product" ("product_id");
