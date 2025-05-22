# 🚀 Workspace-in-a-Box - Vollständige Dokumentation

## 📋 Inhaltsverzeichnis

1. [🎯 Überblick](#-überblick)
2. [✨ Features](#-features)
3. [🏗️ Architektur](#️-architektur)
4. [⚡ Schnellstart](#-schnellstart)
5. [🔧 Installation](#-installation)
6. [🎨 Editor-Auswahl](#-editor-auswahl)
7. [🖥️ Desktop-Verwendung](#️-desktop-verwendung)
8. [🧠 AI-Services](#-ai-services)
9. [⚙️ Konfiguration](#️-konfiguration)
10. [🔒 Sicherheit](#-sicherheit)
11. [🛠️ Entwicklung](#️-entwicklung)
12. [📊 Monitoring](#-monitoring)
13. [🐛 Troubleshooting](#-troubleshooting)
14. [🚀 Erweiterte Nutzung](#-erweiterte-nutzung)
15. [❓ FAQ](#-faq)

---

## 🎯 Überblick

**Workspace-in-a-Box** ist eine vollständige, browserbasierte AI-Entwicklungsumgebung, die alle modernen AI-Tools und -Services in einem einzigen, zugänglichen Desktop vereint.

### Was ist das?

Eine containerisierte Entwicklungsumgebung, die über einen einzigen Browser-Tab zugänglich ist und folgende Komponenten integriert:

- **🖥️ Linux Desktop** - Vollständige Desktop-Umgebung im Browser
- **⚡ Zed Editor / VS Code** - Moderne Code-Editoren mit AI-Unterstützung
- **🧠 N8N** - Workflow-Automation und AI-Orchestrierung
- **💬 Open WebUI** - Chat-Interface für lokale LLMs
- **🤖 Ollama** - Lokale Large Language Models
- **📊 Qdrant** - Vector-Datenbank für RAG-Anwendungen
- **🗄️ Supabase** - Vollständige Backend-as-a-Service
- **📝 Produktivitäts-Tools** - AppFlowy, AFFINE, GitLab

### Warum Workspace-in-a-Box?

✅ **Ein Browser-Tab für alles** - Keine Port-Konflikte oder separate Fenster
✅ **Plattform-unabhängig** - Läuft überall wo Docker läuft
✅ **Vollständig isoliert** - Alle Services in separaten Containern
✅ **Moderne Editoren** - Zed-Editor oder VS Code mit vollständiger Konfiguration
✅ **AI-First Development** - Optimiert für moderne AI-Workflows
✅ **Skalierbar** - Profile-basierte Service-Aktivierung

---

## ✨ Features

### 🎨 **Editor-Integration**
- **Zed Editor** (empfohlen) - Ultra-schnell, Rust-basiert, kollaborativ
- **VS Code** - Vollständig konfiguriert mit Extensions
- **Language Servers** - TypeScript, Python, Rust, Docker, YAML
- **AI-Code-Completion** - Integrierte AI-Unterstützung
- **Container-Development** - Optimiert für Docker-basierte Entwicklung

### 🧠 **AI-Services**
- **Lokale LLMs** - Ollama mit GPU-Unterstützung
- **RAG-System** - Vector-basierte Dokumentensuche
- **Workflow-Automation** - N8N für AI-Pipelines
- **Chat-Interface** - Open WebUI für Modell-Interaktion
- **Observability** - Langfuse für LLM-Monitoring

### 🖥️ **Desktop-Umgebung**
- **Browser-basiert** - Zugriff über Guacamole
- **Vorkonfiguriert** - Alle Tools und Bookmarks bereit
- **Entwicklungstools** - Git, Docker CLI, Terminal
- **File-Sharing** - Nahtloser Dateiaustausch mit Host

### 📊 **Produktivität**
- **Notizen** - AppFlowy (Notion-Alternative)
- **Kollaboration** - AFFINE Workspace
- **Versionskontrolle** - GitLab CE
- **Datenbank** - Supabase mit Studio
- **API-Gateway** - Kong für Service-Routing

---

## 🏗️ Architektur

### System-Übersicht

```
┌─────────────────────────────────────────────────────────────┐
│                    Browser (Port 8080)                      │
└─────────────────────┬───────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────┐
│                 Guacamole Gateway                           │
└─────────────────────┬───────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────┐
│              Linux Desktop Container                        │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────────────────┐│
│  │ Zed Editor  │ │   Browser   │ │      Terminal           ││
│  │             │ │             │ │                         ││
│  └─────────────┘ └─────────────┘ └─────────────────────────┘│
└─────────────────────┬───────────────────────────────────────┘
                      │ Internal Docker Network (localai)
    ┌─────────────────┼─────────────────┐
    │                 │                 │
┌───▼────┐ ┌─────▼────┐ ┌────▼────┐ ┌──▼─────┐
│   N8N  │ │  Ollama  │ │ Qdrant  │ │ WebUI  │
│  :5678 │ │  :11434  │ │  :6333  │ │ :8080  │
└────────┘ └──────────┘ └─────────┘ └────────┘
```

### Container-Architektur

| **Container** | **Funktion** | **Zugriff** | **Dependencies** |
|---------------|--------------|-------------|------------------|
| `guacamole` | Web-Gateway | 8080 → Browser | guacd, guacamole-db |
| `desktop` | Linux-Desktop | VNC über Guacamole | Alle AI-Services |
| `n8n` | Workflow-Engine | desktop:5678 | db, ollama |
| `ollama` | LLM-Runtime | desktop:11434 | - |
| `open-webui` | Chat-Interface | desktop:8080 | ollama |
| `qdrant` | Vector-DB | desktop:6333 | - |
| `db` | PostgreSQL | desktop:5432 | - |
| `kong` | API-Gateway | desktop:8000 | db |

### Netzwerk-Design

- **Ein einziges Docker-Netzwerk** (`localai`)
- **Interne Service-Discovery** via Container-Namen
- **Nur Port 8080 exponiert** (Guacamole)
- **Sichere Container-zu-Container Kommunikation**

---

## ⚡ Schnellstart

### Voraussetzungen

- **Docker** 20.10+ mit Docker Compose
- **4GB RAM** (minimum), 8GB+ empfohlen
- **10GB freier Speicherplatz**
- **Moderne Browser** (Chrome, Firefox, Safari, Edge)

### 3-Minuten-Setup

```bash
# 1. Repository klonen
git clone https://github.com/161sam/local-ai-work-env.git
cd local-ai-work-env

# 2. Umgebung konfigurieren
cp .env.example .env
# Optional: .env anpassen (Passwörter ändern)

# 3. Workspace starten
python setup_workspace.py --profile cpu

# 4. Browser öffnen
# http://localhost:8080
# Login: guacadmin / guacadmin
```

### Erste Schritte im Desktop

1. **Desktop-Verbindung** in Guacamole erstellen:
   - Protocol: VNC
   - Hostname: desktop
   - Port: 5901
   - Password: password

2. **Editor öffnen**:
   - Zed: Desktop-Icon oder `zed` im Terminal
   - VS Code: Desktop-Icon oder `code` im Terminal

3. **AI-Services nutzen**:
   - N8N: http://n8n:5678
   - Open WebUI: http://open-webui:8080
   - Alle anderen über Desktop-Bookmarks

---

## 🔧 Installation

### Detaillierte Installation

#### Schritt 1: System vorbereiten

**Linux (Ubuntu/Debian):**
```bash
# Docker installieren
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Docker Compose (falls nicht enthalten)
sudo apt install docker-compose-plugin

# Python (für Setup-Script)
sudo apt install python3 python3-pip
```

**macOS:**
```bash
# Docker Desktop installieren
brew install --cask docker

# Python (falls nicht vorhanden)
brew install python3
```

**Windows:**
```powershell
# Docker Desktop für Windows installieren
# Python von python.org installieren
```

#### Schritt 2: Repository einrichten

```bash
# Repository klonen
git clone https://github.com/161sam/local-ai-work-env.git
cd local-ai-work-env

# Verzeichnisstruktur überprüfen
ls -la
# Sollte enthalten: docker-compose.yml, setup_workspace.py, .env.example
```

#### Schritt 3: Umgebungskonfiguration

```bash
# Basis-Konfiguration erstellen
cp .env.example .env

# Sichere Passwörter generieren (empfohlen)
python -c "import secrets; print('N8N_ENCRYPTION_KEY=' + secrets.token_urlsafe(32))" >> .env
python -c "import secrets; print('JWT_SECRET=' + secrets.token_urlsafe(32))" >> .env
python -c "import secrets; print('POSTGRES_PASSWORD=' + secrets.token_urlsafe(16))" >> .env

# Editor-Präferenz setzen (optional)
echo "SELECTED_EDITOR=zed" >> .env  # oder "vscode"
```

#### Schritt 4: Setup ausführen

```bash
# Vollständiges Setup mit Editor-Auswahl
python setup_workspace.py

# Oder mit Parametern für automatisierte Installation
python setup_workspace.py \
  --profile gpu-nvidia \
  --features productivity development \
  --skip-editor-selection
```

### Setup-Optionen

#### GPU-Profile

```bash
# CPU-only (Standard)
python setup_workspace.py --profile cpu

# NVIDIA GPU
python setup_workspace.py --profile gpu-nvidia

# AMD GPU (Linux)
python setup_workspace.py --profile gpu-amd
```

#### Feature-Sets

```bash
# Nur Core AI Services
python setup_workspace.py --profile cpu

# Mit Produktivitäts-Tools
python setup_workspace.py --profile cpu --features productivity

# Mit Entwicklungstools
python setup_workspace.py --profile cpu --features development

# Vollständiges Setup
python setup_workspace.py --profile cpu --features productivity development observability
```

---

## 🎨 Editor-Auswahl

### Zed Editor (Empfohlen)

**Warum Zed?**
- ⚡ **Ultra-schnell** - Rust-basiert, sofortiger Start
- 🤝 **Kollaboration** - Eingebautes Real-time Pairing
- 🧠 **AI-Integration** - Native AI-Code-Completion
- 🎨 **Modern** - Minimalistisches, ablenkungsfreies Interface
- 🔧 **LSP-Native** - Perfekte Language Server Integration

**Zed-Features im Workspace:**
```json
{
  "theme": "Ayu Dark",
  "buffer_font_family": "JetBrains Mono",
  "languages": {
    "Python": {
      "language_servers": ["python-lsp-server"],
      "format_on_save": "on",
      "formatter": "black"
    },
    "TypeScript": {
      "language_servers": ["typescript-language-server"],
      "format_on_save": "on"
    },
    "Rust": {
      "language_servers": ["rust-analyzer"],
      "format_on_save": "on"
    }
  }
}
```

### VS Code

**Wann VS Code wählen?**
- 🔌 **Extensions** - Spezielle Extensions benötigt
- 🐛 **Debugging** - Integrierte Debug-Tools erforderlich
- 📊 **Jupyter** - Notebook-Integration wichtig
- 🔧 **Remote Development** - VS Code Remote Features

**VS Code-Features im Workspace:**
- **Pre-installierte Extensions**: Python, Rust, Docker, GitLens
- **Integriertes Terminal** mit Zsh + Oh-My-Zsh
- **Docker-Integration** für Container-Development
- **Git-Integration** mit Desktop-GitLab

### Editor-Konfiguration anpassen

```bash
# Zed-Konfiguration bearbeiten
zed ~/.config/zed/settings.json

# VS Code-Konfiguration
code ~/.config/Code/User/settings.json

# Beide Editoren unterstützen:
# - AI-Code-Completion
# - Language Servers für alle Sprachen
# - Integrierte Terminals
# - Git-Integration
# - Docker-File-Support
```

---

## 🖥️ Desktop-Verwendung

### Guacamole-Zugriff

#### Erste Anmeldung
1. **Browser öffnen**: http://localhost:8080
2. **Anmelden**: `guacadmin` / `guacadmin`
3. **Desktop-Verbindung erstellen**:
   - Name: "Linux Desktop"
   - Protocol: VNC
   - Hostname: `desktop`
   - Port: `5901`
   - Password: `password`

#### Desktop-Oberfläche

**Vorkonfigurierte Elemente:**
- **Desktop-Icons** für alle AI-Services
- **Browser-Bookmarks** für interne URLs
- **Terminal** mit Zsh + Oh-My-Zsh
- **File Manager** mit Shared-Folders
- **Editor-Shortcuts** (Zed/VS Code)

**Tastaturkürzel:**
- `Ctrl+Alt+T` - Terminal öffnen
- `Ctrl+Space` - Anwendungsmenü
- `Alt+Tab` - Zwischen Anwendungen wechseln
- `Ctrl+Shift+C/V` - Kopieren/Einfügen im Terminal

### File-Sharing

#### Shared Directories

```bash
# Vom Host-System zugänglich:
./desktop-shared/     # Sichtbar als /shared im Desktop
./shared/            # N8N-Workflows und Daten

# Im Desktop verfügbar:
/home/kasm-user/Projects/     # Entwicklungsprojekte
/home/kasm-user/Documents/    # Dokumente
/shared/                      # Host-Dateien
```

#### Dateiaustausch

```bash
# Datei vom Host in Desktop kopieren
cp mein-projekt.zip ./desktop-shared/

# Im Desktop verfügbar unter:
/shared/mein-projekt.zip

# Projekte entwickeln
cd /home/kasm-user/Projects/
git clone https://github.com/user/project.git
zed project/  # oder: code project/
```

### Terminal-Umgebung

#### Zsh-Konfiguration

```bash
# Oh-My-Zsh mit nützlichen Plugins
plugins=(git docker docker-compose node npm python rust)

# Aliase für AI-Services
alias check-services='~/Scripts/check-services.sh'
alias n8n-logs='docker logs n8n'
alias webui-logs='docker logs open-webui'
alias dc='docker-compose'
```

#### Entwicklungstools

```bash
# Vorinstallierte Tools:
git --version          # Git mit Desktop-Integration
docker --version       # Docker CLI für Container-Management
node --version         # Node.js + npm für TypeScript/JS
python3 --version      # Python + pip für AI-Entwicklung
rustc --version        # Rust für System Programming
go version            # Go für Backend-Development

# Language Servers:
typescript-language-server --version
pylsp --version
rust-analyzer --version
```

---

## 🧠 AI-Services

### N8N - Workflow Automation

#### Zugriff und Setup
```
URL: http://n8n:5678 (im Desktop-Browser)
Erste Anmeldung: Account erstellen (nur lokal)
```

#### Vorkonfigurierte Workflows
- **Local RAG AI Agent** - Dokumenten-basierte AI-Antworten
- **Google Drive Integration** - Automatische Dokumentenverarbeitung
- **Slack Integration** - AI-Bots für Teams
- **Web Search + Chat** - Internet-basierte AI-Recherche

#### Entwicklung eigener Workflows

```javascript
// N8N Code-Node Beispiel
const response = await $http.request({
  method: 'POST',
  url: 'http://ollama:11434/api/generate',
  body: {
    model: 'llama3.1',
    prompt: $json.userInput,
    stream: false
  }
});

return [{ json: { aiResponse: response.response } }];
```

### Ollama - Large Language Models

#### Verfügbare Modelle
```bash
# Im Desktop-Terminal:
docker exec ollama ollama list

# Neue Modelle installieren:
docker exec ollama ollama pull llama3.1:8b
docker exec ollama ollama pull codellama:13b
docker exec ollama ollama pull mistral:7b
```

#### API-Verwendung

```python
# Python-Client
import requests

response = requests.post('http://ollama:11434/api/generate', json={
    'model': 'llama3.1',
    'prompt': 'Explain quantum computing',
    'stream': False
})

print(response.json()['response'])
```

```bash
# cURL
curl -X POST http://ollama:11434/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "model": "llama3.1",
    "prompt": "Write a Python function to calculate Fibonacci numbers",
    "stream": false
  }'
```

### Open WebUI - Chat Interface

#### Features
- **Multi-Model Support** - Verschiedene Ollama-Modelle
- **Chat-History** - Persistente Gespräche
- **File Upload** - Dokumente für RAG
- **Model Comparison** - Side-by-side Tests
- **Custom Functions** - N8N-Integration

#### N8N-Integration aktivieren

```python
# In Open WebUI → Functions → Create Function
# Name: n8n_workflow
# Code: (siehe n8n_pipe.py im Repository)

def pipe(body: dict, __user__: dict = None) -> dict:
    # Weiterleitung an N8N-Workflow
    response = requests.post(
        'http://n8n:5678/webhook/your-webhook-id',
        json={'message': body['messages'][-1]['content']}
    )
    return {'response': response.json()}
```

### Qdrant - Vector Database

#### Zugriff
```
URL: http://qdrant:6333/dashboard (im Desktop-Browser)
API: http://qdrant:6333
```

#### RAG-Setup

```python
# Vector-Store für Dokumente erstellen
import requests

# Collection erstellen
requests.put('http://qdrant:6333/collections/documents', json={
    'vectors': {
        'size': 384,  # nomic-embed-text Dimension
        'distance': 'Cosine'
    }
})

# Dokument hinzufügen
requests.put('http://qdrant:6333/collections/documents/points', json={
    'points': [{
        'id': 1,
        'vector': embedding_vector,  # Von Ollama nomic-embed-text
        'payload': {'text': 'Document content', 'source': 'file.pdf'}
    }]
})
```

### Supabase - Backend as a Service

#### Dashboard
```
URL: http://kong:8000 (im Desktop-Browser)
Login: Siehe .env-Datei (DASHBOARD_USERNAME/PASSWORD)
```

#### Database-Schema für AI

```sql
-- RAG-Dokumente
CREATE TABLE documents_pg (
    id BIGSERIAL PRIMARY KEY,
    content TEXT,
    embedding VECTOR(384),
    metadata JSONB
);

-- Chat-History
CREATE TABLE chat_messages (
    id BIGSERIAL PRIMARY KEY,
    session_id UUID,
    role TEXT,
    content TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Workflow-Results
CREATE TABLE n8n_results (
    id BIGSERIAL PRIMARY KEY,
    workflow_id TEXT,
    input_data JSONB,
    output_data JSONB,
    executed_at TIMESTAMP DEFAULT NOW()
);
```

---

## ⚙️ Konfiguration

### Umgebungsvariablen

#### Core-Konfiguration
```bash
# .env
SELECTED_EDITOR=zed              # oder "vscode"
DESKTOP_PASSWORD=password        # VNC-Passwort
DESKTOP_TIMEZONE=Europe/Berlin   # Zeitzone

# AI-Services
OLLAMA_MODELS=llama3.1,codellama,mistral
N8N_ENCRYPTION_KEY=your-secret-key
POSTGRES_PASSWORD=secure-password
```

#### GPU-Konfiguration
```bash
# NVIDIA GPU
NVIDIA_VISIBLE_DEVICES=all
NVIDIA_DRIVER_CAPABILITIES=compute,utility

# AMD GPU (ROCm)
HSA_OVERRIDE_GFX_VERSION=10.3.0
```

#### Service-URLs (Produktion)
```bash
# Domain-basierte URLs (optional)
N8N_HOSTNAME=n8n.yourdomain.com
WEBUI_HOSTNAME=chat.yourdomain.com
GUACAMOLE_HOSTNAME=desktop.yourdomain.com
LETSENCRYPT_EMAIL=admin@yourdomain.com
```

### Docker-Compose Profile

#### Profile aktivieren
```bash
# Basis-Services
docker-compose --profile cpu up -d

# Mit Desktop
docker-compose --profile cpu --profile desktop up -d

# Vollständig
docker-compose --profile gpu-nvidia --profile desktop --profile productivity --profile development up -d
```

#### Profile-Definitionen

| **Profile** | **Services** | **Beschreibung** |
|-------------|--------------|------------------|
| `cpu` | ollama-cpu | Ollama ohne GPU |
| `gpu-nvidia` | ollama-gpu | Ollama mit NVIDIA GPU |
| `desktop` | guacamole, desktop | Browser-Desktop |
| `productivity` | appflowy, affine | Produktivitäts-Tools |
| `development` | gitlab, n8n-extended | Development-Tools |
| `observability` | langfuse | LLM-Monitoring |

### Service-spezifische Konfiguration

#### N8N-Anpassungen
```javascript
// N8N-Settings (über UI)
{
  "executionProcess": "main",
  "timezone": "Europe/Berlin",
  "userManagement": {
    "isInstanceOwnerSetUp": true
  },
  "publicApi": {
    "disabled": false
  }
}
```

#### Ollama-Modell-Management
```bash
# Modelle verwalten
docker exec ollama ollama list
docker exec ollama ollama pull llama3.1:70b
docker exec ollama ollama rm old-model

# Modell-Performance tunen
docker exec ollama ollama run llama3.1 --temperature 0.7 --top-p 0.9
```

#### Desktop-Anpassungen
```bash
# Desktop-Themes
gsettings set org.gnome.desktop.interface gtk-theme 'Adwaita-dark'

# Editor-Standard festlegen
update-alternatives --set editor /usr/local/bin/zed

# Startup-Programme
echo 'firefox http://n8n:5678' >> ~/.config/autostart/n8n.desktop
```

---

## 🔒 Sicherheit

### Netzwerk-Sicherheit

#### Container-Isolation
- **Separates Docker-Netzwerk** - Keine Host-Netzwerk-Exposition
- **Nur Port 8080 exponiert** - Minimaler Attack Surface
- **Container-zu-Container Kommunikation** - Verschlüsselt über Docker-Netzwerk

#### Firewall-Konfiguration
```bash
# UFW (Ubuntu)
sudo ufw enable
sudo ufw allow 8080/tcp  # Nur Guacamole
sudo ufw deny 5678/tcp   # N8N nicht direkt erreichbar
sudo ufw deny 11434/tcp  # Ollama nicht direkt erreichbar

# iptables
iptables -A INPUT -p tcp --dport 8080 -j ACCEPT
iptables -A INPUT -p tcp --dport 5678 -j DROP
iptables -A INPUT -p tcp --dport 11434 -j DROP
```

### Authentifizierung

#### Guacamole-Sicherheit
```sql
-- Starke Passwörter setzen
UPDATE guacamole_user SET password_hash = SHA2('new-secure-password', 256) WHERE username = 'guacadmin';

-- Zusätzliche Benutzer
INSERT INTO guacamole_user (username, password_hash) VALUES ('developer', SHA2('dev-password', 256));
```

#### Service-Authentication
```bash
# N8N Basic Auth aktivieren
N8N_BASIC_AUTH_ACTIVE=true
N8N_BASIC_AUTH_USER=admin
N8N_BASIC_AUTH_PASSWORD=secure-password

# Supabase JWT-Security
JWT_SECRET=$(openssl rand -base64 64)
ANON_KEY=$(generate-jwt-key)
SERVICE_ROLE_KEY=$(generate-service-jwt-key)
```

### Daten-Sicherheit

#### Volume-Verschlüsselung
```bash
# Encrypted Docker Volumes (Linux)
docker volume create --driver local \
  --opt type=none \
  --opt device=/encrypted/path \
  --opt o=bind \
  encrypted_volume
```

#### Backup-Strategie
```bash
# Automatische Backups
#!/bin/bash
# backup.sh
docker exec supabase-db pg_dump -U postgres postgres > backup_$(date +%Y%m%d).sql
docker exec n8n cat /home/node/.n8n/config.json > n8n_config_$(date +%Y%m%d).json
tar -czf workspace_backup_$(date +%Y%m%d).tar.gz ./desktop-shared ./shared
```

#### Secret-Management
```bash
# Docker Secrets (Swarm Mode)
echo "my-secret-password" | docker secret create postgres_password -
echo "jwt-secret-key" | docker secret create jwt_secret -

# In docker-compose.yml:
secrets:
  postgres_password:
    external: true
  jwt_secret:
    external: true
```

---

## 🛠️ Entwicklung

### Entwicklungsworkflow

#### Projekt-Setup
```bash
# Im Desktop-Terminal
cd /home/kasm-user/Projects/
git clone https://github.com/user/ai-project.git
cd ai-project/

# Editor öffnen
zed .  # oder: code .

# Dependencies installieren
npm install  # für JS/TS
pip install -r requirements.txt  # für Python
cargo build  # für Rust
```

#### AI-Development-Pattern

**1. Prototyping in Open WebUI**
```
1. Idee in Chat testen
2. Prompt engineering
3. Model-Vergleiche
4. Erste Implementierung
```

**2. N8N-Workflow entwickeln**
```
1. Open WebUI → N8N-Integration
2. Workflow-Nodes erstellen
3. API-Endpunkte definieren
4. Testing und Debugging
```

**3. Code-Implementation**
```python
# AI-Service-Client
class AIWorkspaceClient:
    def __init__(self):
        self.ollama_url = "http://ollama:11434"
        self.n8n_url = "http://n8n:5678"
        self.qdrant_url = "http://qdrant:6333"

    def generate_text(self, prompt, model="llama3.1"):
        response = requests.post(f"{self.ollama_url}/api/generate", json={
            "model": model,
            "prompt": prompt,
            "stream": False
        })
        return response.json()["response"]

    def trigger_workflow(self, workflow_id, data):
        response = requests.post(f"{self.n8n_url}/webhook/{workflow_id}", json=data)
        return response.json()

    def search_documents(self, query, limit=5):
        # RAG-Implementation
        embedding = self.get_embedding(query)
        response = requests.post(f"{self.qdrant_url}/collections/documents/points/search", json={
            "vector": embedding,
            "limit": limit
        })
        return response.json()["result"]
```

### Container-Development

#### Live-Reloading
```bash
# Python-Entwicklung mit Hot-Reload
pip install watchdog
watchmedo auto-restart --patterns="*.py" --recursive -- python app.py

# Node.js mit Nodemon
npm install -g nodemon
nodemon --watch . --ext js,ts server.js

# Rust mit Cargo Watch
cargo install cargo-watch
cargo watch -x run
```

#### Debugging

**VS Code Debugging:**
```json
// .vscode/launch.json
{
    "configurations": [
        {
            "name": "Python: Current File",
            "type": "python",
            "request": "launch",
            "program": "${file}",
            "console": "integratedTerminal",
            "env": {
                "OLLAMA_URL": "http://ollama:11434"
            }
        }
    ]
}
```

**Zed Debugging:**
```json
// Zed tasks.json
{
    "tasks": [
        {
            "label": "Run Python",
            "command": "python3",
            "args": ["${file}"],
            "group": "build",
            "env": {
                "OLLAMA_URL": "http://ollama:11434"
            }
        }
    ]
}
```

### Testing-Strategien

#### AI-Service Tests
```python
import pytest
import requests

class TestAIServices:
    def test_ollama_health(self):
        response = requests.get("http://ollama:11434/api/tags")
        assert response.status_code == 200

    def test_n8n_health(self):
        response = requests.get("http://n8n:5678/healthz")
        assert response.status_code == 200

    def test_rag_pipeline(self):
        # Document-Upload
        # Embedding-Generation
        # Similarity-Search
        # Answer-Generation
        pass
```

#### Integration Tests
```bash
# Service-Integration testen
#!/bin/bash
# test-integration.sh

echo "Testing Ollama..."
curl -s http://ollama:11434/api/tags | jq .

echo "Testing N8N..."
curl -s http://n8n:5678/healthz

echo "Testing Qdrant..."
curl -s http://qdrant:6333/health

echo "Testing RAG-Pipeline..."
python test_rag.py
```

---

## 📊 Monitoring

### Service-Monitoring

#### Health-Checks
```bash
# Eingebauter Health-Check-Script
~/Scripts/check-services.sh

# Ausgabe:
# ✅ n8n (n8n:5678) - Running
# ✅ open-webui (open-webui:8080) - Running
# ✅ ollama (ollama:11434) - Running
# ❌ qdrant (qdrant:6333) - Not responding
```

#### Docker-Monitoring
```bash
# Container-Status
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

# Resource-Usage
docker stats --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}"

# Log-Monitoring
docker logs n8n --tail 100 -f
docker logs ollama --tail 100 -f
```

#### System-Metriken
```bash
# Im Desktop-Terminal
htop          # System-Übersicht
iotop         # Disk I/O
nvidia-smi    # GPU-Usage (falls NVIDIA)
```

### Langfuse - LLM Observability

#### Setup (Optional)
```bash
# Langfuse-Profile aktivieren
docker-compose --profile cpu --profile desktop --profile observability up -d

# Zugriff: http://langfuse:3000
```

#### Integration
```python
from langfuse import Langfuse

langfuse = Langfuse(
    public_key="your-public-key",
    secret_key="your-secret-key",
    host="http://langfuse:3000"
)

# LLM-Calls tracken
trace = langfuse.trace(name="ai-workflow")
generation = trace.generation(
    name="ollama-completion",
    model="llama3.1",
    input=prompt,
    output=response
)
```

### Performance-Optimierung

#### Ollama-Performance
```bash
# GPU-Memory optimieren
OLLAMA_GPU_MEMORY_FRACTION=0.8

# Model-Parallelisierung
OLLAMA_NUM_PARALLEL=4

# Context-Size tunen
OLLAMA_CONTEXT_LENGTH=4096
```

#### Container-Resources
```yaml
# docker-compose.yml
services:
  ollama:
    deploy:
      resources:
        limits:
          cpus: '4.0'
          memory: 8G
        reservations:
          cpus: '2.0'
          memory: 4G
```

---

## 🐛 Troubleshooting

### Häufige Probleme

#### Guacamole-Verbindung fehlschlägt

**Problem**: Desktop-Verbindung zeigt "Verbindung fehlgeschlagen"

**Lösung**:
```bash
# 1. Container-Status prüfen
docker ps | grep -E "(guacamole|desktop)"

# 2. Desktop-Container-Logs
docker logs desktop

# 3. VNC-Port testen
docker exec desktop ss -tlnp | grep 5901

# 4. Container-Neustart
docker restart desktop guacd guacamole
```

#### Ollama-Modelle laden nicht

**Problem**: "Model not found" Fehler

**Lösung**:
```bash
# 1. Verfügbare Modelle prüfen
docker exec ollama ollama list

# 2. Modell manuell laden
docker exec ollama ollama pull llama3.1

# 3. Ollama-Container-Logs
docker logs ollama

# 4. GPU-Setup prüfen (falls GPU-Profile)
docker exec ollama nvidia-smi  # NVIDIA
docker exec ollama rocm-smi    # AMD
```

#### N8N-Workflows funktionieren nicht

**Problem**: Workflows starten nicht oder geben Fehler zurück

**Lösung**:
```bash
# 1. N8N-Status prüfen
curl http://n8n:5678/healthz

# 2. Datenbank-Verbindung testen
docker exec n8n pg_isready -h db -U postgres

# 3. N8N-Logs analysieren
docker logs n8n

# 4. Workflow-Credentials prüfen
# In N8N UI: Settings → Credentials
```

#### Editor startet nicht im Desktop

**Problem**: Zed oder VS Code öffnet nicht

**Lösung**:
```bash
# 1. Editor-Installation prüfen
which zed
which code

# 2. Desktop-Terminal öffnen und manuell starten
zed --version
code --version

# 3. Desktop-Container neu bauen
docker-compose build desktop
docker-compose up -d desktop

# 4. Editor-Konfiguration prüfen
ls ~/.config/zed/
ls ~/.config/Code/
```

### Service-spezifische Probleme

#### Qdrant-Speicher voll

```bash
# Disk-Usage prüfen
docker exec qdrant df -h

# Alte Collections löschen
curl -X DELETE http://qdrant:6333/collections/old_collection

# Volume-Cleanup
docker volume prune
```

#### Supabase-Migration-Fehler

```bash
# Migration-Status prüfen
docker exec db psql -U postgres -c "\dt"

# Manuelle Migration
docker exec db psql -U postgres -f /docker-entrypoint-initdb.d/migration.sql

# Database-Reset (VORSICHT!)
docker volume rm localai_supabase_db_data
docker-compose up -d db
```

#### Open WebUI-Chat funktioniert nicht

```bash
# 1. Ollama-Verbindung testen
curl http://ollama:11434/api/tags

# 2. WebUI-Logs prüfen
docker logs open-webui

# 3. Browser-Cache leeren
# Strg+Shift+R oder Incognito-Modus

# 4. WebUI-Neustart
docker restart open-webui
```

### Performance-Troubleshooting

#### Langsame LLM-Antworten

```bash
# 1. GPU-Usage prüfen
nvidia-smi  # oder: rocm-smi

# 2. Memory-Usage analysieren
docker stats ollama

# 3. Model-Size reduzieren
docker exec ollama ollama pull llama3.1:8b  # statt 70b

# 4. Context-Length reduzieren
# In .env: OLLAMA_CONTEXT_LENGTH=2048
```

#### Hoher Memory-Verbrauch

```bash
# 1. Container-Memory analysieren
docker stats --format "table {{.Container}}\t{{.MemUsage}}\t{{.MemPerc}}"

# 2. Ungenutzten Memory freigeben
docker system prune -a

# 3. Swap aktivieren (Linux)
sudo swapon -s
sudo fallocate -l 4G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile

# 4. Memory-Limits setzen
# In docker-compose.yml für problematische Services
```

### Debug-Tools

#### Container-Diagnostics

```bash
# Container-Details
docker inspect container_name

# Prozesse im Container
docker exec container_name ps aux

# Netzwerk-Verbindungen
docker exec container_name netstat -tlnp

# Disk-Usage im Container
docker exec container_name df -h
```

#### Log-Analyse

```bash
# Strukturierte Logs
docker logs container_name --since 1h | grep ERROR

# Log-Aggregation
docker-compose logs --follow --tail=100

# Logs in Datei speichern
docker logs n8n > n8n-debug.log 2>&1
```

---

## 🚀 Erweiterte Nutzung

### Custom-Services hinzufügen

#### Eigene Container integrieren

```yaml
# docker-compose.yml erweitern
services:
  my-ai-service:
    image: my-custom-ai:latest
    container_name: my-ai-service
    networks:
      - localai
    environment:
      - API_KEY=${MY_AI_API_KEY}
    volumes:
      - ./my-ai-config:/config
    profiles:
      - custom
```

#### Service-Discovery

```bash
# Im Desktop verfügbar unter:
http://my-ai-service:8080

# Desktop-Bookmark erstellen
echo '[Desktop Entry]
Name=My AI Service
Exec=firefox http://my-ai-service:8080
Icon=firefox
Type=Application' > ~/Desktop/MyAI.desktop
chmod +x ~/Desktop/MyAI.desktop
```

### Multi-Environment Setup

#### Development/Staging/Production

```bash
# Development
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d

# Staging
docker-compose -f docker-compose.yml -f docker-compose.staging.yml up -d

# Production
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

#### Environment-Files

```bash
# .env.development
SELECTED_EDITOR=zed
DEBUG_MODE=true
OLLAMA_MODELS=llama3.1:8b
N8N_LOG_LEVEL=debug

# .env.production
SELECTED_EDITOR=zed
DEBUG_MODE=false
OLLAMA_MODELS=llama3.1:70b
N8N_LOG_LEVEL=warn
LETSENCRYPT_EMAIL=admin@company.com
```

### Clustering und Skalierung

#### Docker Swarm

```bash
# Swarm initialisieren
docker swarm init

# Service skalieren
docker service scale workspace_ollama=3
docker service scale workspace_n8n=2

# Load Balancing
docker service create --name lb --publish 8080:80 --network localai nginx
```

#### Kubernetes-Deployment

```yaml
# kubernetes/workspace-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: workspace-desktop
spec:
  replicas: 1
  selector:
    matchLabels:
      app: workspace-desktop
  template:
    metadata:
      labels:
        app: workspace-desktop
    spec:
      containers:
      - name: desktop
        image: workspace/desktop:latest
        ports:
        - containerPort: 6901
        env:
        - name: SELECTED_EDITOR
          value: "zed"
```

### CI/CD-Integration

#### GitHub Actions

```yaml
# .github/workflows/workspace.yml
name: Workspace CI/CD
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3

    - name: Start Workspace
      run: |
        python setup_workspace.py --skip-editor-selection --profile cpu

    - name: Test Services
      run: |
        sleep 60  # Wait for services
        python -m pytest tests/integration/

    - name: Test AI Workflows
      run: |
        python tests/test_n8n_workflows.py
        python tests/test_ollama_api.py
```

#### GitLab CI/CD

```yaml
# .gitlab-ci.yml
stages:
  - test
  - deploy

test_workspace:
  stage: test
  script:
    - python setup_workspace.py --skip-editor-selection
    - python -m pytest tests/
  services:
    - docker:dind

deploy_production:
  stage: deploy
  script:
    - docker-compose -f docker-compose.prod.yml up -d
  only:
    - main
```

### Backup und Disaster Recovery

#### Automatisierte Backups

```bash
#!/bin/bash
# scripts/backup.sh

BACKUP_DIR="/backups/workspace-$(date +%Y%m%d)"
mkdir -p $BACKUP_DIR

# Database Backups
docker exec supabase-db pg_dump -U postgres postgres > $BACKUP_DIR/postgres.sql
docker exec guacamole-db pg_dump -U guacamole_user guacamole_db > $BACKUP_DIR/guacamole.sql

# Volume Backups
docker run --rm -v localai_n8n_storage:/data -v $BACKUP_DIR:/backup alpine tar czf /backup/n8n_data.tar.gz /data
docker run --rm -v localai_ollama_storage:/data -v $BACKUP_DIR:/backup alpine tar czf /backup/ollama_data.tar.gz /data

# Configuration Backup
cp -r ./desktop-shared $BACKUP_DIR/
cp .env $BACKUP_DIR/
cp docker-compose.yml $BACKUP_DIR/

# Upload to Cloud (optional)
# aws s3 sync $BACKUP_DIR s3://my-workspace-backups/
```

#### Disaster Recovery

```bash
#!/bin/bash
# scripts/restore.sh

BACKUP_DIR=$1
if [ -z "$BACKUP_DIR" ]; then
    echo "Usage: ./restore.sh /path/to/backup"
    exit 1
fi

# Stop services
docker-compose down

# Restore databases
docker-compose up -d db guacamole-db
sleep 10
docker exec -i supabase-db psql -U postgres < $BACKUP_DIR/postgres.sql
docker exec -i guacamole-db psql -U guacamole_user guacamole_db < $BACKUP_DIR/guacamole.sql

# Restore volumes
docker run --rm -v localai_n8n_storage:/data -v $BACKUP_DIR:/backup alpine tar xzf /backup/n8n_data.tar.gz -C /
docker run --rm -v localai_ollama_storage:/data -v $BACKUP_DIR:/backup alpine tar xzf /backup/ollama_data.tar.gz -C /

# Restore configuration
cp $BACKUP_DIR/.env ./
cp -r $BACKUP_DIR/desktop-shared ./

# Restart services
docker-compose up -d
```

---

## ❓ FAQ

### Allgemeine Fragen

**Q: Kann ich das Workspace ohne Docker verwenden?**
A: Nein, das System ist speziell für Container-basierte Deployment entwickelt. Docker ist erforderlich für die Service-Isolation und Netzwerk-Konfiguration.

**Q: Welche Hardware-Anforderungen gibt es?**
A: Minimum: 4GB RAM, 10GB Speicher. Empfohlen: 8GB+ RAM, 50GB+ Speicher, GPU für bessere LLM-Performance.

**Q: Kann ich andere Editoren verwenden?**
A: Das System ist für Zed und VS Code optimiert. Andere Editoren können manuell installiert werden, haben aber keine vorkonfigurierte Integration.

**Q: Ist das System produktionsbereit?**
A: Für Development und Prototyping ja. Für Production sollten zusätzliche Sicherheits- und Skalierungs-Maßnahmen implementiert werden.

### Editor-Fragen

**Q: Warum ist Zed der empfohlene Editor?**
A: Zed bietet bessere Performance, native AI-Integration und moderne Kollaborations-Features. VS Code ist verfügbar für Nutzer mit spezifischen Extension-Anforderungen.

**Q: Kann ich zwischen Editoren wechseln?**
A: Ja, beide Editoren sind installiert. Setzen Sie `SELECTED_EDITOR` in der .env-Datei oder verwenden Sie beide parallel.

**Q: Funktionieren VS Code Extensions?**
A: Ja, die meisten Extensions funktionieren. Einige require spezielle Container-Permissions oder externe Services.

### AI-Service-Fragen

**Q: Welche LLM-Modelle werden unterstützt?**
A: Alle Ollama-kompatiblen Modelle. Standard: llama3.1, codellama, mistral. GPU-Modelle für bessere Performance.

**Q: Kann ich externe AI-APIs verwenden?**
A: Ja, über N8N-Workflows oder direkt in Ihrem Code. OpenAI, Anthropic, etc. APIs können integriert werden.

**Q: Wie funktioniert RAG?**
A: Dokumente werden automatisch in Qdrant indiziert. N8N-Workflows nutzen Embeddings für Similarity-Search und Context-Generation.

### Netzwerk-Fragen

**Q: Warum nur Port 8080?**
A: Sicherheit durch minimale Exposition. Alle Services sind über den Desktop-Browser erreichbar, was einem VPN-ähnlichen Zugang entspricht.

**Q: Kann ich Services direkt erreichen?**
A: Nur über den Desktop-Browser. Für direkten Zugang können zusätzliche Ports in docker-compose.yml exponiert werden.

**Q: Funktioniert es mit Reverse Proxies?**
A: Ja, Caddy ist integriert. Für Nginx/Apache sind zusätzliche Konfigurationen erforderlich.

### Performance-Fragen

**Q: Wie kann ich die Performance verbessern?**
A: 1) GPU verwenden, 2) Mehr RAM zuweisen, 3) SSD-Speicher, 4) Kleinere LLM-Modelle für Development.

**Q: Warum ist Ollama langsam?**
A: Meist CPU-only Ausführung. Verwenden Sie `--profile gpu-nvidia` oder `--profile gpu-amd` für Hardware-Beschleunigung.

**Q: Kann ich mehrere Instanzen laufen lassen?**
A: Ja, mit verschiedenen Ports und Projektnamen: `docker-compose -p workspace2 -f docker-compose.yml up -d`

### Troubleshooting-Fragen

**Q: Desktop-Verbindung funktioniert nicht?**
A: 1) Container-Status prüfen, 2) VNC-Port testen, 3) Guacamole-Konfiguration überprüfen, 4) Container neustarten.

**Q: N8N-Workflows schlagen fehl?**
A: 1) Service-URLs prüfen (n8n:5678, nicht localhost), 2) Credentials konfigurieren, 3) Netzwerk-Connectivity testen.

**Q: Wie debugge ich Container-Probleme?**
A: `docker logs <container>`, `docker exec <container> ps aux`, `docker inspect <container>` für detaillierte Diagnose.

### Entwicklungs-Fragen

**Q: Kann ich eigene Services hinzufügen?**
A: Ja, erweitern Sie docker-compose.yml mit eigenen Services im localai-Netzwerk.

**Q: Wie integriere ich externe Datenbanken?**
A: Fügen Sie Verbindungsstrings zu .env hinzu und konfigurieren Sie Services entsprechend.

**Q: Unterstützt das System Hot-Reloading?**
A: Ja, für Development-Workflows. Verwenden Sie Volume-Mounts für Ihren Code und entsprechende Development-Server.

### Sicherheits-Fragen

**Q: Wie sicher ist das Setup?**
A: Für lokale Development sehr sicher. Für Production sind zusätzliche Maßnahmen wie HTTPS, Authentication und Firewalling erforderlich.

**Q: Werden Daten verschlüsselt?**
A: Container-zu-Container Kommunikation ist über Docker-Netzwerk gesichert. Zusätzliche Verschlüsselung kann für sensible Daten konfiguriert werden.

**Q: Kann ich SSO integrieren?**
A: Ja, über Guacamole oder Service-spezifische Authentication-Provider.

---

## 📚 Zusätzliche Ressourcen

### Offizielle Dokumentationen
- [Docker Compose](https://docs.docker.com/compose/)
- [N8N Documentation](https://docs.n8n.io/)
- [Ollama Documentation](https://ollama.ai/docs)
- [Zed Editor Docs](https://zed.dev/docs)
- [Guacamole Manual](https://guacamole.apache.org/doc/gug/)

### Community und Support
- [GitHub Issues](https://github.com/161sam/local-ai-work-env/issues)
- [N8N Community](https://community.n8n.io/)
- [Ollama Discord](https://discord.gg/ollama)
- [Zed Community](https://github.com/zed-industries/community)

### Verwandte Projekte
- [Local AI Starter Kit](https://github.com/n8n-io/self-hosted-ai-starter-kit)
- [Kasm Workspaces](https://www.kasmweb.com/)
- [Supabase Self-Hosting](https://supabase.com/docs/guides/self-hosting)

---

**🎯 Das war die vollständige Dokumentation für Workspace-in-a-Box!**

Diese Dokumentation deckt alle Aspekte ab - von der Installation bis zur erweiterten Nutzung. Bei Fragen oder Problemen nutzen Sie den Troubleshooting-Bereich oder erstellen Sie ein GitHub Issue.
