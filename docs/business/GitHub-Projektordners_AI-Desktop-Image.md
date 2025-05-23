
---

## 📁 Projektstruktur: `ai-desktop-cloud-init`

```
ai-desktop-cloud-init/
├── README.md
├── cloud-init/
│   ├── user-data.yaml
│   └── meta-data (leer oder optional)
├── compose/
│   ├── docker-compose.yml
│   └── .env (optional)
├── scripts/
│   ├── install-zed.sh
│   ├── prepare.sh
│   └── startup.sh
└── resources/
    └── zed-latest.deb (optional Download-Verweis)
```

---

## 📜 `README.md` (Auszug)

```markdown
# AI Desktop Cloud-Init Image

Cloud-init konfiguriertes Ubuntu-Desktop-Image für OpenStack, mit vorkonfiguriertem AI-Toolstack in Docker Containern.

## Enthaltene Services

- Ollama (LLMs)
- Qdrant (Vektordatenbank)
- Open WebUI (Chat-Interface)
- N8N (Workflow Automation)
- Flowise (Langchain GUI)
- SearXNG (Privacy-Suche)
- Supabase (BaaS)
- Zed Editor
- GitLab (Lightweight Setup)

## Anleitung

1. Passe `cloud-init/user-data.yaml` mit deinem SSH-Key an
2. Erzeuge ein ISO oder `cloud-localds` Image
3. Starte mit `virt-install` oder lade in Glance (OpenStack)
```

---

## 🗂️ `cloud-init/user-data.yaml`

```yaml
#cloud-config
users:
  - name: ubuntu
    groups: sudo, docker
    shell: /bin/bash
    sudo: ['ALL=(ALL) NOPASSWD:ALL']
    ssh_authorized_keys:
      - ssh-rsa AAAA...your_key_here...

write_files:
  - path: /opt/ai-workspace/docker-compose.yml
    permissions: '0644'
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
        flowise:
          image: flowiseai/flowise
          ports: ["3000:3000"]
      volumes:
        ollama_data:

runcmd:
  - bash /opt/scripts/prepare.sh
  - docker compose -f /opt/ai-workspace/docker-compose.yml up -d
```

---

## 🧩 `scripts/prepare.sh`

```bash
#!/bin/bash
set -e

apt update
apt install -y docker.io docker-compose curl unzip git
usermod -aG docker ubuntu
systemctl enable docker

# Optional: Zed Editor
bash /opt/scripts/install-zed.sh
```

---

## ⚙️ `scripts/install-zed.sh`

```bash
#!/bin/bash
wget -qO zed.deb https://github.com/zed-industries/zed/releases/latest/download/Zed.deb
dpkg -i zed.deb || apt --fix-broken install -y
rm zed.deb
```

---

## ➕ Optional: `resources/zed-latest.deb`

→ Statt per `wget`, kannst du auch eine lokale Kopie einfügen (nicht nötig, aber empfohlen wenn kein Internet)

---

## 📥 Bereitstellung

### ISO erzeugen:

```bash
cloud-localds user-data.img cloud-init/user-data.yaml
```

### OpenStack:

```bash
openstack image create "ai-desktop" \
  --file ubuntu-base.qcow2 \
  --disk-format qcow2 \
  --container-format bare \
  --public
```

---
