# 🚀 Workspace-in-a-Box - AI Development Environment

**Complete browser-based AI development workspace with modern editors, local LLMs, and productivity tools.**

## ✨ Features

- 🖥️ **Browser Desktop** - Full Linux desktop accessible via web browser
- ⚡ **Modern Editors** - Choose between Zed Editor or VS Code with full configuration
- 🧠 **AI Stack** - N8N, Ollama, Open WebUI, Qdrant, Langfuse
- 🌊 **No-Code AI** - Flowise for visual AI workflow building
- 🔍 **Smart Search** - SearXNG meta search engine
- 📝 **Productivity** - AppFlowy, AFFINE, GitLab
- 🗄️ **Backend** - Complete Supabase stack
- 🔒 **Secure** - Only one port exposed (8080)

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- 4GB+ RAM (8GB+ recommended)
- 20GB+ free disk space

### Installation

```bash
# 1. Clone repository
git clone https://github.com/yourusername/workspace-in-a-box.git
cd workspace-in-a-box

# 2. Configure environment
cp .env.example .env
# Edit .env with your settings (optional for local use)

# 3. Start workspace
python setup_workspace.py --profile cpu

# 4. Access desktop
# Browser: http://localhost:8080
# Login: guacadmin/guacadmin
```

### First Login

1. **Open Browser**: http://localhost:8080
2. **Login**: `guacadmin` / `guacadmin`
3. **Create Desktop Connection**:
   - Name: Linux Desktop
   - Protocol: VNC
   - Hostname: `desktop`
   - Port: `5901`
   - Password: `password`
4. **Connect** and enjoy your AI workspace!

## 🎨 Editor Selection

During setup, choose your preferred editor:

### Zed Editor (Recommended)
- ⚡ Ultra-fast startup (< 100ms)
- 🤝 Built-in collaboration
- 🧠 AI code completion
- 🔧 Native LSP support

### Visual Studio Code
- 🔌 Rich extension ecosystem
- 🐛 Integrated debugging
- 📊 Git integration
- 🌐 Remote development

Both editors come pre-configured with:
- Language servers (Python, TypeScript, Rust, etc.)
- Development tools and extensions
- AI development optimizations

## 🧠 AI Services

All services are accessible from the desktop browser:

| Service | URL | Description |
|---------|-----|-------------|
| **N8N** | http://n8n:5678 | AI Workflow Automation |
| **Open WebUI** | http://open-webui:8080 | Chat with Local LLMs |
| **Flowise** | http://flowise:3001 | No-Code AI Builder |
| **Ollama** | http://ollama:11434 | Local LLM API |
| **Qdrant** | http://qdrant:6333 | Vector Database |
| **Langfuse** | http://langfuse:3002 | LLM Observability |

## 📝 Productivity Tools

| Service | URL | Description |
|---------|-----|-------------|
| **SearXNG** | http://searxng:8081 | Meta Search Engine |
| **AppFlowy** | http://appflowy:8082 | Notion Alternative |
| **AFFINE** | http://affine:3010 | Collaborative Workspace |
| **Supabase** | http://kong:8000 | Database & Backend |

## 🛠️ Development Tools

| Service | URL | Description |
|---------|-----|-------------|
| **GitLab** | http://gitlab:8083 | Git Repository & CI/CD |

## ⚙️ Configuration

### GPU Support

```bash
# NVIDIA GPU
python setup_workspace.py --profile gpu-nvidia

# AMD GPU (Linux)
python setup_workspace.py --profile gpu-amd

# CPU only
python setup_workspace.py --profile cpu
```

### Feature Profiles

```bash
# Desktop only (minimal)
python setup_workspace.py --profile cpu

# With productivity tools
python setup_workspace.py --profile cpu --features desktop productivity

# Full development stack
python setup_workspace.py --profile cpu --features desktop productivity development

# Everything including observability
python setup_workspace.py --full-stack
```

### Production Deployment

1. **Update .env** with your domains:
```bash
N8N_HOSTNAME=n8n.yourdomain.com
WEBUI_HOSTNAME=chat.yourdomain.com
GUACAMOLE_HOSTNAME=desktop.yourdomain.com
LETSENCRYPT_EMAIL=admin@yourdomain.com
```

2. **Start with Caddy**:
```bash
python setup_workspace.py --profile cpu --features desktop productivity production
```

## 📁 File Sharing

- **Host → Desktop**: Place files in `./desktop-shared/`
- **Desktop access**: Files appear in `/shared/`
- **N8N workflows**: Stored in `./shared/`
- **Projects**: Develop in `/home/kasm-user/Projects/`

## 🔧 Development Workflow

1. **Start Workspace**: `python setup_workspace.py`
2. **Access Desktop**: http://localhost:8080
3. **Open Editor**: Zed or VS Code icon on desktop
4. **Create Project**: `/home/kasm-user/Projects/my-ai-app/`
5. **Use AI Services**: Pre-configured bookmarks in desktop browser

### Example: AI Chat Application

```python
# In desktop editor: /home/kasm-user/Projects/ai-chat/app.py
import requests

def chat_with_ollama(message):
    response = requests.post('http://ollama:11434/api/generate', json={
        'model': 'llama3.1',
        'prompt': message,
        'stream': False
    })
    return response.json()['response']

# Test from desktop terminal
# python app.py
```

## 📊 Monitoring

### Health Checks
```bash
# In desktop terminal
~/Scripts/check-services.sh
```

### Docker Status
```bash
# In desktop terminal  
~/Scripts/docker-status.sh
```

### Service Logs
```bash
# On host system
docker logs n8n
docker logs open-webui
docker logs flowise
```

## 🐛 Troubleshooting

### Desktop Connection Issues

**Problem**: Can't connect to desktop
**Solution**:
```bash
# Check containers
docker ps | grep desktop
docker logs desktop
docker logs guacamole

# Restart if needed
docker restart desktop guacd guacamole
```

### Service Not Responding

**Problem**: AI service not accessible
**Solution**:
```bash
# Check service status
docker logs <service-name>

# Restart specific service
docker restart <service-name>

# Check internal connectivity from desktop
curl http://n8n:5678
```

### Performance Issues

**Solutions**:
- Allocate more RAM to Docker
- Use SSD storage
- Enable GPU acceleration
- Reduce concurrent services

## 📚 Advanced Usage

### Custom Services

Add your own services to `docker-compose.yml`:

```yaml
my-service:
  <<: *common-env
  image: my-custom-service
  container_name: my-service
  profiles: ["custom"]
```

### Backup Strategy

```bash
# Backup volumes
docker run --rm -v workspace_n8n_storage:/data -v $(pwd):/backup alpine tar czf /backup/n8n-backup.tar.gz /data

# Backup configurations
tar czf workspace-backup.tar.gz ./desktop-shared ./shared .env
```

### Multi-Environment

```bash
# Development
cp .env .env.dev
# Edit .env.dev

# Production  
cp .env .env.prod
# Edit .env.prod

# Use specific environment
cp .env.prod .env
python setup_workspace.py --profile gpu-nvidia --full-stack
```

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Test your changes
4. Submit pull request

## 📄 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [N8N](https://n8n.io/) - Workflow automation
- [Supabase](https://supabase.com/) - Backend as a service
- [Ollama](https://ollama.ai/) - Local LLM runtime
- [Guacamole](https://guacamole.apache.org/) - Clientless remote desktop
- [Zed](https://zed.dev/) - Modern code editor
- [Original Local AI Package](https://github.com/coleam00/local-ai-packaged) - Base inspiration

---

**🎉 Enjoy your complete AI development workspace!**
