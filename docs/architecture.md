# PyVenturer Architecture

## Purpose

PyVenturer is a framework-first learning platform.

The first curriculum is Python. The architecture should support future curricula
such as Java, JavaScript, SQL, AI Agents, Data Engineering, Cloud Technologies,
and other technical subjects.

The platform should not be hardcoded around a single course, a single
programming language, or a game engine.

## Product Direction

PyVenturer should feel like a structured learning platform with light
gamification.

The platform should teach real skills through:

- lessons
- exercises
- quizzes
- projects
- placement tests
- recommendations
- progress tracking
- badges
- future AI tutoring

The product should not be centered around fake game commands like `move_right()`
or `collect_gem()`.

Games may exist later as real projects that students build using actual
programming concepts.

---

## High-Level User Journey

```text
Anonymous Visitor
    ↓
Landing Page
    ↓
Quick Goal / Profile Questions
    ↓
Recommended Courses
    ↓
Placement Assessment
    ↓
Recommended Starting Point
    ↓
Try Sample Lesson / Exercise
  ↓
Create Account To Save Progress
  ↓
Continue Learning

```

The key principle is:

Show value before registration.

High-Level System Diagram

```text
┌───────────────────────────────────────┐
│               Frontend                │
│ React + TypeScript + Tailwind          │
└───────────────────┬───────────────────┘
          │
          ▼
┌───────────────────────────────────────┐
│                API Layer              │
│ FastAPI Routes                         │
└───────────────────┬───────────────────┘
          │
          ▼
┌───────────────────────────────────────┐
│              Service Layer            │
├───────────────────────────────────────┤
│ Content Service                        │
│ Recommendation Service                 │
│ Placement Service                      │
│ Exercise Service                       │
│ Quiz Service                           │
│ Project Service                        │
│ Progress Service                       │
│ Badge Service                          │
│ Auth / Account Service                 │
│ Tutor Service                          │
└───────────────────┬───────────────────┘
          │
          ▼
┌───────────────────────────────────────┐
│            Repository Layer           │
├───────────────────────────────────────┤
│ Course Repository                      │
│ Content Repository                     │
│ User Repository                        │
│ Progress Repository                    │
│ Assessment Repository                  │
│ Badge Repository                       │
└───────────────────┬───────────────────┘
          │
          ▼
┌───────────────────────────────────────┐
│              Data Storage             │
├───────────────────────────────────────┤
│ SQLite for MVP                         │
│ PostgreSQL later                       │
│ CMS later                              │
└───────────────────────────────────────┘
```

Core Architecture Principle

The platform should be content-driven.

This means:

courses come from data lessons come from data quizzes come from data exercises
come from data projects come from data recommendations are rule-driven or data-
driven frontend components render data, not hardcoded curriculum Main Domain
Model Language

Represents a curriculum language or subject area.

Examples:

Python Java JavaScript SQL AI Agents

Fields may include:

id name slug description is_active Course

A learning path within a language or subject.

Examples:

Python for Beginners Python for Automation Python for Data Analysis Python for
AI Builders

Fields may include:

id language_id title slug description target_audience difficulty
estimated_duration is_active Module

A major section inside a course.

Example:

Course: Python for Beginners Module: Variables and Data

Fields may include:

id course_id title description order_index unlock_rule Topic

A focused learning concept inside a module.

Examples:

print() variables strings for loops functions

Fields may include:

id module_id title description order_index Lesson

Instructional content for a topic.

Fields may include:

id topic_id title body code_examples estimated_minutes order_index Exercise

An interactive coding challenge.

Fields may include:

id lesson_id title instructions starter_code language_id grader_type
grader_config solution_reference order_index

Supported grader types:

output_match code_contains code_not_contains unit_test manual_project_rubric
Quiz

A knowledge check.

Fields may include:

id lesson_id title passing_score order_index

Quiz questions and correct answers must be stored server-side.

Frontend should not receive correct answers before submission.

Project

A larger applied assignment.

Examples:

greeting app number guessing game calculator quiz game expense tracker chatbot
AI agent

Fields may include:

id course_id module_id title description instructions rubric difficulty
order_index Placement Assessment

Used to determine the learner's starting level.

Fields may include:

id course_id title passing_score recommendation_rules

A placement result may recommend:

start selected course start easier course skip first module review prerequisite
topics Learner Profile

Stores information used to personalize recommendations.

Fields may include:

id user_id age_range experience_level learning_goal preferred_style
motivation_type selected_theme_id

Personalization must not rely on gender stereotypes.

Theme

Represents a user-selectable presentation style for the platform.

Themes may define:

id name slug description color_tokens image_tokens icon_style illustration_style
layout_density tone is_active

Theme tokens may control:

primary color secondary color accent color background color surface color hero
image lesson image badge image icon set illustration style

Themes must not define or change:

course content lesson content exercise instructions quiz answers grading rules
placement scoring recommendation rules progress logic unlock rules

Themes are selected by the learner or inferred from explicit preference and
motivation. They must never be selected from gender stereotypes.

Progress

Tracks learner activity.

Fields may include:

user_id course_id lesson_id exercise_id quiz_id project_id status score
completed_at attempts Badge

Represents achievements.

Examples:

First Lesson Complete First Exercise Solved Perfect Quiz Python Starter Project
Builder

Fields may include:

id title description criteria icon Core Engines

1. Content Engine

Responsible for retrieving and organizing:

languages courses modules topics lessons exercises quizzes projects

