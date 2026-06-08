CREATE TABLE IF NOT EXISTS learner_profiles (
    anonymous_user_id TEXT PRIMARY KEY,
    user_id           TEXT,
    age_range         TEXT NOT NULL,
    experience_level  TEXT NOT NULL,
    learning_goal     TEXT NOT NULL,
    motivation_type   TEXT NOT NULL,
    preferred_style   TEXT NOT NULL,
    selected_theme_id TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS progress (
    anonymous_user_id   TEXT PRIMARY KEY,
    user_id             TEXT,
    xp                  INTEGER NOT NULL DEFAULT 0,
    streak              INTEGER NOT NULL DEFAULT 0,
    completed_lessons   TEXT NOT NULL DEFAULT '[]',
    completed_exercises TEXT NOT NULL DEFAULT '[]',
    completed_quizzes   TEXT NOT NULL DEFAULT '[]',
    placement_scores    TEXT NOT NULL DEFAULT '{}',
    badge_ids           TEXT NOT NULL DEFAULT '[]'
);

CREATE TABLE IF NOT EXISTS users (
    id            TEXT PRIMARY KEY,
    email         TEXT UNIQUE NOT NULL,
    name          TEXT NOT NULL,
    password_hash TEXT NOT NULL,
    created_at    TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_profiles_user_id ON learner_profiles(user_id);
CREATE INDEX IF NOT EXISTS idx_progress_user_id ON progress(user_id);
