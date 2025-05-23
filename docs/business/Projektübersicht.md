

# 🔍 **Projektübersicht: Self-Hosted AI Workspace Cloud mit OpenStack**

---

## 🎯 **Projektziel**

Du planst den Aufbau einer **skalierbaren, sicheren und containerisierten AI-Workspace-Cloud** auf Basis von **OpenStack**. Ziel ist es, **Enterprise-Nutzern über den Browser eine vollständige Linux-Desktopumgebung** mit zahlreichen AI- und Productivity-Tools bereitzustellen – **pro Nutzer isoliert, GPU-beschleunigt, in VMs virtualisiert, services containerisiert**.

Langfristig soll das Setup auf **18 physische Nodes** skaliert werden, derzeit wird mit **2 leistungsstarken Servern + einem Raspberry Pi** eine **Testumgebung** aufgebaut.

---

## 🏗️ **Zielarchitektur**

### 🔧 Dienste pro User-Workspace (alle in Docker-Containern in der VM):

| Kategorie           | Services                                                 |
| ------------------- | -------------------------------------------------------- |
| **AI Services**     | Ollama (LLMs), Qdrant (Vector DB), Flowise, Open WebUI   |
| **Automation**      | N8N (Workflows)                                          |
| **Productivity**    | AppFlowy, AFFINE, OpenProject                            |
| **Developer Tools** | Zed Editor, GitLab CE                                    |
| **Search/Browser**  | SearXNG (metasuche), Supabase (BaaS), Langfuse (Logging) |

### 🧑‍💼 Nutzer erhalten:

* eine **vollständige Desktop-VM** (z. B. Ubuntu XFCE via VNC/Web)
* Zugriff über **Browser (Guacamole oder Kasm)**
* Vorinstallierte Containerdienste je Service
* Zugriff auf `/shared`, Modellcache, Git-Projekte

---

## 🧰 **Kerntechnologien**

| Ebene                | Technologie                                 |
| -------------------- | ------------------------------------------- |
| **Virtualisierung**  | OpenStack (Nova, Glance, Neutron, Keystone) |
| **Netzwerk**         | Neutron (VXLAN), Floating IPs, NAT          |
| **Containerdienste** | Docker, Podman (in User-VMs)                |
| **Storage**          | Aktuell NFS via Raspberry Pi, später Ceph   |
| **GPU**              | NVIDIA via passthrough (Ollama + LLMs)      |
| **Monitoring**       | Prometheus, Loki, Grafana, Alertmanager     |
| **Secrets**          | Vault (später)                              |

---

## 📦 **Hardwareplanung**

| Phase     | Ressourcen                                                                               |
| --------- | ---------------------------------------------------------------------------------------- |
| **Jetzt** | 2 Server (i7/i9 mit je 64 GB RAM, 1 GPU) + Pi 4                                          |
| **Ziel**  | 18 Nodes mit spezialisierter Rolle pro Node (GPU, Storage, Service, Control, Image Pool) |

> Besonderheit: Du willst **OpenStack direkt und vollständig installieren**, nicht über DevStack oder Kolla.

---

## 📁 **Storage Strategie**

### Jetzt:

* Raspberry Pi als NFS-Server oder MinIO für `/shared`, Modell-Cache, Backups

### Später:

* **Ceph-Cluster (3+ Nodes)** für:

  * RBD Volumes (für Cinder)
  * CephFS (für Nutzer-Dateien)
  * RGW (für S3-kompatible Modelle, Logs)

**Anforderungen pro Ceph-Node:**

* 4–8 vCPU, 16–32 GB RAM, 2–4 Disks
* System-SSD 240–512 GB **nicht** für OSDs nutzen
* OSDs: 2×4 TB HDDs empfohlen

---

## 🧪 **Testumgebung (Ist-Zustand)**

| Node  | Rollen                               |
| ----- | ------------------------------------ |
| node1 | OpenStack Controller + Compute       |
| node2 | Compute + GPU (für Ollama etc.)      |
| rpi4  | NFS oder MinIO als einfacher Storage |

Ziel: Mit 2 Nodes vollständigen Stack inkl. Floating IPs, VXLAN, Glance, Nova, Neutron und Horizon bereitstellen.

---

## 📦 **Deploymentplan (Test zu Produktion)**

| Phase  | Inhalte                                                                 |
| ------ | ----------------------------------------------------------------------- |
| **1.** | Bare-Metal OpenStack Setup (keystone, nova, neutron, horizon)           |
| **2.** | Bereitstellung eines Golden Images (Ubuntu XFCE + Docker Compose Setup) |
| **3.** | Webzugriff über Guacamole                                               |
| **4.** | GPU-Passthrough + Containerized Ollama LLMs                             |
| **5.** | Einbindung rpi4 als NFS für `/shared` und Modell-Speicher               |
| **6.** | Service-Isolation pro Nutzer via Podman/Docker                          |
| **7.** | Observability via Prometheus + Loki                                     |
| **8.** | Migration auf Ceph + Multi-Node-Ausbau (3, 6, ... → 18 Nodes)           |

---

## 🔐 **Sicherheitsstrategie (vorgesehen)**

* Pro User eigene VM
* Keine Dienste exposed außer über Floating IP / Guacamole
* Auth via OpenStack/Keycloak/OAuth2-Proxy (optional)
* Ceph mit verschlüsselten OSDs (später)
* Vault zur Secret-Verwaltung (später)
* LLM-Monitoring mit Langfuse + Logging mit Loki

---

## 📄 Nächste Umsetzungsbausteine (bereitstellbar)

| Baustein                                  | Status / Anmerkung |
| ----------------------------------------- | ------------------ |
| `cloud-init`-VM-Image mit AI-Toolchain    | Bereitstellbar     |
| OpenStack-Ansible-Setup für 2 Nodes       | Bereitstellbar     |
| `docker-compose.yml` für alle AI-Services | Bereitstellbar     |
| `cephadm`-Bootstrap-Script für später     | Bereitstellbar     |
| Guacamole + OAuth2-Proxy Deployment       | Bereitstellbar     |
| System-Partitionierungs-/fstab-Vorlage    | Bereitstellbar     |

---

## ✅ Empfohlener nächster Schritt

**Empfehlung:**

> Starte mit einem **Golden Image mit cloud-init**, in dem **alle AI-Tools vorkonfiguriert sind**, um deine erste OpenStack-VM zu testen und den Nutzer-Workflow zu validieren.

Alternativ oder parallel:

* Konfiguriere Nova/Neutron und Floating IPs
* Bereite Guacamole-Zugang via VNC vor

---

### Nächste Schritte:

1. 🖥️ `cloud-init`-fertiges AI-Desktop-Image?
2. ⚙️ `docker-compose.yml` für alle Tools in der VM?
3. 📜 OpenStack-Ansible-Setup für `node1` + `node2`?
4. 🧊 Ceph-Cluster-Vorbereitung (3 Node-Simulation)?

