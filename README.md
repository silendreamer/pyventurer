# PyVenturer

**Learn Python. Create Anything.**

PyVenturer is a framework-first learning platform for coding and technical
skills.

The first curriculum will be Python. The platform is designed so future
curricula can support Java, JavaScript, SQL, AI Agents, Data Engineering, Cloud
Technologies, and other technical subjects.

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

## Core Product Idea

The platform should help a learner move from a simple first program to building
real things:

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

Framework First

The first development goal is not to create a full Python course.

The first development goal is to create the platform framework:

Landing Page → Learner Profile → Course Recommendations → Placement Check → Try
Sample Content → Create Account To Save Progress → Continue Learning

Only tiny seed content should be added at first to test the end-to-end flow.

## Show Value Before Registration

Users should not be forced to create an account immediately.

The preferred flow is:

User lands on the site. User answers a few quick questions. Platform recommends
a course or path. User takes a short placement check. User sees a recommended
starting point. User tries a sample lesson or exercise. User is asked to create
an account to save progress.

Registration should come after the user understands the value.

## User-Selectable Themes

PyVenturer should allow learners to choose a visual theme for the experience.

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

Example theme directions:

- Explorer
- Builder
- Creator
- Minimal
- Competitive
- Classroom

The same lesson, exercise, quiz, or project should be renderable through
different themes without changing the underlying learning content.

## First Curriculum

The first real curriculum will be:

Python

Possible future Python paths:

Python for Absolute Beginners Python for Kids Python for Teens Python for
Automation Python for Data Analysis Python for Games Python for AI Builders

## Future Curricula

The architecture should eventually support:

Java JavaScript SQL AI Agents Data Engineering Cloud Technologies Cloud
Automation Other technical subjects

The platform should not need a rewrite to support these.

## Main Platform Concepts

Core entities:

Language Course Module Topic Lesson Exercise Quiz Project Placement Assessment
User Learner Profile Theme Progress Badge Recommendation Technical Direction

## Preferred Stack

Preferred stack:

Frontend:

React TypeScript Vite TailwindCSS Monaco Editor

Backend:

FastAPI Python SQLite for early MVP PostgreSQL later SQLModel or SQLAlchemy-
compatible structure Repository and service pattern

## Current Status

Planning and framework design.

The next step is to build the platform skeleton with:

database tables APIs basic UI flow tiny seed/demo content placement flow
recommendation flow anonymous try-before-register experience account creation
for saved progress Development Principle

## Development Principle

Build the framework first.

Add real curriculum later.
