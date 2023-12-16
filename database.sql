DROP DATABASE IF EXISTS gardenstore;

CREATE DATABASE gardenstore;

USE gardenstore;

-- CREATION OF TABLES

CREATE TABLE CATEGORY(

    id_category BIGINT NOT NULL AUTO_INCREMENT,
    name_category VARCHAR(255) NOT NULL UNIQUE,

    CONSTRAINT pk_category PRIMARY KEY (id_category)
);

CREATE TABLE OFFER(

    id_offer BIGINT NOT NULL AUTO_INCREMENT,
    name_offer VARCHAR(255) NOT NULL,
    start_date DATE DEFAULT (CURDATE()) NOT NULL,
    end_date DATE NOT NULL,
    discount SMALLINT NOT NULL CHECK(discount <= 100 AND discount >= 1),

    CONSTRAINT pk_offer PRIMARY KEY (id_offer)
);

CREATE TABLE USER(

    id_user BIGINT NOT NULL AUTO_INCREMENT,
    first_name VARCHAR(20) DEFAULT '(without first name)' NULL,
    last_name VARCHAR(20) DEFAULT '(without last name)' NULL,
    username VARCHAR(60) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(100) NOT NULL,
    last_login TIMESTAMP NULL,
    is_staff BIT NOT NULL,
    is_superuser BIT NOT NULL,

    CONSTRAINT pk_user PRIMARY KEY (id_user)
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
    capacity INT NOT NULL CHECK(capacity > 100),
    capacity_ocuped INT DEFAULT 0 NOT NULL,
    phone VARCHAR(12) NOT NULL UNIQUE CHECK(length(phone) = 12),
    direction TEXT NOT NULL,
    bussiness_name VARCHAR(255) NOT NULL UNIQUE,
    id_commune BIGINT NOT NULL,

    CONSTRAINT pk_branch PRIMARY KEY (id_branch),
    CONSTRAINT fk_branch_commune FOREIGN KEY (id_commune) REFERENCES COMMUNE(id_commune)

);

CREATE TABLE SUBSCRIPTION(

    id_subcription BIGINT NOT NULL AUTO_INCREMENT,
    created TIMESTAMP DEFAULT (NOW()) NOT NULL,
    state BIT DEFAULT 1 NOT NULL,
    mount SMALLINT NOT NULL CHECK(mount >= 5000),
    id_user BIGINT NOT NULL,

    CONSTRAINT pk_subcription PRIMARY KEY (id_subcription),
    CONSTRAINT fk_subcription_user FOREIGN KEY (id_user) REFERENCES USER(id_user)
);

CREATE TABLE CART(

    id_cart BIGINT NOT NULL AUTO_INCREMENT,
    total INT DEFAULT 0 NOT NULL,
    total_quantity INT DEFAULT 0 NOT NULL,
    total_products INT DEFAULT 0 NOT NULL,
    id_user BIGINT NOT NULL,

    CONSTRAINT pk_cart PRIMARY KEY (id_cart),
    CONSTRAINT fk_cart_user FOREIGN KEY (id_user) REFERENCES USER(id_user)
);

CREATE TABLE PRODUCT(

    id_product BIGINT NOT NULL AUTO_INCREMENT,
    title VARCHAR(255) NOT NULL UNIQUE,
    price INT NOT NULL CHECK(price > 1000),
    stock INT NOT NULL DEFAULT 0,
    sold INT NOT NULL DEFAULT 0,
    brand VARCHAR(40) NOT NULL,
    image BLOB NOT NULL,
    aviable BIT NOT NULL DEFAULT 0,
    slug VARCHAR(100) NOT NULL UNIQUE,
    created TIMESTAMP DEFAULT (NOW()) NOT NULL,
    description TEXT NULL,
    id_category BIGINT NOT NULL,
    id_offer BIGINT NULL,

    CONSTRAINT pk_product PRIMARY KEY (id_product),
    CONSTRAINT fk_product_category FOREIGN KEY (id_category) REFERENCES CATEGORY(id_category),
    CONSTRAINT fk_product_offer FOREIGN KEY (id_offer) REFERENCES OFFER(id_offer)
);

CREATE TABLE BRANCH_PRODUCT(

    id_branch_product BIGINT NOT NULL AUTO_INCREMENT,
    quantity INT NOT NULL CHECK(quantity > 0),
    id_branch BIGINT NOT NULL,
    id_product BIGINT NOT NULL,

    CONSTRAINT pk_branch_product PRIMARY KEY (id_branch_product),
    CONSTRAINT fk_branch_product_branch FOREIGN KEY (id_branch) REFERENCES BRANCH(id_branch),
    CONSTRAINT fk_branch_product_product FOREIGN KEY (id_product) REFERENCES PRODUCT(id_product)
);

