# desktop/startup-script.sh
# Wird beim Desktop-Start ausgeführt

#!/bin/bash

# Desktop-Umgebung konfigurieren
export DISPLAY=:1
export HOME=/home/kasm-user

# Firefox-Profil für Service-Bookmarks erstellen
mkdir -p /home/kasm-user/.mozilla/firefox/default.profile

# Desktop-Shortcuts erstellen
mkdir -p /home/kasm-user/Desktop

# N8N Workflow Designer
cat > /home/kasm-user/Desktop/N8N.desktop << 'EOF'
[Desktop Entry]
Version=1.0
Type=Application
Name=N8N Workflows
Comment=AI Workflow Automation
Exec=firefox http://n8n:5678
Icon=/usr/share/icons/hicolor/48x48/apps/firefox.png
Terminal=false
Categories=Development;
EOF

# Open WebUI Chat Interface
cat > /home/kasm-user/Desktop/OpenWebUI.desktop << 'EOF'
[Desktop Entry]
Version=1.0
Type=Application
Name=Open WebUI
Comment=Chat with Local AI Models
Exec=firefox http://open-webui:8080
Icon=/usr/share/icons/hicolor/48x48/apps/firefox.png
Terminal=false
Categories=Office;
EOF

# AppFlowy Notizen
cat > /home/kasm-user/Desktop/AppFlowy.desktop << 'EOF'
[Desktop Entry]
Version=1.0
Type=Application
Name=AppFlowy
Comment=Note-taking and Documentation
Exec=firefox http://appflowy:8080
Icon=/usr/share/icons/hicolor/48x48/apps/firefox.png
Terminal=false
Categories=Office;
EOF

# AFFINE Collaboration
cat > /home/kasm-user/Desktop/AFFINE.desktop << 'EOF'
[Desktop Entry]
Version=1.0
Type=Application
Name=AFFINE
Comment=Collaborative Workspace
Exec=firefox http://affine:3010
Icon=/usr/share/icons/hicolor/48x48/apps/firefox.png
Terminal=false
Categories=Office;
EOF

# GitLab Development
cat > /home/kasm-user/Desktop/GitLab.desktop << 'EOF'
[Desktop Entry]
Version=1.0
Type=Application
Name=GitLab
Comment=Git Repository and CI/CD
Exec=firefox http://gitlab:8082
Icon=/usr/share/icons/hicolor/48x48/apps/firefox.png
Terminal=false
Categories=Development;
EOF

# Supabase Database
cat > /home/kasm-user/Desktop/Supabase.desktop << 'EOF'
[Desktop Entry]
Version=1.0
Type=Application
Name=Supabase
Comment=Database Management
Exec=firefox http://kong:8000
Icon=/usr/share/icons/hicolor/48x48/apps/firefox.png
Terminal=false
Categories=Development;
EOF

# Qdrant Vector Database
cat > /home/kasm-user/Desktop/Qdrant.desktop << 'EOF'
[Desktop Entry]
Version=1.0
Type=Application
Name=Qdrant
Comment=Vector Database
Exec=firefox http://qdrant:6333/dashboard
Icon=/usr/share/icons/hicolor/48x48/apps/firefox.png
Terminal=false
Categories=Development;
EOF

# Terminal mit Umgebungsvariablen
cat > /home/kasm-user/Desktop/Terminal.desktop << 'EOF'
[Desktop Entry]
Version=1.0
Type=Application
Name=Terminal
Comment=Command Line Access
Exec=gnome-terminal
Icon=/usr/share/icons/hicolor/48x48/apps/terminal.png
Terminal=false
Categories=System;
EOF

