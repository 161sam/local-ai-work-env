# 🚀 Workspace-in-a-Box Setup Guide

## 📋 Voraussetzungen

### System-Anforderungen

| **Komponente** | **Minimum** | **Empfohlen** |
|----------------|-------------|---------------|
| **CPU** | 4 Kerne | 8+ Kerne |
| **RAM** | 4GB | 8GB+ |
| **Storage** | 20GB frei | 50GB+ SSD |
| **Docker** | 20.10+ | Latest |
| **OS** | Linux/macOS/Windows | Ubuntu 22.04+ |

### Software-Installation

#### Linux (Ubuntu/Debian)
```bash
# Docker installieren
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Neuanmeldung erforderlich
newgrp docker

# Python für Setup-Script
sudo apt update
sudo apt install python3 python3-pip git curl -y
```

#### macOS
```bash
# Docker Desktop
brew install --cask docker

# Python und Tools
brew install python3 git curl

# Docker Desktop starten
open /Applications/Docker.app
```

#### Windows
```powershell
# Chocolatey Package Manager
Set-ExecutionPolicy Bypass -Scope Process -Force
[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# Docker Desktop
choco install docker-desktop

# Python und Git
choco install python3 git

# WSL2 aktivieren (für Docker)
wsl --install
```

## 🔧 Installation

### Schritt 1: Repository Setup

```bash
# Repository klonen
git clone https://github.com/161sam/local-ai-work-env.git
cd local-ai-work-env

# Branch überprüfen
git branch
git status

# Falls nicht auf main Branch:
git checkout main
```

### Schritt 2: Umgebungskonfiguration

#### Basis-Setup
```bash
# .env-Datei erstellen
cp .env.example .env

# Grundkonfiguration anpassen
nano .env  # oder code .env
```

#### Wichtige Umgebungsvariablen

```bash
# Editor-Auswahl
SELECTED_EDITOR=zed              # oder "vscode"

# Desktop-Konfiguration
DESKTOP_PASSWORD=secure-password
DESKTOP_TIMEZONE=Europe/Berlin

# Datenbank-Passwörter (ÄNDERN!)
POSTGRES_PASSWORD=change-this-secure-password
GUAC_POSTGRES_PASSWORD=change-this-guac-password

# N8N Sicherheit
N8N_ENCRYPTION_KEY=generate-32-char-key
N8N_USER_MANAGEMENT_JWT_SECRET=generate-jwt-secret

# Weitere Secrets generieren:
JWT_SECRET=generate-jwt-secret
NEXTAUTH_SECRET=generate-nextauth-secret
```

#### Automatische Secret-Generierung
```bash
# Sichere Secrets generieren
python3 -c "
import secrets
print('# Generated Secrets - Add to .env')
print(f'N8N_ENCRYPTION_KEY={secrets.token_urlsafe(32)}')
print(f'JWT_SECRET={secrets.token_urlsafe(32)}')
print(f'POSTGRES_PASSWORD={secrets.token_urlsafe(16)}')
print(f'GUAC_POSTGRES_PASSWORD={secrets.token_urlsafe(16)}')
print(f'NEXTAUTH_SECRET={secrets.token_urlsafe(32)}')
"
```

### Schritt 3: Hardware-spezifische Konfiguration

#### CPU-only Setup
```bash
# Standard-Setup für CPU-only
echo "GPU_PROFILE=cpu" >> .env
```

#### NVIDIA GPU Setup
```bash
# NVIDIA Container Runtime installieren
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | \
  sudo tee /etc/apt/sources.list.d/nvidia-docker.list

sudo apt-get update
sudo apt-get install -y nvidia-docker2
sudo systemctl restart docker

# GPU-Profile aktivieren
echo "GPU_PROFILE=gpu-nvidia" >> .env

# GPU-Test
docker run --rm --gpus all nvidia/cuda:11.0-base nvidia-smi
```

#### AMD GPU Setup (Linux)
```bash
# AMD ROCm installieren
wget -q -O - https://repo.radeon.com/rocm/rocm.gpg.key | sudo apt-key add -
echo "deb [arch=amd64] https://repo.radeon.com/rocm/apt/debian/ ubuntu main" | \
  sudo tee /etc/apt/sources.list.d/rocm.list

sudo apt update
sudo apt install rocm-dkms -y
sudo usermod -a -G render,video $USER

# GPU-Profile aktivieren
echo "GPU_PROFILE=gpu-amd" >> .env

# GPU-Test
docker run --rm --device=/dev/kfd --device=/dev/dri rocm/pytorch:latest rocm-smi
```