The Content Engine should not care whether data comes from JSON, SQLite,
PostgreSQL, or CMS.

1. Recommendation Engine

Responsible for recommending courses and next steps.

Inputs may include:

learner profile age range experience level learning goal placement result
progress course prerequisites

Outputs may include:

recommended course recommended starting module prerequisite recommendation next
best lesson

1. Placement Engine

Responsible for evaluating whether a selected course is appropriate.

Flow:

User selects course ↓ Platform gives short placement assessment ↓ Backend grades
assessment ↓ Platform recommends starting point

Example result:

You selected Python for Data Analysis, but your placement score suggests
starting with Python for Beginners first.

1. Exercise Engine

Responsible for interactive coding exercises.

Responsibilities:

load exercise provide starter code run submitted code grade answer return result
update progress award XP if appropriate

Frontend should display the editor and result.

Backend should run and grade.

1. Quiz Engine

Responsible for quiz delivery and grading.

Rules:

frontend receives questions and answer choices frontend does not receive correct
answers before submission backend grades quiz backend returns score,
explanations, and progress updates

1. Project Engine

Responsible for larger assignments.

Projects may be automatically graded, manually reviewed, or rubric-based.

Initial implementation can use rubric placeholders.

1. Progress Engine

Responsible for tracking:

completed lessons completed exercises quiz scores placement scores projects XP
badges course progress

1. Badge Engine

Responsible for awarding achievements.

Badges should be rule-based.

Examples:

If learner completes first exercise, award "First Code Run". If learner scores
100% on a quiz, award "Perfect Quiz".

1. Tutor Engine

Future AI-powered support.

Initial implementation may be static hints.

Future implementation may provide:

hints error explanations recommended next steps encouragement concept review

Tutor should not immediately give full solutions.

1. Theme Engine

Responsible for resolving the learner's selected presentation theme.

Responsibilities:

load available themes validate selected theme resolve color/image/icon tokens
provide theme data to the frontend persist learner theme preference

The Theme Engine is a presentation system. It must stay separate from the
Content Engine, Recommendation Engine, Placement Engine, Exercise Engine, Quiz
Engine, Progress Engine, and Badge Engine.

The same course, lesson, exercise, quiz, or project should render correctly
under multiple themes without changing learning content or backend outcomes.

Frontend Architecture

Suggested pages:

/ Landing Page

/onboarding Quick learner profile and goals

/recommendations Recommended courses

/courses Course catalog

/courses/:courseSlug Course overview

/courses/:courseSlug/placement Placement assessment

/learn/:courseSlug Course learning dashboard

/lessons/:lessonId Lesson page

/exercises/:exerciseId Interactive exercise page

/quizzes/:quizId Quiz page

/projects/:projectId Project page

/progress Progress dashboard

/account Account creation / login

Suggested components:

LandingHero GoalSelector LearnerProfileForm CourseCard RecommendationCard
PlacementAssessment LessonViewer CodeEditor ExerciseRunner QuizQuestion
ProjectBrief ProgressBar BadgeList ThemeSelector AccountPrompt Backend
Architecture

Suggested structure:

backend/ app/ main.py api/ routes/ onboarding.py courses.py placement.py
lessons.py exercises.py quizzes.py projects.py progress.py themes.py auth.py services/
content_service.py recommendation_service.py placement_service.py
exercise_service.py quiz_service.py project_service.py progress_service.py
badge_service.py theme_service.py tutor_service.py repositories/ course_repository.py
content_repository.py user_repository.py progress_repository.py
assessment_repository.py theme_repository.py models/ database.py schemas.py domain.py runners/
base_runner.py python_runner.py future_java_runner.py
future_javascript_runner.py future_sql_runner.py graders/ base_grader.py
output_match_grader.py code_contains_grader.py unit_test_grader.py db/
session.py migrations/ tests/ Database-First Direction

The product should be designed around database-backed content.

However, early development may use tiny seed data.

The important rule:

No frontend component should care where content comes from.

Eventually, content should be manageable through an admin interface or CMS.

Minimal Seed Content

Although the platform is framework-first, it should not be completely empty.

Use tiny demo content to test the flow.

Example:

Language: Python Course: Python Demo Path Module: Demo Module Topic: print()
Lesson: What is print()? Exercise: Print Hello Quiz: 2 questions Placement: 3
questions

This is not the real course.

It only proves the system works.

Account Flow

The platform should allow anonymous exploration first.

Anonymous user can:

answer profile questions see recommendations take placement try a sample lesson
or exercise

Then prompt:

Create an account to save your progress.

Account creation should come after value is shown.

Gamification Layer

Gamification should be separate from curriculum.

Supported features:

XP badges progress bars ranks streak placeholder

Gamification should encourage learning, not replace learning.

Themes

Themes are presentation layers.

They should not change the underlying curriculum.

Learners should be able to choose a theme that changes the look and feel of the
page, including colors, images, icons, illustration style, and optional tone.
Theme choice should be stored as part of the learner profile or anonymous
session and applied consistently across landing, onboarding, recommendations,
lessons, exercises, quizzes, projects, and progress views.

Examples:

Explorer Theme Builder Theme Creator Theme Minimal Theme Competitive Theme

The same lesson can be rendered with different tone and visuals.

Do not base themes on gender stereotypes.

Long-Term Vision

The long-term vision is:

Learning Platform Framework ↓ Python Curriculum ↓ Real Projects ↓ AI Agents ↓
More Curricula

The architecture should make this possible without a major rewrite.
