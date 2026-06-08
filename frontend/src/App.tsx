import {
  Award,
  BookOpen,
  CheckCircle2,
  ChevronRight,
  Code2,
  Flame,
  GraduationCap,
  Lightbulb,
  Palette,
  Play,
  Save,
  Sparkles,
  Target,
} from "lucide-react";
import { useEffect, useMemo, useState } from "react";
import type { CSSProperties, ReactNode } from "react";
import { api } from "./api";
import type { Exercise, LearnerProfile, Lesson, Progress, Question, Quiz, Recommendation, Theme } from "./types";

const anonymousUserId = "demo-user";

const defaultTheme: Theme = {
  id: "explorer",
  name: "Explorer",
  slug: "explorer",
  description: "Open, bright, and discovery-focused.",
  tone: "curious",
  tokens: {
    primary: "#0f766e",
    secondary: "#2563eb",
    accent: "#f59e0b",
    background: "#f7fbf9",
    surface: "#ffffff",
    text: "#10201f",
    muted: "#60706d",
    code_background: "#101827",
    hero_image: "linear-gradient(135deg, #dff7ef 0%, #dbeafe 60%, #fff7ed 100%)",
    lesson_image: "linear-gradient(135deg, #ccfbf1, #bfdbfe)",
  },
};

const emptyProgress: Progress = {
  anonymous_user_id: anonymousUserId,
  xp: 0,
  streak: 0,
  completed_lessons: [],
  completed_exercises: [],
  completed_quizzes: [],
  placement_scores: {},
  badges: [],
};

type Placement = {
  id: string;
  course_id: string;
  title: string;
  passing_score: number;
  questions: Question[];
};

