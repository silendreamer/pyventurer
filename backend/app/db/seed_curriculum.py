import json
import sqlite3
from typing import Any


BEGINNER_COURSE_ID = "python-demo"
BEGINNER_COURSE_SLUG = "python-for-beginners"
INTERMEDIATE_COURSE_ID = "python-intermediate"
INTERMEDIATE_COURSE_SLUG = "python-for-intermediate-users"


MODULES = [
    {
        "title": "Welcome to Python",
        "slug": "welcome-to-python",
        "lessons": [
            "What is Python?",
            "What can you build with Python?",
            "How code runs",
            "Your first Python program",
            "Common beginner mistakes",
        ],
        "project": "Run your first Python program",
    },
    {
        "title": "Printing and Comments",
        "slug": "printing-and-comments",
        "lessons": [
            "Using print()",
            "Printing text",
            "Printing multiple values",
            "Comments with #",
            "Reading error messages",
        ],
        "project": "Personal intro card",
        "example_code": 'print("Name: Alex")\nprint("Goal: Learn Python")\nprint("Favorite app: YouTube")',
    },
    {
        "title": "Variables",
        "slug": "variables",
        "lessons": [
            "What is a variable?",
            "Naming variables",
            "Changing variable values",
            "Variables with text",
            "Variables with numbers",
        ],
        "project": "Profile generator",
        "example_code": 'name = "Alex"\nage = 12\nprint(name)\nprint(age)',
    },
    {
        "title": "Strings",
        "slug": "strings",
        "lessons": ["What is a string?", "Joining strings", "f-strings", "String methods", "String length"],
        "project": "Username creator",
        "example_code": 'first_name = "Alex"\nfavorite_color = "blue"\nusername = f"{first_name}_{favorite_color}"\nprint(username)',
    },
    {
        "title": "Numbers and Math",
        "slug": "numbers-and-math",
        "lessons": ["Integers and floats", "Basic math", "Floor division and modulo", "Type conversion", "Rounding numbers"],
        "project": "Tip calculator",
        "example_code": "bill = 40\ntip = bill * 0.18\ntotal = bill + tip\nprint(total)",
    },
    {
        "title": "Input and Output",
        "slug": "input-and-output",
        "lessons": ["Using input()", "Storing user input", "Converting input", "Building prompts", "Combining input and output"],
        "project": "Greeting app",
        "example_code": 'name = input("What is your name? ")\nprint(f"Hello, {name}!")',
    },
    {
        "title": "Decisions",
        "slug": "decisions",
        "lessons": ["Booleans", "Comparisons", "if statements", "else statements", "elif statements", "and, or, not"],
        "project": "Age checker",
        "example_code": 'age = int(input("Age: "))\n\nif age >= 13:\n    print("You can join the teen course.")\nelse:\n    print("Start with the beginner course.")',
    },
    {
        "title": "Loops",
        "slug": "loops",
        "lessons": ["Why loops matter", "for loops", "range()", "Looping through strings", "while loops", "break and continue"],
        "project": "Countdown timer",
        "example_code": 'for number in range(5, 0, -1):\n    print(number)\n\nprint("Go!")',
    },
    {
        "title": "Lists",
        "slug": "lists",
        "lessons": ["What is a list?", "Accessing list items", "Adding items", "Removing items", "Looping through lists", "List length"],
        "project": "Favorite movies list",
        "example_code": 'movies = ["Toy Story", "Frozen", "Spider-Man"]\n\nfor movie in movies:\n    print(movie)',
    },
    {
        "title": "Dictionaries",
        "slug": "dictionaries",
        "lessons": ["What is a dictionary?", "Reading values", "Adding values", "Updating values", "Looping through dictionaries"],
        "project": "Student profile app",
        "example_code": 'student = {\n    "name": "Alex",\n    "age": 12,\n    "course": "Python"\n}\n\nprint(student["name"])',
    },
    {
        "title": "Functions",
        "slug": "functions",
        "lessons": ["Why functions matter", "Defining a function", "Calling a function", "Parameters", "Return values", "Function practice"],
        "project": "Calculator functions",
        "example_code": "def add(a, b):\n    return a + b\n\nprint(add(3, 5))",
    },
    {
        "title": "Errors and Debugging",
        "slug": "errors-and-debugging",
        "lessons": ["What is an error?", "Syntax errors", "Name errors", "Type errors", "Debug with print", "Basic try/except"],
        "project": "Safe number converter",
        "example_code": 'try:\n    age = int(input("Age: "))\n    print(age)\nexcept ValueError:\n    print("Please enter a number.")',
    },
    {
        "title": "Files and Simple Data",
        "slug": "files-and-simple-data",
        "status": "locked",
        "lessons": ["What is a file?", "Reading a text file", "Writing a text file", "Appending to a file", "Intro to CSV", "Intro to JSON"],
        "project": "Simple notes app",
        "example_code": 'with open("notes.txt", "w") as file:\n    file.write("Today I learned Python!")',
    },
    {
        "title": "Imports and Useful Libraries",
        "slug": "imports-and-useful-libraries",
        "status": "locked",
        "lessons": ["What is a library?", "import random", "import math", "import datetime", "What is pip?", "When to use libraries"],
        "project": "Random password generator",
        "example_code": "import random\n\nnumber = random.randint(1, 10)\nprint(number)",
    },
    {
        "title": "Beginner Projects",
        "slug": "beginner-projects",
        "lessons": [],
        "projects": [
            "Greeting App",
            "Tip Calculator",
            "Number Guessing Game",
            "Quiz Game",
            "Simple Expense Tracker",
            "Text Adventure Game",
        ],
        "final_project": "Build one complete beginner Python app",
    },
]


