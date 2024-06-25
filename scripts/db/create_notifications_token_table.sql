USE ofd_db;
CREATE TABLE IF NOT EXISTS notifications_token
(
	id INT NOT NULL AUTO_INCREMENT,
    buyer_id INT NOT NULL,
    notifications_token VARCHAR(1000) NOT NULL,
	is_active BOOL NOT NULL DEFAULT TRUE,
	created_date TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
	updated_date TIMESTAMP NULL DEFAULT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (buyer_id) REFERENCES buyer (id)
);
