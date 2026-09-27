-- MySQL schema for DeployFlow
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

-- Task comments
CREATE TABLE IF NOT EXISTS `comments` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `task_id` INT NOT NULL,
  `user_id` INT NOT NULL,
  `parent_id` INT NULL,
  `content` TEXT NOT NULL,
  `attachment_path` VARCHAR(255),
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (task_id) REFERENCES tasks(id) ON DELETE CASCADE,
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
  FOREIGN KEY (parent_id) REFERENCES comments(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Comment read receipts
CREATE TABLE IF NOT EXISTS `comment_read_receipts` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `comment_id` INT NOT NULL,
  `user_id` INT NOT NULL,
  `seen_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  UNIQUE KEY `uq_comment_read_receipt` (`comment_id`, `user_id`),
  FOREIGN KEY (comment_id) REFERENCES comments(id) ON DELETE CASCADE,
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Clarification requests
CREATE TABLE IF NOT EXISTS `clarification_requests` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `task_id` INT NOT NULL,
  `raised_by` INT NOT NULL,
  `assigned_to` INT NULL,
  `question` TEXT NOT NULL,
  `answer` TEXT,
  `status` VARCHAR(32) DEFAULT 'Open',
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `resolved_at` DATETIME NULL,
  FOREIGN KEY (task_id) REFERENCES tasks(id) ON DELETE CASCADE,
  FOREIGN KEY (raised_by) REFERENCES users(id) ON DELETE CASCADE,
  FOREIGN KEY (assigned_to) REFERENCES users(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Status reports
CREATE TABLE IF NOT EXISTS `status_reports` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `task_id` INT NULL,
  `project_id` INT NOT NULL,
  `submitted_by` INT NOT NULL,
  `report_date` DATE,
  `work_done` TEXT NOT NULL,
  `blockers` TEXT,
  `hours_spent` DECIMAL(10,2),
  `next_steps` TEXT,
  `status` VARCHAR(32) DEFAULT 'Pending',
  `manager_feedback` TEXT,
  `reviewed_by` INT NULL,
  `reviewed_at` DATETIME NULL,
  FOREIGN KEY (task_id) REFERENCES tasks(id) ON DELETE SET NULL,
  FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
  FOREIGN KEY (submitted_by) REFERENCES users(id) ON DELETE CASCADE,
  FOREIGN KEY (reviewed_by) REFERENCES users(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Announcements
CREATE TABLE IF NOT EXISTS `announcements` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `project_id` INT NOT NULL,
  `posted_by` INT NOT NULL,
  `message` TEXT NOT NULL,
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `pinned` TINYINT(1) DEFAULT 0,
  FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
  FOREIGN KEY (posted_by) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Notifications
CREATE TABLE IF NOT EXISTS `notifications` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `user_id` INT,
  `message` VARCHAR(255),
  `link` VARCHAR(255),
  `is_read` TINYINT(1) DEFAULT 0,
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Indexes for performance
CREATE INDEX idx_tasks_project_id ON tasks(project_id);
CREATE INDEX idx_tasks_assigned_to ON tasks(assigned_to);
CREATE INDEX idx_projects_manager_id ON projects(manager_id);
CREATE INDEX idx_comments_task_id ON comments(task_id);
CREATE INDEX idx_notifications_user_id ON notifications(user_id);
CREATE INDEX idx_comment_read_receipts_comment_id ON comment_read_receipts(comment_id);
CREATE INDEX idx_comment_read_receipts_user_id ON comment_read_receipts(user_id);
CREATE INDEX idx_clarification_requests_task_id ON clarification_requests(task_id);
CREATE INDEX idx_status_reports_project_id ON status_reports(project_id);
CREATE INDEX idx_status_reports_task_id ON status_reports(task_id);
CREATE INDEX idx_announcements_project_id ON announcements(project_id);
