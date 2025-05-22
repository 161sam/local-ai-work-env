# ⚡ Editor Guide - Zed & VS Code im Workspace

## 🎨 Editor-Übersicht

### Zed Editor (Empfohlen)

**Warum Zed im AI-Workspace?**
- 🚀 **Performance** - Rust-basiert, instant startup (< 100ms)
- 🤝 **Kollaboration** - Built-in real-time pairing ohne Plugins
- 🧠 **AI-Native** - Integrierte AI-Code-Completion und Chat
- 🎯 **Focus** - Minimalistisches UI ohne Ablenkungen
- ⚡ **Modern** - GPU-accelerated UI, native async

### VS Code

**Wann VS Code wählen?**
- 🔌 **Extensions** - Spezielle Extensions erforderlich
- 🐛 **Debugging** - Complex debugging workflows
- 📊 **Jupyter** - Notebook-Integration wichtig
- 🔧 **Legacy** - Bestehende VS Code-Workflows

---

## ⚡ Zed Editor

### Erste Schritte

#### Zed öffnen
```bash
# Im Desktop-Terminal
zed                    # Leeres Fenster
zed .                  # Aktuelles Verzeichnis
zed /path/to/project   # Spezifisches Projekt
zed file.py           # Einzelne Datei
```

#### Projekt-Setup
```bash
# Neues Projekt erstellen
cd /home/kasm-user/Projects/
mkdir ai-experiment
cd ai-experiment

# Grundstruktur
echo 'print("Hello AI Workspace!")' > hello.py
echo '# AI Experiment' > README.md
mkdir src tests

# Zed öffnen
zed .
```

### Zed-Konfiguration

#### Settings anpassen
```bash
# Konfigurationsdatei öffnen
zed ~/.config/zed/settings.json
```

```json
{
  "theme": "Ayu Dark",
  "buffer_font_family": "JetBrains Mono",
  "buffer_font_size": 14,
  "ui_font_size": 16,
  "preferred_line_length": 100,
  "soft_wrap": "preferred_line_length",
  "tab_size": 2,
  "hard_tabs": false,
  "autosave": "on_focus_change",
  "format_on_save": "on",

  "terminal": {
    "shell": {"program": "/bin/zsh"},
    "working_directory": "current_project_directory"
  },

  "project_panel": {"dock": "left"},
  "outline_panel": {"dock": "right"},
  "collaboration_panel": {"dock": "left"},

  "git": {
    "inline_blame": {"enabled": true},
    "git_gutter": "tracked_files"
  },

  "vim_mode": false,

  "languages": {
    "Python": {
      "language_servers": ["python-lsp-server"],
      "format_on_save": "on",
      "formatter": "black",
      "tab_size": 4
    },
    "JavaScript": {
      "language_servers": ["typescript-language-server"],
      "format_on_save": "on",
      "formatter": "prettier"
    },
    "TypeScript": {
      "language_servers": ["typescript-language-server"],
      "format_on_save": "on",
      "formatter": "prettier"
    },
    "Rust": {
      "language_servers": ["rust-analyzer"],
      "format_on_save": "on"
    },
    "JSON": {
      "language_servers": ["vscode-json-languageserver"],
      "format_on_save": "on"
    },
    "YAML": {
      "language_servers": ["yaml-language-server"],
      "format_on_save": "on"
    },
    "Dockerfile": {
      "language_servers": ["docker-langserver"]
    }
  },

  "lsp": {
    "rust-analyzer": {
      "binary": {"path": "/home/kasm-user/.cargo/bin/rust-analyzer"},
      "initialization_options": {
        "check": {"command": "clippy"}
      }
    },
    "python-lsp-server": {
      "binary": {"path": "/usr/local/bin/pylsp"},
      "initialization_options": {
        "settings": {
          "pylsp": {
            "plugins": {
              "black": {"enabled": true},
              "pylint": {"enabled": true},
              "mypy": {"enabled": true}
            }
          }
        }
      }
    }
  }
}
```

