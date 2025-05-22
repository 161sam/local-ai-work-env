#!/bin/bash
# transform-repository.sh
# Komplette Repository-Transformation zu Workspace-in-a-Box

set -e

echo "🚀 Workspace-in-a-Box Repository Transformation"
echo "=============================================="

# Farben für Output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

confirm_action() {
    echo -e "${YELLOW}⚠️  $1${NC}"
    read -p "Continue? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "❌ Transformation cancelled."
        exit 1
    fi
}

# Schritt 1: Backup erstellen
echo -e "${BLUE}📦 Creating backup...${NC}"
BACKUP_BRANCH="backup-before-workspace-$(date +%Y%m%d_%H%M%S)"
git checkout -b "$BACKUP_BRANCH"
git add -A
git commit -m "Backup before Workspace-in-a-Box transformation"
echo -e "${GREEN}✅ Backup created on branch: $BACKUP_BRANCH${NC}"

# Zurück zum main branch
git checkout main

# Schritt 2: Services stoppen
echo -e "${BLUE}🛑 Stopping existing services...${NC}"
python start_services.py --profile cpu down 2>/dev/null || true
docker-compose -f work-env/docker-compose-extended.yml down 2>/dev/null || true
docker-compose -f work-env/docker-compose.yml down 2>/dev/null || true
docker system prune -f
echo -e "${GREEN}✅ Services stopped${NC}"

# Schritt 3: Neue Verzeichnisstruktur erstellen
echo -e "${BLUE}📁 Creating new directory structure...${NC}"

# Desktop-Umgebung
mkdir -p desktop/{editor-config/{zed,vscode},desktop-shortcuts,dev-tools,projects,scripts}

# Datenbank
mkdir -p database/init

# Guacamole
mkdir -p guacamole/init

# Scripts
mkdir -p scripts

# N8N erweitern
mkdir -p n8n/{templates,tools}

# Shared Ordner
mkdir -p desktop-shared

# Dokumentation
mkdir -p docs

echo -e "${GREEN}✅ Directory structure created${NC}"

# Schritt 4: Dateien verschieben
echo -e "${BLUE}📦 Moving files...${NC}"

# Scripts verschieben
if [ -f "work-env/generate-env.sh" ]; then
    mv work-env/generate-env.sh scripts/
    echo "  📄 Moved generate-env.sh to scripts/"
fi

# N8N Workflow Templates
if [ -f "Local_RAG_AI_Agent_n8n_Workflow.json" ]; then
    mv Local_RAG_AI_Agent_n8n_Workflow.json n8n/templates/
    echo "  📄 Moved workflow template to n8n/templates/"
fi

