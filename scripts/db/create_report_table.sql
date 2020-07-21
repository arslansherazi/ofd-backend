USE ofd_db;
CREATE TABLE IF NOT EXISTS report
(
	id INT NOT NULL AUTO_INCREMENT,
	merchant_id INT NOT NULL,
	last_day_orders INT NOT NULL DEFAULT 0,
	last_week_orders INT NOT NULL DEFAULT 0,
	last_month_orders INT NOT NULL DEFAULT 0,
	total_orders INT NOT NULL DEFAULT 0,
	total_revenue INT NOT NULL DEFAULT 0,
	created_date TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
	updated_date TIMESTAMP NULL DEFAULT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (merchant_id) REFERENCES merchant (id),
    KEY idx_merchant (merchant_id) USING BTREE
);
