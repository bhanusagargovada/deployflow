-- MySQL schema for Project Management & Deployment Tracking System
CREATE DATABASE IF NOT EXISTS `project_tracker` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `project_tracker`;

-- Users
CREATE TABLE IF NOT EXISTS `users` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `username` VARCHAR(64) NOT NULL UNIQUE,
  `email` VARCHAR(120) NOT NULL UNIQUE,
  `password_hash` VARCHAR(128) NOT NULL,
  `role` VARCHAR(32) DEFAULT 'Team Member',
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `is_active` TINYINT(1) DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Projects
CREATE TABLE IF NOT EXISTS `projects` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `name` VARCHAR(140) NOT NULL,
  `description` TEXT,
  `priority` VARCHAR(20) DEFAULT 'Medium',
  `deadline` DATE,
  `status` VARCHAR(32) DEFAULT 'Planned',
  `manager_id` INT,
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (manager_id) REFERENCES users(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Tasks
CREATE TABLE IF NOT EXISTS `tasks` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `title` VARCHAR(200) NOT NULL,
  `description` TEXT,
  `priority` VARCHAR(20) DEFAULT 'Medium',
  `deadline` DATE,
  `status` VARCHAR(32) DEFAULT 'To Do',
  `progress` INT DEFAULT 0,
  `project_id` INT,
  `assigned_to` INT,
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
  FOREIGN KEY (assigned_to) REFERENCES users(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Releases
CREATE TABLE IF NOT EXISTS `releases` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `project_id` INT,
  `version` VARCHAR(64) NOT NULL,
  `release_date` DATE,
  `notes` TEXT,
  `status` VARCHAR(32) DEFAULT 'Success',
  `released_by` INT,
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
  FOREIGN KEY (released_by) REFERENCES users(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Project members
CREATE TABLE IF NOT EXISTS `project_members` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `project_id` INT,
  `user_id` INT,
  `role` VARCHAR(64) DEFAULT 'Member',
  FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Activity logs
CREATE TABLE IF NOT EXISTS `activity_logs` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `user_id` INT,
  `action` VARCHAR(200),
  `timestamp` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `meta` TEXT,
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Indexes for performance
CREATE INDEX idx_tasks_project_id ON tasks(project_id);
CREATE INDEX idx_tasks_assigned_to ON tasks(assigned_to);
CREATE INDEX idx_projects_manager_id ON projects(manager_id);
CREATE INDEX idx_comments_task_id ON comments(task_id);
CREATE INDEX idx_notifications_user_id ON notifications(user_id);