EXERCISES = {
    "your-first-python-program": ("Print Hello, World!", "Write code that prints exactly: Hello, World!", 'print("Hello, World!")', "Hello, World!"),
    "using-print": ("Print Hello World", "Write Python code that prints exactly: Hello World", 'print("Hello World")', "Hello World"),
    "printing-text": ("Print Text", "Print exactly: Python is useful", 'print("Python is useful")', "Python is useful"),
    "printing-multiple-values": ("Print Multiple Values", "Print exactly: Alex Python", 'print("Alex", "Python")', "Alex Python"),
    "comments-with": ("Comment and Print", "Add a comment, then print exactly: Comments help", '# Explain the next line\nprint("Comments help")', "Comments help"),
    "what-is-a-variable": ("Greet with a Variable", 'Create a variable called greeting and set it to "Hello PyVenturer", then print it.', 'greeting = "Hello PyVenturer"\nprint(greeting)', "Hello PyVenturer"),
    "variables-with-text": ("Text Variable", 'Store "Alex" in a variable called name and print it.', 'name = "Alex"\nprint(name)', "Alex"),
    "variables-with-numbers": ("Number Variable", "Store 12 in a variable called age and print it.", "age = 12\nprint(age)", "12"),
    "what-is-a-string": ("Print a String", 'Print exactly: strings are text', 'print("strings are text")', "strings are text"),
    "basic-math": ("Add Numbers", "Print the result of 3 + 5.", "print(3 + 5)", "8"),
}


LEGACY_IDS = {
    "using-print": {"lesson_id": "lesson-print", "exercise_id": "exercise-print-hello", "quiz_id": "quiz-print-basics"},
    "what-is-a-variable": {"lesson_id": "lesson-variables", "exercise_id": "exercise-variables-greeting"},
}


def seed_curriculum(connection: sqlite3.Connection) -> None:
    with connection:
        _seed_languages(connection)
        _seed_courses(connection)
        lesson_lookup = _seed_modules_lessons_projects(connection)
        _seed_exercises(connection, lesson_lookup)
        _seed_quizzes(connection)
        _seed_completion_rules(connection)
        _seed_placement(connection)


