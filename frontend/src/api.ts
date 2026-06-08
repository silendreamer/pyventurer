import type { LearnerProfile } from "./types";

const API_URL = import.meta.env.VITE_API_URL ?? "http://127.0.0.1:8001/api";

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_URL}${path}`, {
    ...init,
    headers: {
      "Content-Type": "application/json",
      ...(init?.headers ?? {}),
    },
  });
  if (!response.ok) {
    throw new Error(`API request failed: ${response.status}`);
  }
  return response.json() as Promise<T>;
}

export const api = {
  themes: () => request("/themes"),
  selectTheme: (anonymousUserId: string, themeId: string) =>
    request("/themes/select", {
      method: "POST",
      body: JSON.stringify({ anonymous_user_id: anonymousUserId, theme_id: themeId }),
    }),
  catalog: () => request("/catalog"),
  saveProfile: (anonymousUserId: string, profile: LearnerProfile) =>
    request("/onboarding/profile", {
      method: "POST",
      body: JSON.stringify({ anonymous_user_id: anonymousUserId, profile }),
    }),
  course: (slug: string) => request(`/courses/${slug}`),
  placement: (courseId: string) => request(`/courses/${courseId}/placement`),
  submitPlacement: (anonymousUserId: string, courseId: string, answers: Record<string, string>) =>
    request(`/courses/${courseId}/placement`, {
      method: "POST",
      body: JSON.stringify({ anonymous_user_id: anonymousUserId, answers }),
    }),
  exercise: (exerciseId: string) => request(`/exercises/${exerciseId}`),
  submitExercise: (anonymousUserId: string, exerciseId: string, code: string) =>
    request(`/exercises/${exerciseId}/submit`, {
      method: "POST",
      body: JSON.stringify({ anonymous_user_id: anonymousUserId, code }),
    }),
  quiz: (quizId: string) => request(`/quizzes/${quizId}`),
  submitQuiz: (anonymousUserId: string, quizId: string, answers: Record<string, string>) =>
    request(`/quizzes/${quizId}/submit`, {
      method: "POST",
      body: JSON.stringify({ anonymous_user_id: anonymousUserId, answers }),
    }),
  completeLesson: (anonymousUserId: string, lessonId: string) =>
    request(`/progress/${anonymousUserId}/lessons/${lessonId}/complete`, { method: "POST" }),
  progress: (anonymousUserId: string) => request(`/progress/${anonymousUserId}`),
  createAccount: (anonymousUserId: string, name: string, email: string) =>
    request("/account", {
      method: "POST",
      body: JSON.stringify({ anonymous_user_id: anonymousUserId, name, email }),
    }),
};
