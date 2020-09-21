USE ofd_db;
CREATE TABLE IF NOT EXISTS feedback
(
	id INT NOT NULL AUTO_INCREMENT,
	buyer_id INT NOT NULL,
	menu_item_id INT NOT NULL,
	review VARCHAR(255) NULL DEFAULT NULL,
	rating FLOAT NOT NULL,
	created_date TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
	updated_date TIMESTAMP NULL DEFAULT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (buyer_id) REFERENCES buyer (id),
    FOREIGN KEY (menu_item_id) REFERENCES menu_item (id),
    KEY idx_buyer (buyer_id) USING BTREE,
    KEY idx_menu_item (menu_item_id) USING BTREE
);
