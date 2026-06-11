from typing import Literal

from pydantic import BaseModel


class Language(BaseModel):
    id: str
    name: str
    slug: str
    description: str
    is_active: bool = True


class Course(BaseModel):
    id: str
    language_id: str
    title: str
    slug: str
    description: str
    target_audience: str
    difficulty: str
    estimated_duration: str
    outcomes: list[str]
    status: str = "published"
    course_goal: str = ""
    next_course_slug: str | None = None
    is_active: bool = True


class Lesson(BaseModel):
    id: str
    course_id: str
    topic: str
    title: str
    body: str
    code_examples: list[str]
    estimated_minutes: int
    slug: str = ""
    short_description: str = ""
    learning_objective: str = ""
    status: str = "preview"
    order_index: int = 0


class Exercise(BaseModel):
    id: str
    lesson_id: str
    title: str
    instructions: str
    starter_code: str
    language_id: str
    grader_type: Literal["output_match", "code_contains", "code_not_contains", "unit_test"]
    grader_config: dict[str, str]
    slug: str = ""
    status: str = "preview"
    order_index: int = 0


class QuizQuestion(BaseModel):
    id: str
    prompt: str
    choices: list[str]


class QuizQuestionWithAnswer(QuizQuestion):
    correct_choice: str
    explanation: str


class Quiz(BaseModel):
    id: str
    lesson_id: str
    title: str
    passing_score: int
    questions: list[QuizQuestionWithAnswer]
    slug: str = ""
    module_id: str | None = None
    status: str = "published"


class PlacementQuestion(BaseModel):
    id: str
    prompt: str
    choices: list[str]
    correct_choice: str


class PlacementAssessment(BaseModel):
    id: str
    course_id: str
    title: str
    passing_score: int
    questions: list[PlacementQuestion]


class LearnerProfile(BaseModel):
    age_range: str
    experience_level: str
    learning_goal: str
    motivation_type: str
    preferred_style: str
    selected_theme_id: str


class Recommendation(BaseModel):
    course: Course
    starting_lesson_id: str
    starting_exercise_id: str
    reason: str
    next_steps: list[str]


class Badge(BaseModel):
    id: str
    title: str
    description: str
    icon: str


class ProgressState(BaseModel):
    anonymous_user_id: str
    xp: int
    streak: int
    completed_lessons: list[str]
    completed_exercises: list[str]
    completed_quizzes: list[str]
    placement_scores: dict[str, int]
    badges: list[Badge]


class ThemeTokens(BaseModel):
    primary: str
    secondary: str
    accent: str
    background: str
    surface: str
    text: str
    muted: str
    code_background: str
    hero_image: str
    lesson_image: str


class Theme(BaseModel):
    id: str
    name: str
    slug: str
    description: str
    icon_style: str
    illustration_style: str
    layout_density: str
    tone: str
    tokens: ThemeTokens
    is_active: bool = True
