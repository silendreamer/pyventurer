# PyVenturer Agent Instructions

Tagline: Learn Python. Create Anything.

## Product Direction

PyVenturer is a framework-first learning platform.

The first curriculum will be Python, but the platform must not be hardcoded only
for Python.

Long-term, PyVenturer should be able to support:

- Python
- Java
- JavaScript
- SQL
- AI Agents
- Data Engineering
- Cloud Technologies
- Other technical subjects

The platform should teach real-world skills through structured learning paths,
interactive exercises, quizzes, projects, recommendations, placement checks,
progress tracking, XP, and badges.

## Core Product Philosophy

Teach real skills, not fake game commands.

Good examples:

- `print()`
- variables
- strings
- loops
- functions
- lists
- dictionaries
- files
- imports
- libraries
- APIs
- projects
- games built with real Python
- AI agents

Avoid making fake platform-specific commands the core learning mechanism.

Bad examples as core curriculum:

- `move_right()`
- `collect_gem()`
- `turn_left()`

Those may be used later inside an optional game-building project, but they must
not be the foundation of the learning platform.

## Build the Framework First

The priority is to build the learning platform framework before creating large
courses.

The framework should support:

- landing page
- learner profile
- course catalog
- course recommendations
- placement assessments
- lessons
- exercises
- quizzes
- projects
- progress tracking
- badges
- theme selection
- account creation
- saved progress

Use tiny demo seed content only to prove that the platform works end-to-end.

Do not build a full Python course yet.

## Show Value Before Registration

Do not force users to create an account before seeing value.

Preferred user journey:

```text
Landing Page
→ Quick Goal/Profile Questions
→ Recommended Courses
→ Placement Check
→ Try Sample Lesson or Exercise
→ Ask User To Create Account To Save Progress
```

Account creation should feel useful, not forced.

Content-Driven Architecture

All learning content must come from data.

Do not hardcode courses, modules, topics, lessons, exercises, quizzes, projects,
or recommendations into React components.

Content should eventually be stored in a database and managed through an
admin/CMS workflow.

For early development, minimal seed data is acceptable.

Repository and Service Pattern

Use clear boundaries.

Routes should be thin.

Business logic belongs in services.

Data access belongs in repositories.

Frontend should not know where content comes from.

Backend should expose stable API contracts.

Preferred backend layering:

API Routes → Services → Repositories → Database Backend Is Source of Truth

Frontend renders the experience.

Backend owns:

grading quiz scoring placement scoring recommendations unlock rules progress
tracking badge awarding

Never trust frontend for final grading, progress, or unlock decisions.

Main Systems

Keep these systems separate:

Content Engine Recommendation Engine Placement Engine Exercise Engine Quiz
Engine Project Engine Progress Engine Badge Engine Account/Auth System Tutor
Engine Theme Engine

Avoid tightly coupling these systems.

Personalization

Personalization should be based on:

age range experience level learning goal motivation preferred style placement
result progress

Do not personalize based on stereotypes.

Do not assume boys want games and girls want fashion.

Themes should be based on learner motivation, not gender.

Possible theme styles later:

Explorer Builder Creator Minimal Competitive Classroom

The same curriculum should be presentable through different themes.

Themes may change page colors, imagery, icons, illustration style, layout
atmosphere, and optional UI tone.

Themes must not change curriculum content, placement scoring, grading,
recommendations, progress rules, unlock rules, or badge criteria.

Theme choice should be treated as a user preference and stored in the learner
profile or anonymous session.

Multi-Curriculum Future

Design the platform so future curricula can be added mostly through database
content and curriculum- specific runner/grader implementations.

Implement Python first.

Do not overbuild Java, JavaScript, or SQL now.

But keep these concepts clean:

language course module topic lesson exercise quiz project runner grader Runner
and Grader

Exercises should support multiple grading strategies.

Initial grader types:

output match code contains code does not contain simple unit test manual project
rubric placeholder

For Python execution:

treat user code as untrusted never use unrestricted exec() use timeouts restrict
dangerous operations document limitations clearly

Future languages may require separate runners.

Examples:

PythonRunner JavaRunner JavaScriptRunner SqlRunner

Only PythonRunner should be implemented initially.

UI Direction

The UI should feel modern, clean, and motivating.

It should not look like a pure game.

It should feel closer to:

structured learning platform interactive coding environment light gamification
adaptive course guide

Avoid building the entire product around a grid world or character movement.

Gamification

Use light gamification:

XP badges progress bars ranks streak placeholder completion celebrations

Gamification should motivate learning.

It should not replace real learning.

Testing

Add tests for important business logic.

Critical areas:

placement scoring recommendation rules exercise grading quiz scoring progress
updates badge awarding runner safety What Not To Do

Do not:

build a CodeMonkey-style game as the core platform hardcode curriculum into
frontend components hardcode course recommendations expose correct quiz answers
before submission put business logic in React put business logic directly in API
routes couple curriculum to one programming language require registration before
showing value create large course content before the framework works personalize
using gender stereotypes
