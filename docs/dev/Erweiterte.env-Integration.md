# .env.example (Erweitert - behält Original-Struktur bei)

# ============================================
# ORIGINAL LOCAL AI PACKAGE CONFIGURATION
# ============================================

############
# [required]
# n8n credentials
############
N8N_ENCRYPTION_KEY=super-secret-key
N8N_USER_MANAGEMENT_JWT_SECRET=even-more-secret

############
# [required]
# Supabase Secrets
############
POSTGRES_PASSWORD=your-super-secret-and-long-postgres-password
JWT_SECRET=your-super-secret-jwt-token-with-at-least-32-characters-long
ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyAgCiAgICAicm9sZSI6ICJhbm9uIiwKICAgICJpc3MiOiAic3VwYWJhc2UtZGVtbyIsCiAgICAiaWF0IjogMTY0MTc2OTIwMCwKICAgICJleHAiOiAxNzk5NTM1NjAwCn0.dc_X5iR_VP_qT0zsiyj_I_OZ2T9FtRU2BBNWN8Bu4GE
SERVICE_ROLE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyAgCiAgICAicm9sZSI6ICJzZXJ2aWNlX3JvbGUiLAogICAgImlzcyI6ICJzdXBhYmFzZS1kZW1vIiwKICAgICJpYXQiOiAxNjQxNzY5MjAwLAogICAgImV4cCI6IDE3OTk1MzU2MDAKfQ.DaYlNEoUrrEn2Ig7tqibS-PHK5vgusbcbo7X36XVt4Q
DASHBOARD_USERNAME=supabase
DASHBOARD_PASSWORD=this_password_is_insecure_and_should_be_updated
POOLER_TENANT_ID=your-tenant-id

############
# [required]
# Langfuse credentials
############
CLICKHOUSE_PASSWORD=super-secret-key-1
MINIO_ROOT_PASSWORD=super-secret-key-2
LANGFUSE_SALT=super-secret-key-3
NEXTAUTH_SECRET=super-secret-key-4
ENCRYPTION_KEY=generate-with-openssl # generate via `openssl rand -hex 32`

############
# [required for prod]
# Caddy Config
############
# N8N_HOSTNAME=n8n.yourdomain.com
# WEBUI_HOSTNAME=openwebui.yourdomain.com
# FLOWISE_HOSTNAME=flowise.yourdomain.com
# SUPABASE_HOSTNAME=supabase.yourdomain.com
# LANGFUSE_HOSTNAME=langfuse.yourdomain.com
# OLLAMA_HOSTNAME=ollama.yourdomain.com
# SEARXNG_HOSTNAME=searxng.yourdomain.com
# LETSENCRYPT_EMAIL=internal

############
# [optional] Original configurations
############
SEARXNG_UWSGI_WORKERS=4
SEARXNG_UWSGI_THREADS=4
POSTGRES_HOST=db
POSTGRES_DB=postgres
POSTGRES_PORT=5432

# ============================================
# EXTENDED FEATURES CONFIGURATION
# ============================================

############
# [desktop] Guacamole & Desktop Environment
############
GUAC_POSTGRES_PASSWORD=secure-guacamole-db-password
DESKTOP_PASSWORD=password
VNC_PASSWORD=password
DESKTOP_USER=kasm-user
DESKTOP_TIMEZONE=Europe/Berlin

# Guacamole URLs (for production reverse proxy)
# GUACAMOLE_HOSTNAME=desktop.yourdomain.com

############
# [productivity] AppFlowy & AFFINE
############
# AppFlowy nutzt die bestehende Supabase-DB
APPFLOWY_DATABASE_URL=postgres://postgres:${POSTGRES_PASSWORD}@db:5432/appflowy

# AFFINE nutzt die bestehende Supabase-DB und neuen Redis
AFFINE_DATABASE_URL=postgres://postgres:${POSTGRES_PASSWORD}@db:5432/affine
AFFINE_REDIS_HOST=redis
AFFINE_REDIS_PORT=6379
AFFINE_SERVER_HOST=0.0.0.0
AFFINE_SERVER_PORT=3010

# Production URLs
# APPFLOWY_HOSTNAME=notes.yourdomain.com
# AFFINE_HOSTNAME=workspace.yourdomain.com

############
# [development] GitLab & Extended N8N
############
# GitLab bekommt eigene PostgreSQL-Instanz
GITLAB_ROOT_PASSWORD=change-this-gitlab-root-password
GITLAB_POSTGRES_DB=gitlab
GITLAB_POSTGRES_USER=gitlab
GITLAB_POSTGRES_PASSWORD=secure-gitlab-db-password
GITLAB_EXTERNAL_URL=http://localhost:8082
GITLAB_SSH_PORT=2222

# Extended N8N (zweite Instanz)
N8N_EXTENDED_ENCRYPTION_KEY=different-encryption-key-for-extended-n8n
N8N_EXTENDED_JWT_SECRET=different-jwt-secret-for-extended-n8n

# Production URLs
# GITLAB_HOSTNAME=git.yourdomain.com
# N8N_EXTENDED_HOSTNAME=n8n-extended.yourdomain.com

############
# [optional] Additional Services
############
# Redis für AFFINE und andere Services
REDIS_PASSWORD=optional-redis-password

# Backup Configuration
BACKUP_ENABLED=true
BACKUP_SCHEDULE="0 2 * * *"  # Daily at 2 AM
BACKUP_RETENTION_DAYS=30
BACKUP_LOCATION=./backups

############
# [internal] Service URLs - DO NOT CHANGE
############
# Interne Service-Discovery URLs
INTERNAL_OLLAMA_URL=http://ollama:11434
INTERNAL_QDRANT_URL=http://qdrant:6333
INTERNAL_SUPABASE_URL=http://kong:8000
INTERNAL_DESKTOP_URL=http://desktop:6901
INTERNAL_GUACAMOLE_URL=http://guacamole:8080
