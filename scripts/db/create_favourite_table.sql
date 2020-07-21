USE ofd_db;
CREATE TABLE IF NOT EXISTS favourite
(
	id INT NOT NULL AUTO_INCREMENT,
	user_id INT NOT NULL,
    menu_item_id INT NOT NULL,
	created_date TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
	updated_date TIMESTAMP NULL DEFAULT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (user_id) REFERENCES apis_user (id),
    FOREIGN KEY (menu_item_id) REFERENCES menu_item (id),
    KEY idx_status (user_id) USING BTREE,
    KEY idx_delivery (menu_item_id) USING BTREE
);
