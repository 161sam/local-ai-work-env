# Strukturkonflikte und Redundanzen

## 🚨 **Kritische Konflikte**

### **1. Doppelte Docker-Compose-Dateien**
- **Original**: `docker-compose.yml` (Root)
- **Fork**: `work-env/docker-compose.yml` + `work-env/docker-compose-extended.yml`
- **Problem**: Verschiedene Netzwerknamen, Service-Definitionen, Volumes

### **2. Parallele Start-Mechanismen**
- **Original**: `start_services.py`
- **Fork**: `start-extended-stack.py`
- **Problem**: Inkonsistente Parameter, verschiedene Profile-Handling

### **3. Netzwerk-Inkonsistenzen**
```yaml
# Original
networks:
  default:
    name: localai

# Fork work-env/docker-compose.yml
networks:
  local-ai-network:
    name: local-ai-network

# Fork docker-compose-extended.yml
networks:
  ai-network:
    name: extended-ai-network
```

### **4. Service-Redundanzen**
**Doppelt definierte Services:**
- `ollama` vs `ollama-cpu`/`ollama-gpu`
- `n8n` (verschiedene Konfigurationen)
- `postgres`/`db` vs `supabase-db` vs `guac-postgres`

### **5. Umgebungsvariablen-Chaos**
- **Original**: `.env.example` (63 Variablen)
- **Fork**: `work-env/env-template` (200+ Variablen)
- **Problem**: Überlappende, inkonsistente Namen

## 🔧 **Architektur-Probleme**

### **1. Inkonsistente Service-Discovery**
```yaml
# Original n8n config
- OLLAMA_HOST=http://ollama:11434

# Fork config
- OLLAMA_HOST=http://ollama:11434
# Aber Service heißt manchmal 'ollama-cpu'
```

### **2. Port-Konflikte**
- Guacamole: 8080 (konfliktiert mit potentiellen anderen Services)
- Multiple PostgreSQL-Instances ohne klare Trennung

### **3. Volume-Management**
- Verschiedene Volume-Präfixe
- Inkonsistente Daten-Persistierung
- Überlappende Mount-Points

## 📊 **Redundante Komponenten**

### **Services**
- **3x PostgreSQL**: `db`, `supabase-db`, `guac-postgres`, `gitlab-postgres`
- **2x Redis**: Original Valkey + neues Redis
- **2x N8N**: Haupt- und Extended-Instanz
- **Multiple Reverse Proxies**: Kong + Caddy

### **Scripts**
- `setup-extended-ai-stack.sh` vs Original-Setup
- `generate-env.sh` vs `.env.example`
- Verschiedene Python-Starter

### **Konfigurationsdateien**
- Multiple Caddyfiles
- Verschiedene .env-Templates
- Überlappende Workflow-Definitionen
