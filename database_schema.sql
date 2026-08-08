CREATE DATABASE IF NOT EXISTS gov_scheme_connect;
USE gov_scheme_connect;

DROP TABLE IF EXISTS applications;
DROP TABLE IF EXISTS schemes;
DROP TABLE IF EXISTS users;

-- ==============================================================================
-- 1. USERS TABLE
-- ==============================================================================
CREATE TABLE users (
    id INT(11) AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('admin', 'citizen') NOT NULL DEFAULT 'citizen',
    full_name VARCHAR(100) NOT NULL,
    phone_number VARCHAR(15) DEFAULT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    is_active TINYINT(1) NOT NULL DEFAULT 1,
    
    -- Indexes
    INDEX idx_email (email),
    INDEX idx_role (role)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ==============================================================================
-- 2. SCHEMES TABLE
-- ==============================================================================
CREATE TABLE schemes (
    id INT(11) AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    category VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    eligibility_criteria TEXT NOT NULL,
    required_documents TEXT NOT NULL,
    created_by INT(11) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    is_active TINYINT(1) NOT NULL DEFAULT 1,
    
    -- Foreign Key
    FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE RESTRICT,
    
    -- Indexes
    INDEX idx_category (category),
    INDEX created_by (created_by)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ==============================================================================
-- 3. APPLICATIONS TABLE
-- ==============================================================================
CREATE TABLE applications (
    id INT(11) AUTO_INCREMENT PRIMARY KEY,
    user_id INT(11) NOT NULL,
    scheme_id INT(11) NOT NULL,
    status ENUM('Pending', 'Accepted', 'Rejected') NOT NULL DEFAULT 'Pending',
    document_url TEXT NOT NULL,
    rejection_reason TEXT DEFAULT NULL,
    applied_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    reviewed_by INT(11) DEFAULT NULL,
    reviewed_at TIMESTAMP NULL DEFAULT NULL,
    admin_remarks TEXT DEFAULT NULL,
    
    -- Foreign Keys
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (scheme_id) REFERENCES schemes(id) ON DELETE CASCADE,
    FOREIGN KEY (reviewed_by) REFERENCES users(id) ON DELETE SET NULL,
    
    -- Constraints & Indexes
    UNIQUE KEY unique_user_scheme (user_id, scheme_id),
    INDEX idx_status (status),
    INDEX idx_user_id (user_id),
    INDEX idx_scheme_id (scheme_id),
    INDEX reviewed_by (reviewed_by)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;