function App() {
  const [themes, setThemes] = useState<Theme[]>([]);
  const [theme, setTheme] = useState<Theme>(defaultTheme);
  const [step, setStep] = useState("start");
  const [recommendations, setRecommendations] = useState<Recommendation[]>([]);
  const [lesson, setLesson] = useState<Lesson | null>(null);
  const [exercise, setExercise] = useState<Exercise | null>(null);
  const [placement, setPlacement] = useState<Placement | null>(null);
  const [quiz, setQuiz] = useState<Quiz | null>(null);
  const [progress, setProgress] = useState<Progress>(emptyProgress);
  const [profile, setProfile] = useState<LearnerProfile>({
    age_range: "teen-adult",
    experience_level: "new",
    learning_goal: "build",
    motivation_type: "create-real-projects",
    preferred_style: "guided",
    selected_theme_id: "explorer",
  });
  const [placementAnswers, setPlacementAnswers] = useState<Record<string, string>>({});
  const [placementResult, setPlacementResult] = useState<string>("");
  const [code, setCode] = useState('print("Hello World")');
  const [runResult, setRunResult] = useState<{ passed: boolean; output: string; message: string } | null>(null);
  const [quizAnswers, setQuizAnswers] = useState<Record<string, string>>({});
  const [quizResult, setQuizResult] = useState<string>("");
  const [accountMessage, setAccountMessage] = useState("");
  const [apiMessage, setApiMessage] = useState("");

  useEffect(() => {
    Promise.all([api.themes(), api.progress(anonymousUserId)])
      .then(([themeData, progressData]) => {
        const typedThemes = (themeData as { themes: Theme[] }).themes;
        setThemes(typedThemes);
        setTheme(typedThemes[0] ?? defaultTheme);
        setProgress(progressData as Progress);
        setApiMessage("");
      })
      .catch(() => {
        setThemes([defaultTheme]);
        setApiMessage("Backend connection is unavailable. Showing the local starter experience.");
      });
  }, []);

  const cssVars = useMemo(
    () =>
      ({
        "--primary": theme.tokens.primary,
        "--secondary": theme.tokens.secondary,
        "--accent": theme.tokens.accent,
        "--background": theme.tokens.background,
        "--surface": theme.tokens.surface,
        "--text": theme.tokens.text,
        "--muted": theme.tokens.muted,
        "--code-bg": theme.tokens.code_background,
        "--hero-image": theme.tokens.hero_image,
        "--lesson-image": theme.tokens.lesson_image,
      }) as CSSProperties,
    [theme]
  );

  async function chooseTheme(themeId: string) {
    const selected = (await api.selectTheme(anonymousUserId, themeId)) as Theme;
    setTheme(selected);
    setProfile((current) => ({ ...current, selected_theme_id: selected.id }));
  }

  async function submitProfile() {
    const result = (await api.saveProfile(anonymousUserId, profile)) as {
      recommendations: Recommendation[];
      theme: Theme;
    };
    setRecommendations(result.recommendations);
    setTheme(result.theme);
    setStep("recommendations");
  }

  async function loadCourse(recommendation: Recommendation) {
    const [courseData, placementData] = await Promise.all([
      api.course(recommendation.course.slug),
      api.placement(recommendation.course.id),
    ]);
    const course = courseData as { lesson: Lesson; exercise: Exercise; quiz: { id: string } };
    setLesson(course.lesson);
    setExercise(course.exercise);
    setCode(course.exercise.starter_code);
    setPlacement(placementData as Placement);
    setStep("placement");
  }

  async function submitPlacement() {
    if (!placement) return;
    const result = (await api.submitPlacement(anonymousUserId, placement.course_id, placementAnswers)) as {
      score: number;
      recommendation: string;
    };
    setPlacementResult(`${result.score}% - ${result.recommendation}`);
    const updatedProgress = (await api.progress(anonymousUserId)) as Progress;
    setProgress(updatedProgress);
  }

  async function completeLesson() {
    if (!lesson || !exercise) return;
    const updated = (await api.completeLesson(anonymousUserId, lesson.id)) as Progress;
    setProgress(updated);
    const loadedExercise = (await api.exercise(exercise.id)) as Exercise;
    setExercise(loadedExercise);
    setStep("lesson");
  }

  async function runExercise() {
    if (!exercise) return;
    const result = (await api.submitExercise(anonymousUserId, exercise.id, code)) as {
      passed: boolean;
      output: string;
      message: string;
      progress: Progress;
    };
    setRunResult(result);
    setProgress(result.progress);
  }

  async function loadQuiz() {
    const loadedQuiz = (await api.quiz("quiz-print-basics")) as Quiz;
    setQuiz(loadedQuiz);
    setStep("quiz");
  }

  async function submitQuiz() {
    if (!quiz) return;
    const result = (await api.submitQuiz(anonymousUserId, quiz.id, quizAnswers)) as {
      score: number;
      passed: boolean;
      progress: Progress;
    };
    setQuizResult(`${result.score}% - ${result.passed ? "Passed" : "Keep practicing"}`);
    setProgress(result.progress);
  }

  async function createAccount() {
    const result = (await api.createAccount(anonymousUserId, "Demo Learner", "learner@example.com")) as {
      message: string;
    };
    setAccountMessage(result.message);
  }

  return (
    <main className="app" style={cssVars}>
      <header className="topbar">
        <div>
          <div className="brand">PyVenturer</div>
          <div className="tagline">Learn Python. Create Anything.</div>
        </div>
        <div className="top-status" aria-label="Progress summary">
          <span>
            <Sparkles size={15} />
            {progress.xp} XP
          </span>
          <span>
            <Flame size={15} />
            {progress.streak} streak
          </span>
          <span>
            <Award size={15} />
            {progress.badges.length} badges
          </span>
        </div>
        <nav className="steps" aria-label="Learning journey">
          {["start", "recommendations", "placement", "lesson", "quiz", "save"].map((item) => (
            <button key={item} className={step === item ? "step active" : "step"} onClick={() => setStep(item)}>
              {item}
            </button>
          ))}
        </nav>
      </header>

      {step === "start" ? (
        <section className="hero-band">
          <div className="hero-copy">
            <p className="eyebrow">Python first, real skills always</p>
            <h1>Python is the launchpad for building useful things.</h1>
            <p>
              It powers automation, data work, APIs, apps, games, and AI tools. PyVenturer starts with your age, skill
              level, goals, style, and theme so the first lesson feels like it was chosen for you.
            </p>
          </div>
        </section>
      ) : (
        <section className="learning-strip">
          <div>
            <strong>{recommendations[0]?.course.title ?? "Python Demo Path"}</strong>
            <span>{step === "lesson" ? "Sample lesson and coding exercise" : "Guided learner path"}</span>
          </div>
          <ThemeSelector themes={themes} selectedTheme={theme} onSelect={chooseTheme} compact />
        </section>
      )}

      <section className="workspace">
        <section className="main-panel">
          {apiMessage && <div className="result">{apiMessage}</div>}
          {step === "start" && (
            <OnboardingPanel
              profile={profile}
              setProfile={setProfile}
              onSubmit={submitProfile}
              themes={themes}
              selectedTheme={theme}
              onThemeSelect={chooseTheme}
            />
          )}
          {step === "recommendations" && (
            <RecommendationPanel recommendations={recommendations} onStart={loadCourse} />
          )}
          {step === "placement" && placement && (
            <PlacementPanel
              placement={placement}
              answers={placementAnswers}
              setAnswers={setPlacementAnswers}
              result={placementResult}
              onSubmit={submitPlacement}
              onContinue={completeLesson}
            />
          )}
          {step === "lesson" && lesson && exercise && (
            <LessonPanel
              lesson={lesson}
              exercise={exercise}
              code={code}
              setCode={setCode}
              runResult={runResult}
              onRun={runExercise}
              onQuiz={loadQuiz}
            />
          )}
          {step === "quiz" && quiz && (
            <QuizPanel
              quiz={quiz}
              answers={quizAnswers}
              setAnswers={setQuizAnswers}
              result={quizResult}
              onSubmit={submitQuiz}
              onSave={() => setStep("save")}
            />
          )}
          {step === "save" && (
            <AccountPrompt progress={progress} message={accountMessage} onCreate={createAccount} />
          )}
        </section>
      </section>
    </main>
  );
}

