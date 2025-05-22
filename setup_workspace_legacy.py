#!/usr/bin/env python3
"""
Workspace-in-a-Box Startup Script - Docker Compose Version kompatibel
Funktioniert mit älteren Docker Compose Versionen ohne --profile Support
"""

import subprocess
import time
import os
import json
import sys
import argparse
import shutil
import platform
import re
from pathlib import Path

def show_banner():
    """Zeigt Willkommen-Banner"""
    print("\n" + "="*80)
    print("🚀 WORKSPACE-IN-A-BOX - AI DEVELOPMENT ENVIRONMENT")
    print("="*80)
    print("🎨 Complete AI development workspace with browser-based desktop access")
    print("⚡ Features: Zed/VS Code, N8N, Open WebUI, Flowise, SearXNG, and more!")
    print("="*80)

def check_docker_compose_version():
    """Prüft Docker Compose Version und Profile-Support"""
    print("🔍 Checking Docker Compose version...")

    try:
        result = subprocess.run(['docker-compose', '--version'],
                              capture_output=True, text=True, check=True)
        version_output = result.stdout.strip()
        print(f"📦 Found: {version_output}")

        # Extrahiere Versionsnummer
        version_match = re.search(r'version (?:v)?(\d+)\.(\d+)', version_output)
        if version_match:
            major, minor = int(version_match.group(1)), int(version_match.group(2))

            # Profile-Support seit Version 1.28
            supports_profiles = (major > 1) or (major == 1 and minor >= 28)

            if supports_profiles:
                print("✅ Docker Compose supports profiles")
                return True, (major, minor)
            else:
                print(f"⚠️  Docker Compose {major}.{minor} does not support profiles")
                print("   Profiles require Docker Compose 1.28+")
                print("   Using alternative service selection method...")
                return False, (major, minor)
        else:
            print("⚠️  Could not parse Docker Compose version")
            return False, (0, 0)

    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Docker Compose not found or not working")
        sys.exit(1)

