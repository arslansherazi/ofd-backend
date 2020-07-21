USE ofd_db;
CREATE TABLE IF NOT EXISTS ingredient
(
	id INT NOT NULL AUTO_INCREMENT,
    dish_id INT NOT NULL,
    name VARCHAR(100) NOT NULL,
    quantity INT NOT NULL,
    unit varchar(50) NOT NULL,
    created_date TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
	updated_date TIMESTAMP NULL DEFAULT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (dish_id) REFERENCES dish (id),
    KEY idx_name (name) USING BTREE
);
