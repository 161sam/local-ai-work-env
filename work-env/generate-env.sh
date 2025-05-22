#!/bin/bash
# generate-env.sh - Automatische Generierung einer sicheren .env-Datei

set -e

echo "🔐 Extended AI Stack - Sichere .env Generierung"
echo "================================================="

# Prüfen ob .env bereits existiert
if [ -f ".env" ]; then
    echo "⚠️  .env Datei existiert bereits!"
    read -p "Möchten Sie sie überschreiben? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "❌ Abgebrochen. Bestehende .env-Datei wurde nicht verändert."
        exit 1
    fi
    cp .env .env.backup.$(date +%Y%m%d_%H%M%S)
    echo "✅ Backup erstellt: .env.backup.$(date +%Y%m%d_%H%M%S)"
fi

# Funktionen für sichere Passwort-Generierung
generate_password() {
    openssl rand -base64 32 | tr -d "=+/" | cut -c1-25
}

generate_hex_key() {
    openssl rand -hex 32
}

generate_jwt_secret() {
    openssl rand -base64 64 | tr -d "=+/" | cut -c1-64
}

generate_alphanumeric() {
    cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 32 | head -n 1
}

echo "🔑 Generiere sichere Passwörter und Schlüssel..."

# Generiere alle benötigten Secrets
N8N_ENCRYPTION_KEY=$(generate_hex_key)
N8N_JWT_SECRET=$(generate_jwt_secret)
POSTGRES_PASSWORD=$(generate_password)
JWT_SECRET=$(generate_jwt_secret)
WEBUI_SECRET_KEY=$(generate_hex_key)
GUAC_POSTGRES_PASSWORD=$(generate_password)
GITLAB_ROOT_PASSWORD=$(generate_password)
GITLAB_POSTGRES_PASSWORD=$(generate_password)
WEBHOOK_SECRET=$(generate_hex_key)
DASHBOARD_PASSWORD=$(generate_password)

# Langfuse Secrets
CLICKHOUSE_PASSWORD=$(generate_password)
MINIO_ROOT_PASSWORD=$(generate_password)
LANGFUSE_SALT=$(generate_password)
NEXTAUTH_SECRET=$(generate_hex_key)
ENCRYPTION_KEY=$(generate_hex_key)

# Weitere Secrets
SECRET_KEY_BASE=$(generate_hex_key)
VAULT_ENC_KEY=$(generate_hex_key)

echo "📝 Erstelle .env-Datei mit generierten Werten..."

# .env-Datei erstellen
cat > .env << EOF
# ========================================
# EXTENDED AI STACK CONFIGURATION
# ========================================
# Auto-generated on $(date)
# 
# ⚠️  WICHTIG: Für Produktion alle Domain-Settings anpassen!

############
# [REQUIRED] CORE AI STACK - N8N & Security
############

N8N_ENCRYPTION_KEY=${N8N_ENCRYPTION_KEY}
N8N_USER_MANAGEMENT_JWT_SECRET=${N8N_JWT_SECRET}

# N8N Configuration
N8N_HOST=localhost
N8N_PROTOCOL=http
N8N_PORT=5678
N8N_WEBHOOK_URL=http://localhost:5678/
N8N_EDITOR_BASE_URL=http://localhost:5678
GENERIC_TIMEZONE=Europe/Berlin

# N8N Extended Instance
N8N_EXTENDED_HOST=localhost
N8N_EXTENDED_PORT=5679
N8N_EXTENDED_WEBHOOK_URL=http://localhost:5679/

############
# [REQUIRED] DATABASE & SUPABASE CONFIGURATION
############

POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
POSTGRES_HOST=supabase-db
POSTGRES_DB=postgres
POSTGRES_PORT=5432
POSTGRES_USER=postgres