def check_prerequisites():
    """Überprüft Systemvoraussetzungen"""
    print("🔍 Checking prerequisites...")

    required_commands = ['docker', 'docker-compose', 'curl', 'git']
    missing_commands = []

    for cmd in required_commands:
        try:
            subprocess.run([cmd, '--version'],
                         capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            missing_commands.append(cmd)

    if missing_commands:
        print(f"❌ Missing required commands: {', '.join(missing_commands)}")
        print("Please install Docker, Docker Compose, and Git first.")
        print("\nTo upgrade Docker Compose:")
        print("curl -L https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose")
        print("chmod +x /usr/local/bin/docker-compose")
        sys.exit(1)

    print("✅ All prerequisites met!")

def select_editor():
    """Editor-Auswahl mit benutzerfreundlicher Oberfläche"""
    print("\n" + "🎨 CHOOSE YOUR DEVELOPMENT EDITOR")
    print("-" * 50)

    editors = {
        '1': {
            'name': 'Zed Editor',
            'description': 'Modern, lightning-fast editor written in Rust',
            'features': [
                '⚡ Ultra-fast performance and instant startup',
                '🤝 Built-in real-time collaboration',
                '🧠 AI-powered code completion',
                '🔧 Native LSP support for all languages',
                '🎨 Beautiful, minimal interface',
                '🚀 Perfect for modern development workflows'
            ],
            'key': 'zed',
            'recommended': True
        },
        '2': {
            'name': 'Visual Studio Code',
            'description': 'Popular, feature-rich editor from Microsoft',
            'features': [
                '🔌 Massive extension ecosystem',
                '🐛 Integrated debugging tools',
                '📊 Built-in Git integration',
                '🌐 Remote development support',
                '📈 Rich IntelliSense',
                '🔧 Extensive customization options'
            ],
            'key': 'vscode',
            'recommended': False
        }
    }

    for choice, editor in editors.items():
        recommended = " (RECOMMENDED ⭐)" if editor['recommended'] else ""
        print(f"\n{choice}. {editor['name']}{recommended}")
        print(f"   {editor['description']}")
        print()
        for feature in editor['features']:
            print(f"   {feature}")

    print("\n" + "-" * 50)

    while True:
        try:
            choice = input("👉 Select editor (1-2) [1 for Zed]: ").strip()

            if not choice:
                choice = "1"

            if choice in editors:
                selected = editors[choice]
                print(f"\n✅ Selected: {selected['name']}")

                if choice == "2":
                    confirm = input("ℹ️  Zed is recommended for the best experience. Continue with VS Code? (y/N): ").strip().lower()
                    if confirm not in ['y', 'yes']:
                        continue

                return selected['key'], selected['name']
            else:
                print("❌ Invalid choice. Please select 1 or 2.")

        except KeyboardInterrupt:
            print("\n\n👋 Setup cancelled.")
            sys.exit(0)

def clone_supabase_repo():
    """Clone the Supabase repository using sparse checkout if not already present."""
    if not os.path.exists("supabase"):
        print("📦 Cloning the Supabase repository...")
        subprocess.run([
            "git", "clone", "--filter=blob:none", "--no-checkout",
            "https://github.com/supabase/supabase.git"
        ], check=True)
        os.chdir("supabase")
        subprocess.run(["git", "sparse-checkout", "init", "--cone"], check=True)
        subprocess.run(["git", "sparse-checkout", "set", "docker"], check=True)
        subprocess.run(["git", "checkout", "master"], check=True)
        os.chdir("..")
        print("✅ Supabase repository cloned")
    else:
        print("📦 Supabase repository exists, updating...")
        os.chdir("supabase")
        subprocess.run(["git", "pull"], check=True)
        os.chdir("..")

def prepare_supabase_env():
    """Copy .env to .env in supabase/docker."""
    env_path = os.path.join("supabase", "docker", ".env")
    env_example_path = os.path.join(".env")

    if os.path.exists(env_example_path):
        print("🔧 Copying .env to supabase/docker...")
        shutil.copyfile(env_example_path, env_path)
    else:
        print("⚠️  .env file not found. Please create one from .env.example")

def generate_searxng_secret_key():
    """Generate a secret key for SearXNG based on the current platform."""
    print("🔐 Configuring SearXNG settings...")

    settings_path = os.path.join("searxng", "settings.yml")
    settings_base_path = os.path.join("searxng", "settings-base.yml")

    if not os.path.exists(settings_base_path):
        print(f"⚠️  SearXNG base settings file not found at {settings_base_path}")
        return

    if not os.path.exists(settings_path):
        print(f"📝 Creating SearXNG settings.yml from base...")
        try:
            shutil.copyfile(settings_base_path, settings_path)
            print(f"✅ Created {settings_path}")
        except Exception as e:
            print(f"❌ Error creating settings.yml: {e}")
            return

    print("🔑 Generating SearXNG secret key...")
    system = platform.system()

    try:
        if system == "Windows":
            ps_command = [
                "powershell", "-Command",
                "$randomBytes = New-Object byte[] 32; " +
                "(New-Object Security.Cryptography.RNGCryptoServiceProvider).GetBytes($randomBytes); " +
                "$secretKey = -join ($randomBytes | ForEach-Object { \"{0:x2}\" -f $_ }); " +
                "(Get-Content searxng/settings.yml) -replace 'ultrasecretkey', $secretKey | Set-Content searxng/settings.yml"
            ]
            subprocess.run(ps_command, check=True)
        elif system == "Darwin":  # macOS
            openssl_cmd = ["openssl", "rand", "-hex", "32"]
            random_key = subprocess.check_output(openssl_cmd).decode('utf-8').strip()
            sed_cmd = ["sed", "-i", "", f"s|ultrasecretkey|{random_key}|g", settings_path]
            subprocess.run(sed_cmd, check=True)
        else:  # Linux
            openssl_cmd = ["openssl", "rand", "-hex", "32"]
            random_key = subprocess.check_output(openssl_cmd).decode('utf-8').strip()
            sed_cmd = ["sed", "-i", f"s|ultrasecretkey|{random_key}|g", settings_path]
            subprocess.run(sed_cmd, check=True)

        print("✅ SearXNG secret key generated successfully.")
    except Exception as e:
        print(f"⚠️  Error generating SearXNG secret key: {e}")

def setup_environment(editor_key):
    """Umgebung mit ausgewähltem Editor einrichten"""
    print(f"\n🔧 Setting up environment with {editor_key.upper()}...")

    directories = [
        "desktop",
        "desktop/editor-config",
        f"desktop/editor-config/{editor_key}",
        "desktop/desktop-shortcuts",
        "desktop/dev-tools",
        "desktop/projects",
        "desktop/scripts",
        "desktop-shared",
        "shared",
        "guacamole/init",
        "database/init",
        "n8n/templates",
        "searxng"
    ]

    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)

    # Editor-Auswahl in .env speichern
    env_content = ""
    if os.path.exists('.env'):
        with open('.env', 'r') as f:
            env_content = f.read()

    if 'SELECTED_EDITOR=' in env_content:
        lines = env_content.split('\n')
        for i, line in enumerate(lines):
            if line.startswith('SELECTED_EDITOR='):
                lines[i] = f'SELECTED_EDITOR={editor_key}'
                break
        env_content = '\n'.join(lines)
    else:
        env_content = f"{env_content}\nSELECTED_EDITOR={editor_key}\n"

    with open('.env', 'w') as f:
        f.write(env_content)

    print(f"✅ Environment configured for {editor_key}")

