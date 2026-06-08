# PyVenturer Architecture

## Purpose

PyVenturer is a framework-first learning platform.

The first curriculum is Python. The architecture should support future curricula
such as Java, JavaScript, SQL, AI Agents, Data Engineering, Cloud Technologies,
and other technical subjects.

The platform should not be hardcoded around a single course, a single
programming language, or a game engine.

## Current MVP Status

The MVP skeleton is implemented with a React frontend and FastAPI backend.

Implemented now:

- staged learner onboarding
- Python value intro on landing
- course recommendation flow
- placement assessment
- one sample lesson
- one interactive coding exercise
- one quiz
- progress tracking
- XP, streak, and badges
- user-selectable themes
- backend auth endpoints for register, login, logout, and current user
- frontend register/login screens after value is shown
- backend-owned recommendation, placement, quiz, exercise, progress, and badge
  logic
- SQLite-backed profile, progress, and user repositories
- in-memory seed content and theme repositories
- backend tests for important business rules

Not implemented yet:

- migrations
- full Python curriculum
- projects workflow
- real CMS/admin tooling
- AI tutor
- Monaco editor
- production runner isolation
- deployment

## High-Level User Journey

```text
Anonymous Visitor
  -> Landing Page with Python value message
  -> Staged Profile Questions
     -> age range
     -> skill level
     -> learning goal
     -> preferred learning style
     -> selected theme
  -> Recommended Course
  -> Placement Assessment
  -> Recommended Starting Point
  -> Try Sample Lesson / Exercise
  -> Try Quiz
  -> Create Account To Save Progress
```

The key principle is: show value before registration.

## Current System Shape

```text
Frontend
  React + TypeScript + Vite + custom CSS
  Renders API-provided content and theme tokens

API Layer
  FastAPI routes
  Thin wrappers around services

Service Layer
  Content Service
  Recommendation Service
  Placement Service
  Exercise Service
  Quiz Service
  Progress Service
  Badge Service
  Theme Service
  Account Service placeholder

Repository Layer
  In-memory content repository
  SQLite-backed progress/profile repository
  SQLite-backed user repository
  In-memory theme repository

Current Data Storage
  SQLite for MVP persistence

Future Data Storage
  PostgreSQL or another production persistent database
  CMS/admin content management
```

## Core Architecture Principle

The platform should be content-driven.

This means:

- courses come from data
- lessons come from data
- quizzes come from data
- exercises come from data
- projects come from data
- recommendations are rule-driven or data-driven
- frontend components render data, not hardcoded curriculum

The current MVP uses tiny in-memory seed content to prove the full flow.
Profile, progress, badges, and users are persisted in SQLite. Future development
should move learning content into persistent storage or CMS-managed records.

## Current Backend Structure

```text
backend/
  app/
    main.py
    api/routes/
      onboarding.py
      courses.py
      placement.py
      exercises.py
      quizzes.py
      progress.py
      themes.py
    models/
      domain.py
      schemas.py
    repositories/
      content_repository.py
      progress_repository.py
      theme_repository.py
      user_repository.py
    services/
      auth_service.py
      account_service.py
      badge_service.py
      content_service.py
      exercise_service.py
      placement_service.py
      progress_service.py
      quiz_service.py
      recommendation_service.py
      theme_service.py
  tests/
    test_engines.py
    test_auth.py
    test_persistence.py
```

## Current Frontend Structure

```text
frontend/
  src/
    App.tsx
    api.ts
    main.tsx
    styles.css
    types.ts
    vite-env.d.ts
```

The current frontend is a single-page MVP shell. It intentionally keeps the
journey visible in one app while the backend owns grading, scoring,
recommendations, progress, and badges.

## Main Domain Model

### Language

Represents a curriculum language or subject area.

Examples:

- Python
- Java
- JavaScript
- SQL
- AI Agents

### Course

A learning path within a language or subject.

Current seed:

- Python for Beginners

Future examples:

- Python for Beginners
- Python for Automation
- Python for Data Analysis
- Python for AI Builders

### Lesson