#### Tastenkürzel anpassen
```bash
# Keymap öffnen
zed ~/.config/zed/keymap.json
```

```json
[
  {
    "context": "Editor",
    "bindings": {
      "ctrl-shift-p": "command_palette::Toggle",
      "ctrl-p": "file_finder::Toggle",
      "ctrl-shift-f": "project_search::ToggleFocus",
      "ctrl-`": "terminal_panel::ToggleFocus",
      "ctrl-shift-e": "project_panel::ToggleFocus",
      "ctrl-shift-o": "outline::Toggle",
      "ctrl-j": "editor::JoinLines",
      "ctrl-d": "editor::SelectNext",
      "ctrl-shift-l": "editor::SelectAll",
      "alt-up": "editor::MoveLineUp",
      "alt-down": "editor::MoveLineDown",
      "ctrl-shift-k": "editor::DeleteLine",
      "ctrl-enter": "editor::OpenExcerpts",
      "ctrl-shift-enter": "assistant::InlineAssist"
    }
  },
  {
    "context": "Terminal",
    "bindings": {
      "ctrl-shift-c": "terminal::Copy",
      "ctrl-shift-v": "terminal::Paste"
    }
  },
  {
    "context": "ProjectPanel",
    "bindings": {
      "a": "project_panel::NewFile",
      "shift-a": "project_panel::NewDirectory",
      "x": "project_panel::Cut",
      "c": "project_panel::Copy",
      "v": "project_panel::Paste",
      "d": "project_panel::Delete"
    }
  }
]
```

### AI-Features in Zed

#### AI-Code-Completion
```python
# Zed's AI versteht Kontext automatisch
def calculate_fibonacci(n):
    # Zed schlägt automatisch Implementation vor
    if n <= 1:
        return n
    return calculate_fibonacci(n-1) + calculate_fibonacci(n-2)

# AI erkennt Patterns und schlägt Tests vor
def test_fibonacci():
    assert calculate_fibonacci(0) == 0
    assert calculate_fibonacci(1) == 1
    assert calculate_fibonacci(5) == 5
```

#### AI-Chat Integration
- **Ctrl+Shift+Enter** - Inline AI-Assist
- **Cmd/Ctrl+?** - AI-Chat öffnen
- **Natural Language** - "Refactor this function to use dynamic programming"

#### Kollaboration
```bash
# Projekt teilen (für Team-Development)
# In Zed: View → Collab Panel → Share Project
# Link teilen mit Team-Mitgliedern
```

### Zed für AI-Development

#### Python AI-Projekte
```python
# .zed/settings.json (projekt-spezifisch)
{
  "languages": {
    "Python": {
      "formatter": "black",
      "format_on_save": "on",
      "language_servers": ["python-lsp-server"],
      "tab_size": 4
    }
  },
  "lsp": {
    "python-lsp-server": {
      "initialization_options": {
        "settings": {
          "pylsp": {
            "plugins": {
              "black": {"enabled": true},
              "isort": {"enabled": true},
              "mypy": {"enabled": true},
              "pylint": {"enabled": true}
            }
          }
        }
      }
    }
  }
}
```

#### N8N-Workflows entwickeln
```javascript
// Zed hat JSON/JS-Support für N8N-Nodes
{
  "nodes": [
    {
      "parameters": {
        "model": "llama3.1",
        "prompt": "={{ $json.userInput }}"
      },
      "type": "ollama.chat",
      "position": [400, 300]
    }
  ]
}
```

#### Docker-Integration
```dockerfile
# Zed erkennt Dockerfile-Syntax automatisch
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["python", "app.py"]
```

### Zed-Workflow-Tipps

#### Projekt-Management
- **Ctrl+P** - Schnelles File-Switching
- **Ctrl+Shift+P** - Command Palette
- **Ctrl+Shift+F** - Projekt-weite Suche
- **F2** - Symbol umbenennen
- **Ctrl+Click** - Go to Definition

#### Multi-Cursor-Editing
- **Ctrl+D** - Nächste Occurrence auswählen
- **Ctrl+Shift+L** - Alle Occurrences auswählen
- **Alt+Click** - Cursor hinzufügen
- **Ctrl+Alt+Up/Down** - Multi-Cursor vertikal

#### Terminal-Integration
- **Ctrl+`** - Terminal toggle
- **Terminal unterstützt alle Container-Commands**:
  ```bash
  docker logs n8n
  curl http://ollama:11434/api/tags
  python scripts/test_ai.py
  ```

