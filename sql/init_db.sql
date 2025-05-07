-- Esquema de base de datos profesional para producción
-- Uso de UUIDs, timestamps, índices y campos de auditoría

-- Tabla: users (usuarios)
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    phone VARCHAR(20),
    role VARCHAR(20) NOT NULL DEFAULT 'user',       -- e.g. user, admin
    status VARCHAR(20) NOT NULL DEFAULT 'active',   -- e.g. active, suspended
    email_verified_at TIMESTAMP WITH TIME ZONE,
    last_login_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
    deleted_at TIMESTAMP WITH TIME ZONE               -- para soft-delete
);

-- Tabla: leagues (ligas)
CREATE TABLE leagues (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL UNIQUE,
    code VARCHAR(10) NOT NULL UNIQUE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
    deleted_at TIMESTAMP WITH TIME ZONE
);

-- Tabla: user_leagues (usuarios_ligas)
-- Relación many-to-many entre users y leagues, con presupuesto y puntos por usuario en cada liga
CREATE TABLE user_leagues (
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    league_id UUID NOT NULL REFERENCES leagues(id) ON DELETE CASCADE,
    budget NUMERIC(12,2) NOT NULL DEFAULT 1000,
    points INTEGER NOT NULL DEFAULT 0,
    joined_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
    PRIMARY KEY (user_id, league_id)
);

-- Tabla: teams (equipos)
CREATE TABLE teams (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    league_id UUID NOT NULL REFERENCES leagues(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
    UNIQUE(user_id, league_id, name)
);

-- Tabla: players (deportistas)
CREATE TABLE players (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(150) NOT NULL,
    category VARCHAR(50),
    club VARCHAR(100),
    market_price NUMERIC(12,2) NOT NULL,
    points INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now()
);

-- Tabla: team_players (equipos_deportistas)
-- Relación many-to-many entre teams y players
CREATE TABLE team_players (
    team_id UUID NOT NULL REFERENCES teams(id) ON DELETE CASCADE,
    player_id UUID NOT NULL REFERENCES players(id) ON DELETE CASCADE,
    added_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
    PRIMARY KEY (team_id, player_id)
);

-- Tabla: market (mercado)
-- Jugadores disponibles en el mercado por liga
CREATE TABLE market (
    league_id UUID NOT NULL REFERENCES leagues(id) ON DELETE CASCADE,
    player_id UUID NOT NULL REFERENCES players(id) ON DELETE CASCADE,
    available_from TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
    price NUMERIC(12,2) NOT NULL,
    PRIMARY KEY (league_id, player_id)
);

-- Índices adicionales para optimizar consultas frecuentes
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_teams_user_league ON teams(user_id, league_id);
CREATE INDEX idx_players_club ON players(club);
CREATE INDEX idx_market_league_price ON market(league_id, price);

-- Triggers para actualizar updated_at automáticamente
CREATE OR REPLACE FUNCTION set_updated_at()
RETURNS TRIGGER AS $$
BEGIN
   NEW.updated_at = now();
   RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Asociar trigger en tablas con updated_at
DO $$
BEGIN
  FOR tbl IN ARRAY['users','leagues','teams','players'] LOOP
    EXECUTE format('CREATE TRIGGER trg_%I_updated_at BEFORE UPDATE ON %I FOR EACH ROW EXECUTE FUNCTION set_updated_at()', tbl, tbl);
  END LOOP;
END;
$$;