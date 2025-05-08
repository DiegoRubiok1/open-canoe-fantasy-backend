-- Esquema de base de datos profesional para producción
-- Uso de UUIDs, timestamps, índices y campos de auditoría

-- Create database with proper encoding
CREATE DATABASE IF NOT EXISTS `opencanoefantasy`
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

-- Handle user creation and privileges safely
DROP USER IF EXISTS 'fantasy'@'localhost';
CREATE USER 'fantasy'@'localhost' IDENTIFIED BY 'fantasy123';
GRANT ALL PRIVILEGES ON `opencanoefantasy`.* TO 'fantasy'@'localhost';
FLUSH PRIVILEGES;

USE `opencanoefantasy`;

-- Drop existing tables in reverse order of dependencies
DROP TABLE IF EXISTS market;
DROP TABLE IF EXISTS team_players;
DROP TABLE IF EXISTS players;
DROP TABLE IF EXISTS teams;
DROP TABLE IF EXISTS user_leagues;
DROP TABLE IF EXISTS leagues;
DROP TABLE IF EXISTS users;

-- Tabla: users (usuarios)
CREATE TABLE users (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    phone VARCHAR(20),
    role VARCHAR(20) NOT NULL DEFAULT 'user',       -- e.g. user, admin
    status VARCHAR(20) NOT NULL DEFAULT 'active',   -- e.g. active, suspended
    email_verified_at TIMESTAMP NULL,
    last_login_at TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL
);

-- Tabla: leagues (ligas)
CREATE TABLE leagues (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    code VARCHAR(10) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL
);

-- Tabla: user_leagues (usuarios_ligas)
-- Relación many-to-many entre users y leagues, con presupuesto y puntos por usuario en cada liga
CREATE TABLE user_leagues (
    user_id BIGINT UNSIGNED,
    league_id BIGINT UNSIGNED,
    budget DECIMAL(12,2) NOT NULL DEFAULT 1000,
    points INT NOT NULL DEFAULT 0,
    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, league_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (league_id) REFERENCES leagues(id) ON DELETE CASCADE
);

-- Tabla: teams (equipos)
CREATE TABLE teams (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id BIGINT UNSIGNED NOT NULL,
    league_id BIGINT UNSIGNED NOT NULL,
    name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE(user_id, league_id, name),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (league_id) REFERENCES leagues(id) ON DELETE CASCADE
);

-- Tabla: players (deportistas)
CREATE TABLE players (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    category VARCHAR(50) NOT NULL,
    club VARCHAR(100) NOT NULL,
    market_price DECIMAL(12,2) NOT NULL,
    points INT NOT NULL DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Tabla: team_players (equipos_deportistas)
-- Relación many-to-many entre teams y players
CREATE TABLE team_players (
    team_id BIGINT UNSIGNED NOT NULL,
    player_id BIGINT UNSIGNED NOT NULL,
    clause DECIMAL(12,2) NOT NULL,
    titular BOOLEAN NOT NULL DEFAULT FALSE,
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (team_id, player_id),
    FOREIGN KEY (team_id) REFERENCES teams(id) ON DELETE CASCADE,
    FOREIGN KEY (player_id) REFERENCES players(id) ON DELETE CASCADE
);

-- Tabla: market (mercado)
-- Jugadores disponibles en el mercado por liga
CREATE TABLE market (
    league_id BIGINT UNSIGNED NOT NULL,
    player_id BIGINT UNSIGNED NOT NULL,
    available_from TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    price DECIMAL(12,2) NOT NULL,
    PRIMARY KEY (league_id, player_id),
    FOREIGN KEY (league_id) REFERENCES leagues(id) ON DELETE CASCADE,
    FOREIGN KEY (player_id) REFERENCES players(id) ON DELETE CASCADE
);

-- Índices adicionales para optimizar consultas frecuentes
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_teams_user_league ON teams(user_id, league_id);
CREATE INDEX idx_players_club ON players(club);
CREATE INDEX idx_market_league_price ON market(league_id, price);
CREATE INDEX idx_market_player_price ON market(player_id, price);

-- Triggers para actualizar updated_at automáticamente
DELIMITER //

CREATE TRIGGER trg_users_updated_at 
    BEFORE UPDATE ON users
    FOR EACH ROW
BEGIN
    SET NEW.updated_at = CURRENT_TIMESTAMP;
END//

CREATE TRIGGER trg_leagues_updated_at 
    BEFORE UPDATE ON leagues
    FOR EACH ROW
BEGIN
    SET NEW.updated_at = CURRENT_TIMESTAMP;
END//

CREATE TRIGGER trg_teams_updated_at 
    BEFORE UPDATE ON teams
    FOR EACH ROW
BEGIN
    SET NEW.updated_at = CURRENT_TIMESTAMP;
END//

CREATE TRIGGER trg_players_updated_at 
    BEFORE UPDATE ON players
    FOR EACH ROW
BEGIN
    SET NEW.updated_at = CURRENT_TIMESTAMP;
END//

DELIMITER ;

ALTER TABLE market
ADD CONSTRAINT chk_price CHECK (price >= 0);

ALTER TABLE users
ADD CONSTRAINT chk_status CHECK (status IN ('active', 'suspended', 'deleted'));