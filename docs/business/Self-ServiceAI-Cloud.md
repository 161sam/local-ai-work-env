

## ✅ **Ziel: Self-Service AI Cloud mit vollständigem Browser-Desktop**

---

## 🧱 **1. Architektur-Blueprint (Rollenbasierte Cluster-Zuweisung)**

| Node-Typ       | Anzahl | Funktion                                           |
| -------------- | ------ | -------------------------------------------------- |
| `gpu-worker`   | 4      | Ollama + LLM-Services mit CUDA                     |
| `nas-node`     | 2      | Ceph / NFS / MinIO für User-Daten, Modelle, Logs   |
| `image-pool`   | 3      | OpenStack Glance + Kasm-Images für User-Desktops   |
| `service-node` | 6      | Service-Cluster (Qdrant, Langfuse, WebUI, GitLab…) |

> 💡 *Control-Plane (OpenStack Keystone, Horizon etc.) wird separat vorausgesetzt (nicht in den 15 Nodes enthalten).*

---

## 🧠 **2. Technologische Eckpunkte**

| Kategorie                      | Empfehlung                                               |
| ------------------------------ | -------------------------------------------------------- |
| **Hypervisor**                 | KVM/QEMU (via OpenStack Nova)                            |
| **Storage**                    | CephFS (user data), RBD (VM volumes), S3 API für Modelle |
| **GPU Management**             | NVIDIA vGPU / passthrough mit `nvidia-container-toolkit` |
| **Service-Orchestrierung**     | Kubernetes (k8s) auf service-nodes                       |
| **VM-Desktops**                | Kasm Workspaces, Proxmox Templates oder Cloud-init       |
| **Browser-Zugriff**            | Apache Guacamole oder Kasm, pro User-VM                  |
| **Monitoring & Observability** | Prometheus, Grafana, Loki, Alertmanager                  |

---

## 🧑‍💼 **3. Nutzeransicht (Enterprise-User)**

> Jeder Nutzer erhält über den Browser Zugriff auf **eine eigene Linux-VM mit vorkonfigurierten AI-Tools**. Diese VM enthält:

* **Zugriff via Guacamole / Kasm (Port 443)**
* **Vorinstallierte Tools (Containerisiert über Podman oder systemd-nspawn):**

  * `n8n`, `Ollama`, `Qdrant`, `Open WebUI`, `Langfuse`, `Flowise`, `SearXNG`, `GitLab`, `Zed Editor`, `AppFlowy`, `AFFINE`, `OpenProject`

🧊 *Jeder dieser Dienste läuft in einem isolierten Environment (Systemd-Unit, Podman Container oder LXD).*

---

## ⚙️ **4. Infrastrukturkomponenten**

### 🔧 Pro User Setup:

| Komponente             | Umsetzungsvorschlag                                      |
| ---------------------- | -------------------------------------------------------- |
| **Desktop-VM**         | Kasm oder QEMU-basierte Template-VM (Ubuntu Jammy, XFCE) |
| **Isolierte Services** | Podman rootless containers (user-level systemd)          |
| **Storage**            | `/mnt/shared` via CephFS, Modelle persistent             |
| **Service Access**     | via `localhost:<port>` im Browser-Desktop                |
| **User-seitig Root**   | optional, via sudo/jailkit reguliert                     |

---

### 🧑‍💻 Entwickler-Cluster (shared services)

| Service    | Bereitstellung      | Deployment-Modell               |
| ---------- | ------------------- | ------------------------------- |
| GitLab CE  | Kubernetes (Helm)   | Shared oder user-projektbasiert |
| Langfuse   | Kubernetes + S3     | Multi-Tenant möglich            |
| Ollama-API | Dedicated GPU nodes | via Kubernetes DaemonSet        |
| SearXNG    | Kubernetes          | Shared + rate-limited           |

---

## 🔐 **5. Sicherheit & Isolation**