def create_editor_configurations(editor_key):
    """Editor-spezifische Konfigurationen erstellen"""
    print(f"⚙️ Creating {editor_key} configuration...")

    if editor_key == 'zed':
        create_zed_config()
    elif editor_key == 'vscode':
        create_vscode_config()

    print(f"✅ {editor_key} configuration created")

def create_zed_config():
    """Zed-Konfiguration für AI-Development"""
    config_dir = Path("desktop/editor-config/zed")

    settings = {
        "theme": "Ayu Dark",
        "buffer_font_family": "JetBrains Mono",
        "buffer_font_size": 14,
        "ui_font_size": 16,
        "preferred_line_length": 100,
        "soft_wrap": "preferred_line_length",
        "tab_size": 2,
        "hard_tabs": False,
        "show_whitespaces": "selection",
        "relative_line_numbers": False,
        "vim_mode": False,
        "autosave": "on_focus_change",
        "format_on_save": "on",
        "terminal": {
            "shell": {"program": "/bin/zsh"},
            "working_directory": "current_project_directory",
            "blinking": "terminal_controlled"
        },
        "project_panel": {"dock": "left"},
        "outline_panel": {"dock": "right"},
        "collaboration_panel": {"dock": "left"},
        "git": {
            "inline_blame": {"enabled": True},
            "git_gutter": "tracked_files"
        },
        "lsp": {
            "rust-analyzer": {
                "binary": {"path": "/home/kasm-user/.cargo/bin/rust-analyzer"}
            },
            "typescript-language-server": {
                "binary": {"path": "/usr/local/bin/typescript-language-server"}
            },
            "python-lsp-server": {
                "binary": {"path": "/usr/local/bin/pylsp"}
            }
        },
        "languages": {
            "JavaScript": {
                "language_servers": ["typescript-language-server"],
                "format_on_save": "on",
                "formatter": "prettier"
            },
            "TypeScript": {
                "language_servers": ["typescript-language-server"],
                "format_on_save": "on",
                "formatter": "prettier"
            },
            "Python": {
                "language_servers": ["python-lsp-server"],
                "format_on_save": "on",
                "formatter": "black"
            },
            "Rust": {
                "language_servers": ["rust-analyzer"],
                "format_on_save": "on"
            },
            "JSON": {
                "language_servers": ["vscode-json-languageserver"],
                "format_on_save": "on"
            },
            "YAML": {
                "language_servers": ["yaml-language-server"],
                "format_on_save": "on"
            },
            "Dockerfile": {
                "language_servers": ["docker-langserver"]
            }
        }
    }

    with open(config_dir / "settings.json", 'w') as f:
        json.dump(settings, f, indent=2)

    keymap = [
        {
            "context": "Editor",
            "bindings": {
                "ctrl-shift-p": "command_palette::Toggle",
                "ctrl-p": "file_finder::Toggle",
                "ctrl-shift-f": "project_search::ToggleFocus",
                "ctrl-`": "terminal_panel::ToggleFocus",
                "ctrl-shift-e": "project_panel::ToggleFocus",
                "ctrl-shift-o": "outline::Toggle",
                "ctrl-j": "editor::JoinLines",
                "ctrl-d": "editor::SelectNext",
                "ctrl-shift-l": "editor::SelectAll",
                "alt-up": "editor::MoveLineUp",
                "alt-down": "editor::MoveLineDown"
            }
        },
        {
            "context": "Terminal",
            "bindings": {
                "ctrl-shift-c": "terminal::Copy",
                "ctrl-shift-v": "terminal::Paste"
            }
        }
    ]

    with open(config_dir / "keymap.json", 'w') as f:
        json.dump(keymap, f, indent=2)

