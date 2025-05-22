#!/bin/bash
# setup-extended-ai-stack.sh - Setup-Skript für das erweiterte AI-Stack

echo "🚀 Setting up Extended AI Stack with Guacamole Desktop..."

# Verzeichnisse erstellen
mkdir -p init-guacamole
mkdir -p desktop-shared
mkdir -p shared
mkdir -p supabase/docker/volumes/db
mkdir -p gitlab-db

# Guacamole Datenbank-Initialisierung
echo "📊 Preparing Guacamole database initialization..."
docker run --rm guacamole/guacamole /opt/guacamole/bin/initdb.sh --postgres > init-guacamole/initdb.sql

echo "Created Guacamole database initialization script"

# .env Datei erweitern
cat > .env.extended << 'EOF'
# ========================================
# EXTENDED AI STACK CONFIGURATION
# ========================================

# N8N Configuration (original)
N8N_ENCRYPTION_KEY=your_n8n_encryption_key_here
N8N_USER_MANAGEMENT_JWT_SECRET=your_jwt_secret_here

# Supabase Secrets (original)
POSTGRES_PASSWORD=your_secure_postgres_password
JWT_SECRET=your_jwt_secret_for_supabase
ANON_KEY=your_anon_key
SERVICE_ROLE_KEY=your_service_role_key
DASHBOARD_USERNAME=supabase
DASHBOARD_PASSWORD=your_dashboard_password
POOLER_TENANT_ID=tenant_id

# Langfuse credentials (original)
CLICKHOUSE_PASSWORD=clickhouse_password
MINIO_ROOT_PASSWORD=minio_password
LANGFUSE_SALT=langfuse_salt
NEXTAUTH_SECRET=nextauth_secret
ENCRYPTION_KEY=encryption_key

# Caddy Config (original)
N8N_HOSTNAME=n8n.localhost
WEBUI_HOSTNAME=webui.localhost
FLOWISE_HOSTNAME=flowise.localhost
SUPABASE_HOSTNAME=supabase.localhost
OLLAMA_HOSTNAME=ollama.localhost
SEARXNG_HOSTNAME=searxng.localhost
LETSENCRYPT_EMAIL=your-email@example.com

# Additional Supabase Settings
API_EXTERNAL_URL=http://localhost:8000
SITE_URL=http://localhost:3000
ADDITIONAL_REDIRECT_URLS=""
DISABLE_SIGNUP=false
ENABLE_EMAIL_SIGNUP=true
ENABLE_EMAIL_AUTOCONFIRM=false
ENABLE_ANONYMOUS_USERS=false
ENABLE_PHONE_SIGNUP=false
ENABLE_PHONE_AUTOCONFIRM=false
JWT_EXPIRY=3600
SMTP_ADMIN_EMAIL=""
SMTP_HOST=""
SMTP_PORT=587
SMTP_USER=""
SMTP_PASS=""
SMTP_SENDER_NAME=""
MAILER_URLPATHS_INVITE=/auth/v1/verify
MAILER_URLPATHS_CONFIRMATION=/auth/v1/verify
MAILER_URLPATHS_RECOVERY=/auth/v1/verify
MAILER_URLPATHS_EMAIL_CHANGE=/auth/v1/verify

# Extended Services Configuration
WEBUI_SECRET_KEY=your_webui_secret_key

# Desktop Environment Settings
DESKTOP_USER=kasm-user
DESKTOP_PASSWORD=password
VNC_PASSWORD=password

# Service URLs (internal)
GUACAMOLE_URL=http://localhost:8080
DESKTOP_VNC_URL=http://desktop:6901
APPFLOWY_URL=http://localhost:8081
AFFINE_URL=http://localhost:3010
GITLAB_URL=http://localhost:8082
N8N_EXTENDED_URL=http://localhost:5679
EOF

# Caddyfile für Reverse Proxy erstellen
cat > Caddyfile << 'EOF'
# Caddyfile für Extended AI Stack

{
    auto_https off
    local_certs
}

