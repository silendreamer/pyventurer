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

CREATE TABLE IF NOT EXISTS languages (
    id          TEXT PRIMARY KEY,
    name        TEXT NOT NULL,
    slug        TEXT UNIQUE NOT NULL,
    description TEXT NOT NULL,
    status      TEXT NOT NULL DEFAULT 'published',
    is_active   INTEGER NOT NULL DEFAULT 1,
    order_index INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS courses (
    id                 TEXT PRIMARY KEY,
    language_id        TEXT NOT NULL,
    title              TEXT NOT NULL,
    slug               TEXT UNIQUE NOT NULL,
    description        TEXT NOT NULL,
    target_audience    TEXT NOT NULL,
    difficulty         TEXT NOT NULL,
    estimated_duration TEXT NOT NULL,
    course_goal        TEXT NOT NULL DEFAULT '',
    next_course_slug   TEXT,
    status             TEXT NOT NULL DEFAULT 'published',
    order_index        INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY(language_id) REFERENCES languages(id)
);

CREATE TABLE IF NOT EXISTS course_prerequisites (
    course_id              TEXT NOT NULL,
    prerequisite_course_id TEXT NOT NULL,
    PRIMARY KEY(course_id, prerequisite_course_id),
    FOREIGN KEY(course_id) REFERENCES courses(id),
    FOREIGN KEY(prerequisite_course_id) REFERENCES courses(id)
);

CREATE TABLE IF NOT EXISTS modules (
    id          TEXT PRIMARY KEY,
    course_id   TEXT NOT NULL,
    title       TEXT NOT NULL,
    slug        TEXT NOT NULL,
    description TEXT NOT NULL,
    status      TEXT NOT NULL DEFAULT 'published',
    order_index INTEGER NOT NULL DEFAULT 0,
    UNIQUE(course_id, slug),
    FOREIGN KEY(course_id) REFERENCES courses(id)
);

CREATE TABLE IF NOT EXISTS lessons (
    id                 TEXT PRIMARY KEY,
    module_id          TEXT NOT NULL,
    course_id          TEXT NOT NULL,
    title              TEXT NOT NULL,
    slug               TEXT NOT NULL,
    topic              TEXT NOT NULL,
    short_description  TEXT NOT NULL,
    learning_objective TEXT NOT NULL,
    body               TEXT NOT NULL,
    example_code       TEXT,
    starter_code       TEXT,
    estimated_minutes  INTEGER NOT NULL DEFAULT 5,
    status             TEXT NOT NULL DEFAULT 'preview',
    order_index        INTEGER NOT NULL DEFAULT 0,
    UNIQUE(course_id, slug),
    FOREIGN KEY(module_id) REFERENCES modules(id),
    FOREIGN KEY(course_id) REFERENCES courses(id)
);

CREATE TABLE IF NOT EXISTS exercises (
    id            TEXT PRIMARY KEY,
    lesson_id     TEXT NOT NULL,
    title         TEXT NOT NULL,
    slug          TEXT UNIQUE NOT NULL,
    instructions  TEXT NOT NULL,
    starter_code  TEXT NOT NULL,
    language_id   TEXT NOT NULL,
    grader_type   TEXT NOT NULL,
    grader_config TEXT NOT NULL DEFAULT '{}',
    status        TEXT NOT NULL DEFAULT 'preview',
    order_index   INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY(lesson_id) REFERENCES lessons(id),
    FOREIGN KEY(language_id) REFERENCES languages(id)
);

CREATE TABLE IF NOT EXISTS quizzes (
    id            TEXT PRIMARY KEY,
    module_id     TEXT NOT NULL,
    lesson_id     TEXT,
    title         TEXT NOT NULL,
    slug          TEXT UNIQUE NOT NULL,
    passing_score INTEGER NOT NULL DEFAULT 70,
    status        TEXT NOT NULL DEFAULT 'published',
    order_index   INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY(module_id) REFERENCES modules(id),
    FOREIGN KEY(lesson_id) REFERENCES lessons(id)
);

CREATE TABLE IF NOT EXISTS quiz_questions (
    id          TEXT PRIMARY KEY,
    quiz_id     TEXT NOT NULL,
    prompt      TEXT NOT NULL,
    explanation TEXT NOT NULL,
    order_index INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY(quiz_id) REFERENCES quizzes(id)
);

CREATE TABLE IF NOT EXISTS quiz_answer_choices (
    id          TEXT PRIMARY KEY,
    question_id TEXT NOT NULL,
    choice_text TEXT NOT NULL,
    is_correct  INTEGER NOT NULL DEFAULT 0,
    order_index INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY(question_id) REFERENCES quiz_questions(id)
);

CREATE TABLE IF NOT EXISTS projects (
    id           TEXT PRIMARY KEY,
    course_id    TEXT NOT NULL,
    module_id    TEXT,
    title        TEXT NOT NULL,
    slug         TEXT UNIQUE NOT NULL,
    description  TEXT NOT NULL,
    project_type TEXT NOT NULL DEFAULT 'mini',
    status       TEXT NOT NULL DEFAULT 'preview',
    order_index  INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY(course_id) REFERENCES courses(id),
    FOREIGN KEY(module_id) REFERENCES modules(id)
);

CREATE TABLE IF NOT EXISTS course_completion_rules (
    course_id                         TEXT PRIMARY KEY,
    lesson_completion_threshold       INTEGER NOT NULL DEFAULT 80,
    average_quiz_score_threshold      INTEGER NOT NULL DEFAULT 70,
    final_assessment_score_threshold  INTEGER NOT NULL DEFAULT 70,
    required_mini_projects            INTEGER NOT NULL DEFAULT 3,
    required_final_projects           INTEGER NOT NULL DEFAULT 1,
    unlock_course_slug                TEXT,
    FOREIGN KEY(course_id) REFERENCES courses(id)
);

CREATE TABLE IF NOT EXISTS placement_assessments (
    id            TEXT PRIMARY KEY,
    course_id     TEXT NOT NULL,
    title         TEXT NOT NULL,
    passing_score INTEGER NOT NULL DEFAULT 67,
    status        TEXT NOT NULL DEFAULT 'published',
    FOREIGN KEY(course_id) REFERENCES courses(id)
);

CREATE TABLE IF NOT EXISTS placement_questions (
    id             TEXT PRIMARY KEY,
    assessment_id  TEXT NOT NULL,
    prompt         TEXT NOT NULL,
    choices        TEXT NOT NULL,
    correct_choice TEXT NOT NULL,
    order_index    INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY(assessment_id) REFERENCES placement_assessments(id)
);

CREATE INDEX IF NOT EXISTS idx_courses_language ON courses(language_id);
CREATE INDEX IF NOT EXISTS idx_modules_course ON modules(course_id);
CREATE INDEX IF NOT EXISTS idx_lessons_module ON lessons(module_id);
CREATE INDEX IF NOT EXISTS idx_exercises_lesson ON exercises(lesson_id);
CREATE INDEX IF NOT EXISTS idx_quizzes_module ON quizzes(module_id);
CREATE INDEX IF NOT EXISTS idx_quiz_questions_quiz ON quiz_questions(quiz_id);
CREATE INDEX IF NOT EXISTS idx_projects_course ON projects(course_id);