---

## 📝 VS Code

### VS Code-Setup

#### Ersten Start
```bash
# VS Code öffnen
code                    # Leeres Fenster
code .                  # Aktuelles Verzeichnis
code /path/to/project   # Spezifisches Projekt
```

#### Extension-Installation
```bash
# Kommandozeile-Installation
code --install-extension ms-python.python
code --install-extension ms-python.black-formatter
code --install-extension rust-lang.rust-analyzer
code --install-extension ms-vscode.vscode-typescript-next
code --install-extension bradlc.vscode-tailwindcss
code --install-extension ms-vscode.vscode-json
code --install-extension redhat.vscode-yaml
code --install-extension ms-vscode.docker
code --install-extension ms-toolsai.jupyter
code --install-extension github.copilot
```

#### Settings-Konfiguration
```bash
# Settings öffnen
code ~/.config/Code/User/settings.json
```

```json
{
  "workbench.colorTheme": "Dark+ (default dark)",
  "editor.fontFamily": "JetBrains Mono, Consolas, monospace",
  "editor.fontSize": 14,
  "editor.lineHeight": 22,
  "editor.tabSize": 2,
  "editor.insertSpaces": true,
  "editor.detectIndentation": true,
  "editor.renderWhitespace": "selection",
  "editor.rulers": [80, 100],
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.fixAll": true,
    "source.organizeImports": true
  },
  "files.autoSave": "onFocusChange",
  "explorer.confirmDelete": false,
  "git.enableSmartCommit": true,
  "git.confirmSync": false,
  "terminal.integrated.shell.linux": "/bin/zsh",
  "terminal.integrated.fontFamily": "JetBrains Mono",

  "python.defaultInterpreterPath": "/usr/bin/python3",
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": true,
  "python.formatting.provider": "black",
  "python.analysis.typeCheckingMode": "basic",

  "typescript.preferences.quoteStyle": "single",
  "javascript.preferences.quoteStyle": "single",

  "docker.showStartPage": false,
  "docker.commands.build": "docker build --platform linux/amd64 .",

  "jupyter.askForKernelRestart": false,
  "jupyter.interactiveWindow.textEditor.executeSelection": true
}
```

### VS Code für AI-Development

#### Python-Development
```python
# VS Code erkennt Virtual Environments automatisch
import requests
import json
from typing import Dict, List

class OllamaClient:
    def __init__(self, base_url: str = "http://ollama:11434"):
        self.base_url = base_url

    def generate(self, model: str, prompt: str) -> Dict:
        """Generate text using Ollama model."""
        response = requests.post(
            f"{self.base_url}/api/generate",
            json={
                "model": model,
                "prompt": prompt,
                "stream": False
            }
        )
        return response.json()

    def list_models(self) -> List[Dict]:
        """List available models."""
        response = requests.get(f"{self.base_url}/api/tags")
        return response.json().get("models", [])

# VS Code zeigt Type-Hints und IntelliSense
client = OllamaClient()
models = client.list_models()  # Autocomplete verfügbar
```

#### Jupyter-Integration
```python
# .ipynb Dateien direkt in VS Code
# %%
import pandas as pd
import matplotlib.pyplot as plt

# AI-Generated Data Analysis
data = pd.read_csv('/shared/ai_results.csv')
data.head()

# %%
# Visualization
plt.figure(figsize=(10, 6))
plt.plot(data['timestamp'], data['accuracy'])
plt.title('AI Model Accuracy Over Time')
plt.show()
```