# N8N
n8n.localhost {
    reverse_proxy n8n:5678
}

# Open WebUI
webui.localhost {
    reverse_proxy open-webui:8080
}

# Guacamole
guac.localhost {
    reverse_proxy guacamole:8080
}

# AppFlowy
appflowy.localhost {
    reverse_proxy appflowy:8080
}

# AFFINE
affine.localhost {
    reverse_proxy affine:3010
}

# GitLab
gitlab.localhost {
    reverse_proxy gitlab:8082
}

# N8N Extended
n8n-ext.localhost {
    reverse_proxy n8n-extended:5678
}

# Supabase
supabase.localhost {
    reverse_proxy kong:8000
}

# Ollama
ollama.localhost {
    reverse_proxy ollama:11434
}

# Qdrant
qdrant.localhost {
    reverse_proxy qdrant:6333
}
EOF

# Start-Skript für erweiterten Stack
cat > start-extended-stack.py << 'EOF'
#!/usr/bin/env python3
"""
Extended AI Stack Startup Script
Erweitert das original local-ai-packaged Setup um zusätzliche Services
"""

import subprocess
import sys
import argparse
import time
import os

def run_command(command, check=True):
    """Run a shell command"""
    print(f"🔄 Running: {command}")
    try:
        result = subprocess.run(command, shell=True, check=check, capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        return result
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running command: {e}")
        if e.stderr:
            print(e.stderr)
        return None

def wait_for_service(service_name, port, timeout=120):
    """Wait for a service to be ready"""
    print(f"⏳ Waiting for {service_name} to be ready on port {port}...")
    start_time = time.time()
    while time.time() - start_time < timeout:
        result = run_command(f"curl -s http://localhost:{port} > /dev/null", check=False)
        if result and result.returncode == 0:
            print(f"✅ {service_name} is ready!")
            return True
        time.sleep(5)
    print(f"❌ {service_name} failed to start within {timeout} seconds")
    return False

def main():
    parser = argparse.ArgumentParser(description='Start Extended AI Stack')
    parser.add_argument('--profile', 
                       choices=['cpu', 'gpu-nvidia', 'gpu-amd', 'none'], 
                       default='cpu',
                       help='GPU profile to use')
    parser.add_argument('--services', 
                       choices=['all', 'core', 'desktop', 'extended'], 
                       default='all',
                       help='Which services to start')
    
    args = parser.parse_args()
    
    print("🚀 Starting Extended AI Stack...")
    print(f"📊 Profile: {args.profile}")
    print(f"🔧 Services: {args.services}")
    
    # Check if .env file exists
    if not os.path.exists('.env'):
        if os.path.exists('.env.extended'):
            print("📋 Copying .env.extended to .env")
            run_command("cp .env.extended .env")
        else:
            print("❌ No .env file found. Please create one based on .env.extended")
            sys.exit(1)
    
    # Generate Guacamole DB init if not exists
    if not os.path.exists('init-guacamole/initdb.sql'):
        print("📊 Generating Guacamole database initialization...")
        run_command("docker run --rm guacamole/guacamole /opt/guacamole/bin/initdb.sh --postgres > init-guacamole/initdb.sql")
    
    # Start services based on selection
    compose_files = "-f docker-compose-extended.yml"
    
    if args.services in ['all', 'core']:
        print("🔄 Starting core AI services...")
        run_command(f"docker-compose -p extended-ai {compose_files} --profile {args.profile} up -d n8n ollama qdrant open-webui")
        
        # Wait for core services
        wait_for_service("N8N", 5678)
        wait_for_service("Ollama", 11434)
        wait_for_service("Open WebUI", 3000)
    
    if args.services in ['all', 'desktop']:
        print("🖥️ Starting desktop and Guacamole services...")
        run_command(f"docker-compose -p extended-ai {compose_files} up -d guac-postgres guacd guacamole desktop")
        
        # Wait for desktop services
        wait_for_service("Guacamole", 8080)
        wait_for_service("Desktop", 6901)
    
    if args.services in ['all', 'extended']:
        print("🔧 Starting extended services...")
        run_command(f"docker-compose -p extended-ai {compose_files} up -d appflowy affine gitlab redis n8n-extended")
        
        # Wait for extended services
        wait_for_service("AppFlowy", 8081)
        wait_for_service("AFFINE", 3010)
        # GitLab takes longer to start
        wait_for_service("GitLab", 8082, timeout=300)
    
    if args.services == 'all':
        print("🌐 Starting reverse proxy...")
        run_command(f"docker-compose -p extended-ai {compose_files} up -d caddy")
    
    print("\n" + "="*60)
    print("🎉 Extended AI Stack is now running!")
    print("="*60)
    print("\n📋 Service URLs:")
    print("🖥️  Guacamole Desktop:    http://localhost:8080")
    print("🧠 N8N Workflow:         http://localhost:5678")
    print("💬 Open WebUI:           http://localhost:3000")
    print("🤖 Ollama API:           http://localhost:11434")
    print("📊 Qdrant:               http://localhost:6333")
    print("📝 AppFlowy:             http://localhost:8081")
    print("✨ AFFINE:               http://localhost:3010")
    print("🦊 GitLab:               http://localhost:8082")
    print("🔧 N8N Extended:         http://localhost:5679")
    print("🗄️  Supabase:            http://localhost:8000")
    print("\n🖥️  Desktop VNC (direct): http://localhost:6901")
    print("\n🔑 Default Credentials:")
    print("   Guacamole:     guacadmin / guacadmin")
    print("   Desktop VNC:   kasm-user / password")
    print("   GitLab:        root / (check container logs)")
    print("\n📁 Shared Folders:")
    print("   Desktop:       ./desktop-shared")
    print("   N8N:          ./shared")
    
    print("\n🚀 Setup Complete! Access your services using the URLs above.")
    print("💡 Tip: Configure Guacamole connections to access desktop and services")

if __name__ == '__main__':
    main()
EOF

# Guacamole Verbindungs-Konfigurationsskript
cat > configure-guacamole.sh << 'EOF'
#!/bin/bash
# configure-guacamole.sh - Konfiguration für Guacamole-Verbindungen

echo "🔧 Configuring Guacamole connections..."

# Warten bis Guacamole bereit ist
echo "⏳ Waiting for Guacamole to be ready..."
while ! curl -s http://localhost:8080/guacamole > /dev/null; do
    sleep 5
done

echo "✅ Guacamole is ready!"

echo "🖥️ Desktop Connection Configuration:"
echo "   Protocol: VNC"
echo "   Hostname: desktop"
echo "   Port: 5901"
echo "   Password: password"
echo ""
echo "📝 To configure manually:"
echo "1. Go to http://localhost:8080/guacamole"
echo "2. Login with guacadmin/guacadmin"
echo "3. Go to Settings > Connections"
echo "4. Create New Connection:"
echo "   - Name: Linux Desktop"
echo "   - Protocol: VNC"
echo "   - Hostname: desktop"
echo "   - Port: 5901"
echo "   - Password: password"
echo "5. Save and connect!"

echo ""
echo "🌐 Service URLs accessible from desktop:"
echo "   - N8N: http://n8n:5678"
echo "   - Open WebUI: http://open-webui:8080"
echo "   - AppFlowy: http://appflowy:8080"
echo "   - AFFINE: http://affine:3010"
echo "   - GitLab: http://gitlab:8082"
echo "   - Supabase: http://kong:8000"
EOF

# Berechtigungen setzen
chmod +x start-extended-stack.py
chmod +x configure-guacamole.sh

echo "✅ Setup complete!"
echo ""
echo "📋 Next steps:"
echo "1. Copy .env.extended to .env and configure your secrets"
echo "2. Run: python3 start-extended-stack.py --profile cpu"
echo "3. Run: ./configure-guacamole.sh for connection setup"
echo ""
echo "🚀 Your extended AI stack will be ready to use!"
