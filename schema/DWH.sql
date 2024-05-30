CREATE TABLE "dim_product" (
  "product_id" int PRIMARY KEY NOT NULL,
  "product_name" varchar(255),
  "original_price" float,
  "price" float,
  "stock" int,
  "brand" varchar(255),
  "ratings" float,
  "date_add" date,
  "vendor_id" int NOT NULL,
  "category_id" int NOT NULL
);

CREATE TABLE "dim_vendor" (
  "vendor_id" int PRIMARY KEY NOT NULL,
  "name" varchar(255),
  "ratings" float,
  "date_join" date
);

CREATE TABLE "dim_customer" (
  "customer_id" int PRIMARY KEY,
  "fullname" varchar(30),
  "email" varchar(50),
  "date_of_birth" date,
  "phone" varchar(20),
  "age" int,
  "date_join" date,
  "avatar_url" varchar(200),
  "address_id" int NOT NULL,
  "list_product_rs" varchar(255)
);

CREATE TABLE "dim_order" (
  "order_id" int PRIMARY KEY NOT NULL,
  "order_number" varchar(255),
  "shipping_date" date,
  "order_date" date,
  "order_amount" float,
  "total_price" float,
  "order_status" varchar(255),
  "customer_id" int NOT NULL
);

CREATE TABLE "fact_order_product" (
  "order_product_id" int PRIMARY KEY NOT NULL,
  "product_id" int NOT NULL,
  "order_id" int NOT NULL,
  "quantity" int
);

CREATE TABLE "fact_review" (
  "review_id" int PRIMARY KEY NOT NULL,
  "description" text,
  "ratings" float,
  "product_id" int NOT NULL,
  "customer_id" int NOT NULL
);

CREATE TABLE "dim_category" (
  "category_id" int PRIMARY KEY NOT NULL,
  "category_name" varchar(255),
  "slug" varchar(255)
);

ALTER TABLE "dim_product" ADD FOREIGN KEY ("vendor_id") REFERENCES "dim_vendor" ("vendor_id");

ALTER TABLE "dim_product" ADD FOREIGN KEY ("category_id") REFERENCES "dim_category" ("category_id");

ALTER TABLE "dim_order" ADD FOREIGN KEY ("customer_id") REFERENCES "dim_customer" ("customer_id");

ALTER TABLE "fact_order_product" ADD FOREIGN KEY ("order_id") REFERENCES "dim_order" ("order_id");

ALTER TABLE "fact_order_product" ADD FOREIGN KEY ("product_id") REFERENCES "dim_product" ("product_id");

ALTER TABLE "fact_review" ADD FOREIGN KEY ("customer_id") REFERENCES "dim_customer" ("customer_id");

ALTER TABLE "fact_review" ADD FOREIGN KEY ("product_id") REFERENCES "dim_product" ("product_id");