def _upsert(connection: sqlite3.Connection, table: str, values: dict[str, Any]) -> None:
    columns = list(values)
    placeholders = ", ".join("?" for _ in columns)
    assignments = ", ".join(f"{column}=excluded.{column}" for column in columns if column != "id")
    sql = (
        f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({placeholders}) "
        f"ON CONFLICT(id) DO UPDATE SET {assignments}"
    )
    connection.execute(sql, tuple(values[column] for column in columns))


def _slugify(value: str) -> str:
    normalized = value.lower().replace("#", "").replace("()", "")
    for character in [",", ":", "!", "?", "/", "\\", "'", '"']:
        normalized = normalized.replace(character, "")
    return "-".join(normalized.split())


def _lesson_id(slug: str) -> str:
    return LEGACY_IDS.get(slug, {}).get("lesson_id", f"lesson-{slug}")


def _exercise_id(lesson_slug: str) -> str:
    return LEGACY_IDS.get(lesson_slug, {}).get("exercise_id", f"exercise-{lesson_slug}")


def _module_id(slug: str) -> str:
    return f"module-{slug}"


def _quiz_id(module_slug: str) -> str:
    if module_slug == "printing-and-comments":
        return "quiz-print-basics"
    return f"quiz-{module_slug}"


def _seed_languages(connection: sqlite3.Connection) -> None:
    _upsert(
        connection,
        "languages",
        {
            "id": "python",
            "name": "Python",
            "slug": "python",
            "description": "Learn practical Python skills from your first print statement to real projects.",
            "status": "published",
            "is_active": 1,
            "order_index": 0,
        },
    )


def _seed_courses(connection: sqlite3.Connection) -> None:
    _upsert(
        connection,
        "courses",
        {
            "id": BEGINNER_COURSE_ID,
            "language_id": "python",
            "title": "Python for Beginners",
            "slug": BEGINNER_COURSE_SLUG,
            "description": "Learn basic Python syntax and build small command-line programs.",
            "target_audience": "No coding experience",
            "difficulty": "Beginner",
            "estimated_duration": "12-16 hours",
            "course_goal": (
                "Understand basic Python syntax, write and run small programs, use variables, "
                "strings, numbers, conditionals, loops, lists, dictionaries, functions, files, "
                "imports, and build small command-line projects."
            ),
            "next_course_slug": INTERMEDIATE_COURSE_SLUG,
            "status": "published",
            "order_index": 0,
        },
    )
    _upsert(
        connection,
        "courses",
        {
            "id": INTERMEDIATE_COURSE_ID,
            "language_id": "python",
            "title": "Python for Intermediate Users",
            "slug": INTERMEDIATE_COURSE_SLUG,
            "description": "Coming soon: deeper Python, larger projects, and stronger problem solving.",
            "target_audience": "Learners who finished Python for Beginners",
            "difficulty": "Intermediate",
            "estimated_duration": "Coming soon",
            "course_goal": "Continue after beginner foundations.",
            "next_course_slug": None,
            "status": "coming_soon",
            "order_index": 1,
        },
    )
    connection.execute(
        "INSERT OR IGNORE INTO course_prerequisites (course_id, prerequisite_course_id) VALUES (?, ?)",
        (INTERMEDIATE_COURSE_ID, BEGINNER_COURSE_ID),
    )