CREATE TABLE ITEMS(

    id_items BIGINT NOT NULL AUTO_INCREMENT,
    quantity INT NOT NULL CHECK(quantity > 0),
    price INT NOT NULL CHECK(price > 1000),
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
    first_name VARCHAR(20) NOT NULL,
    last_name VARCHAR(20) NOT NULL,
    gender VARCHAR(20) NOT NULL CHECK(gender = 'masculino' OR gender = 'femenino' OR gender = 'otro'),
    email VARCHAR(255) NOT NULL UNIQUE,
    phone VARCHAR(12) NOT NULL UNIQUE,
    run INT NOT NULL UNIQUE CHECK(LENGTH(CAST(run AS VARCHAR)) = 7 OR LENGTH(CAST(run AS VARCHAR)) = 8),
    dv CHAR(1) NOT NULL,
    birthday DATE NOT NULL,
    date_contrat DATE DEFAULT (CURDATE()) NOT NULL,
    salary INT NOT NULL CHECK(salary >= 100000),
    id_branch BIGINT NOT NULL,
    id_post BIGINT NOT NULL,

    CONSTRAINT pk_employee PRIMARY KEY (id_employee),
    CONSTRAINT fk_employee_branch FOREIGN KEY (id_branch) REFERENCES BRANCH(id_branch),
    CONSTRAINT fk_employee_post FOREIGN KEY (id_post) REFERENCES POST(id_post)

);

CREATE TABLE VOUCHER(

    id_voucher BIGINT NOT NULL AUTO_INCREMENT,
    code_uuid VARCHAR(32) NOT NULL UNIQUE CHECK(length(code_uuid) = 32),
    created TIMESTAMP DEFAULT (NOW()) NOT NULL,
    state BIT DEFAULT 1 NOT NULL,
    net_mount INT NOT NULL CHECK(net_mount >= 180),
    iva_price INT NOT NULL CHECK(iva_price >= 180),
    total_price INT NOT NULL CHECK(total_price >= 1000),
    quantity_products INT NOT NULL CHECK(quantity_products > 0),
    conditions VARCHAR(2) DEFAULT 'PR' NOT NULL,
    withdrawal VARCHAR(20) NOT NULL CHECK(withdrawal = 'retiro en tienda' OR withdrawal = 'envio a domicilio'),
    direction TEXT NULL,
    num_deparment INT NULL,
    id_commune BIGINT NULL,
    id_branch BIGINT NULL,
    id_user BIGINT NOT NULL,

    CONSTRAINT pk_voucher PRIMARY KEY (id_voucher),
    CONSTRAINT fk_voucher_commune FOREIGN KEY (id_commune) REFERENCES COMMUNE(id_commune),
    CONSTRAINT fk_voucher_branch FOREIGN KEY (id_branch) REFERENCES BRANCH(id_branch),
    CONSTRAINT fk_voucher_user FOREIGN KEY (id_user) REFERENCES USER(id_user)
);

CREATE TABLE VOUCHER_ITEMS(

	  id_voucher_items BIGINT NOT NULL AUTO_INCREMENT,
    name_product VARCHAR(255) NOT NULL UNIQUE,
    price INT NOT NULL CHECK(price > 1000),
    quantity INT NOT NULL CHECK(quantity > 0),
    id_voucher BIGINT NOT NULL,
    id_product BIGINT NOT NULL,

    CONSTRAINT pk_voucher_items PRIMARY KEY (id_voucher_items),
    CONSTRAINT fk_voucher_items_voucher FOREIGN KEY (id_voucher) REFERENCES voucher(id_voucher),
    CONSTRAINT fk_voucher_items_product FOREIGN KEY (id_product) REFERENCES PRODUCT(id_product)
);

