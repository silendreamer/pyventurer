import json

from app.db.connection import get_connection
from app.models.badges import BADGE_DEFINITIONS
from app.models.domain import Badge, LearnerProfile, ProgressState


class ProgressRepository:
    def save_profile(self, anonymous_user_id: str, profile: LearnerProfile) -> LearnerProfile:
        conn = get_connection()
        conn.execute(
            """INSERT OR REPLACE INTO learner_profiles
               (anonymous_user_id, age_range, experience_level, learning_goal,
                motivation_type, preferred_style, selected_theme_id)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (
                anonymous_user_id,
                profile.age_range,
                profile.experience_level,
                profile.learning_goal,
                profile.motivation_type,
                profile.preferred_style,
                profile.selected_theme_id,
            ),
        )
        conn.commit()
        self._ensure_progress(anonymous_user_id)
        return profile

    def get_profile(self, anonymous_user_id: str) -> LearnerProfile | None:
        conn = get_connection()
        row = conn.execute(
            "SELECT * FROM learner_profiles WHERE anonymous_user_id = ?",
            (anonymous_user_id,),
        ).fetchone()
        if row is None:
            return None
        return LearnerProfile(
            age_range=row["age_range"],
            experience_level=row["experience_level"],
            learning_goal=row["learning_goal"],
            motivation_type=row["motivation_type"],
            preferred_style=row["preferred_style"],
            selected_theme_id=row["selected_theme_id"],
        )

    def update_theme(self, anonymous_user_id: str, theme_id: str) -> LearnerProfile | None:
        profile = self.get_profile(anonymous_user_id)
        if profile is None:
            return None
        conn = get_connection()
        conn.execute(
            "UPDATE learner_profiles SET selected_theme_id = ? WHERE anonymous_user_id = ?",
            (theme_id, anonymous_user_id),
        )
        conn.commit()
        return profile.model_copy(update={"selected_theme_id": theme_id})

    def get_progress(self, anonymous_user_id: str) -> ProgressState:
        return self._ensure_progress(anonymous_user_id)

    def get_progress_for_user(self, user_id: str) -> ProgressState:
        conn = get_connection()
        row = conn.execute(
            "SELECT anonymous_user_id FROM progress WHERE user_id = ? ORDER BY rowid DESC LIMIT 1",
            (user_id,),
        ).fetchone()
        if row is not None:
            return self._read_progress(row["anonymous_user_id"])
        conn.execute(
            "INSERT OR IGNORE INTO progress (anonymous_user_id, user_id) VALUES (?, ?)",
            (user_id, user_id),
        )
        conn.commit()
        return self._read_progress(user_id)

    def record_placement(self, anonymous_user_id: str, assessment_id: str, score: int) -> ProgressState:
        progress = self._ensure_progress(anonymous_user_id)
        scores = progress.placement_scores
        scores[assessment_id] = score
        xp = max(progress.xp, 10)
        conn = get_connection()
        conn.execute(
            "UPDATE progress SET placement_scores = ?, xp = ? WHERE anonymous_user_id = ?",
            (json.dumps(scores), xp, anonymous_user_id),
        )
        conn.commit()
        return self._read_progress(anonymous_user_id)

    def complete_lesson(self, anonymous_user_id: str, lesson_id: str) -> ProgressState:
        progress = self._ensure_progress(anonymous_user_id)
        if lesson_id in progress.completed_lessons:
            return progress
        lessons = progress.completed_lessons + [lesson_id]
        xp = progress.xp + 15
        conn = get_connection()
        conn.execute(
            "UPDATE progress SET completed_lessons = ?, xp = ? WHERE anonymous_user_id = ?",
            (json.dumps(lessons), xp, anonymous_user_id),
        )
        conn.commit()
        return self._read_progress(anonymous_user_id)

    def complete_exercise(self, anonymous_user_id: str, exercise_id: str) -> ProgressState:
        progress = self._ensure_progress(anonymous_user_id)
        if exercise_id in progress.completed_exercises:
            return progress
        exercises = progress.completed_exercises + [exercise_id]
        xp = progress.xp + 25
        streak = max(progress.streak, 1)
        conn = get_connection()
        conn.execute(
            "UPDATE progress SET completed_exercises = ?, xp = ?, streak = ? WHERE anonymous_user_id = ?",
            (json.dumps(exercises), xp, streak, anonymous_user_id),
        )
        conn.commit()
        return self._read_progress(anonymous_user_id)

    def complete_quiz(self, anonymous_user_id: str, quiz_id: str) -> ProgressState:
        progress = self._ensure_progress(anonymous_user_id)
        if quiz_id in progress.completed_quizzes:
            return progress
        quizzes = progress.completed_quizzes + [quiz_id]
        xp = progress.xp + 20
        conn = get_connection()
        conn.execute(
            "UPDATE progress SET completed_quizzes = ?, xp = ? WHERE anonymous_user_id = ?",
            (json.dumps(quizzes), xp, anonymous_user_id),
        )
        conn.commit()
        return self._read_progress(anonymous_user_id)

    def award_badge(self, anonymous_user_id: str, badge: Badge) -> ProgressState:
        progress = self._ensure_progress(anonymous_user_id)
        existing_ids = {b.id for b in progress.badges}
        if badge.id in existing_ids:
            return progress
        badge_ids = [b.id for b in progress.badges] + [badge.id]
        conn = get_connection()
        conn.execute(
            "UPDATE progress SET badge_ids = ? WHERE anonymous_user_id = ?",
            (json.dumps(badge_ids), anonymous_user_id),
        )
        conn.commit()
        return self._read_progress(anonymous_user_id)

    def _ensure_progress(self, anonymous_user_id: str) -> ProgressState:
        conn = get_connection()
        conn.execute(
            "INSERT OR IGNORE INTO progress (anonymous_user_id) VALUES (?)",
            (anonymous_user_id,),
        )
        conn.commit()
        return self._read_progress(anonymous_user_id)

    def _read_progress(self, anonymous_user_id: str) -> ProgressState:
        conn = get_connection()
        row = conn.execute(
            "SELECT * FROM progress WHERE anonymous_user_id = ?",
            (anonymous_user_id,),
        ).fetchone()
        badge_ids = json.loads(row["badge_ids"])
        badges = [BADGE_DEFINITIONS[bid] for bid in badge_ids if bid in BADGE_DEFINITIONS]
        return ProgressState(
            anonymous_user_id=row["anonymous_user_id"],
            xp=row["xp"],
            streak=row["streak"],
            completed_lessons=json.loads(row["completed_lessons"]),
            completed_exercises=json.loads(row["completed_exercises"]),
            completed_quizzes=json.loads(row["completed_quizzes"]),
            placement_scores=json.loads(row["placement_scores"]),
            badges=badges,
        )


progress_repository = ProgressRepository()
