
-- Creación de esquemas
CREATE SCHEMA IF NOT EXISTS feelback_dev;
CREATE SCHEMA IF NOT EXISTS feelback_test;



-- Creacion de tablas para feelback_dev
CREATE TABLE IF NOT EXISTS feelback_dev.users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE IF NOT EXISTS feelback_dev.sentiments (
    id SERIAL PRIMARY KEY,
    description VARCHAR(20) NOT NULL UNIQUE 
        CHECK (description IN ('positive', 'neutral', 'negative'))
);

CREATE TABLE IF NOT EXISTS feelback_dev.messages (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES feelback_dev.users(id) ON DELETE CASCADE,
    text TEXT NOT NULL,
    liked BOOLEAN DEFAULT NULL,
    id_sentiment INTEGER NOT NULL REFERENCES feelback_dev.sentiments(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS feelback_dev.stats (
    user_id INTEGER PRIMARY KEY REFERENCES feelback_dev.users(id) ON DELETE CASCADE,
    positive INTEGER DEFAULT 0,
    negative INTEGER DEFAULT 0,
    neutral INTEGER DEFAULT 0,
    liked INTEGER DEFAULT 0,
    disliked INTEGER DEFAULT 0
);

-- Índices para usuarios
CREATE INDEX IF NOT EXISTS idx_users_email ON feelback_dev.users(email);
CREATE INDEX IF NOT EXISTS idx_users_username ON feelback_dev.users(username);

-- Índices para mensajes
CREATE INDEX IF NOT EXISTS idx_messages_user_id ON feelback_dev.messages(user_id);
CREATE INDEX IF NOT EXISTS idx_messages_sentiment ON feelback_dev.messages(id_sentiment);
CREATE INDEX IF NOT EXISTS idx_messages_created_at ON feelback_dev.messages(created_at);

-- Índices para estadísticas
CREATE INDEX IF NOT EXISTS idx_stats_user_id ON feelback_dev.stats(user_id);

-- Insertar tipos de sentimientos
INSERT INTO feelback_dev.sentiments (id, description) VALUES 
    (1, 'positive'),
    (2, 'neutral'),
    (3, 'negative')
ON CONFLICT (description) DO NOTHING;



-- ============================================


-- Creación de tablas para feelback_test
CREATE TABLE IF NOT EXISTS feelback_test.users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE IF NOT EXISTS feelback_test.sentiments (
    id SERIAL PRIMARY KEY,
    description VARCHAR(20) NOT NULL UNIQUE 
        CHECK (description IN ('positive', 'neutral', 'negative'))
);

CREATE TABLE IF NOT EXISTS feelback_test.messages (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES feelback_test.users(id) ON DELETE CASCADE,
    text TEXT NOT NULL,
    liked BOOLEAN DEFAULT NULL,
    id_sentiment INTEGER NOT NULL REFERENCES feelback_test.sentiments(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS feelback_test.stats (
    user_id INTEGER PRIMARY KEY REFERENCES feelback_test.users(id) ON DELETE CASCADE,
    positive INTEGER DEFAULT 0,
    negative INTEGER DEFAULT 0,
    neutral INTEGER DEFAULT 0,
    liked INTEGER DEFAULT 0,
    disliked INTEGER DEFAULT 0
);

-- Índices para usuarios
CREATE INDEX IF NOT EXISTS idx_users_email ON feelback_test.users(email);
CREATE INDEX IF NOT EXISTS idx_users_username ON feelback_test.users(username);

-- Índices para mensajes
CREATE INDEX IF NOT EXISTS idx_messages_user_id ON feelback_test.messages(user_id);
CREATE INDEX IF NOT EXISTS idx_messages_sentiment ON feelback_test.messages(id_sentiment);
CREATE INDEX IF NOT EXISTS idx_messages_created_at ON feelback_test.messages(created_at);

-- Índices para estadísticas
CREATE INDEX IF NOT EXISTS idx_stats_user_id ON feelback_test.stats(user_id);

-- Insertar tipos de sentimientos
INSERT INTO feelback_test.sentiments (id, description) VALUES 
    (1, 'positive'),
    (2, 'neutral'),
    (3, 'negative')
ON CONFLICT (description) DO NOTHING;


-- Mostrar información de las tablas creadas
DO $$
BEGIN
    RAISE NOTICE '=== FeelBack Database Initialized ===';
    RAISE NOTICE 'Schemas created: feelback_dev, feelback_test';
    RAISE NOTICE 'Tables created: users, sentiments, messages, stats';
    RAISE NOTICE 'Initial data: 3 sentiment types inserted';
    RAISE NOTICE '============================================';
END $$;

