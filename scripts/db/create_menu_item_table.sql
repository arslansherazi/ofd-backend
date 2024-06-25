USE ofd_db;
CREATE TABLE IF NOT EXISTS menu_item
(
	id INT NOT NULL AUTO_INCREMENT,
	merchant_id INT NOT NULL,
    name VARCHAR(100) NOT NULL,
	unit VARCHAR(50) NOT NULL,
	quantity INT NOT NULL,
	price INT NOT NULL,
	discount INT NULL DEFAULT 0,
	image_url TEXT NOT NULL,
	rating FLOAT NULL DEFAULT NULL,
	total_rating FLOAT NULL DEFAULT NULL,
	rating_count INT NULL DEFAULT NULL,
	is_active BOOL NOT NULL DEFAULT True,
	created_date TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
	updated_date TIMESTAMP NULL DEFAULT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (merchant_id) REFERENCES merchant (id),
    KEY idx_name (name) USING BTREE,
    KEY idx_discount (discount) USING BTREE,
    KEY idx_rating (rating) USING BTREE
);