function ThemeSelector({
  themes,
  selectedTheme,
  onSelect,
  compact = false,
}: {
  themes: Theme[];
  selectedTheme: Theme;
  onSelect: (id: string) => void;
  compact?: boolean;
}) {
  return (
    <div className={compact ? "theme-panel theme-panel-compact" : "theme-panel"}>
      <div className="panel-title">
        <Palette size={18} />
        Theme
      </div>
      <div className="theme-list">
        {themes.map((item) => (
          <button
            className={item.id === selectedTheme.id ? "theme-choice selected" : "theme-choice"}
            key={item.id}
            onClick={() => onSelect(item.id)}
          >
            <span style={{ background: item.tokens.primary }} />
            {item.name}
          </button>
        ))}
      </div>
      {!compact && <p>{selectedTheme.description}</p>}
    </div>
  );
}

type OnboardingStep = {
  id: string;
  title: string;
  body: string;
  field?: keyof LearnerProfile;
  options?: { value: string; label: string; description: string }[];
};

const onboardingSteps: OnboardingStep[] = [
  {
    id: "why-python",
    title: "Why Python?",
    body: "Python is readable, powerful, and everywhere: automation scripts, data analysis, APIs, games, AI agents, and cloud workflows. It is a practical first language because small wins turn into real projects quickly.",
  },
  {
    id: "age",
    title: "What age range should we design for?",
    body: "This helps us tune pacing and examples without making assumptions about interests.",
    field: "age_range",
    options: [
      { value: "under-13", label: "Under 13", description: "Shorter lessons and extra guidance." },
      { value: "13-17", label: "13-17", description: "Project-focused, clear pacing." },
      { value: "teen-adult", label: "Adult", description: "Practical skills and independent flow." },
    ],
  },
  {
    id: "skill",
    title: "What is your current skill level?",
    body: "Your answer helps us decide whether to start with fundamentals or move faster.",
    field: "experience_level",
    options: [
      { value: "new", label: "Brand new", description: "I have not coded much yet." },
      { value: "some", label: "Some practice", description: "I know a few basics." },
      { value: "confident", label: "Confident", description: "I want to skip easy material." },
    ],
  },
  {
    id: "goal",
    title: "What do you want Python to help you build?",
    body: "Courses should connect topics to outcomes, not just list concepts.",
    field: "learning_goal",
    options: [
      { value: "build", label: "Real projects", description: "Apps, tools, and portfolio work." },
      { value: "automation", label: "Automation", description: "Scripts that save time." },
      { value: "data", label: "Data", description: "Analysis and visualization." },
      { value: "ai", label: "AI builders", description: "Agents, chatbots, and AI tools." },
    ],
  },
  {
    id: "style",
    title: "How do you like to learn?",
    body: "This affects presentation and guidance, not the underlying curriculum.",
    field: "preferred_style",
    options: [
      { value: "guided", label: "Guided", description: "Step-by-step with helpful prompts." },
      { value: "minimal", label: "Minimal", description: "Quiet, focused, less hand-holding." },
      { value: "challenge", label: "Challenge", description: "Faster checks and more doing." },
    ],
  },
  {
    id: "theme",
    title: "Choose your page theme",
    body: "Themes change colors, graphics, and atmosphere. They do not change grading, content, or recommendations.",
  },
];