### Schritt 4: Setup ausführen

#### Interaktive Installation
```bash
# Vollständiges Setup mit Editor-Auswahl
python3 setup_workspace.py

# Setup-Dialog wird gestartet:
# 1. Editor-Auswahl (Zed/VS Code)
# 2. GPU-Profil-Erkennung
# 3. Feature-Auswahl
# 4. Prerequisite-Checks
# 5. Service-Start
```

#### Automatisierte Installation
```bash
# Ohne Editor-Dialog (verwendet Zed als Standard)
python3 setup_workspace.py \
  --profile gpu-nvidia \
  --features productivity development \
  --skip-editor-selection

# Nur Core-Services
python3 setup_workspace.py --profile cpu

# Vollständiges Setup
python3 setup_workspace.py \
  --profile gpu-nvidia \
  --features productivity development observability
```

### Schritt 5: Service-Validierung

#### Automatische Health-Checks
Das Setup-Script führt automatische Validierung durch:
- ✅ Docker-Verbindung
- ✅ Container-Startup
- ✅ Service-Erreichbarkeit
- ✅ Desktop-Verfügbarkeit

#### Manuelle Validierung
```bash
# Container-Status
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

# Service-Endpoints testen
curl -s http://localhost:8080 | grep -q "Guacamole" && echo "✅ Guacamole OK"

# Desktop-Logs prüfen
docker logs desktop --tail 20

# AI-Services testen (über Desktop-Browser später)
```

## 🖥️ Erste Nutzung

### Desktop-Zugriff

#### Schritt 1: Browser öffnen
```
URL: http://localhost:8080
```

#### Schritt 2: Guacamole-Anmeldung
```
Benutzername: guacadmin
Passwort: guacadmin
```

#### Schritt 3: Desktop-Verbindung erstellen
1. **Settings** → **Connections** → **New Connection**
2. **Connection Settings**:
   - Name: `Linux Desktop`
   - Protocol: `VNC`
   - Hostname: `desktop`
   - Port: `5901`
   - Password: `password`
3. **Save** und **Connect**

### Editor-Setup

#### Zed-Editor
```bash
# Im Desktop-Terminal
zed --version

# Erstes Projekt öffnen
cd /home/kasm-user/Projects/
mkdir hello-world
cd hello-world
echo 'print("Hello Workspace!")' > hello.py
zed .
```

#### VS Code
```bash
# Im Desktop-Terminal
code --version

# Extensions installieren (falls noch nicht automatisch installiert)
code --install-extension ms-python.python
code --install-extension rust-lang.rust-analyzer

# Projekt öffnen
code /home/kasm-user/Projects/
```

### AI-Services testen

#### N8N-Zugriff
1. **Desktop-Browser** öffnen
2. **Bookmark**: N8N Workflows oder http://n8n:5678
3. **Account erstellen** (nur lokale Anmeldung)
4. **Vorkonfigurierte Workflows** testen

#### Open WebUI
1. **Desktop-Browser**: http://open-webui:8080
2. **Account erstellen**
3. **Chat mit Ollama-Modellen**
4. **File-Upload für RAG testen**

#### Ollama-Test
```bash
# Im Desktop-Terminal
curl -X POST http://ollama:11434/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "model": "llama3.1",
    "prompt": "Hello, how are you?",
    "stream": false
  }'
```

## 🔧 Anpassungen

### Editor-Präferenz ändern

#### Zur Laufzeit wechseln
```bash
# Im Desktop beide Editoren verfügbar:
zed my-project/     # Zed verwenden
code my-project/    # VS Code verwenden
```

#### Standard-Editor ändern
```bash
# .env-Datei anpassen
echo "SELECTED_EDITOR=vscode" >> .env  # oder =zed

# Container neu bauen
docker-compose build desktop
docker-compose up -d desktop
```

### Service-Profile anpassen