# Supabase Authentication & API Keys
JWT_SECRET=${JWT_SECRET}
ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyAgCiAgICAicm9sZSI6ICJhbm9uIiwKICAgICJpc3MiOiAic3VwYWJhc2UtZGVtbyIsCiAgICAiaWF0IjogMTY0MTc2OTIwMCwKICAgICJleHAiOiAxNzk5NTM1NjAwCn0.dc_X5iR_VP_qT0zsiyj_I_OZ2T9FtRU2BBNWN8Bu4GE
SERVICE_ROLE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyAgCiAgICAicm9sZSI6ICJzZXJ2aWNlX3JvbGUiLAogICAgImlzcyI6ICJzdXBhYmFzZS1kZW1vIiwKICAgICJpYXQiOiAxNjQxNzY5MjAwLAogICAgImV4cCI6IDE3OTk1MzU2MDAKfQ.DaYlNEoUrrEn2Ig7tqibS-PHK5vgusbcbo7X36XVt4Q

# Supabase Dashboard
DASHBOARD_USERNAME=supabase
DASHBOARD_PASSWORD=${DASHBOARD_PASSWORD}
POOLER_TENANT_ID=1000

# Supabase URLs and Settings
SITE_URL=http://localhost:3000
API_EXTERNAL_URL=http://localhost:8000
SUPABASE_PUBLIC_URL=http://localhost:8000
ADDITIONAL_REDIRECT_URLS=
DISABLE_SIGNUP=false
JWT_EXPIRY=3600

############
# [REQUIRED] GUACAMOLE & DESKTOP CONFIGURATION
############

GUAC_POSTGRES_DB=guacamole_db
GUAC_POSTGRES_USER=guacamole_user
GUAC_POSTGRES_PASSWORD=${GUAC_POSTGRES_PASSWORD}

# Desktop Environment
DESKTOP_USER=kasm-user
DESKTOP_PASSWORD=password
VNC_PASSWORD=password
DESKTOP_TIMEZONE=Europe/Berlin

############
# [REQUIRED] AI SERVICES CONFIGURATION
############

OLLAMA_HOST=http://ollama:11434
OLLAMA_MODELS=llama3.1,codellama,mistral

# Open WebUI
WEBUI_SECRET_KEY=${WEBUI_SECRET_KEY}
WEBUI_AUTH=true
WEBUI_DEFAULT_USER_ROLE=user

# Qdrant Vector Database
QDRANT_API_KEY=
QDRANT_COLLECTION_NAME=default

############
# [REQUIRED] EXTENDED SERVICES CONFIGURATION
############

# AppFlowy Configuration
APPFLOWY_DATABASE_URL=postgres://postgres:${POSTGRES_PASSWORD}@supabase-db:5432/appflowy
APPFLOWY_API_URL=http://appflowy:8080/api
APPFLOWY_API_KEY=

# AFFINE Configuration  
AFFINE_DATABASE_URL=postgres://postgres:${POSTGRES_PASSWORD}@supabase-db:5432/affine
AFFINE_REDIS_HOST=redis
AFFINE_REDIS_PORT=6379
AFFINE_SERVER_HOST=0.0.0.0
AFFINE_SERVER_PORT=3010
AFFINE_API_URL=http://affine:3010/api
AFFINE_API_KEY=

# GitLab Configuration
GITLAB_HOSTNAME=gitlab.local
GITLAB_ROOT_PASSWORD=${GITLAB_ROOT_PASSWORD}
GITLAB_POSTGRES_DB=gitlab
GITLAB_POSTGRES_USER=gitlab
GITLAB_POSTGRES_PASSWORD=${GITLAB_POSTGRES_PASSWORD}
GITLAB_EXTERNAL_URL=http://localhost:8082
GITLAB_SSH_PORT=2222

# GitLab Integration
GITLAB_TOKEN=
GITLAB_URL=http://gitlab:8082

# Redis Configuration
REDIS_PASSWORD=

############
# [OPTIONAL] WORKFLOW INTEGRATION
############

# GitHub Integration
GITHUB_TOKEN=
GITHUB_ORG=

