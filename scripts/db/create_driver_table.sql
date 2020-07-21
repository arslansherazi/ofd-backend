USE ofd_db;
CREATE TABLE IF NOT EXISTS driver
(
	id INT NOT NULL AUTO_INCREMENT,
	order_id INT NOT NULL,
    first_name VARCHAR(100) NOT NULL,
	last_name VARCHAR(100) NOT NULL,
	vehicle_model VARCHAR(50) NOT NULL,
	vehicle_number VARCHAR(50) NOT NULL,
	contact_no VARCHAR(50) NOT NULL,
	created_date TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
	updated_date TIMESTAMP NULL DEFAULT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (order_id) REFERENCES order_history (id)
);
