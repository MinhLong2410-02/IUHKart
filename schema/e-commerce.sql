CREATE TABLE "Order" (
  "OrderId" int PRIMARY KEY NOT NULL,
  "OrderNumber" varchar(255),
  "ShippingDate" date,
  "OrderDate" date,
  "OrderAmount" float,
  "OrderStatus" varchar(255),
  "Cart_CartId" int NOT NULL,
  "CustomerId" int NOT NULL,
  "AddressId" int
);

CREATE TABLE "OrderProduct" (
  "OrderProductId" int PRIMARY KEY NOT NULL,
  "ProductId" int NOT NULL,
  "OrderId" int NOT NULL,
  "Price" float,
  "Quantity" int
);

CREATE TABLE "Product" (
  "ProductId" int PRIMARY KEY NOT NULL,
  "ProductName" varchar(255),
  "CategoryId" int NOT NULL,
  "VendorId" int NOT NULL,
  "OriginalPrice" float,
  "Stock" int,
  "Brand" varchar(255)
);

CREATE TABLE "ProductImage" (
  "ProductImgId" int PRIMARY KEY,
  "ProductId" int,
  "ProductImgUrl" varchar
);

CREATE TABLE "Discount" (
  "DiscountId" int PRIMARY KEY,
  "Percentage" float
);

CREATE TABLE "ProductDiscount" (
  "ProductDiscountId" int PRIMARY KEY,
  "ProductId" int,
  "DiscountId" int,
  "StartDate" datetime,
  "EndDate" datetime
);

CREATE TABLE "Payment" (
  "PaymentId" int PRIMARY KEY NOT NULL,
  "OrderId" int NOT NULL,
  "PaymentMode" varchar(255),
  "CustomerId" int NOT NULL,
  "Date_of_payment" date
);

CREATE TABLE "Address" (
  "AddressId" int PRIMARY KEY NOT NULL,
  "City_Province" varchar(100),
  "AddressDetail" varchar(200)
);

CREATE TABLE "Cart" (
  "CartId" int PRIMARY KEY NOT NULL,
  "ProductId" int NOT NULL,
  "CustomerId" int NOT NULL,
  "GrandTotal" float,
  "ItemsTotal" int
);

CREATE TABLE "Review" (
  "ReviewId" int PRIMARY KEY NOT NULL,
  "Description" text,
  "Ratings" varchar(255),
  "ProductId" int NOT NULL,
  "CustomerId" int NOT NULL
);

CREATE TABLE "Vendor" (
  "VendorId" int PRIMARY KEY NOT NULL,
  "Name" varchar(255),
  "Phone" varchar(20),
  "TotalSales" float,
  "Email" varchar(50),
  "Description" text,
  "AddressId" int
);

CREATE TABLE "Category" (
  "CategoryId" int PRIMARY KEY NOT NULL,
  "CategoryName" varchar(255),
  "Description" text
);

CREATE TABLE "Customer" (
  "CustomerId" int PRIMARY KEY NOT NULL,
  "FullName" varchar(30),
  "Email" varchar(50),
  "DateOfBirth" date,
  "Phone" varchar(20),
  "Age" smallint,
  "AvatarUrl" varchar(200),
  "AddressId" int
);

ALTER TABLE "ProductDiscount" ADD FOREIGN KEY ("DiscountId") REFERENCES "Discount" ("DiscountId");

ALTER TABLE "ProductDiscount" ADD FOREIGN KEY ("ProductId") REFERENCES "Product" ("ProductId");

ALTER TABLE "Order" ADD FOREIGN KEY ("CustomerId") REFERENCES "Customer" ("CustomerId");

ALTER TABLE "OrderProduct" ADD FOREIGN KEY ("OrderId") REFERENCES "Order" ("OrderId");

ALTER TABLE "OrderProduct" ADD FOREIGN KEY ("ProductId") REFERENCES "Product" ("ProductId");

ALTER TABLE "Product" ADD FOREIGN KEY ("VendorId") REFERENCES "Vendor" ("VendorId");

ALTER TABLE "Product" ADD FOREIGN KEY ("CategoryId") REFERENCES "Category" ("CategoryId");

ALTER TABLE "Payment" ADD FOREIGN KEY ("OrderId") REFERENCES "Order" ("OrderId");

ALTER TABLE "Payment" ADD FOREIGN KEY ("CustomerId") REFERENCES "Customer" ("CustomerId");

ALTER TABLE "Customer" ADD FOREIGN KEY ("AddressId") REFERENCES "Address" ("AddressId");

ALTER TABLE "Vendor" ADD FOREIGN KEY ("AddressId") REFERENCES "Address" ("AddressId");

ALTER TABLE "Order" ADD FOREIGN KEY ("AddressId") REFERENCES "Address" ("AddressId");

ALTER TABLE "Cart" ADD FOREIGN KEY ("CustomerId") REFERENCES "Customer" ("CustomerId");

ALTER TABLE "Cart" ADD FOREIGN KEY ("ProductId") REFERENCES "Product" ("ProductId");

ALTER TABLE "Review" ADD FOREIGN KEY ("CustomerId") REFERENCES "Customer" ("CustomerId");

ALTER TABLE "Review" ADD FOREIGN KEY ("ProductId") REFERENCES "Product" ("ProductId");

ALTER TABLE "ProductImage" ADD FOREIGN KEY ("ProductId") REFERENCES "Product" ("ProductId");
