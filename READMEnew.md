# Extended AI Stack mit Guacamole Desktop

## 🎯 Überblick

Dieses Setup erweitert das [local-ai-packaged](https://github.com/coleam00/local-ai-packaged) System um:

- **🖥️ Guacamole Desktop**: Browser-Zugriff auf Linux Desktop
- **📝 AppFlowy**: Notion-Alternative
- **✨ AFFINE**: Kollaboratives Workspace-Tool  
- **🦊 GitLab**: Self-hosted Git-Repository und CI/CD
- **🔧 N8N Extended**: Zusätzliche N8N-Instanz für spezielle Workflows

## 🏗️ Architektur

```
Browser → Guacamole → Linux Desktop
                   ↙
           Lokale Services:
           ├── N8N (AI Workflows)
           ├── Open WebUI (Chat Interface)
           ├── AppFlowy (Notizen)
           ├── AFFINE (Collaboration)
           ├── GitLab (Code Repository)
           ├── Ollama (Local LLM)
           └── Qdrant (Vector Database)
```

## 🔧 Systemanforderungen

### Minimum:
- **CPU**: 4 Kerne
- **RAM**: 8 GB
- **Storage**: 50 GB freier Speicherplatz
- **Docker**: Version 20.10+
- **Docker Compose**: Version 2.0+

### Empfohlen:
- **CPU**: 8+ Kerne
- **RAM**: 16+ GB
- **Storage**: 100+ GB SSD
- **GPU**: NVIDIA GPU für Ollama (optional)

## 🚀 Schnellinstallation

### 1. Repository klonen

```bash
# Original Repository klonen
git clone https://github.com/coleam00/local-ai-packaged.git
cd local-ai-packaged

# Unsere erweiterten Dateien hinzufügen
# (Die Dateien aus den Artifacts in das Verzeichnis kopieren)
```

### 2. Umgebungsvariablen konfigurieren

```bash
# .env.extended zu .env kopieren und anpassen
cp .env.extended .env

# Wichtige Variablen setzen:
nano .env
```

**Minimale Konfiguration für .env:**
```bash
# Sichere Passwörter generieren
N8N_ENCRYPTION_KEY=$(openssl rand -base64 32)
N8N_USER_MANAGEMENT_JWT_SECRET=$(openssl rand -base64 32)
POSTGRES_PASSWORD=$(openssl rand -base64 16)
JWT_SECRET=$(openssl rand -base64 32)
WEBUI_SECRET_KEY=$(openssl rand -base64 32)

# Service-Konfiguration
GENERIC_TIMEZONE=Europe/Berlin
```

### 3. Setup ausführen

```bash
# Setup-Skript ausführen
chmod +x setup-extended-ai-stack.sh
./setup-extended-ai-stack.sh

# Stack starten (CPU-Version)
python3 start-extended-stack.py --profile cpu

# Oder mit NVIDIA GPU
python3 start-extended-stack.py --profile gpu-nvidia
```

### 4. Guacamole konfigurieren

```bash
# Guacamole-Verbindungen einrichten
./configure-guacamole.sh
```

## 🌐 Service-URLs

Nach dem Start sind folgende Services verfügbar:

| Service | URL | Beschreibung |
|---------|-----|--------------|
| **🖥️ Guacamole** | http://localhost:8080 | Desktop im Browser |
| **🧠 N8N** | http://localhost:5678 | AI Workflow-Automation |
| **💬 Open WebUI** | http://localhost:3000 | Chat mit lokalen LLMs |
| **🤖 Ollama** | http://localhost:11434 | Local LLM API |
| **📊 Qdrant** | http://localhost:6333 | Vector Database |
| **📝 AppFlowy** | http://localhost:8081 | Notion-Alternative |
| **✨ AFFINE** | http://localhost:3010 | Kollaboration |
| **🦊 GitLab** | http://localhost:8082 | Git Repository |
| **🔧 N8N Extended** | http://localhost:5679 | Erweiterte Workflows |
| **🗄️ Supabase** | http://localhost:8000 | Database Interface |

## 🔑 Standard-Zugangsdaten

### Guacamole
- **Benutzername**: `guacadmin`
- **Passwort**: `guacadmin`

### Linux Desktop (VNC)
- **Benutzername**: `kasm-user`
- **Passwort**: `password`

### GitLab
- **Benutzername**: `root`
- **Passwort**: Siehe Container-Logs mit `docker logs gitlab`

## 🖥️ Desktop-Konfiguration

### Guacamole-Verbindung einrichten:

1. **Guacamole öffnen**: http://localhost:8080
2. **Anmelden** mit `guacadmin/guacadmin`
3. **Settings** → **Connections** → **New Connection**
4. **Verbindung konfigurieren**:
   - **Name**: Linux Desktop
   - **Protocol**: VNC
   - **Hostname**: `desktop`
   - **Port**: `5901`
   - **Password**: `password`
5. **Speichern** und **Verbinden**

### Browser-Bookmarks im Desktop

Der Linux Desktop sollte folgende Bookmarks erhalten:

```bash
# Bookmarks-Datei für Firefox im Desktop erstellen
mkdir -p ./desktop-config/firefox
cat > ./desktop-config/firefox/bookmarks.html << 'EOF'
<!DOCTYPE NETSCAPE-Bookmark-file-1>
<HTML>
<HEAD>
<TITLE>Bookmarks</TITLE>
</HEAD>
<H1>Local AI Services</H1>
<DL>
    <DT><A HREF="http://n8n:5678">N8N Workflows</A>
    <DT><A HREF="http://open-webui:8080">Open WebUI Chat</A>
    <DT><A HREF="http://appflowy:8080">AppFlowy Notes</A>
    <DT><A HREF="http://affine:3010">AFFINE Workspace</A>
    <DT><A HREF="http://gitlab:8082">GitLab Repository</A>
    <DT><A HREF="http://kong:8000">Supabase API</A>
    <DT><A HREF="http://qdrant:6333">Qdrant Vector DB</A>
</DL>
EOF
```

## 🔧 Erweiterte Konfiguration

### GPU-Unterstützung aktivieren

**NVIDIA GPU:**
```bash
# NVIDIA Container Runtime installieren
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list

sudo apt-get update && sudo apt-get install -y nvidia-docker2
sudo systemctl restart docker

# Mit GPU starten
python3 start-extended-stack.py --profile gpu-nvidia
```

### Volumes und Daten-Persistierung

**Wichtige Verzeichnisse:**
- `./desktop-shared/` - Dateien zwischen Host und Desktop teilen
- `./shared/` - N8N-Workflows und -Daten
- Docker Volumes für persistente Daten

### Service-spezifische Konfiguration

**N8N Workflows:**
```bash
# Beispiel-Workflows importieren
curl -o ./shared/example-workflows.json \
  https://raw.githubusercontent.com/n8n-io/n8n/master/packages/cli/templates/workflows.json
```

**GitLab CI/CD:**
```bash
# GitLab Runner registrieren (optional)
docker exec -it gitlab gitlab-runner register
```

## 🛠️ Troubleshooting

### Häufige Probleme

**1. Guacamole zeigt "503 Service Unavailable"**
```bash
# Services neu starten
docker-compose -f docker-compose-extended.yml restart guacd guacamole
```

**2. Desktop-Verbindung schlägt fehl**
```bash
# Desktop Container überprüfen
docker logs linux-desktop
# VNC-Port testen
telnet localhost 6901
```

**3. Ollama lädt Modelle nicht**
```bash
# Modell manuell herunterladen
docker exec ollama ollama pull llama3.1
```

**4. GitLab startet nicht**
```bash
# Mehr Speicher zuweisen
docker-compose -f docker-compose-extended.yml up -d gitlab --scale gitlab=1 --memory=4g
```

### Logs überprüfen

```bash
# Alle Service-Logs
docker-compose -f docker-compose-extended.yml logs -f

# Spezifische Services
docker logs guacamole
docker logs linux-desktop
docker logs n8n
```

### Performance-Optimierung

**Für schwächere Hardware:**
```bash
# Nur Core-Services starten
python3 start-extended-stack.py --services core

# Schrittweise erweitern
python3 start-extended-stack.py --services desktop
python3 start-extended-stack.py --services extended
```

## 🔄 Updates und Wartung

### Updates durchführen

```bash
# Alle Container stoppen
docker-compose -f docker-compose-extended.yml down

# Images aktualisieren
docker-compose -f docker-compose-extended.yml pull

# Neu starten
python3 start-extended-stack.py --profile cpu
```

### Backups erstellen

```bash
# Wichtige Volumes sichern
docker run --rm -v extended-ai_n8n_data:/data -v $(pwd):/backup alpine tar czf /backup/n8n-backup.tar.gz /data

# Desktop-Daten sichern
tar czf desktop-backup.tar.gz ./desktop-shared ./shared
```

## 🤝 Beitrag und Support

### Community
- **GitHub Issues**: Probleme melden
- **Discussions**: Fragen und Ideen diskutieren

### Entwicklung
```bash
# Entwicklungsumgebung
git clone [your-fork]
cd extended-ai-stack
# Änderungen testen
docker-compose -f docker-compose-extended.yml config
```

## 📜 Lizenz

Dieses Projekt erweitert das Apache 2.0 lizenzierte local-ai-packaged System und steht unter derselben Lizenz.

---

**🎉 Viel Spaß mit Ihrem Extended AI Stack!**

Bei Fragen oder Problemen öffnen Sie gerne ein Issue oder kontaktieren Sie die Community.