# N8N Tool Workflows verschieben
if [ -d "n8n-tool-workflows" ]; then
    mv n8n-tool-workflows/* n8n/tools/ 2>/dev/null || true
    rmdir n8n-tool-workflows 2>/dev/null || true
    echo "  📄 Moved tool workflows to n8n/tools/"
fi

# Flowise Tools organisieren
if [ -d "flowise" ]; then
    echo "  📄 Flowise directory kept in place"
fi

echo -e "${GREEN}✅ Files moved${NC}"

# Schritt 5: Alte Dateien löschen
echo -e "${BLUE}🗑️  Removing redundant files...${NC}"

# READMEs umbenennen (Backup)
if [ -f "README.md" ]; then
    mv README.md README-original.md
    echo "  📄 Renamed README.md to README-original.md"
fi

if [ -f "READMEfork.md" ]; then
    mv READMEfork.md READMEfork-original.md
    echo "  📄 Renamed READMEfork.md to READMEfork-original.md"
fi

# Alten start_services.py umbenennen
if [ -f "start_services.py" ]; then
    mv start_services.py start_services-original.py
    echo "  📄 Renamed start_services.py to start_services-original.py"
fi

# Docker-Compose sichern und entfernen
if [ -f "docker-compose.yml" ]; then
    mv docker-compose.yml docker-compose-original.yml
    echo "  📄 Renamed docker-compose.yml to docker-compose-original.yml"
fi

# work-env Verzeichnis komplett entfernen
if [ -d "work-env" ]; then
    rm -rf work-env/
    echo "  📄 Removed work-env/ directory"
fi

echo -e "${GREEN}✅ Cleanup completed${NC}"

# Schritt 6: Platzhalter für neue Dateien erstellen
echo -e "${BLUE}📝 Creating file placeholders...${NC}"

# README Platzhalter
cat > README.md << 'EOF'
# 🚀 Workspace-in-a-Box - AI Development Environment

## Quick Start

```bash
# 1. Configure environment
cp .env.example .env
# Edit .env with your settings

# 2. Start workspace with editor selection
python setup_workspace.py --profile cpu

# 3. Access desktop
# Browser: http://localhost:8080
# Login: guacadmin/guacadmin
```

**TODO**: Complete this README with full documentation
EOF

# Setup-Skript Platzhalter
cat > setup_workspace.py << 'EOF'
#!/usr/bin/env python3
"""
Workspace-in-a-Box Setup Script
TODO: Add the complete setup script from chat
"""

print("🚀 Workspace-in-a-Box Setup")
print("TODO: Implement complete setup script")
EOF
chmod +x setup_workspace.py

# Docker-Compose Platzhalter
cat > docker-compose.yml << 'EOF'
# Workspace-in-a-Box Docker Compose Configuration
# TODO: Add the complete docker-compose.yml from chat

version: '3.8'

networks:
  localai:
    driver: bridge
    name: localai

# TODO: Add all services, volumes, etc.
EOF

# Desktop Dockerfile Platzhalter
cat > desktop/Dockerfile.desktop << 'EOF'
# Workspace-in-a-Box Desktop Container
# TODO: Add the complete Dockerfile from chat

FROM kasmweb/desktop:1.15.0-rolling

# TODO: Add editor installation and configuration
EOF

# .env.example erweitern
cat >> .env.example << 'EOF'

############
# [NEW] Workspace-in-a-Box Configuration
############

# Editor Selection (zed or vscode)
SELECTED_EDITOR=zed

# Desktop Environment
DESKTOP_PASSWORD=password
DESKTOP_TIMEZONE=Europe/Berlin

# Guacamole
GUAC_POSTGRES_PASSWORD=secure-guacamole-password

# TODO: Add complete extended configuration
EOF

echo -e "${GREEN}✅ Placeholders created${NC}"

# Schritt 7: Git Status anzeigen
echo -e "${BLUE}📊 Repository status:${NC}"
git status --short

# Schritt 8: Nächste Schritte
echo ""
echo -e "${YELLOW}🎯 TRANSFORMATION COMPLETE!${NC}"
echo ""
echo -e "${BLUE}📋 NEXT STEPS:${NC}"
echo "1. Replace placeholder files with complete content from chat:"
echo "   - docker-compose.yml"
echo "   - setup_workspace.py" 
echo "   - desktop/Dockerfile.desktop"
echo "   - desktop/install-editors.sh"
echo "   - Complete .env.example"
echo ""
echo "2. Test the setup:"
echo "   python setup_workspace.py --profile cpu"
echo ""
echo "3. Commit changes:"
echo "   git add -A"
echo "   git commit -m 'Transform to Workspace-in-a-Box setup'"
echo ""
echo -e "${GREEN}🚀 Your repository is ready for Workspace-in-a-Box!${NC}"

# Optional: Zeige Datei-Änderungen
echo ""
echo -e "${BLUE}📈 Files changed:${NC}"
echo "Added:"
find . -name "*.py" -o -name "*.yml" -o -name "*.md" | grep -E "(setup_workspace|docker-compose)" | head -10
echo ""
echo "Moved:"
echo "  work-env/generate-env.sh → scripts/generate-env.sh"
echo "  n8n-tool-workflows/* → n8n/tools/"
echo ""
echo "Removed:"  
echo "  work-env/ (entire directory)"
echo "  Redundant docker-compose files"