# Project Management Integration
OPENPROJECT_URL=
OPENPROJECT_TOKEN=
OPENPROJECT_NEW_STATUS_ID=1
OPENPROJECT_IN_PROGRESS_STATUS_ID=7
OPENPROJECT_PR_CREATED_STATUS_ID=2
OPENPROJECT_RESOLVED_STATUS_ID=12

# LLM API Configuration
LLM_API_KEY=
LLM_MODEL=anthropic/claude-3-5-sonnet-20240620
OPENAI_API_KEY=

############
# [OPTIONAL] NOTIFICATION & WEBHOOKS
############

DISCORD_WEBHOOK_URL=
WEBHOOK_SECRET=${WEBHOOK_SECRET}

# Email Configuration
SMTP_ADMIN_EMAIL=admin@localhost
SMTP_HOST=
SMTP_PORT=587
SMTP_USER=
SMTP_PASS=
SMTP_SENDER_NAME=Extended AI Stack
ENABLE_EMAIL_SIGNUP=true
ENABLE_EMAIL_AUTOCONFIRM=false
ENABLE_ANONYMOUS_USERS=false
ENABLE_PHONE_SIGNUP=false
ENABLE_PHONE_AUTOCONFIRM=false

############
# [OPTIONAL] LANGFUSE OBSERVABILITY
############

CLICKHOUSE_PASSWORD=${CLICKHOUSE_PASSWORD}
MINIO_ROOT_PASSWORD=${MINIO_ROOT_PASSWORD}
LANGFUSE_SALT=${LANGFUSE_SALT}
NEXTAUTH_SECRET=${NEXTAUTH_SECRET}
ENCRYPTION_KEY=${ENCRYPTION_KEY}

############
# [PRODUCTION] REVERSE PROXY & SSL - UNCOMMENT FOR PRODUCTION
############

# N8N_HOSTNAME=n8n.yourdomain.com
# WEBUI_HOSTNAME=webui.yourdomain.com  
# GUACAMOLE_HOSTNAME=desktop.yourdomain.com
# APPFLOWY_HOSTNAME=notes.yourdomain.com
# AFFINE_HOSTNAME=workspace.yourdomain.com
# GITLAB_HOSTNAME=git.yourdomain.com
# SUPABASE_HOSTNAME=db.yourdomain.com
# OLLAMA_HOSTNAME=ai.yourdomain.com
# LETSENCRYPT_EMAIL=admin@yourdomain.com

############
# [OPTIONAL] ADVANCED CONFIGURATION
############

ORG_NAME=
SKIP_REPOS=
ONLY_REPOS=

PROJECT_MAPPING={}

# MCP Configuration
MCP_ENABLED=true
MCP_SERVER_PORT=3333
MCP_SERVER_HOST=localhost
MCP_DEFAULT_TOOLS=create_github_issue,update_work_package,sync_documentation

# Logging
LOG_LEVEL=info
LOG_DIR=./logs

############
# [SYSTEM] DOCKER & NETWORKING
############

DOCKER_SOCKET_LOCATION=/var/run/docker.sock
NETWORK_NAME=extended-ai-network

############
# [INTERNAL] ADVANCED SETTINGS
############

POOLER_PROXY_PORT_TRANSACTION=6543
POOLER_DEFAULT_POOL_SIZE=20
POOLER_MAX_CLIENT_CONN=100
SECRET_KEY_BASE=${SECRET_KEY_BASE}
VAULT_ENC_KEY=${VAULT_ENC_KEY}

KONG_HTTP_PORT=8000
KONG_HTTPS_PORT=8443

PGRST_DB_SCHEMAS=public,storage,graphql_public

STUDIO_DEFAULT_ORGANIZATION=Extended AI Organization
STUDIO_DEFAULT_PROJECT=Main Project
STUDIO_PORT=3000

FUNCTIONS_VERIFY_JWT=false

MAILER_URLPATHS_CONFIRMATION="/auth/v1/verify"
MAILER_URLPATHS_INVITE="/auth/v1/verify"
MAILER_URLPATHS_RECOVERY="/auth/v1/verify"
MAILER_URLPATHS_EMAIL_CHANGE="/auth/v1/verify"