#### Docker-Integration
```bash
# VS Code Docker-Extension Features:
# - Container-Browser
# - Image-Management
# - Log-Viewing
# - Container-Attach

# Dockerfile-Support mit IntelliSense
FROM python:3.11-slim
# VS Code schlägt automatisch vor:
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
```

#### Git-Integration
```bash
# Git-Features in VS Code:
# - Visual Diff
# - Staging-Area
# - Branch-Management
# - Merge-Conflict-Resolution

# Source Control Panel (Ctrl+Shift+G)
git add .
git commit -m "Add AI model training script"
git push origin main
```

### VS Code-Workflow

#### Debugging-Setup
```json
// .vscode/launch.json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Current File",
            "type": "python",
            "request": "launch",
            "program": "${file}",
            "console": "integratedTerminal",
            "env": {
                "OLLAMA_URL": "http://ollama:11434",
                "N8N_URL": "http://n8n:5678"
            }
        },
        {
            "name": "Python: AI Script",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/src/ai_script.py",
            "args": ["--model", "llama3.1"],
            "console": "integratedTerminal"
        }
    ]
}
```

#### Tasks-Automation
```json
// .vscode/tasks.json
{
    "version": "2.0.0",
    "tasks": [
        {
            "label": "Run AI Tests",
            "type": "shell",
            "command": "python",
            "args": ["-m", "pytest", "tests/"],
            "group": "test",
            "presentation": {
                "reveal": "always",
                "panel": "new"
            }
        },
        {
            "label": "Start N8N Workflow",
            "type": "shell",
            "command": "curl",
            "args": [
                "-X", "POST",
                "http://n8n:5678/webhook/test-workflow",
                "-H", "Content-Type: application/json",
                "-d", "{\"test\": true}"
            ]
        }
    ]
}
```

#### Workspace-Konfiguration
```json
// .vscode/settings.json (Projekt-spezifisch)
{
    "python.defaultInterpreterPath": "./venv/bin/python",
    "python.testing.pytestEnabled": true,
    "python.testing.pytestArgs": ["tests/"],

    "files.associations": {
        "*.n8n": "json",
        "Dockerfile.*": "dockerfile"
    },

    "editor.rulers": [88],  // PEP 8 für Python
    "python.formatting.blackArgs": ["--line-length", "88"]
}
```

---

## 🔄 Editor-Vergleich

### Performance

| **Aspekt** | **Zed** | **VS Code** |
|------------|---------|-------------|
| **Startup-Zeit** | < 100ms | 1-3s |
| **Memory-Usage** | ~50MB | 200-500MB |
| **Responsiveness** | Instant | Gut |
| **File-Handling** | Sehr groß | Groß |

### Features

| **Feature** | **Zed** | **VS Code** |
|-------------|---------|-------------|
| **AI-Integration** | ✅ Native | 🔌 Extensions |
| **Kollaboration** | ✅ Built-in | 🔌 Live Share |
| **Debugging** | ⚠️ Basic | ✅ Advanced |
| **Extensions** | ⚠️ Limited | ✅ Massive |
| **Language-Support** | ✅ LSP-Native | ✅ Excellent |
| **Git-Integration** | ✅ Good | ✅ Excellent |
| **Jupyter** | ❌ No | ✅ Native |

### AI-Development

| **Use Case** | **Empfehlung** | **Grund** |
|--------------|----------------|-----------|
| **N8N-Workflows** | Zed | JSON/JS-Performance |
| **Python-Prototyping** | Zed | Schneller Iteration |
| **Data-Science** | VS Code | Jupyter-Integration |
| **Debugging** | VS Code | Bessere Debug-Tools |
| **Pair-Programming** | Zed | Native Kollaboration |
| **Large-Scale-Projects** | VS Code | Extension-Ecosystem |

---

## 🛠️ Entwicklungs-Workflows

### AI-Prototyping-Workflow