| Aspekt                 | Maßnahme                                                        |
| ---------------------- | --------------------------------------------------------------- |
| **User-Isolation**     | Volle VM-Isolation via OpenStack Nova (nicht nur Container)     |
| **Service-Isolation**  | Jeder Service in separatem Podman-Namespace oder systemd-cgroup |
| **Netzwerk-Isolation** | VXLAN pro User-Netz + Firewall via OpenStack Security Groups    |
| **Zugangskontrolle**   | Keycloak (SSO/OIDC) + OAuth2 Proxy + Guacamole Auth             |
| **Logging & Auditing** | Loki + FluentBit + Promtail pro Node                            |

---

## 🧪 **6. Initial Setup Plan (Schritt-für-Schritt)**

1. **OpenStack-Cluster aufbauen** (Nova, Neutron, Cinder, Glance, Keystone)
2. **Ceph Storage einbinden** (für User Volumes und Shared Storage)
3. **VM-Image vorbereiten (z. B. mit cloud-init, XFCE, Kasm)**
4. **Guacamole + OAuth2 Proxy bereitstellen**
5. **Service-Vorlagen bauen (Podman + systemd units)**
6. **User-Onboarding automatisieren (Terraform + Ansible für Provisioning)**
7. **Kubernetes auf service-nodes einrichten (kubeadm + taints + labels)**
8. **Monitoring einrichten (Prometheus, Loki, Grafana mit SSO)**

---

## 🔁 **Optional: Skalierung**

* **GPU Nodes** können horizontal über OpenStack + Nova Scheduling genutzt werden.
* **Service-Nodes** skalieren über Kubernetes HPA
* **Langfristig:** Tenant Isolation per OpenStack-Projekt + RBAC

---



---

## 📐 **Beispiel-Topologie für OpenStack AI-Workspace Cloud**

---

### 🧱 **1. Node-Übersicht**

| Rolle               | Anzahl | Beschreibung                                         |
| ------------------- | ------ | ---------------------------------------------------- |
| **Control Plane**   | 3      | API, DB, Messaging, Dashboard (Keystone, Horizon...) |
| **GPU-Worker**      | 4      | AI-Inferenz (Ollama, LLMs) mit NVIDIA A100/L40S      |
| **Storage/NAS**     | 2      | Ceph Mon + OSD + RGW (für Volumes + Shared FS)       |
| **Image Pool**      | 3      | Glance-Cache + Kasm-Images + DHCP/Metadata           |
| **Service Cluster** | 6      | Kubernetes für zentrale Dienste (N8N, Langfuse...)   |

**Gesamt: 18 Nodes**

> Du wolltest 15, aber für HA ist 3× Control Plane empfohlen – wir können auch auf 1 reduzieren für Testumgebungen.

---

## 🔧 **2. Komponenten & Dienste**

### 🧭 **Control Plane (HA-Setup)**

| Komponente       | Dienst                        |
| ---------------- | ----------------------------- |
| `Keystone`       | Identity / Auth (SSO/Token)   |
| `Glance`         | Image-Repository              |
| `Nova`           | VM-Provisionierung            |
| `Neutron`        | Netzwerk-Overlay + DHCP       |
| `Horizon`        | Web-Dashboard für Admins      |
| `Cinder`         | Block Storage für Volumes     |
| `Placement`      | Ressourcen-Allokation         |
| `RabbitMQ`       | Messaging-Backbone            |
| `MariaDB/Galera` | SQL DB für OpenStack Services |
| `Memcached`      | Token-Caching                 |
| `Etcd`           | (optional, z. B. für Octavia) |

> ⚙️ Alle Control Plane-Dienste laufen auf dedizierten Nodes mit Pacemaker oder Containerisierung (z. B. Kolla-Ansible).

---

### 💻 **Compute Nodes**

#### a) **GPU-Worker (4x)**

* NVIDIA GPUs via PCI passthrough oder vGPU
* Nova-Compute mit GPU-Scheduling:

  ```ini
  [filter_scheduler]
  enabled_filters=ComputeFilter,AvailabilityZoneFilter,AggregateInstanceExtraSpecsFilter
  ```