# Performance Tuning
SEARXNG_UWSGI_WORKERS=4
SEARXNG_UWSGI_THREADS=4

# Image Processing
IMGPROXY_ENABLE_WEBP_DETECTION=true

# Development
DEV_MODE=true
DEBUG_ENABLED=false

# Backup
BACKUP_ENABLED=true
BACKUP_SCHEDULE="0 2 * * *"
BACKUP_RETENTION_DAYS=30
BACKUP_LOCATION=./backups
EOF

echo "✅ .env-Datei erfolgreich erstellt!"
echo ""
echo "🔐 Generierte Passwörter (sicher aufbewahren!):"
echo "================================================="
echo "N8N Encryption Key:      ${N8N_ENCRYPTION_KEY:0:20}..."
echo "PostgreSQL Password:     ${POSTGRES_PASSWORD}"
echo "Guacamole DB Password:   ${GUAC_POSTGRES_PASSWORD}"
echo "GitLab Root Password:    ${GITLAB_ROOT_PASSWORD}"
echo "GitLab DB Password:      ${GITLAB_POSTGRES_PASSWORD}"
echo "Dashboard Password:      ${DASHBOARD_PASSWORD}"
echo ""
echo "📋 Nächste Schritte:"
echo "1. Überprüfen Sie die .env-Datei und passen Sie bei Bedarf Werte an"
echo "2. Für Produktions-Deployment: Domain-Settings auskommentieren und konfigurieren"
echo "3. Für API-Integration: Token für GitHub/GitLab/OpenProject hinzufügen"
echo "4. Starten Sie das System: python3 start-extended-stack.py --profile cpu"
echo ""
echo "🔗 Service-URLs nach dem Start:"
echo "- Guacamole Desktop: http://localhost:8080 (guacadmin/guacadmin)"
echo "- N8N Workflows:     http://localhost:5678"
echo "- Open WebUI:        http://localhost:3000"
echo "- AppFlowy:          http://localhost:8081"
echo "- AFFINE:            http://localhost:3010"
echo "- GitLab:            http://localhost:8082 (root/${GITLAB_ROOT_PASSWORD})"
echo ""
echo "💡 Tipp: Passwörter wurden auch in der .env-Datei gespeichert"

# Passwörter in separater Datei für Admin speichern
cat > .env.passwords << EOF
# GENERATED PASSWORDS - $(date)
# Diese Datei enthält alle generierten Passwörter für Admin-Zwecke

N8N_ENCRYPTION_KEY=${N8N_ENCRYPTION_KEY}
N8N_JWT_SECRET=${N8N_JWT_SECRET}
POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
JWT_SECRET=${JWT_SECRET}
WEBUI_SECRET_KEY=${WEBUI_SECRET_KEY}
GUAC_POSTGRES_PASSWORD=${GUAC_POSTGRES_PASSWORD}
GITLAB_ROOT_PASSWORD=${GITLAB_ROOT_PASSWORD}
GITLAB_POSTGRES_PASSWORD=${GITLAB_POSTGRES_PASSWORD}
WEBHOOK_SECRET=${WEBHOOK_SECRET}
DASHBOARD_PASSWORD=${DASHBOARD_PASSWORD}
CLICKHOUSE_PASSWORD=${CLICKHOUSE_PASSWORD}
MINIO_ROOT_PASSWORD=${MINIO_ROOT_PASSWORD}
LANGFUSE_SALT=${LANGFUSE_SALT}
NEXTAUTH_SECRET=${NEXTAUTH_SECRET}
ENCRYPTION_KEY=${ENCRYPTION_KEY}
SECRET_KEY_BASE=${SECRET_KEY_BASE}
VAULT_ENC_KEY=${VAULT_ENC_KEY}
EOF

chmod 600 .env.passwords
echo "🔒 Passwörter auch in .env.passwords gespeichert (nur für Admin lesbar)"
echo ""
echo "🚀 Setup bereit! Führen Sie jetzt './setup-extended-ai-stack.sh' aus."
