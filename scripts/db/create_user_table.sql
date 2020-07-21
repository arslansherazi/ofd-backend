USE ofd_db;
CREATE TABLE IF NOT EXISTS user
(
	id INT NOT NULL AUTO_INCREMENT,
	username VARCHAR(100) NOT NULL,
	email VARCHAR(255) NOT NULL,
	password VARCHAR(100) NOT NULL,
	profile_image_url TEXT NULL DEFAULT NULL,
	user_type INT NOT NULL,
	email_verification_code INT NULL DEFAULT NULL,
	forgot_password_code INT NULL DEFAULT NULL,
	change_email_code INT NULL DEFAULT NULL,
	is_email_verified BOOL NOT NULL DEFAULT FALSE,
	email_verification_code_expiration TIMESTAMP NULL DEFAULT NULL,
	forgot_password_code_expiration TIMESTAMP NULL DEFAULT NULL,
	change_email_code_expiration TIMESTAMP NULL DEFAULT NULL,
	change_password_token VARCHAR(256) NULL DEFAULT NULL,
	is_active BOOL NOT NULL DEFAULT TRUE,
	created_date TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
	updated_date TIMESTAMP NULL DEFAULT NULL,
    PRIMARY KEY (id),
    KEY idx_username (username) USING BTREE,
    KEY idx_email (email) USING BTREE,
    KEY idx_user_type (user_type) USING BTREE
);
