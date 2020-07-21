USE ofd_db;
CREATE TABLE IF NOT EXISTS merchant
(
	id INT NOT NULL AUTO_INCREMENT,
	user_id INT NOT NULL,
	name VARCHAR(100) NOT NULL,
	title VARCHAR(255) NULL DEFAULT NULL,
	contact_no VARCHAR(100) NOT NULL,
	address VARCHAR(255) NOT NULL,
	latitude FLOAT NOT NULL,
	longitude FLOAT NOT NULL,
	location_id INT NOT NULL,
	menus_limit INT NOT NULL,
	items_limit INT NOT NULL,
	is_takeaway_enabled BOOLEAN NOT NULL,
	is_delivery_enabled BOOLEAN NOT NULL,
	opening_time DATETIME NULL DEFAULT NULL,
	closing_time DATETIME NULL DEFAULT NULL,
	opening_days VARCHAR(255) NULL DEFAULT NULL,
	is_open_all_day BOOLEAN NOT NULL DEFAULT FALSE,
	is_open_all_week BOOLEAN NOT NULL DEFAULT FALSE,
	created_date TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
	updated_date TIMESTAMP NULL DEFAULT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (user_id) REFERENCES user (id)
    FOREIGN KEY (location_id) REFERENCES user (location),
    KEY idx_name (name) USING BTREE
    KEY idx_location (location_id) USING BTREE
    KEY idx_name (name) USING BTREE
    KEY idx_takeaway (is_takeaway_enabled) USING BTREE
    KEY idx_delivery (is_delivery_enabled) USING BTREE
);