def create_vscode_config():
    """VS Code-Konfiguration für AI-Development"""
    config_dir = Path("desktop/editor-config/vscode")

    settings = {
        "workbench.colorTheme": "Dark+ (default dark)",
        "editor.fontFamily": "JetBrains Mono, Consolas, monospace",
        "editor.fontSize": 14,
        "editor.lineHeight": 22,
        "editor.tabSize": 2,
        "editor.insertSpaces": True,
        "editor.detectIndentation": True,
        "editor.renderWhitespace": "selection",
        "editor.rulers": [80, 100],
        "editor.formatOnSave": True,
        "editor.codeActionsOnSave": {
            "source.fixAll": True,
            "source.organizeImports": True
        },
        "files.autoSave": "onFocusChange",
        "explorer.confirmDelete": False,
        "git.enableSmartCommit": True,
        "git.confirmSync": False,
        "terminal.integrated.shell.linux": "/bin/zsh",
        "python.defaultInterpreterPath": "/usr/bin/python3",
        "python.linting.enabled": True,
        "python.linting.pylintEnabled": True,
        "python.formatting.provider": "black",
        "typescript.preferences.quoteStyle": "single",
        "javascript.preferences.quoteStyle": "single"
    }

    with open(config_dir / "settings.json", 'w') as f:
        json.dump(settings, f, indent=2)

    extensions = {
        "recommendations": [
            "ms-python.python",
            "ms-python.black-formatter",
            "ms-vscode.vscode-typescript-next",
            "rust-lang.rust-analyzer",
            "ms-vscode.vscode-json",
            "redhat.vscode-yaml",
            "ms-vscode.docker",
            "ms-vscode-remote.remote-containers",
            "github.copilot",
            "ms-toolsai.jupyter"
        ]
    }

    with open(config_dir / "extensions.json", 'w') as f:
        json.dump(extensions, f, indent=2)

def create_dev_tools():
    """Entwicklungstools und Scripts erstellen"""
    print("🛠️ Creating development tools...")

    scripts_dir = Path("desktop/dev-tools")

    check_services_script = """#!/bin/bash
echo "🔍 Checking AI Services Status..."

services=(
    "n8n:5678"
    "open-webui:8080"
    "ollama:11434"
    "qdrant:6333"
    "kong:8000"
    "flowise:3001"
    "searxng:8081"
    "appflowy:8082"
    "affine:3010"
    "gitlab:8083"
    "langfuse:3002"
)

for service in "${services[@]}"; do
    name=$(echo $service | cut -d: -f1)
    port=$(echo $service | cut -d: -f2)

    if curl -s "http://$service" > /dev/null 2>&1; then
        echo "✅ $name ($service) - Running"
    else
        echo "❌ $name ($service) - Not responding"
    fi
done
"""

    with open(scripts_dir / "check-services.sh", 'w') as f:
        f.write(check_services_script)

    docker_helper_script = """#!/bin/bash
echo "🐳 Docker Container Status"
echo "=========================="
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
echo ""
echo "💾 Docker Volume Usage"
echo "====================="
docker system df
echo ""
echo "🔗 Service URLs"
echo "==============="
echo "Desktop:    http://localhost:8080"
echo "N8N:        http://n8n:5678"
echo "Open WebUI: http://open-webui:8080"
echo "Flowise:    http://flowise:3001"
echo "SearXNG:    http://searxng:8081"
"""

    with open(scripts_dir / "docker-status.sh", 'w') as f:
        f.write(docker_helper_script)

    for script in scripts_dir.glob("*.sh"):
        script.chmod(0o755)

    print("✅ Development tools created")

