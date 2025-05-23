

## 🖥️ **Ziel: Goldenes AI-Desktop-Image für OpenStack (cloud-init ready)**

---

### 📌 **Basisdaten**

| Eigenschaft           | Wert                                                                   |
| --------------------- | ---------------------------------------------------------------------- |
| **OS**                | Ubuntu 22.04 LTS (Minimal, Server oder Desktop)                        |
| **UI**                | XFCE (leichtgewichtig, VNC-kompatibel)                                 |
| **Login**             | via cloud-init SSH oder GUI (LightDM)                                  |
| **Tools**             | Docker, Compose, Zed, Git, Node, Python                                |
| **Services (Docker)** | Ollama, N8N, Qdrant, Open WebUI, Supabase, Flowise, GitLab CE, SearXNG |

---

## ⚙️ **1. System vorbereiten**

### 🧰 Pakete installieren:

```bash
# Basis
apt update && apt install -y sudo curl git wget unzip ufw

# GUI
apt install -y xfce4 lightdm lightdm-gtk-greeter xterm

# Netzwerk-Tools
apt install -y net-tools openssh-server

# Docker
curl -fsSL https://get.docker.com | bash
usermod -aG docker ubuntu

# Docker Compose
curl -L "https://github.com/docker/compose/releases/download/v2.24.6/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

# Optional: Zed Editor (manuell, oder Skript siehe unten)
```

---

## 📁 **2. Docker Services: `docker-compose.yml`**

Erstelle unter `/opt/ai-workspace/docker-compose.yml` folgendes Beispiel:

```yaml
version: "3.8"

services:
  ollama:
    image: ollama/ollama
    ports:
      - "11434:11434"
    volumes:
      - ollama_data:/root/.ollama
    deploy:
      resources:
        reservations:
          devices:
            - capabilities: [gpu]

  n8n:
    image: n8nio/n8n
    ports:
      - "5678:5678"
    environment:
      - N8N_BASIC_AUTH_ACTIVE=true
      - N8N_BASIC_AUTH_USER=admin
      - N8N_BASIC_AUTH_PASSWORD=admin

  qdrant:
    image: qdrant/qdrant
    ports:
      - "6333:6333"

  open-webui:
    image: ghcr.io/open-webui/open-webui:main
    ports:
      - "8080:8080"

  flowise:
    image: flowiseai/flowise
    ports:
      - "3000:3000"

  searxng:
    image: searxng/searxng
    ports:
      - "8081:8080"

volumes:
  ollama_data:
```

---

## 📜 **3. cloud-init Konfiguration**

```yaml
#cloud-config
users:
  - name: ubuntu
    groups: sudo, docker
    shell: /bin/bash
    sudo: ['ALL=(ALL) NOPASSWD:ALL']
    ssh_authorized_keys:
      - ssh-rsa AAAA...  # <-- deinen SSH Key einfügen

write_files:
  - path: /opt/ai-workspace/docker-compose.yml
    content: |
      version: "3.8"
      services:
        ollama:
          image: ollama/ollama
          ports: ["11434:11434"]
          volumes: ["ollama_data:/root/.ollama"]
        qdrant:
          image: qdrant/qdrant
          ports: ["6333:6333"]
        open-webui:
          image: ghcr.io/open-webui/open-webui:main
          ports: ["8080:8080"]
      volumes:
        ollama_data:

runcmd:
  - mkdir -p /opt/ai-workspace
  - docker compose -f /opt/ai-workspace/docker-compose.yml up -d
```

---

## 🧪 **4. Image-Erstellung (lokal, z. B. via QEMU oder virt-install)**

```bash
# Mit Ubuntu Cloud Image (https://cloud-images.ubuntu.com/jammy/current/)
wget https://cloud-images.ubuntu.com/jammy/current/jammy-server-cloudimg-amd64.img -O ai-desktop-base.img

# cloud-localds erzeugen
cloud-localds user-data.img user-data.yaml

# Testweise starten:
qemu-system-x86_64 \
  -m 4096 -smp 4 -enable-kvm \
  -drive file=ai-desktop-base.img,format=qcow2 \
  -drive file=user-data.img,format=raw \
  -nic user,model=virtio \
  -nographic
```

---

## 💾 **5. Upload in OpenStack (Glance)**

```bash
openstack image create "AI-Desktop" \
  --file ai-desktop-base.img \
  --disk-format qcow2 \
  --container-format bare \
  --public
```

---

## ✅ Nächste Optionen (Optional):

* Setup-Skript zur Installation von Zed Editor
* Erweiterung um Supabase, GitLab, etc.
* `cloud-init`-Autologin + VNC-Config
* GPU-Unterstützung für Docker in cloud-init automatisieren

---

### 📩 Nächste Schritte**fertiges Bundle (Image + cloud-init)** als `.qcow2` und `.yaml`:

Ich kann dir alternativ eine GitHub-Repo-Struktur liefern mit:

* `user-data.yaml`
* `docker-compose.yml`
* Zed Installer-Skript
* GPU Setup in cloud-init


