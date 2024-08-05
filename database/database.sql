CREATE TABLE IF NOT EXISTS `datasets` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `name` VARCHAR(255) NOT NULL,
  `type` VARCHAR(255) NOT NULL,
  `created_at` TIMESTAMP,
  `updated_at` TIMESTAMP
);

CREATE TABLE IF NOT EXISTS `dataset_items` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `dataset_id` INT NOT NULL,
  `role` VARCHAR(255),
  `parts` TEXT,
  `created_at` TIMESTAMP,
  `updated_at` TIMESTAMP,
  FOREIGN KEY (`dataset_id`) REFERENCES datasets(`id`) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS `conversations` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `name` VARCHAR(255) NOT NULL,
  `datasets_ids` TEXT NOT NULL,
  `created_at` TIMESTAMP,
  `updated_at` TIMESTAMP
);

CREATE TABLE IF NOT EXISTS `attachments` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `name` VARCHAR(255) NOT NULL,
  `path` VARCHAR(255) NOT NULL,
  `created_at` TIMESTAMP,
  `updated_at` TIMESTAMP
);

CREATE TABLE IF NOT EXISTS `messages` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `conversation_id` INT NOT NULL,
  `role` TEXT NOT NULL CHECK (`role` IN ('user', 'model')) DEFAULT 'user',
  `content` TEXT,
  `attachments_ids` INT,
  `created_at` TIMESTAMP,
  `updated_at` TIMESTAMP,
  FOREIGN KEY (`conversation_id`) REFERENCES conversations(`id`) ON DELETE CASCADE
);
