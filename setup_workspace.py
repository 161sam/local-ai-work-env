#!/usr/bin/env python3
"""
Workspace-in-a-Box Startup Script mit Editor-Auswahl
Vollständige Integration von Zed-Editor und VS Code
"""

import subprocess
import time
import os
import json
import sys
import argparse
from pathlib import Path

def show_banner():
    """Zeigt Willkommen-Banner"""
    print("\n" + "="*80)
    print("🚀 WORKSPACE-IN-A-BOX - AI DEVELOPMENT ENVIRONMENT")
    print("="*80)
    print("🎨 Modern AI development workspace with browser-based desktop access")
    print("⚡ Featuring Zed Editor, VS Code, N8N, Open WebUI, and more!")
    print("="*80)

def check_prerequisites():
    """Überprüft Systemvoraussetzungen"""
    print("🔍 Checking prerequisites...")

    required_commands = ['docker', 'docker-compose', 'curl']
    missing_commands = []

    for cmd in required_commands:
        try:
            subprocess.run([cmd, '--version'],
                         capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            missing_commands.append(cmd)

    if missing_commands:
        print(f"❌ Missing required commands: {', '.join(missing_commands)}")
        print("Please install Docker and Docker Compose first.")
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

            if not choice:  # Default zu Zed
                choice = "1"

            if choice in editors:
                selected = editors[choice]
                print(f"\n✅ Selected: {selected['name']}")

                # Bestätigung für VS Code (da Zed empfohlen wird)
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

def setup_environment(editor_key):
    """Umgebung mit ausgewähltem Editor einrichten"""
    print(f"\n🔧 Setting up environment with {editor_key.upper()}...")

    # Verzeichnisse erstellen
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
        "n8n/templates"
    ]

    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"📁 Created: {directory}")

    # Editor-Auswahl in Umgebungsvariable speichern
    env_content = ""
    if os.path.exists('.env'):
        with open('.env', 'r') as f:
            env_content = f.read()

    # SELECTED_EDITOR hinzufügen oder aktualisieren
    if 'SELECTED_EDITOR=' in env_content:
        # Existierende Zeile ersetzen
        lines = env_content.split('\n')
        for i, line in enumerate(lines):
            if line.startswith('SELECTED_EDITOR='):
                lines[i] = f'SELECTED_EDITOR={editor_key}'
                break
        env_content = '\n'.join(lines)
    else:
        # Neue Zeile hinzufügen
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

    # Zed Settings
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

    # Keymap
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

    # Service-Status-Checker
    check_services_script = """#!/bin/bash
echo "🔍 Checking AI Services Status..."

services=(
    "n8n:5678"
    "open-webui:8080"
    "ollama:11434"
    "qdrant:6333"
    "kong:8000"
    "appflowy:8080"
    "affine:3010"
    "gitlab:8082"
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

    # Docker-Helper
    docker_helper_script = """#!/bin/bash
echo "🐳 Docker Container Status"
echo "=========================="
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
echo ""
echo "💾 Docker Volume Usage"
echo "====================="
docker system df
"""

    with open(scripts_dir / "docker-status.sh", 'w') as f:
        f.write(docker_helper_script)

    # Alle Scripts ausführbar machen
    for script in scripts_dir.glob("*.sh"):
        script.chmod(0o755)

    print("✅ Development tools created")

def setup_guacamole():
    """Guacamole-Datenbank einrichten"""
    print("🖥️ Setting up Guacamole database...")

    init_file = Path("guacamole/init/initdb.sql")
    if init_file.exists():
        print("✅ Guacamole already configured")
        return

    try:
        result = subprocess.run([
            "docker", "run", "--rm", "guacamole/guacamole:latest",
            "/opt/guacamole/bin/initdb.sh", "--postgres"
        ], capture_output=True, text=True, check=True)

        with open(init_file, 'w') as f:
            f.write(result.stdout)

        print("✅ Guacamole database configured")
    except subprocess.CalledProcessError as e:
        print(f"⚠️ Could not configure Guacamole automatically: {e}")

def start_services(profile, features):
    """Services mit Docker Compose starten"""
    print(f"🚀 Starting services with profile '{profile}' and features: {features}")

    cmd = ["docker-compose", "up", "-d", "--build"]

    if profile != "none":
        cmd.extend(["--profile", profile])

    for feature in features:
        cmd.extend(["--profile", feature])

    try:
        subprocess.run(cmd, check=True)
        print("✅ Services started successfully")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to start services: {e}")
        sys.exit(1)

def wait_for_services():
    """Auf kritische Services warten"""
    services = [
        ("Guacamole", "localhost:8080", 180),
        ("N8N", "n8n", "5678", 120),
        ("Open WebUI", "open-webui", "8080", 120),
    ]

    for service_name, host, port, timeout in services:
        print(f"⏳ Waiting for {service_name}...")

        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                if host == "localhost":
                    url = f"http://{host}:{port}"
                else:
                    # Internal service check via docker exec
                    result = subprocess.run([
                        "docker", "exec", host, "curl", "-s", "-o", "/dev/null",
                        "-w", "%{http_code}", f"http://localhost:{port}"
                    ], capture_output=True, text=True, timeout=5)

                    if result.returncode == 0 and result.stdout.startswith(('200', '302', '401')):
                        print(f"✅ {service_name} is ready!")
                        break
            except (subprocess.TimeoutExpired, FileNotFoundError):
                pass

            time.sleep(5)
        else:
            print(f"⚠️ {service_name} may not be ready yet")

def show_success_message(editor_name):
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
    print("🧠 AI SERVICES (accessible from desktop):")
    print("   🧠 N8N Workflows:     http://n8n:5678")
    print("   💬 Open WebUI Chat:   http://open-webui:8080")
    print("   📝 AppFlowy Notes:    http://appflowy:8080")
    print("   ✨ AFFINE Workspace:  http://affine:3010")
    print("   🦊 GitLab Repository: http://gitlab:8082")
    print("   🗄️ Supabase Database: http://kong:8000")
    print("   📊 Qdrant Vector DB:  http://qdrant:6333/dashboard")
    print("   🤖 Ollama API:        http://ollama:11434")
    print()
    print("💡 QUICK TIPS:")
    print("   - Desktop has pre-configured bookmarks for all services")
    print("   - Use 'check-services.sh' to verify service status")
    print("   - Files in ./desktop-shared are accessible from desktop")
    print("   - All services communicate via internal Docker network")
    print()
    print("🚀 Happy coding with your new AI development workspace!")
    print("="*80)

def main():
    parser = argparse.ArgumentParser(description='Workspace-in-a-Box Setup')
    parser.add_argument('--profile', choices=['cpu', 'gpu-nvidia', 'gpu-amd'],
                       default='cpu', help='GPU profile')
    parser.add_argument('--skip-editor-selection', action='store_true',
                       help='Skip editor selection (use Zed as default)')
    parser.add_argument('--features', nargs='*',
                       choices=['productivity', 'development', 'observability'],
                       default=['productivity'], help='Features to enable')

    args = parser.parse_args()

    show_banner()
    check_prerequisites()

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
    start_services(args.profile, args.features)
    wait_for_services()

    # Erfolg!
    show_success_message(editor_name)

if __name__ == "__main__":
    main()
