
## 🧱 Ziel: **Produktionsfähiges AI-Workspace Cluster**

### 🔐 Sicherheit · 🔄 GitOps · 🧠 AI-Services · ⚙️ Observability · 🧰 Modularität

---

## 🗺️ **Top-Level Architektur**

```
        🔐 HTTPS
    ┌─────────────┐
    │  Caddy /    │
    │  Traefik    │  ← Let's Encrypt, OAuth2 Proxy
    └────┬────────┘
         │
 ┌───────▼─────────┐
 │    Ingress      │ ← K3s (Traefik) / NGINX
 └───────┬─────────┘
         │
   ┌─────▼────────────┐
   │ AI-Workspace NS  │ (Kubernetes Namespace)
   └─────┬────────────┘
         │
     ┌───▼───────────────────────────────────────────┐
     │ Services (Helm Charts / ArgoCD Apps)          │
     │                                               │
     │  - 🧠 Ollama GPU (DaemonSet + PVC)             │
     │  - 🔁 N8N + Webhooks                           │
     │  - 📊 Qdrant + S3 Backup                       │
     │  - 📝 Supabase + Postgres Operator             │
     │  - 💬 Open WebUI (or chatbot-ui)              │
     │  - 🔧 GitLab / Gitea (extern oder privat)      │
     │  - 📈 Monitoring: Prometheus, Grafana, Loki    │
     │  - 🔑 Vault + Sealed Secrets                   │
     └───────────────────────────────────────────────┘
```

---

## 🔧 Technologie-Stack (empfohlen)

| Kategorie         | Tool/Technologie                                |
| ----------------- | ----------------------------------------------- |
| **Kubernetes**    | [K3s](https://k3s.io/) (lightweight prod-ready) |
| **GitOps**        | ArgoCD + GitHub/GitLab                          |
| **Secrets**       | HashiCorp Vault + `vault-secrets-operator`      |
| **Ingress/TLS**   | Traefik mit cert-manager + OAuth2 Proxy         |
| **Storage**       | Longhorn (lokal) oder EBS (Cloud)               |
| **Observability** | Prometheus, Grafana, Loki, Alertmanager         |
| **CI/CD**         | GitLab CI oder GitHub Actions                   |
| **Backups**       | Velero + S3 / NFS                               |

---

## 🧠 AI Services Deployment

| Service    | Deployment  | Besonderheit                |
| ---------- | ----------- | --------------------------- |
| Ollama     | DaemonSet   | GPU-Nodes, persistent cache |
| Qdrant     | StatefulSet | PVC + Remote Backup         |
| Open WebUI | Deployment  | Autoscaling optional        |
| N8N        | Deployment  | Zugriff via Ingress-Route   |

---

## 🔐 Sicherheitsmaßnahmen

* 🔒 OAuth2 Proxy vor **jeder Oberfläche** (N8N, Supabase Studio, WebUI, Guacamole)
* 🔐 Vault für:

  * API-Keys
  * DB-Passwörter
  * LLM-Zugangstokens
* 🔐 `networkPolicies` → Isolation zwischen Namespaces
* 🔐 `PodSecurityPolicies` oder `PodSecurityAdmission`

---

## 📦 Helm-basiertes Setup (Beispiel)

```bash
# Namespace
kubectl create ns ai-workspace

# Vault installieren
helm repo add hashicorp https://helm.releases.hashicorp.com
helm install vault hashicorp/vault -n ai-workspace

# ArgoCD App für Ollama
kubectl apply -f argo-apps/ollama.yaml

# IngressRoute (Traefik)
kubectl apply -f ingress/ollama-route.yaml
```

---

## 🛠️ GitOps-Workflow

```text
Git Repo (z.B. GitLab Selfhosted)
│
├── /ai-workspace/
│   ├── helm-values/
│   │   ├── ollama-values.yaml
│   │   ├── n8n-values.yaml
│   ├── ingress/
│   │   ├── ollama-ingress.yaml
│   └── argo-apps/
│       ├── ollama.yaml
│       ├── qdrant.yaml
```

Deployments werden automatisch via **ArgoCD** synchronisiert. Secrets werden **sealed** oder von Vault geliefert.

---

## 🧩 Vorteile gegenüber dem Docker-Setup

| Docker-Setup                      | Kubernetes/Argo Setup            |
| --------------------------------- | -------------------------------- |
| Schnell und lokal lauffähig       | Vollautomatisiert und skalierbar |
| Unsicher (Passwörter im Klartext) | Vault & TLS everywhere           |
| GUI-first (VNC im Browser)        | API-first (DevOps geeignet)      |
| Alle Services statisch            | On-demand Scaling (HPA/KS)       |
| schwer zu testen / deployen       | CI/CD + GitOps Integration       |

---

## 🔚 Fazit

Dieses Setup ersetzt die „All-in-One Desktop“-Architektur durch ein **Infrastructure-as-Code Deployment**, das:

* sicher,
* modular,
* CI/CD-fähig
* und Cloud/On-Prem kompatibel ist.


