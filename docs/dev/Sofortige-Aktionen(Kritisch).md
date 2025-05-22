# Beispiel: Erweiterte docker-compose.yml (Auszug)
# Zeigt, wie Guacamole sauber integriert werden kann

version: '3.8'

networks:
  default:
    name: localai

volumes:
  # Original Volumes
  n8n_storage:
  ollama_storage:
  qdrant_storage:
  open-webui:

  # Neue Volumes (sauber getrennt)
  guacamole_postgres_data:
  desktop_home:
  appflowy_data:
  affine_data:

services:
  # ===== ORIGINAL SERVICES (unverändert) =====
  n8n:
    <<: *service-n8n
    container_name: n8n
    restart: unless-stopped
    ports:
      - 5678:5678
    volumes:
      - n8n_storage:/home/node/.n8n
      - ./shared:/data/shared
    depends_on:
      n8n-import:
        condition: service_completed_successfully
    profiles:
      - cpu
      - gpu-nvidia
      - gpu-amd

  ollama-cpu:
    profiles: ["cpu"]
    <<: *service-ollama

  ollama-gpu:
    profiles: ["gpu-nvidia"]
    <<: *service-ollama
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]

  # ===== NEUE SERVICES (sauber getrennt) =====
  # Guacamole Database (eigene Instanz)
  guacamole-postgres:
    image: postgres:15-alpine
    container_name: guacamole-postgres
    environment:
      POSTGRES_DB: guacamole_db
      POSTGRES_USER: guacamole_user
      POSTGRES_PASSWORD: ${GUAC_POSTGRES_PASSWORD}
    volumes:
      - guacamole_postgres_data:/var/lib/postgresql/data
      - ./guacamole/init:/docker-entrypoint-initdb.d:ro
    profiles:
      - desktop
    restart: unless-stopped
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U guacamole_user -d guacamole_db"]
      interval: 10s
      timeout: 5s
      retries: 5

  guacd:
    image: guacamole/guacd:latest
    container_name: guacd
    profiles:
      - desktop
    restart: unless-stopped

  guacamole:
    image: guacamole/guacamole:latest
    container_name: guacamole
    depends_on:
      guacd:
        condition: service_started
      guacamole-postgres:
        condition: service_healthy
    environment:
      GUACD_HOSTNAME: guacd
      POSTGRES_HOSTNAME: guacamole-postgres
      POSTGRES_DATABASE: guacamole_db
      POSTGRES_USER: guacamole_user
      POSTGRES_PASSWORD: ${GUAC_POSTGRES_PASSWORD}
    ports:
      - "8080:8080"
    profiles:
      - desktop
    restart: unless-stopped

  desktop:
    image: kasmweb/desktop:1.15.0-rolling
    container_name: linux-desktop
    environment:
      VNC_PW: ${DESKTOP_PASSWORD:-password}
      KASM_PORT: 6901
    volumes:
      - desktop_home:/home/kasm-user
      - ./desktop-shared:/shared:rw
    ports:
      - "6901:6901"
    profiles:
      - desktop
    restart: unless-stopped
    shm_size: 2gb

  # AppFlowy (nutzt bestehende Supabase-DB)
  appflowy:
    image: appflowyinc/appflowy:latest
    container_name: appflowy
    ports:
      - "8081:8080"
    environment:
      APPFLOWY_DATABASE_URL: postgres://postgres:${POSTGRES_PASSWORD}@db:5432/appflowy
    volumes:
      - appflowy_data:/data
    depends_on:
      - db  # Nutzt bestehende Supabase-DB
    profiles:
      - productivity
    restart: unless-stopped

  # AFFINE (nutzt bestehende Redis-Alternative)
  affine:
    image: ghcr.io/toeverything/affine-graphql:stable
    container_name: affine
    ports:
      - "3010:3010"
    environment:
      NODE_ENV: production
      DATABASE_URL: postgres://postgres:${POSTGRES_PASSWORD}@db:5432/affine
      REDIS_SERVER_HOST: redis
      REDIS_SERVER_PORT: 6379
    volumes:
      - affine_data:/workspace
    depends_on:
      - db
      - redis
    profiles:
      - productivity
    restart: unless-stopped

  # Redis für AFFINE und andere Services
  redis:
    image: redis:7-alpine
    container_name: redis
    command: redis-server --appendonly yes
    volumes:
      - redis_data:/data
    profiles:
      - productivity
      - development
    restart: unless-stopped
