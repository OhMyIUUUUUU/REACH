-- 01_seed_users.sql
-- Seed data for REACH development

INSERT INTO users (id, email, username, password_hash, role)
VALUES
    ('a0000000-0000-0000-0000-000000000001', 'admin@reach.local', 'admin', '$2a$10$abcdefghijklmnopqrstuvwxyz123456', 'admin'),
    ('a0000000-0000-0000-0000-000000000002', 'developer@reach.local', 'dev_user', '$2a$10$abcdefghijklmnopqrstuvwxyz123456', 'user')
ON CONFLICT (email) DO NOTHING;

INSERT INTO activity_logs (user_id, action, details)
VALUES
    ('a0000000-0000-0000-0000-000000000001', 'system_init', '{"message": "Database initialized with seed data"}');
