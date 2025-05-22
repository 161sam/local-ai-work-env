# desktop/install-editors.sh
# Wird im Desktop-Container ausgeführt um gewählten Editor zu installieren

#!/bin/bash
set -e

# Farben für Output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🎨 Installing Development Editor...${NC}"

# Editor-Auswahl aus Konfiguration lesen
EDITOR_CONFIG="/shared/editor-config/editor-choice.json"
if [ ! -f "$EDITOR_CONFIG" ]; then
    echo -e "${YELLOW}⚠️ No editor configuration found. Defaulting to Zed.${NC}"
    SELECTED_EDITOR="zed"
else
    SELECTED_EDITOR=$(cat "$EDITOR_CONFIG" | jq -r '.selected_editor')
fi

echo -e "${BLUE}📦 Selected editor: ${SELECTED_EDITOR}${NC}"

# System-Updates
echo -e "${BLUE}🔄 Updating system packages...${NC}"
apt-get update -qq

# Basis-Entwicklungstools installieren
echo -e "${BLUE}🛠️ Installing development tools...${NC}"
apt-get install -y -qq \
    curl \
    wget \
    git \
    build-essential \
    jq \
    unzip \
    software-properties-common \
    apt-transport-https \
    ca-certificates \
    gnupg \
    lsb-release

# Node.js und npm (für Language Servers)
echo -e "${BLUE}📦 Installing Node.js and development tools...${NC}"
curl -fsSL https://deb.nodesource.com/setup_20.x | bash -
apt-get install -y -qq nodejs

# Python-Entwicklungstools
apt-get install -y -qq \
    python3 \
    python3-pip \
    python3-venv

# Rust (für Zed und Language Servers)
echo -e "${BLUE}🦀 Installing Rust...${NC}"
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
source $HOME/.cargo/env

# Language Servers installieren
echo -e "${BLUE}🔧 Installing Language Servers...${NC}"

# TypeScript Language Server
npm install -g typescript typescript-language-server

# Python Language Server
pip3 install python-lsp-server[all] black pylint

# Rust Analyzer
rustup component add rust-analyzer

# Docker Language Server
npm install -g dockerfile-language-server-nodejs

# YAML Language Server
npm install -g yaml-language-server

# JSON Language Server
npm install -g vscode-json-languageserver

# Editor-spezifische Installation
case $SELECTED_EDITOR in
    "zed")
        echo -e "${BLUE}⚡ Installing Zed Editor...${NC}"
        install_zed
        ;;
    "vscode")
        echo -e "${BLUE}📝 Installing Visual Studio Code...${NC}"
        install_vscode
        ;;
    *)
        echo -e "${RED}❌ Unknown editor: $SELECTED_EDITOR${NC}"
        exit 1
        ;;
esac

# Desktop-Konfiguration anwenden
configure_desktop_environment

echo -e "${GREEN}✅ Editor installation completed!${NC}"