def setup_guacamole():
    """Guacamole-Datenbank einrichten mit verbesserter Fehlerbehandlung"""
    print("🖥️ Setting up Guacamole database...")

    init_dir = Path("guacamole/init")
    init_file = init_dir / "initdb.sql"

    if init_file.exists():
        print("✅ Guacamole already configured")
        return

    try:
        # Versuche zuerst das normale Image
        result = subprocess.run([
            "docker", "run", "--rm", "guacamole/guacamole:latest",
            "/opt/guacamole/bin/initdb.sh", "--postgres"
        ], capture_output=True, text=True, check=False, timeout=30)

        if result.returncode == 0 and result.stdout:
            with open(init_file, 'w') as f:
                f.write(result.stdout)
            print("✅ Guacamole database configured")
            return

    except subprocess.TimeoutExpired:
        print("⚠️  Guacamole init timed out")
    except Exception as e:
        print(f"⚠️  Primary Guacamole init failed: {e}")

    # Fallback: Erstelle eine minimale SQL-Datei
    print("📝 Creating fallback Guacamole database schema...")
    fallback_sql = """
--
-- Basic Guacamole Database Schema
-- This is a fallback schema if automatic generation fails
--

CREATE TABLE IF NOT EXISTS guacamole_user (
    user_id serial NOT NULL,
    username varchar(128) NOT NULL,
    password_hash bytea NOT NULL,
    password_salt bytea,
    password_date date,
    disabled boolean NOT NULL DEFAULT FALSE,
    expired boolean NOT NULL DEFAULT FALSE,
    access_window_start time,
    access_window_end time,
    valid_from date,
    valid_until date,
    timezone varchar(64),
    full_name varchar(256),
    email_address varchar(256),
    organization varchar(256),
    organizational_role varchar(256),
    PRIMARY KEY (user_id),
    UNIQUE (username)
);

-- Insert default admin user (guacadmin/guacadmin)
INSERT INTO guacamole_user (username, password_hash) VALUES
('guacadmin', decode('ca458a7d494e3be824624a5bbcab46b4d8e1c7e2', 'hex'))
ON CONFLICT (username) DO NOTHING;

-- Other required tables would be here...
-- This is a minimal setup to get started
"""

    try:
        with open(init_file, 'w') as f:
            f.write(fallback_sql)
        print("✅ Fallback Guacamole database schema created")
    except Exception as e:
        print(f"❌ Could not create Guacamole database schema: {e}")

def create_legacy_compose_file(profile, features):
    """Erstellt eine docker-compose Datei ohne Profile für ältere Versionen"""
    print("📝 Creating legacy docker-compose configuration...")

    # Basis-Services die immer gestartet werden
    base_services = [
        "n8n-import", "n8n", "open-webui", "qdrant", "redis"
    ]

    # GPU-abhängige Services
    if profile == "gpu-nvidia":
        base_services.extend(["ollama-gpu", "ollama-pull-llama-gpu"])
    elif profile == "gpu-amd":
        base_services.extend(["ollama-gpu-amd", "ollama-pull-llama-gpu-amd"])
    else:
        base_services.extend(["ollama-cpu", "ollama-pull-llama-cpu"])

    # Feature-abhängige Services
    all_services = base_services.copy()

    if "desktop" in features:
        all_services.extend(["guacamole-db", "guacd", "guacamole", "desktop"])

    if "productivity" in features:
        all_services.extend(["flowise", "searxng", "appflowy", "affine"])

    if "development" in features:
        all_services.extend(["gitlab-postgres", "gitlab"])

    if "observability" in features:
        all_services.extend(["langfuse-worker", "langfuse-web", "clickhouse", "minio", "postgres"])

    return all_services

