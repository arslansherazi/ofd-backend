USE ofd_db;
CREATE TABLE IF NOT EXISTS order_history
(
	id INT NOT NULL AUTO_INCREMENT,
	merchant_id INT NOT NULL,
    buyer_id INT NOT NULL,
    order_number VARCHAR(100) NOT NULL,
	status VARCHAR(255) NOT NULL DEFAULT 'Placed',
	price INT NOT NULL,
	discount INT NULL DEFAULT 0,
	is_delivery BOOLEAN NOT NULL DEFAULT FALSE,
	delivery_address VARCHAR(255) NULL DEFAULT NULL,
	latitude FLOAT NULL DEFAULT NULL,
	longitude FLOAT NULL DEFAULT NULL,
	is_price_changed BOOL NOT NULL DEFAULT FALSE,
	created_date TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
	updated_date TIMESTAMP NULL DEFAULT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (merchant_id) REFERENCES merchant (id),
    FOREIGN KEY (buyer_id) REFERENCES buyer (id),
    KEY idx_status (status) USING BTREE,
    KEY idx_delivery (is_delivery) USING BTREE
);