function OnboardingPanel({
  profile,
  setProfile,
  onSubmit,
  themes,
  selectedTheme,
  onThemeSelect,
}: {
  profile: LearnerProfile;
  setProfile: (profile: LearnerProfile) => void;
  onSubmit: () => void;
  themes: Theme[];
  selectedTheme: Theme;
  onThemeSelect: (id: string) => void;
}) {
  const [questionIndex, setQuestionIndex] = useState(0);
  const current = onboardingSteps[questionIndex];
  const isLast = questionIndex === onboardingSteps.length - 1;
  const selectedValue = current.field ? profile[current.field] : "";

  function choose(field: keyof LearnerProfile, value: string) {
    const nextProfile = { ...profile, [field]: value };
    setProfile(nextProfile);
    if (field === "selected_theme_id") {
      onThemeSelect(value);
    }
  }

  return (
    <div className="flow-panel onboarding-panel">
      <div className="onboarding-progress">
        {onboardingSteps.map((item, index) => (
          <span key={item.id} className={index <= questionIndex ? "filled" : ""} />
        ))}
      </div>
      <PanelHeader
        icon={current.id === "why-python" ? <Lightbulb size={22} /> : <Target size={22} />}
        title={current.title}
      />
      <p className="question-body">{current.body}</p>

      {current.options && current.field && (
        <div className="option-grid">
          {current.options.map((option) => (
            <button
              key={option.value}
              className={selectedValue === option.value ? "option-card selected" : "option-card"}
              onClick={() => choose(current.field!, option.value)}
            >
              <strong>{option.label}</strong>
              <span>{option.description}</span>
            </button>
          ))}
        </div>
      )}

      {current.id === "theme" && (
        <div className="option-grid">
          {(themes.length ? themes : [selectedTheme]).map((item) => (
            <button
              key={item.id}
              className={profile.selected_theme_id === item.id ? "option-card selected theme-option" : "option-card theme-option"}
              onClick={() => choose("selected_theme_id", item.id)}
            >
              <i style={{ background: item.tokens.primary }} />
              <strong>{item.name}</strong>
              <span>{item.description}</span>
            </button>
          ))}
        </div>
      )}

      <div className="button-row onboarding-actions">
        {questionIndex > 0 && (
          <button className="secondary-button" onClick={() => setQuestionIndex((index) => index - 1)}>
            Back
          </button>
        )}
        {!isLast ? (
          <button className="primary-button" onClick={() => setQuestionIndex((index) => index + 1)}>
            Next <ChevronRight size={18} />
          </button>
        ) : (
          <button className="primary-button" onClick={onSubmit}>
            Show my recommendation <ChevronRight size={18} />
          </button>
        )}
      </div>
    </div>
  );
}

function RecommendationPanel({
  recommendations,
  onStart,
}: {
  recommendations: Recommendation[];
  onStart: (recommendation: Recommendation) => void;
}) {
  return (
    <div className="flow-panel">
      <PanelHeader icon={<GraduationCap size={22} />} title="Recommended Course" />
      {recommendations.map((recommendation) => (
        <article className="course-card" key={recommendation.course.id}>
          <div>
            <p className="eyebrow">Recommended starting path</p>
            <h2>{recommendation.course.title}</h2>
            <p>{recommendation.course.description}</p>
            <p className="reason">{recommendation.reason}</p>
          </div>
          <ul>
            {recommendation.next_steps.map((nextStep) => (
              <li key={nextStep}>{nextStep}</li>
            ))}
          </ul>
          <button className="primary-button" onClick={() => onStart(recommendation)}>
            Take placement <ChevronRight size={18} />
          </button>
        </article>
      ))}
    </div>
  );
}

function PlacementPanel({
  placement,
  answers,
  setAnswers,
  result,
  onSubmit,
  onContinue,
}: {
  placement: Placement;
  answers: Record<string, string>;
  setAnswers: (answers: Record<string, string>) => void;
  result: string;
  onSubmit: () => void;
  onContinue: () => void;
}) {
  return (
    <div className="flow-panel">
      <PanelHeader icon={<CheckCircle2 size={22} />} title={placement.title} />
      {placement.questions.map((question) => (
        <QuestionBlock key={question.id} question={question} answers={answers} setAnswers={setAnswers} />
      ))}
      <div className="button-row">
        <button className="primary-button" onClick={onSubmit}>Submit placement</button>
        {result && <button className="secondary-button" onClick={onContinue}>Try sample lesson</button>}
      </div>
      {result && <div className="result success">{result}</div>}
    </div>
  );
}

