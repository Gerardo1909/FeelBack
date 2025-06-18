-- Modelo de datos diseñado para FeelBack

-- ===========================================
-- 🧍‍♂️ TABLA USERS
-- Información de registro y autenticación
-- ===========================================

CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ===========================================
-- 💟 TABLA SENTIMENTS
-- Cada tipo de sentimiento disponible en el sistema
-- ===========================================

CREATE TABLE IF NOT EXISTS sentiments (
    id SERIAL PRIMARY KEY,
    description VARCHAR(20) NOT NULL UNIQUE 
        CHECK (description IN ('positive', 'neutral', 'negative'))
);

-- ===========================================
-- 💬 TABLA MESSAGES
-- Cada mensaje enviado al sistema con su resultado de sentimiento
-- ===========================================

CREATE TABLE IF NOT EXISTS messages (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    text TEXT NOT NULL,
    liked BOOLEAN DEFAULT NULL,
    id_sentiment INTEGER NOT NULL REFERENCES sentiments(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ===========================================
-- 📊 TABLA STATS
-- Estadísticas de mensajes enviados por el usuario
-- ===========================================

CREATE TABLE IF NOT EXISTS stats (
    user_id INTEGER PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
    positive INTEGER DEFAULT 0,
    negative INTEGER DEFAULT 0,
    neutral INTEGER DEFAULT 0,
    liked INTEGER DEFAULT 0,
    disliked INTEGER DEFAULT 0
);

-- ===========================================
-- 🔗 ÍNDICES PARA OPTIMIZACIÓN
-- ===========================================

-- Índices para usuarios
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);

-- Índices para mensajes
CREATE INDEX IF NOT EXISTS idx_messages_user_id ON messages(user_id);
CREATE INDEX IF NOT EXISTS idx_messages_sentiment ON messages(id_sentiment);
CREATE INDEX IF NOT EXISTS idx_messages_created_at ON messages(created_at);

-- Índices para estadísticas
CREATE INDEX IF NOT EXISTS idx_stats_user_id ON stats(user_id);


-- ===========================================
-- 🚀 TRIGGERS Y FUNCIONES
-- ===========================================

-- Función para actualizar estadísticas automáticamente
CREATE OR REPLACE FUNCTION update_user_stats()
RETURNS TRIGGER AS $$
BEGIN
    -- Si es un INSERT, incrementar contador
    IF TG_OP = 'INSERT' THEN
        INSERT INTO stats (user_id, positive, negative, neutral)
        VALUES (NEW.user_id, 
                CASE WHEN NEW.id_sentiment = 1 THEN 1 ELSE 0 END,
                CASE WHEN NEW.id_sentiment = 3 THEN 1 ELSE 0 END,
                CASE WHEN NEW.id_sentiment = 2 THEN 1 ELSE 0 END,
                CASE WHEN NEW.liked IS TRUE THEN 1 ELSE 0 END,
                CASE WHEN NEW.liked IS FALSE THEN 1 ELSE 0 END)
        ON CONFLICT (user_id) DO UPDATE SET
            positive = stats.positive + CASE WHEN NEW.id_sentiment = 1 THEN 1 ELSE 0 END,
            negative = stats.negative + CASE WHEN NEW.id_sentiment = 3 THEN 1 ELSE 0 END,
            neutral = stats.neutral + CASE WHEN NEW.id_sentiment = 2 THEN 1 ELSE 0 END, 
            liked = stats.liked + CASE WHEN NEW.liked IS TRUE THEN 1 ELSE 0 END,
            disliked = stats.disliked + CASE WHEN NEW.liked IS FALSE THEN 1 ELSE 0 END;
        RETURN NEW;
    END IF;
    
    -- Si es un DELETE, decrementar contador
    IF TG_OP = 'DELETE' THEN
        UPDATE stats SET
            positive = GREATEST(0, positive - CASE WHEN OLD.id_sentiment = 1 THEN 1 ELSE 0 END),
            negative = GREATEST(0, negative - CASE WHEN OLD.id_sentiment = 3 THEN 1 ELSE 0 END),
            neutral = GREATEST(0, neutral - CASE WHEN OLD.id_sentiment = 2 THEN 1 ELSE 0 END),
            liked = GREATEST(0, liked - CASE WHEN OLD.liked IS TRUE THEN 1 ELSE 0 END),
            disliked = GREATEST(0, disliked - CASE WHEN OLD.liked IS FALSE THEN 1 ELSE 0 END)
        WHERE user_id = OLD.user_id;
        RETURN OLD;
    END IF;
    
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

-- Trigger para actualizar estadísticas automáticamente
CREATE TRIGGER trigger_update_stats
    AFTER INSERT OR DELETE ON messages
    FOR EACH ROW
    EXECUTE FUNCTION update_user_stats();

-- Función para crear estadísticas iniciales al crear un usuario
CREATE OR REPLACE FUNCTION create_initial_stats()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO stats (user_id, positive, negative, neutral, liked, disliked)
    VALUES (NEW.id, 0, 0, 0, 0, 0);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger para crear estadísticas iniciales
CREATE TRIGGER trigger_create_initial_stats
    AFTER INSERT ON users
    FOR EACH ROW
    EXECUTE FUNCTION create_initial_stats();

-- ===========================================
-- 📊 DATOS INICIALES
-- ===========================================

-- Insertar tipos de sentimientos
INSERT INTO sentiments (id, description) VALUES 
    (1, 'positive'),
    (2, 'neutral'),
    (3, 'negative')
ON CONFLICT (description) DO NOTHING;

-- ===========================================
-- ✅ VERIFICACIÓN DEL ESQUEMA
-- ===========================================

-- Mostrar información de las tablas creadas
DO $$
BEGIN
    RAISE NOTICE '=== FeelBack Database Schema Initialized ===';
    RAISE NOTICE 'Tables created: users, sentiments, messages, stats';
    RAISE NOTICE 'Views created: v_messages_complete, v_user_stats';
    RAISE NOTICE 'Triggers created: update_stats, create_initial_stats';
    RAISE NOTICE 'Initial data: 3 sentiment types inserted';
    RAISE NOTICE '============================================';
END $$;