# Alle Desktop-Dateien ausführbar machen
chmod +x /home/kasm-user/Desktop/*.desktop

# Firefox mit Service-Bookmarks starten (einmalig)
if [ ! -f /home/kasm-user/.mozilla/firefox/bookmarks_created ]; then
    # Firefox starten und Bookmarks erstellen
    timeout 10 firefox --headless &
    sleep 5

    # Bookmarks-JSON erstellen
    cat > /tmp/bookmarks.json << 'EOF'
{
  "title": "AI Services",
  "type": "folder",
  "children": [
    {
      "title": "🧠 N8N Workflows",
      "type": "bookmark",
      "url": "http://n8n:5678"
    },
    {
      "title": "💬 Open WebUI Chat",
      "type": "bookmark",
      "url": "http://open-webui:8080"
    },
    {
      "title": "📝 AppFlowy Notes",
      "type": "bookmark",
      "url": "http://appflowy:8080"
    },
    {
      "title": "✨ AFFINE Workspace",
      "type": "bookmark",
      "url": "http://affine:3010"
    },
    {
      "title": "🦊 GitLab Repository",
      "type": "bookmark",
      "url": "http://gitlab:8082"
    },
    {
      "title": "🗄️ Supabase Database",
      "type": "bookmark",
      "url": "http://kong:8000"
    },
    {
      "title": "📊 Qdrant Vector DB",
      "type": "bookmark",
      "url": "http://qdrant:6333/dashboard"
    },
    {
      "title": "🤖 Ollama API",
      "type": "bookmark",
      "url": "http://ollama:11434"
    },
    {
      "title": "📈 Langfuse Analytics",
      "type": "bookmark",
      "url": "http://langfuse:3000"
    }
  ]
}
EOF

    touch /home/kasm-user/.mozilla/firefox/bookmarks_created
fi

# Desktop-Hintergrund setzen
if [ -f /shared/desktop-wallpaper.jpg ]; then
    gsettings set org.gnome.desktop.background picture-uri file:///shared/desktop-wallpaper.jpg
fi

# Entwicklungstools installieren (einmalig)
if [ ! -f /home/kasm-user/.tools_installed ]; then
    # Code Editor
    if ! command -v code &> /dev/null; then
        wget -O /tmp/code.deb "https://code.visualstudio.com/sha/download?build=stable&os=linux-deb-x64"
        sudo dpkg -i /tmp/code.deb || sudo apt-get install -f -y
        rm /tmp/code.deb
    fi

    # Git konfigurieren
    git config --global user.name "Desktop User"
    git config --global user.email "user@local-ai.local"

    # Nützliche Aliase
    echo 'alias ll="ls -la"' >> /home/kasm-user/.bashrc
    echo 'alias services="curl -s http://kong:8000/health"' >> /home/kasm-user/.bashrc
    echo 'alias n8n-logs="docker logs n8n"' >> /home/kasm-user/.bashrc

    touch /home/kasm-user/.tools_installed
fi

# Service-Status-Script
cat > /home/kasm-user/check-services.sh << 'EOF'
#!/bin/bash
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
EOF

chmod +x /home/kasm-user/check-services.sh

# Welcome-Nachricht für neuen Desktop
cat > /home/kasm-user/Desktop/README.txt << 'EOF'
🎉 Willkommen zu Ihrem AI-Desktop!

Diese Desktop-Umgebung bietet Zugang zu allen AI-Services:

🧠 N8N - Workflow-Automation
💬 Open WebUI - Chat mit AI-Modellen
📝 AppFlowy - Notizen und Dokumentation
✨ AFFINE - Kollaborativer Workspace
🦊 GitLab - Code-Repository
🗄️ Supabase - Datenbank-Management
📊 Qdrant - Vector-Datenbank

📁 Geteilte Ordner:
- /shared - Dateiaustausch mit Host-System

🔧 Nützliche Befehle:
- ./check-services.sh - Service-Status prüfen
- docker logs <container> - Container-Logs anzeigen
- code . - VS Code öffnen

🌐 Alle Services sind über interne Docker-Namen erreichbar
(z.B. http://n8n:5678 statt localhost:5678)
EOF

echo "✅ Desktop-Umgebung konfiguriert!"