def _seed_modules_lessons_projects(connection: sqlite3.Connection) -> dict[str, str]:
    lesson_lookup: dict[str, str] = {}
    for module_index, module in enumerate(MODULES):
        module_slug = module["slug"]
        module_id = _module_id(module_slug)
        module_status = module.get("status", "published")
        _upsert(
            connection,
            "modules",
            {
                "id": module_id,
                "course_id": BEGINNER_COURSE_ID,
                "title": module["title"],
                "slug": module_slug,
                "description": f"{module['title']} concepts for beginner Python learners.",
                "status": module_status,
                "order_index": module_index,
            },
        )
        for lesson_index, lesson_title in enumerate(module["lessons"]):
            lesson_slug = _slugify(lesson_title)
            lesson_id = _lesson_id(lesson_slug)
            lesson_lookup[lesson_slug] = lesson_id
            status = "published" if lesson_slug in EXERCISES else module_status if module_status == "locked" else "preview"
            example_code = module.get("example_code")
            _upsert(
                connection,
                "lessons",
                {
                    "id": lesson_id,
                    "module_id": module_id,
                    "course_id": BEGINNER_COURSE_ID,
                    "title": lesson_title,
                    "slug": lesson_slug,
                    "topic": lesson_title,
                    "short_description": f"Learn the beginner Python idea: {lesson_title}.",
                    "learning_objective": f"Understand and practice {lesson_title.lower()} in Python.",
                    "body": f"In this lesson, you will learn how to use {lesson_title.lower()} in a small Python program.",
                    "example_code": example_code,
                    "starter_code": "# Write your code below",
                    "estimated_minutes": 5,
                    "status": status,
                    "order_index": lesson_index,
                },
            )
        project_title = module.get("project")
        if project_title:
            _seed_project(connection, module_id, project_title, "mini", module_status, module_index)
        for project_index, project_title in enumerate(module.get("projects", [])):
            _seed_project(connection, module_id, project_title, "mini", "preview", project_index)
        final_project = module.get("final_project")
        if final_project:
            _seed_project(connection, module_id, final_project, "final", "locked", 99)
    return lesson_lookup


def _seed_project(
    connection: sqlite3.Connection,
    module_id: str,
    title: str,
    project_type: str,
    status: str,
    order_index: int,
) -> None:
    slug = _slugify(title)
    _upsert(
        connection,
        "projects",
        {
            "id": f"project-{slug}",
            "course_id": BEGINNER_COURSE_ID,
            "module_id": module_id,
            "title": title,
            "slug": slug,
            "description": f"Build a small project: {title}.",
            "project_type": project_type,
            "status": status,
            "order_index": order_index,
        },
    )


def _seed_exercises(connection: sqlite3.Connection, lesson_lookup: dict[str, str]) -> None:
    for order_index, (lesson_slug, exercise) in enumerate(EXERCISES.items()):
        title, instructions, starter_code, expected_output = exercise
        lesson_id = lesson_lookup[lesson_slug]
        _upsert(
            connection,
            "exercises",
            {
                "id": _exercise_id(lesson_slug),
                "lesson_id": lesson_id,
                "title": title,
                "slug": f"{lesson_slug}-exercise",
                "instructions": instructions,
                "starter_code": starter_code,
                "language_id": "python",
                "grader_type": "output_match",
                "grader_config": json.dumps({"expected_output": expected_output}),
                "status": "published",
                "order_index": order_index,
            },
        )