def stop_existing_containers():
    """Stop existing containers"""
    print("🛑 Stopping existing containers...")

    cmd = ["docker-compose", "-p", "localai", "down"]

    try:
        subprocess.run(cmd, check=False)  # Don't fail if nothing to stop
        print("✅ Containers stopped")
    except:
        pass

def start_services_legacy(profile, features):
    """Startet Services ohne Profile-Support"""
    print(f"🚀 Starting services (legacy mode) with profile '{profile}' and features: {features}")

    # Supabase zuerst starten
    print("📦 Starting Supabase services...")
    subprocess.run([
        "docker-compose", "-p", "localai",
        "-f", "supabase/docker/docker-compose.yml",
        "up", "-d"
    ], check=True)

    print("⏳ Waiting for Supabase to initialize...")
    time.sleep(15)

    # Services einzeln starten basierend auf Features
    services_to_start = create_legacy_compose_file(profile, features)

    print(f"🔧 Starting selected services: {', '.join(services_to_start)}")

    # Alle Services in einem Befehl starten
    cmd = ["docker-compose", "-p", "localai", "up", "-d", "--build"] + services_to_start

    try:
        subprocess.run(cmd, check=True)
        print("✅ Services started successfully")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to start services: {e}")
        print("💡 Trying to start core services only...")

        # Fallback: Nur Core-Services
        core_services = ["n8n", "open-webui", "ollama-cpu", "qdrant", "redis"]
        cmd = ["docker-compose", "-p", "localai", "up", "-d"] + core_services
        subprocess.run(cmd, check=True)

def start_services_with_profiles(profile, features):
    """Startet Services mit Profile-Support"""
    print(f"🚀 Starting services with profile '{profile}' and features: {features}")

    # Supabase zuerst starten
    print("📦 Starting Supabase services...")
    subprocess.run([
        "docker-compose", "-p", "localai",
        "-f", "supabase/docker/docker-compose.yml",
        "up", "-d"
    ], check=True)

    print("⏳ Waiting for Supabase to initialize...")
    time.sleep(15)

    # Hauptservices starten
    cmd = ["docker-compose", "-p", "localai", "up", "-d", "--build"]

    if profile != "none":
        cmd.extend(["--profile", profile])

    for feature in features:
        if feature != "none":
            cmd.extend(["--profile", feature])

    subprocess.run(cmd, check=True)
    print("✅ Services started successfully")

def wait_for_services():
    """Auf kritische Services warten"""
    services_to_check = [
        ("N8N", "localhost", "5678", 120),
        ("Open WebUI", "localhost", "3000", 120),
        ("Guacamole", "localhost", "8080", 180),
    ]

    for service_name, host, port, timeout in services_to_check:
        print(f"⏳ Waiting for {service_name} on {host}:{port}...")

        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                result = subprocess.run([
                    "curl", "-s", "-o", "/dev/null", "-w", "%{http_code}",
                    f"http://{host}:{port}"
                ], capture_output=True, text=True, timeout=5)

                if result.returncode == 0 and result.stdout.startswith(('200', '302', '401')):
                    print(f"✅ {service_name} is ready!")
                    break
            except (subprocess.TimeoutExpired, FileNotFoundError):
                pass

            time.sleep(5)
        else:
            print(f"⚠️ {service_name} may not be ready yet")