#### Mit Zed (Schnell & Fokussiert)
```bash
# 1. Idee in Open WebUI testen
# Browser: http://open-webui:8080

# 2. Schnelles Prototyping
cd /home/kasm-user/Projects/
mkdir ai-prototype
cd ai-prototype
zed .

# 3. Python-Schnelltest
echo '
import requests

def test_ollama():
    response = requests.post("http://ollama:11434/api/generate",
        json={"model": "llama3.1", "prompt": "Hello AI!", "stream": False})
    print(response.json()["response"])

if __name__ == "__main__":
    test_ollama()
' > quick_test.py

# 4. Ausführen (Zed-Terminal: Ctrl+`)
python quick_test.py
```

#### Mit VS Code (Detailliert & Strukturiert)
```bash
# 1. Projekt-Setup
cd /home/kasm-user/Projects/
mkdir ai-project
cd ai-project
code .

# 2. Virtual Environment
python3 -m venv venv
source venv/bin/activate
pip install requests jupyter pandas matplotlib

# 3. Jupyter-Notebook für Experimente
# VS Code: Neue .ipynb Datei

# 4. Strukturierte Entwicklung
mkdir src tests docs
touch src/__init__.py
touch src/ai_client.py
touch tests/test_ai_client.py
```

### N8N-Workflow-Development

#### Zed-Approach (JSON-First)
```javascript
// N8N-Workflow in Zed editieren
// Datei: workflow.json
{
  "name": "AI Chat Workflow",
  "nodes": [
    {
      "parameters": {
        "httpMethod": "POST",
        "path": "chat",
        "responseMode": "responseNode"
      },
      "type": "n8n-nodes-base.webhook",
      "position": [200, 300]
    },
    {
      "parameters": {
        "model": "llama3.1",
        "prompt": "={{ $json.body.message }}"
      },
      "type": "ollama-chat",
      "position": [400, 300]
    }
  ]
}
```

#### Integration-Testing
```python
# test_n8n_integration.py
import requests
import json

def test_n8n_workflow():
    # Workflow via Webhook testen
    response = requests.post("http://n8n:5678/webhook/chat",
        json={"message": "Hello from test!"})

    assert response.status_code == 200
    result = response.json()
    assert "response" in result
    print(f"AI Response: {result['response']}")

if __name__ == "__main__":
    test_n8n_workflow()
```

### Container-Development

#### Docker-Integration in beiden Editoren
```bash
# Dockerfile-Development
FROM python:3.11-slim

# Beide Editoren haben Dockerfile-Syntax-Highlighting
WORKDIR /app

# Zed: Minimalistisch, schnell
# VS Code: IntelliSense, Linting

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
CMD ["python", "app.py"]
```

#### Development-Container
```json
// .devcontainer/devcontainer.json (VS Code)
{
    "name": "AI Development",
    "image": "python:3.11-slim",
    "features": {
        "ghcr.io/devcontainers/features/docker-in-docker:2": {}
    },
    "customizations": {
        "vscode": {
            "extensions": [
                "ms-python.python",
                "ms-vscode.docker"
            ]
        }
    },
    "postCreateCommand": "pip install -r requirements.txt"
}
```

---

## 💡 Editor-Empfehlungen

### Für AI-Anfänger
**→ Zed Editor**
- Weniger überwältigend
- AI-Features out-of-the-box
- Schneller Einstieg
- Fokus auf Code

### Für Erfahrene Entwickler
**→ VS Code**
- Bekannte Umgebung
- Extensive Debugging-Tools
- Große Extension-Library
- Jupyter-Integration

### Für Teams
**→ Zed Editor**
- Native Kollaboration
- Schnelles Pair-Programming
- Konsistente Performance
- Weniger Konfigurationsaufwand

### Für Data Science
**→ VS Code**
- Jupyter-Notebooks
- Plotting-Integration
- Variable-Explorer
- Pandas-Support

### Für Quick-Prototyping
**→ Zed Editor**
- Instant Startup
- Minimale Ablenkung
- AI-Completion
- Schnelle Iteration

**💡 Tipp**: Beide Editoren sind installiert - probieren Sie beide aus und verwenden Sie den Editor, der für Ihre spezifische Aufgabe am besten geeignet ist!