#### Zusätzliche Features aktivieren
```bash
# Produktivitäts-Tools hinzufügen
docker-compose --profile cpu --profile desktop --profile productivity up -d

# Development-Tools
docker-compose --profile cpu --profile desktop --profile development up -d

# Vollständiger Stack
docker-compose --profile cpu --profile desktop --profile productivity --profile development --profile observability up -d
```

#### Services deaktivieren
```bash
# Nur Core-Services
docker-compose up -d guacamole guacd guacamole-db desktop n8n ollama-cpu open-webui qdrant db kong

# Spezifische Services stoppen
docker stop appflowy affine gitlab
```

### Ressourcen-Limits

#### Memory-Limits setzen
```bash
# docker-compose.yml anpassen
services:
  desktop:
    deploy:
      resources:
        limits:
          memory: 4G
        reservations:
          memory: 2G

  ollama:
    deploy:
      resources:
        limits:
          memory: 8G
        reservations:
          memory: 4G
```

#### CPU-Limits
```bash
services:
  desktop:
    cpus: '2.0'

  ollama:
    cpus: '4.0'
```

## 🐛 Häufige Setup-Probleme

### Docker-Probleme

#### "Permission denied" Fehler
```bash
# User zur Docker-Gruppe hinzufügen
sudo usermod -aG docker $USER
newgrp docker

# Oder temporär mit sudo
sudo docker-compose up -d
```

#### "Port already in use"
```bash
# Port-Nutzung prüfen
sudo netstat -tlnp | grep :8080
sudo lsof -i :8080

# Conflicting Service stoppen
sudo systemctl stop apache2  # oder nginx, oder anderen Service
```

### GPU-Setup-Probleme

#### NVIDIA-GPU nicht erkannt
```bash
# NVIDIA-Driver prüfen
nvidia-smi

# Docker-GPU-Support testen
docker run --rm --gpus all nvidia/cuda:11.0-base nvidia-smi

# Falls Fehler: nvidia-container-runtime neu installieren
sudo apt remove nvidia-docker2
sudo apt install nvidia-docker2
sudo systemctl restart docker
```

#### AMD-GPU Probleme
```bash
# ROCm-Installation prüfen
rocm-smi

# Device-Permissions prüfen
ls -la /dev/kfd /dev/dri/

# User zu render-Gruppe hinzufügen
sudo usermod -a -G render,video $USER
```

### Setup-Script-Probleme

#### Python-Fehler
```bash
# Python-Version prüfen
python3 --version  # Sollte 3.8+ sein

# Required modules installieren
pip3 install requests docker-compose

# Oder mit System-Package-Manager
sudo apt install python3-requests
```

#### Setup hängt bei Service-Start
```bash
# Manuell debuggen
docker-compose up -d --no-deps guacamole
docker logs guacamole

# Container einzeln starten
docker-compose up -d guacamole-db
sleep 10
docker-compose up -d guacd
sleep 5
docker-compose up -d guacamole
```

### Erste-Nutzung-Probleme

#### Guacamole-Login fehlschlägt
```bash
# Container-Status prüfen
docker logs guacamole
docker logs guacamole-db

# Database-Initialisierung prüfen
docker exec guacamole-db psql -U guacamole_user guacamole_db -c "\dt"

# Passwort zurücksetzen (falls nötig)
docker exec guacamole-db psql -U guacamole_user guacamole_db -c "
UPDATE guacamole_user SET password_hash = SHA2('guacadmin', 256) WHERE username = 'guacadmin';"
```

#### Desktop-Verbindung schlägt fehl
```bash
# Desktop-Container prüfen
docker logs desktop
docker exec desktop ps aux | grep vnc

# VNC-Port testen
docker exec desktop ss -tlnp | grep 5901

# Desktop-Container neustarten
docker restart desktop
```

## 🚀 Nächste Schritte

Nach erfolgreichem Setup:

1. **[Desktop-Verwendung](DESKTOP.md)** - Detaillierte Desktop-Nutzung
2. **[Editor-Guide](EDITORS.md)** - Zed/VS Code Konfiguration
3. **[AI-Services](../README.md#ai-services)** - N8N, Ollama, RAG-Setup
4. **[Development](../README.md#development)** - Eigene Projekte entwickeln
5. **[Troubleshooting](TROUBLESHOOTING.md)** - Problem-Lösung

**🎉 Willkommen in Ihrem Workspace-in-a-Box!**
