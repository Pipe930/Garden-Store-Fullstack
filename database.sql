DROP DATABASE IF EXISTS gardenstore;

CREATE DATABASE gardenstore;

USE gardenstore;

-- Creation of Tables

CREATE TABLE CATEGORY(

	id_category BIGINT NOT NULL AUTO_INCREMENT,
	name_category VARCHAR(255) NOT NULL UNIQUE,

	CONSTRAINT pk_category PRIMARY KEY (id_category)
);

CREATE TABLE OFFER(

	id_offer BIGINT NOT NULL AUTO_INCREMENT,
	name_offer VARCHAR(255) NOT NULL,
	start_date DATE DEFAULT (SYSDATE()) NOT NULL,
	end_date DATE NOT NULL CHECK(end_date >= SYSDATE()),
	discount INT(3) NOT NULL CHECK(discount BETWEEN 100 AND 1),

	CONSTRAINT pk_offer PRIMARY KEY (id_offer)
);

CREATE TABLE USERS(

	id_user BIGINT NOT NULL AUTO_INCREMENT,
	first_name VARCHAR(20) DEFAULT '(without first name)' NULL,
	last_name VARCHAR(20) DEFAULT '(without last name)' NULL,
	username VARCHAR(60) NOT NULL UNIQUE,
	email VARCHAR(255) NOT NULL UNIQUE,
	password VARCHAR(100) NOT NULL,
	last_login DATE NOT NULL,
	is_staff CHAR(1) NOT NULL,
	is_superuser CHAR(1) NOT NULL,
	roles VARCHAR(20) NOT NULL,

	CONSTRAINT pk_user PRIMARY KEY (id_user)
);

CREATE TABLE PERSON(

	id_person BIGINT NOT NULL AUTO_INCREMENT,
	first_name VARCHAR(20) NOT NULL,
	last_name VARCHAR(20) NOT NULL,
	run INT(8) NOT NULL UNIQUE,
	dv CHAR(1) NOT NULL,
	email VARCHAR(255) NOT NULL UNIQUE,
	phone VARCHAR(12) NOT NULL UNIQUE,

	CONSTRAINT pk_person PRIMARY KEY (id_person)
);

CREATE TABLE STORE(

	id_store BIGINT NOT NULL AUTO_INCREMENT,
	name_store VARCHAR(255) NOT NULL UNIQUE,
	direction VARCHAR(255) NOT NULL,
	temperature INT(2) NOT NULL,
	capacity INT(10) NOT NULL CHECK(capacity >= 1000),
	ocupied_capacity INT(10) NOT NULL DEFAULT 0,

	CONSTRAINT pk_store PRIMARY KEY (id_store)
);

CREATE TABLE REGION(

	id_region BIGINT NOT NULL AUTO_INCREMENT,
	name_region VARCHAR(20) NOT NULL UNIQUE,
	initials VARCHAR(6) NOT NULL UNIQUE,

	CONSTRAINT pk_region PRIMARY KEY (id_region)
);

CREATE TABLE PROVINCE(

	id_province BIGINT NOT NULL AUTO_INCREMENT,
	name_province VARCHAR(40) NOT NULL UNIQUE,
	id_region BIGINT NOT NULL,

	CONSTRAINT pk_province PRIMARY KEY (id_province),
	CONSTRAINT fk_province_region FOREIGN KEY (id_region) REFERENCES REGION(id_region)
);

CREATE TABLE COMMUNE(

	id_commune BIGINT NOT NULL AUTO_INCREMENT,
	name_commune VARCHAR(40) NOT NULL UNIQUE,
	id_province BIGINT NOT NULL,

	CONSTRAINT pk_commune PRIMARY KEY (id_commune),
	CONSTRAINT fk_commune_province FOREIGN KEY (id_province) REFERENCES PROVINCE(id_province)
);

CREATE TABLE BRANCH(

    id_branch BIGINT NOT NULL AUTO_INCREMENT,
    name_branch VARCHAR(255) NOT NULL UNIQUE,
    direction TEXT NOT NULL,
    bussiness_name VARCHAR(255) NOT NULL UNIQUE,
    id_commune BIGINT NOT NULL,

    CONSTRAINT pk_branch PRIMARY KEY (id_branch),
    CONSTRAINT fk_branch_commune FOREIGN KEY (id_commune) REFERENCES COMMUNE(id_commune)

);

CREATE TABLE SUBSCRIPTION(

	id_subcription BIGINT NOT NULL AUTO_INCREMENT,
	created TIMESTAMP DEFAULT (NOW()) NOT NULL,
	state CHAR(1) DEFAULT 1 NOT NULL,
	mount INT(6) NOT NULL CHECK(mount >= 5000),
	id_user BIGINT NOT NULL,

	CONSTRAINT pk_subcription PRIMARY KEY (id_subcription),
	CONSTRAINT fk_subcription_user FOREIGN KEY (id_user) REFERENCES USERS(id_user)
);

