# -----------------------------
# Frontend build stage
# -----------------------------
FROM node:20-alpine AS frontend-build

WORKDIR /app/frontend

COPY frontend/package*.json ./

RUN if [ -f package-lock.json ]; then npm ci; else npm install; fi

COPY frontend/ ./

ARG VITE_API_URL=/api
ENV VITE_API_URL=${VITE_API_URL}

RUN npm run build


# -----------------------------
# Final runtime stage
# Runs FastAPI backend + Nginx frontend in one Fly.io container
# -----------------------------
FROM python:3.12-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1
ENV PYVENTURER_DB_PATH=/data/pyventurer.db
ENV PORT=8080

# Install nginx for serving the frontend and proxying /api to FastAPI
RUN apt-get update \
    && apt-get install -y --no-install-recommends nginx ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Install backend dependencies
COPY backend/requirements.txt /app/backend/requirements.txt

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r /app/backend/requirements.txt \
    && pip install --no-cache-dir "uvicorn[standard]"

# Copy backend app
COPY backend/ /app/backend/

# Copy built frontend into nginx html folder
COPY --from=frontend-build /app/frontend/dist/ /usr/share/nginx/html/

# Create SQLite data directory
RUN mkdir -p /data

# Configure nginx:
# - serve React app on /
# - proxy /api/* to FastAPI backend on port 8001
RUN cat > /etc/nginx/nginx.conf <<'EOF'
events {}

http {
    server {
        listen 8080;

        root /usr/share/nginx/html;
        index index.html;

        client_max_body_size 20m;

        location /api/ {
            proxy_pass http://127.0.0.1:8001;
            proxy_http_version 1.1;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        location /docs {
            proxy_pass http://127.0.0.1:8001/docs;
            proxy_http_version 1.1;
            proxy_set_header Host $host;
        }

        location /openapi.json {
            proxy_pass http://127.0.0.1:8001/openapi.json;
            proxy_http_version 1.1;
            proxy_set_header Host $host;
        }

        location / {
            try_files $uri $uri/ /index.html;
        }
    }
}
EOF

# Startup script
RUN cat > /app/start.sh <<'EOF'
#!/bin/sh
set -e

echo "Starting PyVenturer backend on port 8001..."
cd /app/backend
uvicorn app.main:app --host 127.0.0.1 --port 8001 &

echo "Starting nginx on port 8080..."
nginx -g "daemon off;"
EOF

RUN chmod +x /app/start.sh

EXPOSE 8080

CMD ["/app/start.sh"]