function LessonPanel({
  lesson,
  exercise,
  code,
  setCode,
  runResult,
  onRun,
  onQuiz,
}: {
  lesson: Lesson;
  exercise: Exercise;
  code: string;
  setCode: (code: string) => void;
  runResult: { passed: boolean; output: string; message: string } | null;
  onRun: () => void;
  onQuiz: () => void;
}) {
  return (
    <div className="lesson-layout">
      <section className="lesson-copy">
        <PanelHeader icon={<BookOpen size={22} />} title={lesson.title} />
        <div className="lesson-image" />
        <p>{lesson.body}</p>
        <pre className="inline-code">{lesson.code_examples[0]}</pre>
      </section>
      <section className="runner">
        <PanelHeader icon={<Code2 size={22} />} title={exercise.title} />
        <p>{exercise.instructions}</p>
        <textarea aria-label="Python code editor" value={code} onChange={(event) => setCode(event.target.value)} />
        <button className="primary-button" onClick={onRun}>
          <Play size={18} /> Run code
        </button>
        {runResult && (
          <div className={runResult.passed ? "result success" : "result"}>
            <strong>{runResult.message}</strong>
            <span>Output: {runResult.output || "(no output)"}</span>
          </div>
        )}
        {runResult?.passed && (
          <button className="secondary-button" onClick={onQuiz}>Take quiz</button>
        )}
      </section>
    </div>
  );
}

function QuizPanel({
  quiz,
  answers,
  setAnswers,
  result,
  onSubmit,
  onSave,
}: {
  quiz: Quiz;
  answers: Record<string, string>;
  setAnswers: (answers: Record<string, string>) => void;
  result: string;
  onSubmit: () => void;
  onSave: () => void;
}) {
  return (
    <div className="flow-panel">
      <PanelHeader icon={<CheckCircle2 size={22} />} title={quiz.title} />
      {quiz.questions.map((question) => (
        <QuestionBlock key={question.id} question={question} answers={answers} setAnswers={setAnswers} />
      ))}
      <div className="button-row">
        <button className="primary-button" onClick={onSubmit}>Submit quiz</button>
        {result && <button className="secondary-button" onClick={onSave}>Save progress</button>}
      </div>
      {result && <div className="result success">{result}</div>}
    </div>
  );
}

function AccountPrompt({
  progress,
  message,
  onCreate,
}: {
  progress: Progress;
  message: string;
  onCreate: () => void;
}) {
  return (
    <div className="flow-panel save-panel">
      <PanelHeader icon={<Save size={22} />} title="Create an account to save progress" />
      <p>You have tried the lesson, run code, earned XP, and unlocked badges before registration.</p>
      <div className="stats wide">
        <div>
          <strong>{progress.xp}</strong>
          <span>XP ready to save</span>
        </div>
        <div>
          <strong>{progress.badges.length}</strong>
          <span>badges</span>
        </div>
      </div>
      <button className="primary-button" onClick={onCreate}>Create demo account</button>
      {message && <div className="result success">{message}</div>}
    </div>
  );
}

function QuestionBlock({
  question,
  answers,
  setAnswers,
}: {
  question: Question;
  answers: Record<string, string>;
  setAnswers: (answers: Record<string, string>) => void;
}) {
  return (
    <fieldset className="question">
      <legend>{question.prompt}</legend>
      <div className="choice-row">
        {question.choices.map((choice) => (
          <label key={choice} className={answers[question.id] === choice ? "choice selected" : "choice"}>
            <input
              type="radio"
              name={question.id}
              value={choice}
              checked={answers[question.id] === choice}
              onChange={() => setAnswers({ ...answers, [question.id]: choice })}
            />
            {choice}
          </label>
        ))}
      </div>
    </fieldset>
  );
}

function PanelHeader({ icon, title }: { icon: ReactNode; title: string }) {
  return (
    <div className="panel-heading">
      {icon}
      <h2>{title}</h2>
    </div>
  );
}

export { App };