# Funktionen für Editor-Installation
install_zed() {
    # Zed für Linux installieren
    echo -e "${BLUE}⚡ Downloading Zed Editor...${NC}"

    # Neueste Zed-Version von GitHub holen
    ZED_VERSION=$(curl -s https://api.github.com/repos/zed-industries/zed/releases/latest | jq -r '.tag_name')
    ZED_URL="https://github.com/zed-industries/zed/releases/download/${ZED_VERSION}/zed-linux-x86_64.tar.gz"

    # Zed herunterladen und installieren
    cd /tmp
    wget -q "$ZED_URL" -O zed.tar.gz
    tar -xzf zed.tar.gz

    # Zed installieren
    mkdir -p /opt/zed
    cp -r zed-linux-x86_64/* /opt/zed/

    # Zed zum PATH hinzufügen
    ln -sf /opt/zed/bin/zed /usr/local/bin/zed

    # Desktop-Datei erstellen
    cat > /usr/share/applications/zed.desktop << 'EOF'
[Desktop Entry]
Version=1.0
Type=Application
Name=Zed
Comment=A high-performance, multiplayer code editor
Exec=/opt/zed/bin/zed %F
Icon=/opt/zed/share/icons/hicolor/512x512/apps/zed.png
Terminal=false
Categories=Development;TextEditor;
StartupWMClass=zed
MimeType=text/plain;text/x-chdr;text/x-csrc;text/x-c++hdr;text/x-c++src;text/x-java;text/x-dsrc;text/x-pascal;text/x-perl;text/x-python;application/x-php;application/x-httpd-php3;application/x-httpd-php4;application/x-httpd-php5;application/xml;text/html;text/css;text/x-sql;text/x-diff;
EOF

    # Berechtigungen setzen
    chmod +x /opt/zed/bin/zed
    chmod 644 /usr/share/applications/zed.desktop

    # Zed-Konfiguration kopieren
    if [ -f "/shared/editor-config/zed/settings.json" ]; then
        mkdir -p /home/kasm-user/.config/zed
        cp /shared/editor-config/zed/* /home/kasm-user/.config/zed/
        chown -R kasm-user:kasm-user /home/kasm-user/.config/zed
    fi

    # Desktop-Shortcut erstellen
    create_zed_desktop_shortcut

    echo -e "${GREEN}✅ Zed Editor installed successfully!${NC}"
}

install_vscode() {
    # VS Code für Linux installieren
    echo -e "${BLUE}📝 Installing Visual Studio Code...${NC}"

    # Microsoft GPG-Schlüssel hinzufügen
    wget -qO- https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > packages.microsoft.gpg
    install -o root -g root -m 644 packages.microsoft.gpg /etc/apt/trusted.gpg.d/

    # VS Code Repository hinzufügen
    echo "deb [arch=amd64,arm64,armhf signed-by=/etc/apt/trusted.gpg.d/packages.microsoft.gpg] https://packages.microsoft.com/repos/code stable main" > /etc/apt/sources.list.d/vscode.list

    # VS Code installieren
    apt-get update -qq
    apt-get install -y -qq code

    # VS Code-Konfiguration kopieren
    if [ -f "/shared/editor-config/vscode/settings.json" ]; then
        mkdir -p /home/kasm-user/.config/Code/User
        cp /shared/editor-config/vscode/settings.json /home/kasm-user/.config/Code/User/

        # Empfohlene Extensions installieren
        if [ -f "/shared/editor-config/vscode/extensions.json" ]; then
            EXTENSIONS=$(cat /shared/editor-config/vscode/extensions.json | jq -r '.recommendations[]')
            for ext in $EXTENSIONS; do
                sudo -u kasm-user code --install-extension "$ext" --force
            done
        fi

        chown -R kasm-user:kasm-user /home/kasm-user/.config/Code
    fi

    # Desktop-Shortcut erstellen
    create_vscode_desktop_shortcut

    echo -e "${GREEN}✅ VS Code installed successfully!${NC}"
}

create_zed_desktop_shortcut() {
    # Zed Desktop-Shortcut
    cat > /home/kasm-user/Desktop/Zed.desktop << 'EOF'
[Desktop Entry]
Version=1.0
Type=Application
Name=⚡ Zed Editor
Comment=Lightning-fast code editor
Exec=/opt/zed/bin/zed
Icon=/opt/zed/share/icons/hicolor/512x512/apps/zed.png
Terminal=false
Categories=Development;TextEditor;
StartupWMClass=zed
EOF

    chmod +x /home/kasm-user/Desktop/Zed.desktop
    chown kasm-user:kasm-user /home/kasm-user/Desktop/Zed.desktop
}

create_vscode_desktop_shortcut() {
    # VS Code Desktop-Shortcut
    cat > /home/kasm-user/Desktop/VSCode.desktop << 'EOF'
[Desktop Entry]
Version=1.0
Type=Application
Name=📝 Visual Studio Code
Comment=Code editing. Redefined.
Exec=/usr/bin/code
Icon=/usr/share/pixmaps/com.visualstudio.code.png
Terminal=false
Categories=Development;TextEditor;
StartupWMClass=code
EOF

    chmod +x /home/kasm-user/Desktop/VSCode.desktop
    chown kasm-user:kasm-user /home/kasm-user/Desktop/VSCode.desktop
}

configure_desktop_environment() {
    echo -e "${BLUE}🖥️ Configuring desktop environment...${NC}"

    # Git-Konfiguration
    sudo -u kasm-user git config --global user.name "Workspace User"
    sudo -u kasm-user git config --global user.email "user@workspace.local"
    sudo -u kasm-user git config --global init.defaultBranch main

    # Shell-Aliase für Entwicklung
    cat >> /home/kasm-user/.bashrc << 'EOF'

# Development aliases
alias ll='ls -la'
alias grep='grep --color=auto'
alias la='ls -A'
alias l='ls -CF'

# Docker aliases
alias dc='docker-compose'
alias dps='docker ps'
alias dlogs='docker logs'

# Service shortcuts
alias n8n-logs='docker logs n8n'
alias webui-logs='docker logs open-webui'
alias check-services='curl -s http://kong:8000/health || echo "Services health check failed"'

# Editor shortcuts
EOF

    # Editor-spezifische Aliase
    if [ "$SELECTED_EDITOR" = "zed" ]; then
        echo "alias edit='zed'" >> /home/kasm-user/.bashrc
        echo "alias ze='zed'" >> /home/kasm-user/.bashrc
    elif [ "$SELECTED_EDITOR" = "vscode" ]; then
        echo "alias edit='code'" >> /home/kasm-user/.bashrc
        echo "alias vs='code'" >> /home/kasm-user/.bashrc
    fi

    # Ordner-Struktur für Entwicklung
    sudo -u kasm-user mkdir -p /home/kasm-user/{Projects,Scripts,Documents,Downloads}

    # Entwicklungs-Workspace vorbereiten
    sudo -u kasm-user mkdir -p /home/kasm-user/Projects/{n8n-workflows,ai-experiments,docker-configs}

    # Shared-Ordner verlinken
    sudo -u kasm-user ln -sf /shared /home/kasm-user/shared-n8n

    echo -e "${GREEN}✅ Desktop environment configured!${NC}"
}

# Cleanup
cleanup() {
    echo -e "${BLUE}🧹 Cleaning up...${NC}"
    apt-get autoremove -y -qq
    apt-get autoclean -qq
    rm -rf /tmp/* /var/tmp/*
    rm -rf /var/lib/apt/lists/*
}

# Cleanup am Ende ausführen
trap cleanup EXIT
