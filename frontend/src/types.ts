export type Theme = {
  id: string;
  name: string;
  slug: string;
  description: string;
  tone: string;
  tokens: {
    primary: string;
    secondary: string;
    accent: string;
    background: string;
    surface: string;
    text: string;
    muted: string;
    code_background: string;
    hero_image: string;
    lesson_image: string;
  };
};

export type LearnerProfile = {
  age_range: string;
  experience_level: string;
  learning_goal: string;
  motivation_type: string;
  preferred_style: string;
  selected_theme_id: string;
};

export type Course = {
  id: string;
  title: string;
  slug: string;
  description: string;
  difficulty: string;
  estimated_duration: string;
  outcomes: string[];
  status: string;
  next_course_slug?: string | null;
};

export type CurriculumLesson = {
  id: string;
  title: string;
  slug: string;
  topic: string;
  description: string;
  status: string;
  order_index: number;
  implemented: boolean;
};

export type CurriculumProject = {
  id: string;
  title: string;
  slug: string;
  description: string;
  type: string;
  status: string;
  order_index: number;
};

export type CurriculumQuizSummary = {
  id: string;
  title: string;
  slug: string;
  status: string;
};

export type CurriculumModule = {
  id: string;
  title: string;
  slug: string;
  description: string;
  status: string;
  order_index: number;
  lessons: CurriculumLesson[];
  projects: CurriculumProject[];
  quiz?: CurriculumQuizSummary | null;
};

export type CurriculumCourse = {
  id: string;
  title: string;
  slug: string;
  description: string;
  status: string;
  next_course_slug?: string | null;
  modules: CurriculumModule[];
};

export type CurriculumLanguage = {
  id: string;
  title: string;
  description: string;
  courses: CurriculumCourse[];
};

export type Recommendation = {
  course: Course;
  starting_lesson_id: string;
  starting_exercise_id: string;
  reason: string;
  next_steps: string[];
};

export type Lesson = {
  id: string;
  title: string;
  topic: string;
  body: string;
  code_examples: string[];
  estimated_minutes: number;
};

export type Exercise = {
  id: string;
  title: string;
  instructions: string;
  starter_code: string;
};

export type Question = {
  id: string;
  prompt: string;
  choices: string[];
};

export type Quiz = {
  id: string;
  title: string;
  passing_score: number;
  questions: Question[];
};

export type Progress = {
  anonymous_user_id: string;
  xp: number;
  streak: number;
  completed_lessons: string[];
  completed_exercises: string[];
  completed_quizzes: string[];
  placement_scores: Record<string, number>;
  badges: { id: string; title: string; description: string; icon: string }[];
};
