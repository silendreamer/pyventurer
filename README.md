# PyVenturer

**Learn Python. Create Anything.**

PyVenturer is a framework-first learning platform for coding and technical
skills.

The first curriculum is Python. The platform is designed so future curricula can
support Java, JavaScript, SQL, AI Agents, Data Engineering, Cloud Technologies,
and other technical subjects.

## What PyVenturer Is

PyVenturer is not just a coding game.

It is not just a static course website.

It is a learning platform framework that supports:

- learner onboarding
- course recommendations
- placement assessments
- structured lessons
- interactive coding exercises
- quizzes
- projects
- progress tracking
- XP and badges
- user-selectable themes
- future AI tutoring

## Current MVP

The MVP skeleton is implemented.

Implemented:

- FastAPI backend with thin API routes
- service and repository layers
- SQLite-backed curriculum tables and seed data for Python for Beginners
- backend-fed curriculum tree with Language -> Course -> Module -> Lesson
- full Python for Beginners outline with modules, lessons, projects, and quizzes
- early backend-graded exercises for runnable beginner lessons
- one placement check
- learner profile onboarding
- course recommendation flow
- anonymous try-before-register experience
- backend auth endpoints for register, login, logout, and current user
- frontend register/login screens for saving progress
- progress, XP, streak, and badges
- SQLite-backed learner profile, user, progress, and curriculum persistence
- user-selectable themes from backend-provided theme tokens
- React/Vite frontend with staged onboarding and interactive lesson flow
- backend tests for recommendation, placement, exercise grading, quiz grading,
  runner safety, theme defaults, auth, and persistence

Not implemented yet:

- admin/CMS content management
- production-safe sandboxed Python runner
- Monaco editor integration
- AI tutor
- projects workflow
- durable production database

## Core Product Idea

The platform should help a learner move from a simple first program:

```python
print("Hello World")
```

to building real things:

- scripts
- games
- APIs
- automation tools
- data projects
- AI agents

The goal is real-world skill development.

## Product Philosophy

PyVenturer should teach real programming.

The core curriculum should use real language concepts such as:

- printing
- variables
- strings
- numbers
- conditionals
- loops
- functions
- lists
- dictionaries
- files
- imports
- libraries
- APIs
- projects

Fake game-specific commands should not be the main curriculum.

Games can exist later as projects students build, not as the core learning
model.

## Framework First

The first development goal is not to create a full Python course. The first
development goal is to create the platform framework:

Landing Page -> Learner Profile -> Course Recommendations -> Placement Check ->
Try Sample Content -> Create Account To Save Progress -> Continue Learning

Only tiny seed content should be added at first to test the end-to-end flow.

## Show Value Before Registration

Users should not be forced to create an account immediately.

The implemented MVP flow is:

1. User lands on the site and sees why Python is useful.
2. User answers staged questions about age range, skill level, goal, learning
   style, and theme.
3. Platform recommends a course or path.
4. User takes a short placement check.
5. User sees a recommended starting point.
6. User tries a sample lesson or exercise.
7. User is asked to create an account to save progress.

Registration should come after the user understands the value.

## User-Selectable Themes

PyVenturer allows learners to choose a visual theme for the experience.

Themes may change:

- colors
- imagery
- icons
- illustration style
- page atmosphere
- tone of optional UI copy

Themes must not change:

- curriculum content
- lesson objectives
- grading rules
- placement scoring
- recommendations
- progress logic

Theme selection should be based on learner preference or motivation, not gender
or stereotypes.

Implemented theme directions:

- Explorer
- Builder
- Minimal

Future theme directions may include:

- Creator
- Competitive
- Classroom

The same lesson, exercise, quiz, or project should be renderable through
different themes without changing the underlying learning content.

## First Curriculum

The first real curriculum will be Python.

Possible future Python paths:

- Python for Absolute Beginners
- Python for Kids
- Python for Teens
- Python for Automation
- Python for Data Analysis
- Python for Games
- Python for AI Builders

Python for Beginners is seeded as a full outline with placeholder lesson bodies,
early runnable exercises, one quiz per module, mini projects, a final project,
and a transition to Python for Intermediate Users as a coming-soon course.

## Curriculum Content

SQLite schema initialization runs automatically when the backend opens the
database. The seed is idempotent and lives in:

```text
backend/app/db/seed_curriculum.py
```

To initialize or refresh seed content manually:

```powershell
python -c "from app.db.connection import get_connection; get_connection()" 
```

from the `backend` directory.

To add content:

- Add a course row in `seed_curriculum.py` and give it a stable slug.
- Add modules to the `MODULES` list with `slug`, `title`, lessons, and projects.
- Add a lesson by adding its title to a module; the seed creates slug, objective,
  placeholder body, status, and ordering.
- Add an exercise by adding an entry to `EXERCISES` keyed by lesson slug.
- Add or customize module quiz questions in `_seed_quizzes`.

The frontend renders the API-provided outline and should not hardcode course
structure.

## Future Curricula

The architecture should eventually support:

- Java
- JavaScript
- SQL
- AI Agents
- Data Engineering
- Cloud Technologies
- Cloud Automation
- Other technical subjects

The platform should not need a rewrite to support these.

## Main Platform Concepts

Core entities:

Language Course Module Topic Lesson Exercise Quiz Project Placement Assessment
User Learner Profile Theme Progress Badge Recommendation Technical Direction

## Preferred Stack

Current MVP stack:

Frontend:

React TypeScript Vite custom CSS

Backend:

FastAPI Python SQLite Repository and service pattern

Deployment:

Vercel can build the Vite frontend and serve the FastAPI backend from the root
`api/index.py` function. Set `PYVENTURER_SECRET_KEY` in Vercel before using auth
outside local demos. The Vercel SQLite path defaults to `/tmp/pyventurer.db`,
which is useful for demo deployments but not durable production persistence.

Future stack direction:

- PostgreSQL
- SQLModel or SQLAlchemy-compatible persistence
- CMS/admin content management
- Monaco editor
- production-safe runner isolation

## Development Principle

Build the framework first.

Add real curriculum later.