CREATE TABLE CART(

	id_cart BIGINT NOT NULL AUTO_INCREMENT,
	total INT(10) DEFAULT 0 NOT NULL,
	total_quantity INT(10) DEFAULT 0 NOT NULL,
	total_products INT(10) DEFAULT 0 NOT NULL,
	id_user BIGINT NOT NULL,

	CONSTRAINT pk_cart PRIMARY KEY (id_cart),
	CONSTRAINT fk_cart_user FOREIGN KEY (id_user) REFERENCES USERS(id_user)
);

CREATE TABLE PRODUCT(

	id_product BIGINT NOT NULL AUTO_INCREMENT,
	name_product VARCHAR(255) NOT NULL UNIQUE,
	price INT(10) NOT NULL CHECK(price > 1000),
	stock INT(10) NOT NULL DEFAULT 0,
	image BLOB NOT NULL,
	aviable CHAR(1) NOT NULL DEFAULT 0 CHECK(avialble BETWEEN 0 AND 1),
	slug VARCHAR(100) NOT NULL UNIQUE,
	created TIMESTAMP DEFAULT (NOW()) NOT NULL,
	description TEXT DEFAULT '(sin descripcion)' NULL,
	id_category BIGINT NOT NULL,
	id_offer BIGINT NULL,

	CONSTRAINT pk_product PRIMARY KEY (id_product),
	CONSTRAINT fk_product_category FOREIGN KEY (id_category) REFERENCES CATEGORY(id_category),
	CONSTRAINT fk_product_offer FOREIGN KEY (id_offer) REFERENCES OFFER(id_offer)
);

CREATE TABLE STORE_PRODUCTS(

    id_store_products BIGINT NOT NULL AUTO_INCREMENT,
    quantity INT(10) NOT NULL CHECK(quantity > 0),
    id_store BIGINT NOT NULL,
    id_product BIGINT NOT NULL,

    CONSTRAINT pk_store_products PRIMARY KEY (id_store_products),
    CONSTRAINT fk_store_products_store FOREIGN KEY (id_store) REFERENCES STORE(id_store),
    CONSTRAINT fk_store_products_product FOREIGN KEY (id_product) REFERENCES PRODUCT(id_product)
);

CREATE TABLE BRANCH_PRODUCT(

    id_branch_product BIGINT NOT NULL AUTO_INCREMENT,
    quantity INT(10) NOT NULL CHECK(quantity > 0),
    id_branch BIGINT NOT NULL,
    id_product BIGINT NOT NULL,

    CONSTRAINT pk_branch_product PRIMARY KEY (id_branch_product),
    CONSTRAINT fk_branch_product_branch FOREIGN KEY (id_branch) REFERENCES BRANCH(id_branch),
    CONSTRAINT fk_branch_product_product FOREIGN KEY (id_product) REFERENCES PRODUCT(id_product)
);

CREATE TABLE ITEMS(

    id_items BIGINT NOT NULL AUTO_INCREMENT,
    quantity INT(10) NOT NULL CHECK(quantity > 0),
    price INT(10) NOT NULL CHECK(price > 1000),
    id_cart BIGINT NOT NULL,
    id_product BIGINT NOT NULL,

    CONSTRAINT pk_items PRIMARY KEY (id_items),
    CONSTRAINT fk_items_cart FOREIGN KEY (id_cart) REFERENCES CART(id_cart),
    CONSTRAINT fk_items_product FOREIGN KEY (id_product) REFERENCES PRODUCT(id_product)
);

CREATE TABLE POST(

    id_post BIGINT NOT NULL AUTO_INCREMENT,
    name_post VARCHAR(40) NOT NULL,

    CONSTRAINT pk_post PRIMARY KEY (id_post)
);

CREATE TABLE EMPLOYEE(

    id_employee BIGINT NOT NULL AUTO_INCREMENT,
    date_contrat DATE DEFAULT (SYSDATE()) NOT NULL,
    salary INT(10) NOT NULL CHECK(salary >= 400000),
    id_branch BIGINT NOT NULL,
    id_post BIGINT NOT NULL,

    CONSTRAINT pk_employee PRIMARY KEY (id_employee),
    CONSTRAINT fk_employee_branch FOREIGN KEY (id_branch) REFERENCES BRANCH(id_branch),
    CONSTRAINT fk_employee_post FOREIGN KEY (id_post) REFERENCES POST(id_post)

) INHERITS (PERSON);