Instructional content for a topic.

Current seed:

- What is `print()`?

### Exercise

An interactive coding challenge.

Current seed:

- Print Hello World

Supported initial grader types:

- `output_match`
- `code_contains`
- `code_not_contains`
- `unit_test`
- `manual_project_rubric`

Only `output_match` is implemented in the current seed exercise.

### Quiz

A knowledge check.

Quiz questions and correct answers must be stored server-side. The frontend
receives questions and choices, but not correct answers before submission.

### Placement Assessment

Used to determine the learner's starting level.

The current seed placement grades three questions and recommends a starting
lesson.

### Learner Profile

Stores information used to personalize recommendations.

Current fields include:

- age range
- experience level
- learning goal
- preferred style
- motivation type
- selected theme

Personalization must not rely on gender stereotypes.

### Theme

Represents a user-selectable presentation style.

Current themes:

- Explorer
- Builder
- Minimal

Themes may define:

- color tokens
- image tokens
- icon style
- illustration style
- layout density
- tone

Themes must not define or change:

- course content
- lesson content
- exercise instructions
- quiz answers
- grading rules
- placement scoring
- recommendation rules
- progress logic
- unlock rules

### Progress

Tracks learner activity.

Current MVP progress includes:

- XP
- streak
- completed lessons
- completed exercises
- completed quizzes
- placement scores
- badges

### Badge

Represents achievements.

Current seed badges include:

- First Code Run
- Python Starter
- Perfect Quiz

## Core Engines

### Content Engine

Retrieves and organizes learning content.

The current implementation uses `ContentService` and `ContentRepository`.

### Recommendation Engine

Recommends courses and next steps based on learner profile fields.

The current implementation recommends Python for Beginners.

### Placement Engine

Grades placement answers in the backend and returns a starting recommendation.

### Exercise Engine

Loads an exercise, runs submitted code through a limited demo runner, grades the
result, updates progress, and awards XP/badges.

The current runner blocks imports, file access, input, dynamic execution, and
some dangerous tokens. This is only a demo safety layer, not a production
sandbox.

### Quiz Engine

Delivers questions without answers, grades submissions in the backend, returns
score/explanations, and updates progress.

### Progress Engine

Tracks completed learning actions, XP, streak, placement scores, and badges.

### Badge Engine

Awards rule-based achievements.

### Theme Engine

Resolves the learner's selected presentation theme and provides theme tokens to
the frontend.

Theme choice is presentation only. It must stay separate from content,
recommendation, placement, grading, progress, and badges.

### Account/Auth System

Backend auth is implemented with registration, login, logout, current-user
lookup, password hashing, signed JWT session tokens, and progress merge support.

The frontend still needs full register/login screens. It currently shows a
placeholder save-progress prompt after the learner has tried the sample content.

### Tutor Engine

Future AI-powered support. It is not implemented in the MVP skeleton.

## Frontend Pages And Flow

The current MVP is a single-page flow with these states:

- Start
- Recommendations
- Placement
- Lesson
- Quiz
- Save

Current UI behavior:

- XP, streak, and badge count live in the top bar.
- Landing includes a compact Python value intro.
- Onboarding asks one question at a time.
- A curriculum sidebar shows Language -> Course -> Module -> Lesson structure
  from backend seed data.
- Completed and available implemented lessons can be opened; future lessons are
  shown locked until content and unlock rules exist.
- Learning pages use a compact context strip instead of a large hero.
- Theme can be selected without changing curriculum or grading.

## Minimal Seed Content

Current seed content:

```text
Language: Python
Course: Python for Beginners
Module: Python Basics
Lesson: What is print()?
Exercise: Print Hello World
Quiz: print() Basics Check
Placement: Python Starting Point Check
Themes: Explorer, Builder, Minimal
```

This is not the real course. It only proves the framework works end to end.

## Long-Term Vision

```text
Learning Platform Framework
  -> Python Curriculum
  -> Real Projects
  -> AI Agents
  -> More Curricula
```

The architecture should make this possible without a major rewrite.
