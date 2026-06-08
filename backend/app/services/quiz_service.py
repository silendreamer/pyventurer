from app.repositories.content_repository import ContentRepository, content_repository
from app.repositories.progress_repository import ProgressRepository, progress_repository
from app.services.badge_service import BadgeService, badge_service


class QuizService:
    def __init__(self, content: ContentRepository, progress: ProgressRepository, badges: BadgeService) -> None:
        self.content = content
        self.progress = progress
        self.badges = badges

    def get_quiz(self, quiz_id: str) -> dict:
        quiz = self.content.get_quiz(quiz_id)
        return {
            "id": quiz.id,
            "lesson_id": quiz.lesson_id,
            "title": quiz.title,
            "passing_score": quiz.passing_score,
            "questions": [
                {"id": question.id, "prompt": question.prompt, "choices": question.choices}
                for question in quiz.questions
            ],
        }

    def submit(self, quiz_id: str, answers: dict[str, str], anonymous_user_id: str) -> dict:
        quiz = self.content.get_quiz(quiz_id)
        correct = sum(1 for question in quiz.questions if answers.get(question.id) == question.correct_choice)
        score = round((correct / len(quiz.questions)) * 100)
        explanations = [
            {
                "question_id": question.id,
                "correct": answers.get(question.id) == question.correct_choice,
                "explanation": question.explanation,
            }
            for question in quiz.questions
        ]
        if score >= quiz.passing_score:
            self.progress.complete_quiz(anonymous_user_id, quiz_id)
            self.badges.award_for_quiz(anonymous_user_id, score)
        return {
            "score": score,
            "passed": score >= quiz.passing_score,
            "explanations": explanations,
            "progress": self.progress.get_progress(anonymous_user_id),
        }


quiz_service = QuizService(content_repository, progress_repository, badge_service)