CREATE TABLE WARRANTY(

	  id_warranty BIGINT NOT NULL AUTO_INCREMENT,
    code_uuid VARCHAR(32) NOT NULL UNIQUE CHECK(length(code_uuid) = 32),
    created TIMESTAMP DEFAULT (NOW()) NOT NULL,
    state BIT NOT NULL DEFAULT 1,
    id_product BIGINT NOT NULL,
    id_voucher BIGINT NOT NULL,

    CONSTRAINT pk_warranty PRIMARY KEY (id_warranty),
    CONSTRAINT fk_warranty_product FOREIGN KEY (id_product) REFERENCES PRODUCT(id_product),
    CONSTRAINT fk_warranty_voucher FOREIGN KEY (id_voucher) REFERENCES voucher(id_voucher)
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

-- TRIGGERS

delimiter //
CREATE TRIGGER TR_CHECK_END_DATE BEFORE INSERT ON OFFER
    FOR EACH ROW BEGIN
        IF DATEDIFF(NEW.end_date, (CURDATE())) > 0 THEN
            SET NEW.end_date = NEW.end_date;
        ELSEIF DATEDIFF(NEW.end_date, (CURDATE())) <= 0 THEN
            SET NEW.end_date = CURDATE() + 1;
        END IF;
    END; //

-- Regiones de Chile

INSERT INTO region VALUES(1, "Arica y Parinacota", "XV");
INSERT INTO region VALUES(2, "Tarapaca", "I");
INSERT INTO region VALUES(3, "Antofagasta", "II");
INSERT INTO region VALUES(4, "Atacama", "III");
INSERT INTO region VALUES(5, "Coquimbo", "IV");
INSERT INTO region VALUES(6, "Valparaíso", "V");
INSERT INTO region VALUES(7, "Libertador General Bernardo O'Higgins", "VI");
INSERT INTO region VALUES(8, "Maule", "VII");
INSERT INTO region VALUES(9, "Ñuble", "XVI");
INSERT INTO region VALUES(10, "Biobio", "VIII");
INSERT INTO region VALUES(11, "La Araucania", "IX");
INSERT INTO region VALUES(12, "Los Rios", "XIV");
INSERT INTO region VALUES(13, "Los Lagos", "X");
INSERT INTO region VALUES(14, "Aysen del General Carlos Ibañez del Campo", "XI");
INSERT INTO region VALUES(15, "Magallanes y de la Antartica Chilena ", "XII");
INSERT INTO region VALUES(16, "Metropolitana de Santiago", "");

-- Provincias de Chile

INSERT INTO province VALUES(1, "Arica", 1);
INSERT INTO province VALUES(2, "Parinacota", 1);

INSERT INTO province VALUES(3, "Iquique", 2);
INSERT INTO province VALUES(4, "Tamarugal", 2);

INSERT INTO province VALUES(5, "Tocopilla", 3);
INSERT INTO province VALUES(6, "El Loa", 3);
INSERT INTO province VALUES(7, "Antofagasta", 3);

INSERT INTO province VALUES(8, "Chañaral", 4);
INSERT INTO province VALUES(9, "Copiapo", 4);
INSERT INTO province VALUES(10, "Huasco", 4);

INSERT INTO province VALUES(11, "Elqui", 5);
INSERT INTO province VALUES(12, "Limari", 5);
INSERT INTO province VALUES(13, "Choapa", 5);

INSERT INTO province VALUES(14, "Petorca", 6);
INSERT INTO province VALUES(15, "Los Andes", 6);
INSERT INTO province VALUES(16, "San Felipe de Aconcagua", 6);
INSERT INTO province VALUES(17, "Quillota", 6);
INSERT INTO province VALUES(18, "Valparaiso", 6);
INSERT INTO province VALUES(19, "San Antonio", 6);
INSERT INTO province VALUES(20, "Isla de Pascua", 6);
INSERT INTO province VALUES(21, "Marga Marga", 6);

INSERT INTO province VALUES(22, "Chacabuco", 16);
INSERT INTO province VALUES(23, "Santiago", 16);
INSERT INTO province VALUES(24, "Cordillera", 16);
INSERT INTO province VALUES(25, "Maipo", 16);
INSERT INTO province VALUES(26, "Melipilla", 16);
INSERT INTO province VALUES(27, "Talagante", 16);

INSERT INTO province VALUES(28, "Cachapoal", 7);
INSERT INTO province VALUES(29, "Colchagua", 7);
INSERT INTO province VALUES(30, " Cardenal Caro", 7);

INSERT INTO province VALUES(31, "Curico", 8);
INSERT INTO province VALUES(32, "Talca", 8);
INSERT INTO province VALUES(33, "Linares", 8);
INSERT INTO province VALUES(34, "Cauquenes", 8);

INSERT INTO province VALUES(35, "Diguillin", 9);
INSERT INTO province VALUES(36, "Itata", 9);
INSERT INTO province VALUES(37, "Punilla", 9);

INSERT INTO province VALUES(38, "Biobio", 10);
INSERT INTO province VALUES(39, "Concepcion", 10);
INSERT INTO province VALUES(40, "Arauco", 10);

INSERT INTO province VALUES(41, "Malleco", 11);
INSERT INTO province VALUES(42, "Cautin", 11);

INSERT INTO province VALUES(43, "Valdivia", 12);
INSERT INTO province VALUES(44, "Ranco", 12);

INSERT INTO province VALUES(45, "Osorno", 13);
INSERT INTO province VALUES(46, "Llanquihue", 13);
INSERT INTO province VALUES(47, "Chiloe", 13);
INSERT INTO province VALUES(48, "Palena", 13);

INSERT INTO province VALUES(49, "Coyhaique", 14);
INSERT INTO province VALUES(50, "Aysen", 14);
INSERT INTO province VALUES(51, " General Carrera", 14);
INSERT INTO province VALUES(52, " Capitan Prat", 14);

INSERT INTO province VALUES(53, "Ultima Esperanza", 15);
INSERT INTO province VALUES(54, "Magallanes", 15);
INSERT INTO province VALUES(55, "Tierra del Fuego", 15);
INSERT INTO province VALUES(56, " Antartica Chilena", 15);

-- Comunas de Chile

INSERT INTO commune VALUES(1, "Arica", 1);
INSERT INTO commune VALUES(2, "Camarones", 1);

INSERT INTO commune VALUES(3, "General Lagos", 2);
INSERT INTO commune VALUES(4, "Putre", 2);

INSERT INTO commune VALUES(5, "Alto Hospicio", 3);
INSERT INTO commune VALUES(6, "Iquique", 3);

INSERT INTO commune VALUES(7, "Camiña", 4);
INSERT INTO commune VALUES(8, "Colchane", 4);
INSERT INTO commune VALUES(9, "Huara", 4);
INSERT INTO commune VALUES(10, "Pica", 4);
INSERT INTO commune VALUES(11, "Pozo Almonte", 4);

INSERT INTO commune VALUES(12, "Antofagasta", 7);
INSERT INTO commune VALUES(13, "Mejillones", 7);
INSERT INTO commune VALUES(14, "Sierra Gorda", 7);
INSERT INTO commune VALUES(15, "Taltal", 7);

INSERT INTO commune VALUES(16, "Calama", 6);
INSERT INTO commune VALUES(17, "Ollagüe", 6);
INSERT INTO commune VALUES(18, "San Pedro de Atacama", 6);

INSERT INTO commune VALUES(19, "Maria Elena", 5);
INSERT INTO commune VALUES(20, "Tocopilla", 5);

INSERT INTO commune VALUES(21, "Chañaral", 8);
INSERT INTO commune VALUES(22, "Diego de Almagro", 8);

INSERT INTO commune VALUES(23, "Caldera", 9);
INSERT INTO commune VALUES(24, "Copiapo", 9);
INSERT INTO commune VALUES(25, "Tierra Amarilla", 9);

INSERT INTO commune VALUES(26, "Alto del Carmen", 10);
INSERT INTO commune VALUES(27, "Freirina", 10);
INSERT INTO commune VALUES(28, "Huasco", 10);
INSERT INTO commune VALUES(29, "Vallenar", 10);

INSERT INTO commune VALUES(30, "Andacollo", 11);
INSERT INTO commune VALUES(31, "Coquimbo", 11);
INSERT INTO commune VALUES(32, "La Higuera", 11);
INSERT INTO commune VALUES(33, "La Serena", 11);
INSERT INTO commune VALUES(34, "Paihuano", 11);
INSERT INTO commune VALUES(35, "Vicuña", 11);

INSERT INTO commune VALUES(36, "Combarbala", 12);
INSERT INTO commune VALUES(37, "Monte Patria", 12);
INSERT INTO commune VALUES(38, "Ovalle", 12);
INSERT INTO commune VALUES(39, "Punitaqui", 12);
INSERT INTO commune VALUES(40, "Rio Hurtado", 12);

INSERT INTO commune VALUES(41, "Canela", 13);
INSERT INTO commune VALUES(42, "Illapel", 13);
INSERT INTO commune VALUES(43, "Los Vilos", 13);
INSERT INTO commune VALUES(44, "Salamanca", 13);

INSERT INTO commune VALUES(45, "Calle Larga", 15);
INSERT INTO commune VALUES(46, "Los Andes", 15);
INSERT INTO commune VALUES(47, "San Esteban", 15);
INSERT INTO commune VALUES(48, "Rinconada", 15);

INSERT INTO commune VALUES(49, "Cabildo", 14);
INSERT INTO commune VALUES(50, "La Ligua", 14);
INSERT INTO commune VALUES(51, "Papudo", 14);
INSERT INTO commune VALUES(52, "Petorca", 14);
INSERT INTO commune VALUES(53, "Zapallar", 14);

INSERT INTO commune VALUES(54, "Hijuelas", 17);
INSERT INTO commune VALUES(55, "La Calera", 17);
INSERT INTO commune VALUES(56, "La Cruz", 17);
INSERT INTO commune VALUES(57, "Nogales", 17);
INSERT INTO commune VALUES(58, "Quillota", 17);

INSERT INTO commune VALUES(59, "Algarrobo", 19);
INSERT INTO commune VALUES(60, "Cartagena", 19);
INSERT INTO commune VALUES(61, "El Quisco", 19);
INSERT INTO commune VALUES(62, "El Tabo", 19);
INSERT INTO commune VALUES(63, "San Antonio", 19);
INSERT INTO commune VALUES(64, "Santo Domingo", 19);

INSERT INTO commune VALUES(65, "Catemu", 16);
INSERT INTO commune VALUES(66, "Llay-Llay", 16);
INSERT INTO commune VALUES(67, "Panquehue", 16);
INSERT INTO commune VALUES(68, "Putaendo", 16);
INSERT INTO commune VALUES(69, "San Felipe", 16);
INSERT INTO commune VALUES(70, "Santa Maria", 16);

INSERT INTO commune VALUES(71, "Viña del Mar", 18);
INSERT INTO commune VALUES(72, "Valparaiso", 18);
INSERT INTO commune VALUES(73, "Quintero", 18);
INSERT INTO commune VALUES(74, "Puchuncavi", 18);
INSERT INTO commune VALUES(75, "Juan Fernandez", 18);
INSERT INTO commune VALUES(76, "Concon", 18);
INSERT INTO commune VALUES(77, "Casablanca", 18);

INSERT INTO commune VALUES(78, "Villa Alemana", 21);
INSERT INTO commune VALUES(79, "Quilpue", 21);
INSERT INTO commune VALUES(80, "Olmue", 21);
INSERT INTO commune VALUES(81, "Limache", 21);

INSERT INTO commune VALUES(82, "Rapa Nui", 20);

INSERT INTO commune VALUES(83, "Colina", 22);
INSERT INTO commune VALUES(84, "Til Til", 22);
INSERT INTO commune VALUES(85, "Lampa", 22);

INSERT INTO commune VALUES(86, "San Jose de Maipo", 24);
INSERT INTO commune VALUES(87, "Puente Alto", 24);
INSERT INTO commune VALUES(88, "Pirque", 24);

INSERT INTO commune VALUES(89, "Calera de Tango", 25);
INSERT INTO commune VALUES(90, "San Bernardo", 25);
INSERT INTO commune VALUES(91, "Buin", 25);
INSERT INTO commune VALUES(92, "Paine", 25);

INSERT INTO commune VALUES(93, "Alhue", 26);
INSERT INTO commune VALUES(94, "San Pedro", 26);
INSERT INTO commune VALUES(95, "Melipilla", 26);
INSERT INTO commune VALUES(96, "Maria Pinto", 26);
INSERT INTO commune VALUES(97, "Curacavi", 26);

INSERT INTO commune VALUES(98, "Cerrillos", 23);
INSERT INTO commune VALUES(99, "Cerro Navia", 23);
INSERT INTO commune VALUES(100, "Conchali", 23);
INSERT INTO commune VALUES(101, "El Bosque", 23);
INSERT INTO commune VALUES(102, "Estacion Central", 23);
INSERT INTO commune VALUES(103, "Huechuraba", 23);
INSERT INTO commune VALUES(104, "Independencia", 23);
INSERT INTO commune VALUES(105, "La Cisterna", 23);
INSERT INTO commune VALUES(106, "La Granja", 23);
INSERT INTO commune VALUES(107, "La Florida", 23);
INSERT INTO commune VALUES(108, "La Pintana", 23);
INSERT INTO commune VALUES(109, "La Reina", 23);
INSERT INTO commune VALUES(110, "Las Condes", 23);
INSERT INTO commune VALUES(111, "Lo Barnechea", 23);
INSERT INTO commune VALUES(112, "Lo Espejo", 23);
INSERT INTO commune VALUES(113, "Lo Prado", 23);
INSERT INTO commune VALUES(114, "Macul", 23);
INSERT INTO commune VALUES(115, "Maipu", 23);
INSERT INTO commune VALUES(116, "Ñuñoa", 23);
INSERT INTO commune VALUES(117, "Pedro Aguirre Cerda", 23);
INSERT INTO commune VALUES(118, "Peñalolen", 23);
INSERT INTO commune VALUES(119, "Providencia", 23);
INSERT INTO commune VALUES(120, "Pudahuel", 23);
INSERT INTO commune VALUES(121, "Quilicura", 23);
INSERT INTO commune VALUES(122, "Quinta Normal", 23);
INSERT INTO commune VALUES(123, "Recoleta", 23);
INSERT INTO commune VALUES(124, "Renca", 23);
INSERT INTO commune VALUES(125, "San Miguel", 23);
INSERT INTO commune VALUES(126, "San Joaquin", 23);
INSERT INTO commune VALUES(127, "San Ramon", 23);
INSERT INTO commune VALUES(128, "Santiago", 23);
INSERT INTO commune VALUES(129, "Vitacura", 23);

INSERT INTO commune VALUES(130, "El Monte", 27);
INSERT INTO commune VALUES(131, "Isla de Maipo", 27);
INSERT INTO commune VALUES(132, "Padre Hurtado", 27);
INSERT INTO commune VALUES(133, "Peñaflor", 27);
INSERT INTO commune VALUES(134, "Talagante", 27);

INSERT INTO commune VALUES(135, "Codegua", 28);
INSERT INTO commune VALUES(136, "Coinco", 28);
INSERT INTO commune VALUES(137, "Coltauco", 28);
INSERT INTO commune VALUES(138, "Doñihue", 28);
INSERT INTO commune VALUES(139, "Graneros", 28);
INSERT INTO commune VALUES(140, "Las Cabras", 28);
INSERT INTO commune VALUES(141, "Machali", 28);
INSERT INTO commune VALUES(142, "Malloa", 28);
INSERT INTO commune VALUES(143, "Mostazal", 28);
INSERT INTO commune VALUES(144, "Olivar", 28);
INSERT INTO commune VALUES(145, "Peumo", 28);
INSERT INTO commune VALUES(146, "Pichidegua", 28);
INSERT INTO commune VALUES(147, "Quinta de Tilcoco", 28);
INSERT INTO commune VALUES(148, "Rancagua", 28);
INSERT INTO commune VALUES(149, "Rengo", 28);
INSERT INTO commune VALUES(150, "Requinoa", 28);
INSERT INTO commune VALUES(151, "San Vicente de Tagua Tagua", 28);

INSERT INTO commune VALUES(152, "La Estrella", 30);
INSERT INTO commune VALUES(153, "Litueche", 30);
INSERT INTO commune VALUES(154, "Marchigüe", 30);
INSERT INTO commune VALUES(155, "Navidad", 30);
INSERT INTO commune VALUES(156, "Paredones", 30);
INSERT INTO commune VALUES(157, "Pichilemu", 30);

INSERT INTO commune VALUES(158, "Chepica", 29);
INSERT INTO commune VALUES(159, "Chimbarongo", 29);
INSERT INTO commune VALUES(160, "Lolol", 29);
INSERT INTO commune VALUES(161, "Nancagua", 29);
INSERT INTO commune VALUES(162, "Palmilla", 29);
INSERT INTO commune VALUES(163, "Peralillo", 29);
INSERT INTO commune VALUES(164, "Placilla", 29);
INSERT INTO commune VALUES(165, "Pumanque", 29);
INSERT INTO commune VALUES(166, "San Fernando", 29);
INSERT INTO commune VALUES(167, "Santa Cruz", 29);

INSERT INTO commune VALUES(168, "Cauquenes", 34);
INSERT INTO commune VALUES(169, "Chanco", 34);
INSERT INTO commune VALUES(170, "Pelluhue", 34);

INSERT INTO commune VALUES(171, "Curico", 31);
INSERT INTO commune VALUES(172, "Hualañe", 31);
INSERT INTO commune VALUES(173, "Licanten", 31);
INSERT INTO commune VALUES(174, "Molina", 31);
INSERT INTO commune VALUES(175, "Rauco", 31);
INSERT INTO commune VALUES(176, "Romeral", 31);
INSERT INTO commune VALUES(177, "Sagrada Familia", 31);
INSERT INTO commune VALUES(178, "Teno", 31);
INSERT INTO commune VALUES(179, "Vichuquen", 31);

INSERT INTO commune VALUES(180, "Colbun", 33);
INSERT INTO commune VALUES(181, "Linares", 33);
INSERT INTO commune VALUES(182, "Longavi", 33);
INSERT INTO commune VALUES(183, "Parral", 33);
INSERT INTO commune VALUES(184, "Retiro", 33);
INSERT INTO commune VALUES(185, "San Javier", 33);
INSERT INTO commune VALUES(186, "Villa Alegre", 33);
INSERT INTO commune VALUES(187, "Yerbas Buenas", 33);

INSERT INTO commune VALUES(188, "Constitucion", 32);
INSERT INTO commune VALUES(189, "Curepto", 32);
INSERT INTO commune VALUES(190, "Empedrado", 32);
INSERT INTO commune VALUES(191, "Maule", 32);
INSERT INTO commune VALUES(192, "Pelarco", 32);
INSERT INTO commune VALUES(193, "Pencahue", 32);
INSERT INTO commune VALUES(194, "Rio Claro", 32);
INSERT INTO commune VALUES(195, "San Clemente", 32);
INSERT INTO commune VALUES(196, "San Rafael", 32);
INSERT INTO commune VALUES(197, "Talca", 32);

INSERT INTO commune VALUES(198, "Cobquecura", 36);
INSERT INTO commune VALUES(199, "Coelemu", 36);
INSERT INTO commune VALUES(200, "Ninhue", 36);
INSERT INTO commune VALUES(201, "Portezuelo", 36);
INSERT INTO commune VALUES(202, "Quirihue", 36);
INSERT INTO commune VALUES(203, "Ranquil", 36);
INSERT INTO commune VALUES(204, "Trehuaco", 36);

INSERT INTO commune VALUES(205, "Bulnes", 35);
INSERT INTO commune VALUES(206, "Chillan Viejo", 35);
INSERT INTO commune VALUES(207, "Chillan", 35);
INSERT INTO commune VALUES(208, "El Carmen", 35);
INSERT INTO commune VALUES(209, "Pemuco", 35);
INSERT INTO commune VALUES(210, "Quillon", 35);
INSERT INTO commune VALUES(211, "Pinto", 35);
INSERT INTO commune VALUES(212, "San Ignacio", 35);
INSERT INTO commune VALUES(213, "Yungay", 35);

INSERT INTO commune VALUES(214, "San Nicolas", 37);
INSERT INTO commune VALUES(215, "San Fabian", 37);
INSERT INTO commune VALUES(216, "San Carlos", 37);
INSERT INTO commune VALUES(217, "Ñiquen", 37);
INSERT INTO commune VALUES(218, "Coihueco", 37);

INSERT INTO commune VALUES(219, "Arauco", 40);
INSERT INTO commune VALUES(220, "Cañete", 40);
INSERT INTO commune VALUES(221, "Contulmo", 40);
INSERT INTO commune VALUES(222, "Curanilahue", 40);
INSERT INTO commune VALUES(223, "Lebu", 40);
INSERT INTO commune VALUES(224, "Los Alamos", 40);
INSERT INTO commune VALUES(225, "Tirua", 40);

INSERT INTO commune VALUES(226, "Alto Biobio", 38);
INSERT INTO commune VALUES(227, "Antuco", 38);
INSERT INTO commune VALUES(228, "Cabrero", 38);
INSERT INTO commune VALUES(229, "Laja", 38);
INSERT INTO commune VALUES(230, "Los Angeles", 38);
INSERT INTO commune VALUES(231, "Mulchen", 38);
INSERT INTO commune VALUES(232, "Nacimiento", 38);
INSERT INTO commune VALUES(233, "Negrete", 38);
INSERT INTO commune VALUES(234, "Quilaco", 38);
INSERT INTO commune VALUES(235, "Quilleco", 38);
INSERT INTO commune VALUES(236, "San Rosendo", 38);
INSERT INTO commune VALUES(237, "Santa Barbara", 38);
INSERT INTO commune VALUES(238, "Tucapel", 38);
INSERT INTO commune VALUES(239, "Yumbel", 38);

INSERT INTO commune VALUES(240, "Chiguayante", 39);
INSERT INTO commune VALUES(241, "Concepcion", 39);
INSERT INTO commune VALUES(242, "Coronel", 39);
INSERT INTO commune VALUES(243, "Florida", 39);
INSERT INTO commune VALUES(244, "Hualpen", 39);
INSERT INTO commune VALUES(245, "Hualqui", 39);
INSERT INTO commune VALUES(246, "Lota", 39);
INSERT INTO commune VALUES(247, "Penco", 39);
INSERT INTO commune VALUES(248, "San Pedro de la Paz", 39);
INSERT INTO commune VALUES(249, "Santa Juana", 39);
INSERT INTO commune VALUES(250, "Talcahuano", 39);
INSERT INTO commune VALUES(251, "Tome", 39);

INSERT INTO commune VALUES(252, "Carahue", 42);
INSERT INTO commune VALUES(253, "Cholchol", 42);
INSERT INTO commune VALUES(254, "Cunco", 42);
INSERT INTO commune VALUES(255, "Curarrehue", 42);
INSERT INTO commune VALUES(256, "Freire", 42);
INSERT INTO commune VALUES(257, "Galvarino", 42);
INSERT INTO commune VALUES(258, "Gorbea", 42);
INSERT INTO commune VALUES(259, "Lautaro", 42);
INSERT INTO commune VALUES(260, "Loncoche", 42);
INSERT INTO commune VALUES(261, "Melipeuco", 42);
INSERT INTO commune VALUES(262, "Nueva Imperial", 42);
INSERT INTO commune VALUES(263, "Padre Las Casas", 42);
INSERT INTO commune VALUES(264, "Perquenco", 42);
INSERT INTO commune VALUES(265, "Pitrufquén", 42);
INSERT INTO commune VALUES(266, "Pucon", 42);
INSERT INTO commune VALUES(267, "Puerto Saavedra", 42);
INSERT INTO commune VALUES(268, "Temuco", 42);
INSERT INTO commune VALUES(269, "Teodoro Schmidt", 42);
INSERT INTO commune VALUES(270, "Tolten", 42);
INSERT INTO commune VALUES(271, "Vilcun", 42);
INSERT INTO commune VALUES(272, "Villarrica", 42);

INSERT INTO commune VALUES(273, "Angol", 41);
INSERT INTO commune VALUES(274, "Collipulli", 41);
INSERT INTO commune VALUES(275, "Curacautín", 41);
INSERT INTO commune VALUES(276, "Ercilla", 41);
INSERT INTO commune VALUES(277, "Lonquimay", 41);
INSERT INTO commune VALUES(278, "Los Sauces", 41);
INSERT INTO commune VALUES(279, "Lumaco", 41);
INSERT INTO commune VALUES(280, "Puren", 41);
INSERT INTO commune VALUES(281, "Renaico", 41);
INSERT INTO commune VALUES(282, "Traiguén", 41);
INSERT INTO commune VALUES(283, "Victoria", 41);

INSERT INTO commune VALUES(284, "Mariquina", 43);
INSERT INTO commune VALUES(285, "Lanco", 43);
INSERT INTO commune VALUES(286, "Mafil", 43);
INSERT INTO commune VALUES(287, "Valdivia", 43);
INSERT INTO commune VALUES(288, "Corral", 43);
INSERT INTO commune VALUES(289, "Paillaco", 43);
INSERT INTO commune VALUES(290, "Los Lagos", 43);
INSERT INTO commune VALUES(291, "Panguipulli", 43);

INSERT INTO commune VALUES(292, "La Unión", 44);
INSERT INTO commune VALUES(293, "Río Bueno", 44);
INSERT INTO commune VALUES(294, "Lago Ranco", 44);
INSERT INTO commune VALUES(295, "Futrono", 44);

INSERT INTO commune VALUES(296, "Ancud", 47);
INSERT INTO commune VALUES(297, "Castro", 47);
INSERT INTO commune VALUES(298, "Chonchi", 47);
INSERT INTO commune VALUES(299, "Curaco de Velez", 47);
INSERT INTO commune VALUES(300, "Dalcahue", 47);
INSERT INTO commune VALUES(301, "Puqueldon", 47);
INSERT INTO commune VALUES(302, "Queilen", 47);
INSERT INTO commune VALUES(303, "Quemchi", 47);
INSERT INTO commune VALUES(304, "Quellon", 47);
INSERT INTO commune VALUES(305, "Quinchao", 47);

INSERT INTO commune VALUES(306, "Calbuco", 46);
INSERT INTO commune VALUES(307, "Cochamo", 46);
INSERT INTO commune VALUES(308, "Fresia", 46);
INSERT INTO commune VALUES(309, "Frutillar", 46);
INSERT INTO commune VALUES(310, "Llanquihue", 46);
INSERT INTO commune VALUES(311, "Los Muermos", 46);
INSERT INTO commune VALUES(312, "Maullin", 46);
INSERT INTO commune VALUES(313, "Puerto Montt", 46);
INSERT INTO commune VALUES(314, "Puerto Varas", 46);

INSERT INTO commune VALUES(315, "Osorno", 45);
INSERT INTO commune VALUES(316, "Puerto Octay", 45);
INSERT INTO commune VALUES(317, "Purranque", 45);
INSERT INTO commune VALUES(318, "Puyehue", 45);
INSERT INTO commune VALUES(319, "Rio Negro", 45);
INSERT INTO commune VALUES(320, "San Juan de la Costa", 45);
INSERT INTO commune VALUES(321, "San Pablo", 45);

INSERT INTO commune VALUES(322, "Chaiten", 48);
INSERT INTO commune VALUES(323, "Futaleufu", 48);
INSERT INTO commune VALUES(324, "Hualaihue", 48);
INSERT INTO commune VALUES(325, "Palena", 48);

INSERT INTO commune VALUES(326, "Cisnes", 50);
INSERT INTO commune VALUES(327, "Guaitecas", 50);
INSERT INTO commune VALUES(328, "Aysen", 50);

INSERT INTO commune VALUES(329, "Cochrane", 52);
INSERT INTO commune VALUES(330, "O'Higgins", 52);
INSERT INTO commune VALUES(331, "Tortel", 52);

INSERT INTO commune VALUES(332, "Coyhaique", 49);
INSERT INTO commune VALUES(333, "Lago Verde", 49);

INSERT INTO commune VALUES(334, "Chile Chico", 51);
INSERT INTO commune VALUES(335, "Rio Ibañez", 51);

INSERT INTO commune VALUES(336, "Antartica", 56);
INSERT INTO commune VALUES(337, "Cabo de Hornos", 56);

INSERT INTO commune VALUES(338, "Laguna Blanca", 54);
INSERT INTO commune VALUES(339, "Punta Arenas", 54);
INSERT INTO commune VALUES(340, "Rio Verde", 54);
INSERT INTO commune VALUES(341, "San Gregorio", 54);

INSERT INTO commune VALUES(342, "Porvenir", 55);
INSERT INTO commune VALUES(343, "Primavera", 55);
INSERT INTO commune VALUES(344, "Timaukel", 55);

INSERT INTO commune VALUES(345, "Natales", 53);
INSERT INTO commune VALUES(346, "Torres del Paine", 53);