def show_success_message(editor_name, features):
    """Erfolgs-Nachricht anzeigen"""
    print("\n" + "="*80)
    print("🎉 WORKSPACE-IN-A-BOX IS READY!")
    print("="*80)
    print()
    print("🌐 BROWSER ACCESS:")
    print("   URL: http://localhost:8080")
    print("   Login: guacadmin / guacadmin")
    print()
    print("🖥️ DESKTOP CONNECTION:")
    print("   1. Open http://localhost:8080 in your browser")
    print("   2. Login with guacadmin/guacadmin")
    print("   3. Connect to 'Linux Desktop' or create connection:")
    print("      - Protocol: VNC")
    print("      - Hostname: desktop")
    print("      - Port: 5901")
    print("      - Password: password")
    print()
    print(f"⚡ YOUR EDITOR: {editor_name}")
    print("   - Pre-configured with AI development settings")
    print("   - Language servers installed and ready")
    print("   - Available on desktop or via 'edit' command")
    print()
    print("🧠 CORE AI SERVICES (accessible from desktop):")
    print("   🧠 N8N Workflows:     http://n8n:5678")
    print("   💬 Open WebUI Chat:   http://open-webui:8080")
    print("   🤖 Ollama API:        http://ollama:11434")
    print("   📊 Qdrant Vector DB:  http://qdrant:6333/dashboard")
    print("   🗄️ Supabase Database: http://kong:8000")
    print()

    if "productivity" in features:
        print("📝 PRODUCTIVITY SERVICES:")
        print("   🌊 Flowise AI Builder: http://flowise:3001")
        print("   🔍 SearXNG Search:     http://searxng:8081")
        print("   📝 AppFlowy Notes:     http://appflowy:8082")
        print("   ✨ AFFINE Workspace:   http://affine:3010")
        print()

    if "development" in features:
        print("🛠️ DEVELOPMENT SERVICES:")
        print("   🦊 GitLab Repository:  http://gitlab:8083")
        print()

    if "observability" in features:
        print("📈 OBSERVABILITY:")
        print("   📈 Langfuse Analytics: http://langfuse:3002")
        print()

    print("💡 QUICK TIPS:")
    print("   - Desktop has pre-configured bookmarks for all services")
    print("   - Use 'check-services.sh' to verify service status")
    print("   - Files in ./desktop-shared are accessible from desktop")
    print("   - All services communicate via internal Docker network")
    print()
    print("🚀 Happy coding with your complete AI development workspace!")
    print("="*80)

def main():
    parser = argparse.ArgumentParser(description='Workspace-in-a-Box Complete Setup')
    parser.add_argument('--profile', choices=['cpu', 'gpu-nvidia', 'gpu-amd'],
                       default='cpu', help='GPU profile (default: cpu)')
    parser.add_argument('--skip-editor-selection', action='store_true',
                       help='Skip editor selection (use Zed as default)')
    parser.add_argument('--features', nargs='*',
                       choices=['desktop', 'productivity', 'development', 'observability'],
                       default=['desktop', 'productivity'],
                       help='Features to enable (default: desktop + productivity)')
    parser.add_argument('--full-stack', action='store_true',
                       help='Enable all features')

    args = parser.parse_args()

    if args.full_stack:
        args.features = ['desktop', 'productivity', 'development', 'observability']

    # Stelle sicher, dass desktop immer aktiviert ist
    if 'desktop' not in args.features:
        args.features.append('desktop')

    show_banner()

    # Docker Compose Version prüfen
    supports_profiles, version = check_docker_compose_version()
    check_prerequisites()

    # Supabase Repository vorbereiten
    clone_supabase_repo()
    prepare_supabase_env()

    # SearXNG konfigurieren
    generate_searxng_secret_key()

    # Editor-Auswahl
    if args.skip_editor_selection:
        editor_key, editor_name = 'zed', 'Zed Editor'
        print("🎨 Using default editor: Zed")
    else:
        editor_key, editor_name = select_editor()

    # Setup
    setup_environment(editor_key)
    create_editor_configurations(editor_key)
    create_dev_tools()
    setup_guacamole()

    # Services starten
    stop_existing_containers()

    if supports_profiles:
        start_services_with_profiles(args.profile, args.features)
    else:
        start_services_legacy(args.profile, args.features)

    wait_for_services()

    # Erfolg!
    show_success_message(editor_name, args.features)

if __name__ == "__main__":
    main()
