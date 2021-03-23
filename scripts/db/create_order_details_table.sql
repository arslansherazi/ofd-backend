USE ofd_db;
CREATE TABLE IF NOT EXISTS order_details
(
	id INT NOT NULL AUTO_INCREMENT,
	order_id INT NOT NULL,
    item_id INT NOT NULL,
    item_quantity INT NOT NULL,
    item_discount INT NOT NULL,
	created_date TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
	updated_date TIMESTAMP NULL DEFAULT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (order_id) REFERENCES order_history (id),
    FOREIGN KEY (item_id) REFERENCES menu_item (id),
    KEY idx_order (order_id) USING BTREE,
    KEY idx_item (item_id) USING BTREE
);