* CUDA/NVIDIA-Toolkit vorinstalliert (für Ollama etc.)

#### b) **Service Nodes (6x)**

* Kubernetes via kubeadm oder k3s
* GitLab, Qdrant, Langfuse etc. laufen hier als Cluster
* Volumes über Ceph RBD

#### c) **Image Pool Nodes (3x)**

* Glance Image-Caching (SSD)
* Kasm Workspace Images, XFCE/Ubuntu Templates
* DHCP/DNSMASQ, Metadata-Service (cloud-init)

---

### 📦 **Storage Nodes (2x)**

* **Ceph Cluster:**

  * Ceph Mon (1 pro Node)
  * Ceph OSD (NVMe/SSD empfohlen)
  * Ceph MDS (für CephFS)
  * RADOS Gateway (S3 API für Langfuse, Ollama Models)
* **NFS (optional)**: Für einfache Home-Shares oder persistenten `/shared`

---

## 🌐 **3. Netzwerk-Topologie**

```text
                                 +----------------------+
                                 |      External Net     |
                                 +----------+-----------+
                                            |
                           +----------------v-----------------+
                           |       Neutron Provider Net       |
                           +----------------+-----------------+
                                            |
       +------------------------------------+------------------------------------+
       |                |                    |                    |              |
+------+-----+   +------+-----+      +-------+------+     +-------+-------+  +----+-----+
| Control 01 |   | Compute 01| ...  | GPU Node 01 | ... | Service Node 01|  | Storage 01|
+------------+   +-----------+      +-------------+     +---------------+  +-----------+
    | API/VIP         | Overlay (VXLAN/FLAT)              | CephNet     |
    |                 | Tenant-Netze                      | S3-Net      |
```

* **Management-Netzwerk**: API, DB, Messaging (isoliert)
* **Tenant-Netz**: pro Projekt/Nutzer über Neutron VXLAN (dynamisch)
* **Storage-Netz**: Ceph-Mon, RBD, RGW
* **Public-Netz**: Floating IPs für Guacamole / Horizon / GitLab

---

## 🖥️ **4. Desktop-Vorlage (per Glance)**

> Basierend auf `Ubuntu 22.04`, XFCE, LightDM, cloud-init

* Tools vorinstalliert: `zed`, `podman`, `n8n`, `ollama`, `docker`, `qdrant`, `supabase`, `langfuse`, `flowise`
* Nutzerumgebung: `/home/workspace/`, `/shared` gemountet via CephFS
* Guacamole-Agent: preinstalled
* cloud-init:

  ```yaml
  #cloud-config
  users:
    - default
    - name: devuser
      groups: sudo
      shell: /bin/bash
      sudo: ['ALL=(ALL) NOPASSWD:ALL']
      ssh-authorized-keys:
        - <public-key>

  packages:
    - podman
    - ollama
    - docker.io
    - zed-editor

  runcmd:
    - [ systemctl, enable, podman-n8n.service ]
    - [ bash, -c, "echo 'setup done' > /var/log/init-complete" ]
  ```

---

## 🔑 **5. Auth & Zugriff**

| Zugriffspunkt     | Methode                           |
| ----------------- | --------------------------------- |
| Horizon Dashboard | OpenStack SSO (Keycloak optional) |
| Guacamole         | OAuth2 Proxy (Keycloak / LDAP)    |
| GitLab / WebUIs   | HTTPS via Traefik Ingress         |
| Desktop-Terminals | SSH über Floating IP (admin only) |
| User-Onboarding   | Terraform + OpenStack Provider    |

---

## 📊 **6. Observability & Auditing**

| Monitoring         | Tool                       |
| ------------------ | -------------------------- |
| Logs               | Loki + Promtail            |
| Metriken           | Prometheus + Node Exporter |
| Tracing (optional) | Jaeger / Tempo             |
| Audit-Logs         | OpenStack Keystone + Ceph  |
| Alerts             | Alertmanager               |

---



