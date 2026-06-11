# PyVenturer MVP Development

## Run Backend

```powershell
cd backend
python -m uvicorn app.main:app --host 127.0.0.1 --port 8001
```

## Run Frontend

```powershell
cd frontend
npm.cmd install
npm.cmd run dev -- --port 5174
```

Open:

```text
http://127.0.0.1:5174
```

The frontend defaults to:

```text
/api
```

Vite proxies `/api` to `http://127.0.0.1:8001` during local development. If
port `5174` is busy, any Vite port can be used. The backend CORS settings allow
local `localhost` and `127.0.0.1` development ports.

## Verify

From the project root:

```powershell
python -m pytest backend
```

From `frontend/`:

```powershell
npm.cmd run build
```

## Current Notes

- Port `8000` may already be used by another local app, so the PyVenturer API
  uses `8001`.
- The MVP uses SQLite through `backend/app/db/connection.py`. By default it
  writes `pyventurer.db` from the backend working directory. Set
  `PYVENTURER_DB_PATH` to use a different database path.
- Backend auth endpoints exist for register, login, logout, and current user.
  The frontend still uses a placeholder save-progress prompt instead of full
  register/login screens.
- The Python runner is intentionally limited and suitable only for demo
  exercises. It is not a production sandbox.

## Vercel Deployment

The root `vercel.json` builds `frontend/` as a Vite app and serves the FastAPI
backend through `api/index.py` as a Python function. The root `.python-version`
and `pyproject.toml` Python constraint steer Vercel away from Python 3.14, and
the Pydantic pin is kept current enough to avoid old `pydantic-core` PyO3 build
failures if Vercel still selects a newer runtime.

Recommended Vercel environment variable:

```text
PYVENTURER_SECRET_KEY=<strong random secret>
```

The MVP SQLite database is stored at `/tmp/pyventurer.db` on Vercel. That keeps
the demo deployable, but `/tmp` is ephemeral serverless storage. Move persistence
to a hosted database before relying on saved accounts or progress in production.
