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
npm.cmd run dev -- --port 5173
```

Open:

```text
http://127.0.0.1:5173
```

The frontend defaults to:

```text
http://127.0.0.1:8001/api
```