def _seed_quizzes(connection: sqlite3.Connection) -> None:
    for module_index, module in enumerate(MODULES):
        module_slug = module["slug"]
        module_id = _module_id(module_slug)
        quiz_id = _quiz_id(module_slug)
        _upsert(
            connection,
            "quizzes",
            {
                "id": quiz_id,
                "module_id": module_id,
                "lesson_id": None,
                "title": f"{module['title']} Check",
                "slug": f"{module_slug}-check",
                "passing_score": 70,
                "status": "published",
                "order_index": module_index,
            },
        )
        questions = [
            (
                "What is this module mainly about?",
                [module["title"], "Fake game commands", "Changing page themes"],
                module["title"],
                f"This module focuses on {module['title'].lower()} in real Python.",
            ),
            (
                "What should PyVenturer teach first?",
                ["Real Python skills", "move_right()", "collect_gem()"],
                "Real Python skills",
                "The core curriculum uses real Python concepts, not fake platform commands.",
            ),
            (
                "When should you move on?",
                ["After practicing the concept", "Before reading anything", "Only after changing themes"],
                "After practicing the concept",
                "Practice helps turn a concept into a skill.",
            ),
        ]
        if module_slug == "printing-and-comments":
            questions = [
                (
                    "What does print() do?",
                    ["Shows output", "Creates a file", "Starts a website"],
                    "Shows output",
                    "print() displays a value in the output.",
                ),
                (
                    "Which code prints Hello World?",
                    ['print("Hello World")', 'move_right("Hello World")', 'collect_gem("Hello World")'],
                    'print("Hello World")',
                    "This is real Python syntax for displaying text.",
                ),
                (
                    "What starts a single-line Python comment?",
                    ["#", "//", "--"],
                    "#",
                    "Python uses # for single-line comments.",
                ),
            ]
        if module_slug == "variables":
            questions = [
                (
                    "Which symbol assigns a value to a variable in Python?",
                    ["=", "==", ":"],
                    "=",
                    "A single equals sign (=) assigns a value.",
                ),
                (
                    "Which is a valid Python variable name?",
                    ["my_score", "2fast", "my-var"],
                    "my_score",
                    "Variable names cannot start with a digit or contain hyphens.",
                ),
                (
                    "What does this print?\nx = 5\nprint(x)",
                    ["5", "x", "print"],
                    "5",
                    "print(x) outputs the value stored in x.",
                ),
            ]
        for question_index, (prompt, choices, correct, explanation) in enumerate(questions):
            if quiz_id == "quiz-print-basics":
                question_id = f"q{question_index + 1}"
            elif quiz_id == "quiz-variables":
                question_id = f"v{question_index + 1}"
            else:
                question_id = f"{quiz_id}-q{question_index + 1}"
            _upsert(
                connection,
                "quiz_questions",
                {
                    "id": question_id,
                    "quiz_id": quiz_id,
                    "prompt": prompt,
                    "explanation": explanation,
                    "order_index": question_index,
                },
            )
            for choice_index, choice in enumerate(choices):
                _upsert(
                    connection,
                    "quiz_answer_choices",
                    {
                        "id": f"{question_id}-c{choice_index + 1}",
                        "question_id": question_id,
                        "choice_text": choice,
                        "is_correct": 1 if choice == correct else 0,
                        "order_index": choice_index,
                    },
                )


def _seed_completion_rules(connection: sqlite3.Connection) -> None:
    connection.execute(
        """
        INSERT INTO course_completion_rules (
            course_id,
            lesson_completion_threshold,
            average_quiz_score_threshold,
            final_assessment_score_threshold,
            required_mini_projects,
            required_final_projects,
            unlock_course_slug
        )
        VALUES (?, 80, 70, 70, 3, 1, ?)
        ON CONFLICT(course_id) DO UPDATE SET
            lesson_completion_threshold=excluded.lesson_completion_threshold,
            average_quiz_score_threshold=excluded.average_quiz_score_threshold,
            final_assessment_score_threshold=excluded.final_assessment_score_threshold,
            required_mini_projects=excluded.required_mini_projects,
            required_final_projects=excluded.required_final_projects,
            unlock_course_slug=excluded.unlock_course_slug
        """,
        (BEGINNER_COURSE_ID, INTERMEDIATE_COURSE_SLUG),
    )


def _seed_placement(connection: sqlite3.Connection) -> None:
    _upsert(
        connection,
        "placement_assessments",
        {
            "id": "placement-python-starting-point",
            "course_id": BEGINNER_COURSE_ID,
            "title": "Python Starting Point Check",
            "passing_score": 67,
            "status": "published",
        },
    )
    questions = [
        ("p1", "Have you written Python before?", ["Not yet", "A little", "Often"], "A little"),
        ("p2", 'What is the output of print("Hi")?', ["Hi", '"Hi"', "print"], "Hi"),
        ("p3", "Which is a real Python concept?", ["variables", "collect_gem", "turn_left"], "variables"),
    ]
    for order_index, (question_id, prompt, choices, correct) in enumerate(questions):
        _upsert(
            connection,
            "placement_questions",
            {
                "id": question_id,
                "assessment_id": "placement-python-starting-point",
                "prompt": prompt,
                "choices": json.dumps(choices),
                "correct_choice": correct,
                "order_index": order_index,
            },
        )
