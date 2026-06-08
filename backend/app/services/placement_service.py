from app.repositories.content_repository import ContentRepository, content_repository
from app.repositories.progress_repository import ProgressRepository, progress_repository


class PlacementService:
    def __init__(self, content: ContentRepository, progress: ProgressRepository) -> None:
        self.content = content
        self.progress = progress

    def get_assessment(self, course_id: str) -> dict:
        assessment = self.content.get_placement_for_course(course_id)
        return {
            "id": assessment.id,
            "course_id": assessment.course_id,
            "title": assessment.title,
            "passing_score": assessment.passing_score,
            "questions": [
                {"id": question.id, "prompt": question.prompt, "choices": question.choices}
                for question in assessment.questions
            ],
        }

    def grade(self, course_id: str, answers: dict[str, str], anonymous_user_id: str) -> dict:
        assessment = self.content.get_placement_for_course(course_id)
        correct = sum(1 for question in assessment.questions if answers.get(question.id) == question.correct_choice)
        score = round((correct / len(assessment.questions)) * 100)
        self.progress.record_placement(anonymous_user_id, assessment.id, score)
        if score >= assessment.passing_score:
            recommendation = "Start with the print() lesson, then continue into variables when more content is added."
        else:
            recommendation = "Start at the beginning with the print() sample lesson."
        return {
            "score": score,
            "passed": score >= assessment.passing_score,
            "recommendation": recommendation,
            "starting_lesson_id": "lesson-print",
        }


placement_service = PlacementService(content_repository, progress_repository)
