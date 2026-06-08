import io
from contextlib import redirect_stdout

from app.repositories.content_repository import ContentRepository, content_repository
from app.repositories.progress_repository import ProgressRepository, progress_repository
from app.services.badge_service import BadgeService, badge_service


class ExerciseService:
    def __init__(self, content: ContentRepository, progress: ProgressRepository, badges: BadgeService) -> None:
        self.content = content
        self.progress = progress
        self.badges = badges

    def get_exercise(self, exercise_id: str) -> dict:
        exercise = self.content.get_exercise(exercise_id)
        return exercise.model_dump(exclude={"grader_config"})

    def submit(self, exercise_id: str, code: str, anonymous_user_id: str) -> dict:
        exercise = self.content.get_exercise(exercise_id)
        output, runtime_error = self._run_python_safely(code)
        passed = False
        message = "Try again."
        if runtime_error:
            message = runtime_error
        elif exercise.grader_type == "output_match":
            expected = exercise.grader_config["expected_output"]
            passed = output.strip() == expected
            message = "Nice work. Your output matched." if passed else f"Expected output: {expected}"
        if passed:
            self.progress.complete_exercise(anonymous_user_id, exercise_id)
            self.badges.award_for_exercise(anonymous_user_id)
        return {
            "passed": passed,
            "output": output.strip(),
            "message": message,
            "progress": self.progress.get_progress(anonymous_user_id),
        }

    def _run_python_safely(self, code: str) -> tuple[str, str | None]:
        forbidden = ["import", "open(", "exec(", "eval(", "__", "input(", "subprocess", "os.", "sys."]
        if any(token in code for token in forbidden):
            return "", "This demo runner blocks imports, file access, input, and dynamic execution."
        safe_builtins = {"print": print}
        buffer = io.StringIO()
        try:
            with redirect_stdout(buffer):
                exec(code, {"__builtins__": safe_builtins}, {})
        except Exception as exc:
            return buffer.getvalue(), f"Python error: {exc}"
        return buffer.getvalue(), None


exercise_service = ExerciseService(content_repository, progress_repository, badge_service)
