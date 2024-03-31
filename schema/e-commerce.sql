CREATE TABLE "Order" (
  "OrderId" int PRIMARY KEY NOT NULL,
  "OrderNumber" varchar(255),
  "ShippingDate" date,
  "OrderDate" date,
  "OrderAmount" float,
  "OrderStatus" varchar(255),
  "Cart_CartId" int NOT NULL,
  "CustomerId" int NOT NULL
);

CREATE TABLE "OrderItem" (
  "OrderItemId" int PRIMARY KEY NOT NULL,
  "ProductId" int NOT NULL,
  "OrderId" int NOT NULL,
  "MRP" float,
  "Quantity" int
);

CREATE TABLE "Product" (
  "ProductId" int PRIMARY KEY NOT NULL,
  "ProductName" varchar(255),
  "SellerId" int NOT NULL,
  "MRP" float,
  "CategoryId" int NOT NULL,
  "Stock" int,
  "Brand" varchar(255)
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
  "StreetName" varchar(255),
  "ApartmentNo" varchar(255),
  "City" varchar(255),
  "State" varchar(255),
  "Pincode" int,
  "CustomerId" int NOT NULL
);

CREATE TABLE "Cart" (
  "CartId" int PRIMARY KEY NOT NULL,
  "CustomerId" int NOT NULL,
  "ProductId" int NOT NULL,
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

CREATE TABLE "Seller" (
  "SellerId" int PRIMARY KEY NOT NULL,
  "Name" varchar(255),
  "Phone" varchar(20),
  "TotalSales" float,
  "Email" varchar(50),
  "Description" text
);

CREATE TABLE "Category" (
  "CategoryId" int PRIMARY KEY NOT NULL,
  "CategoryName" varchar(255),
  "Description" text
);

CREATE TABLE "Customer" (
  "CustomerId" int PRIMARY KEY NOT NULL,
  "FirstName" varchar(30),
  "MiddleName" varchar(30),
  "LastName" varchar(30),
  "Email" varchar(50),
  "DateOfBirth" date,
  "Phone" varchar(20),
  "Age" smallint
);

ALTER TABLE "Order" ADD FOREIGN KEY ("CustomerId") REFERENCES "Customer" ("CustomerId");

ALTER TABLE "OrderItem" ADD FOREIGN KEY ("OrderId") REFERENCES "Order" ("OrderId");

ALTER TABLE "OrderItem" ADD FOREIGN KEY ("ProductId") REFERENCES "Product" ("ProductId");

ALTER TABLE "Product" ADD FOREIGN KEY ("SellerId") REFERENCES "Seller" ("SellerId");

ALTER TABLE "Product" ADD FOREIGN KEY ("CategoryId") REFERENCES "Category" ("CategoryId");

ALTER TABLE "Payment" ADD FOREIGN KEY ("OrderId") REFERENCES "Order" ("OrderId");

ALTER TABLE "Payment" ADD FOREIGN KEY ("CustomerId") REFERENCES "Customer" ("CustomerId");

ALTER TABLE "Address" ADD FOREIGN KEY ("CustomerId") REFERENCES "Customer" ("CustomerId");

ALTER TABLE "Cart" ADD FOREIGN KEY ("CustomerId") REFERENCES "Customer" ("CustomerId");

ALTER TABLE "Cart" ADD FOREIGN KEY ("ProductId") REFERENCES "Product" ("ProductId");

ALTER TABLE "Review" ADD FOREIGN KEY ("CustomerId") REFERENCES "Customer" ("CustomerId");

ALTER TABLE "Review" ADD FOREIGN KEY ("ProductId") REFERENCES "Product" ("ProductId");