CREATE TABLE GROCER(

    id_grocer BIGINT NOT NULL AUTO_INCREMENT,
    id_store BIGINT NOT NULL,

    CONSTRAINT pk_grocer PRIMARY KEY (id_grocer),
    CONSTRAINT fk_employee_store FOREIGN KEY (id_store) REFERENCES STORE(id_store)

) INHERITS (PERSON);

CREATE TABLE CLIENTS(

    id_client BIGINT NOT NULL AUTO_INCREMENT,
    id_user BIGINT NOT NULL,

    CONSTRAINT pk_client PRIMARY KEY (id_client),
    CONSTRAINT fk_client_user FOREIGN KEY (id_user) REFERENCES USERS(id_user)

) INHERITS (PERSON);

CREATE TABLE SUPPLIER(

    id_supplier BIGINT NOT NULL AUTO_INCREMENT,

    CONSTRAINT pk_supplier PRIMARY KEY (id_supplier)

) INHERITS (PERSON);

CREATE TABLE PURCHASE(

	id_purchase BIGINT NOT NULL AUTO_INCREMENT,
    code_uuid VARCHAR(32) NOT NULL UNIQUE CHECK(length(code_uuid) = 32),
    created TIMESTAMP DEFAULT (NOW()) NOT NULL,
    state CHAR(1) DEFAULT 1 NOT NULL CHECK(state BETWEEN 0 AND 1),
    net_mount INT(10) NOT NULL CHECK(net_mount >= 180),
    iva_price INT(10) NOT NULL CHECK(iva_price >= 180),
    total_price INT(10) NOT NULL CHECK(net_mount >= 1000),
    quantity_products INT(10) NOT NULL CHECK(quantity_products > 0),
    conditions VARCHAR(20) DEFAULT 'PR' NOT NULL,
    withdrawal VARCHAR(20) DEFAULT 'Retiro en Tienda' NOT NULL,
    direction TEXT NULL,
    num_deparment INT(6) NULL,
    id_commune BIGINT NULL,
    id_branch BIGINT NULL,
    id_user BIGINT NOT NULL,

    CONSTRAINT pk_purchase PRIMARY KEY (id_purchase),
    CONSTRAINT fk_purchase_commune FOREIGN KEY (id_commune) REFERENCES COMMUNE(id_commune),
    CONSTRAINT fk_purchase_branch FOREIGN KEY (id_branch) REFERENCES BRANCH(id_branch),
    CONSTRAINT fk_purchase_user FOREIGN KEY (id_user) REFERENCES USERS(id_user)
);

CREATE TABLE PURCHASE_ITEMS(

	id_purchase_items BIGINT NOT NULL AUTO_INCREMENT,
    name_product VARCHAR(255) NOT NULL UNIQUE,
    price INT(10) NOT NULL CHECK(price > 1000),
    quantity INT(10) NOT NULL CHECK(quantity > 0),
    date_added DATE DEFAULT (SYSDATE()) NOT NULL,
    id_purchase BIGINT NOT NULL,
    id_product BIGINT NOT NULL,

    CONSTRAINT pk_purchase_items PRIMARY KEY (id_purchase_items),
    CONSTRAINT fk_purchase_items_purchase FOREIGN KEY (id_purchase) REFERENCES PURCHASE(id_purchase),
    CONSTRAINT fk_purchase_items_product FOREIGN KEY (id_product) REFERENCES PRODUCT(id_product)
);

CREATE TABLE DISPATCH_GUIDE(

	id_dispatch_guide BIGINT NOT NULL AUTO_INCREMENT,
    code_uuid VARCHAR(32) NOT NULL UNIQUE CHECK(length(code_uuid) = 32),
    created DATE DEFAULT (SYSDATE()) NOT NULL,
    dispatch_date DATE NULL,
    deliver_date DATE NULL,
    state VARCHAR(2) DEFAULT 'PR' NOT NULL,
    destination TEXT NOT NULL,
    id_branch BIGINT NOT NULL,

    CONSTRAINT pk_dispatch_guide PRIMARY KEY (id_dispatch_guide),
    CONSTRAINT fk_dispatch_guide_branch FOREIGN KEY (id_branch) REFERENCES BRANCH(id_branch)
);

CREATE TABLE GUIE_PRODUCT(

    id_guie_product BIGINT NOT NULL AUTO_INCREMENT,
    quantity INT(10) NOT NULL CHECK(quantity > 0),
    id_dispatch_guide BIGINT NOT NULL,
    id_product BIGINT NOT NULL,

    CONSTRAINT pk_guie_product PRIMARY KEY (id_guie_product),
    CONSTRAINT fk_guie_product_dispatch_guide FOREIGN KEY (id_dispatch_guide) REFERENCES DISPATCH_GUIDE(id_dispatch_guide),
    CONSTRAINT fk_guie_product_product FOREIGN KEY (id_product) REFERENCES PRODUCT(id_product)
);

CREATE TABLE ORDER_PRODUCT(

    id_order_product BIGINT NOT NULL AUTO_INCREMENT,
    code_uuid VARCHAR(32) NOT NULL UNIQUE CHECK(length(code_uuid) = 32),
    created TIMESTAMP DEFAULT (NOW()) NOT NULL,
    id_employee BIGINT NOT NULL,
    id_grocer BIGINT NOT NULL,

    CONSTRAINT pk_order_product PRIMARY KEY (id_order_product),
    CONSTRAINT fk_order_product_employee FOREIGN KEY (id_employee) REFERENCES EMPLOYEE(id_employee),
    CONSTRAINT fk_order_product_grocer FOREIGN KEY (id_grocer) REFERENCES GROCER(id_grocer)
);

CREATE TABLE PRODUCTS_ORDER(

	id_products_order BIGINT NOT NULL AUTO_INCREMENT,
    quantity INT(10) NOT NULL CHECK(quantity > 0),
    id_product BIGINT NOT NULL,
    id_order_product BIGINT NOT NULL,

    CONSTRAINT pk_products_order PRIMARY KEY (id_products_order),
    CONSTRAINT fk_products_order_product FOREIGN KEY (id_product) REFERENCES PRODUCT(id_product),
    CONSTRAINT fk_products_order_order_product FOREIGN KEY (id_order_product) REFERENCES ORDER_PRODUCT(id_order_product)
);

CREATE TABLE BILL(

	id_bill BIGINT NOT NULL AUTO_INCREMENT,
    code_uuid VARCHAR(32) NOT NULL UNIQUE CHECK(length(code_uuid) = 32),
    created TIMESTAMP DEFAULT (NOW()) NOT NULL,
    products JSON NOT NULL,
    total_price INT(10) NOT NULL CHECK(total_price >= 1000),
    total_quantity INT(10) NOT NULL CHECK(total_quantity > 0),
    id_supplier BIGINT NOT NULL,
    id_grocer BIGINT NOT NULL,

    CONSTRAINT pk_bill PRIMARY KEY (id_bill),
    CONSTRAINT fk_bill_supplier FOREIGN KEY (id_supplier) REFERENCES SUPPLIER(id_supplier),
    CONSTRAINT fk_bill_grocer FOREIGN KEY (id_grocer) REFERENCES GROCER(id_grocer)
);

CREATE TABLE WARRANTY(

	id_warranty BIGINT NOT NULL AUTO_INCREMENT,
    code_uuid VARCHAR(32) NOT NULL UNIQUE CHECK(quantity > 0),
    created TIMESTAMP DEFAULT (NOW()) NOT NULL,
    state CHAR(1) NOT NULL DEFAULT 1 CHECK(state BETWEEN 1 AND 0),
    id_product BIGINT NOT NULL,
    id_purchase BIGINT NOT NULL,

    CONSTRAINT pk_warranty PRIMARY KEY (id_warranty),
    CONSTRAINT fk_warranty_product FOREIGN KEY (id_product) REFERENCES PRODUCT(id_product),
    CONSTRAINT fk_warranty_purchase FOREIGN KEY (id_purchase) REFERENCES PURCHASE(id_purchase)
);

CREATE TABLE NEWSLETTER_USER(

	id_newsletter_user BIGINT NOT NULL AUTO_INCREMENT,
    email VARCHAR(255) NOT NULL UNIQUE,
    date_added TIMESTAMP DEFAULT (NOW()) NOT NULL,

    CONSTRAINT pk_newsletter_user PRIMARY KEY (id_newsletter_user)
);

CREATE TABLE NEWSLETTER(

	id_newsletter BIGINT NOT NULL AUTO_INCREMENT,
    name_newsletter VARCHAR(255) NOT NULL,
    subject_newsletter VARCHAR(255) NOT NULL,
    body TEXT NULL,
    created TIMESTAMP DEFAULT (NOW()) NOT NULL,
    id_newsletter_user BIGINT NOT NULL,

    CONSTRAINT pk_newsletter PRIMARY KEY (id_newsletter),
    CONSTRAINT fk_newsletter_newsletter_user FOREIGN KEY (id_newsletter_user) REFERENCES NEWSLETTER_USER(id_newsletter_user)
);


-- INSERT INTO person (first_name, last_name, email, run, dv, phone) VALUES("nicolas", "cisterna", "nicolas.cistena@gmail.com", 21345678, "1", 987562345);
-- INSERT INTO grocer (person_ptr_id, store_id) VALUES(1, 1);
-- INSERT INTO person (first_name, last_name, email, run, dv, phone) VALUES("nestor", "aviles", "nestor.aviles@gmail.com", 23756849, "k", 974382938);
-- INSERT INTO supplier (person_ptr_id) VALUES(2);
