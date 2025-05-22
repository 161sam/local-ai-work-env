#!/usr/bin/env python3
"""
Editor-Auswahl für Workspace-in-a-Box Setup
Ermöglicht Auswahl zwischen Zed-Editor und VS Code
"""

import subprocess
import os
import json
import sys
from pathlib import Path

class EditorSetup:
    def __init__(self):
        self.available_editors = {
            'zed': {
                'name': 'Zed Editor',
                'description': 'Modern, lightning-fast editor written in Rust',
                'features': ['🚀 Ultra-fast performance', '🤝 Built-in collaboration', '🔧 LSP support', '⚡ Instant startup'],
                'install_method': 'download_release',
                'default': True
            },
            'vscode': {
                'name': 'Visual Studio Code',
                'description': 'Popular, feature-rich editor from Microsoft',
                'features': ['🔌 Rich extension ecosystem', '🐛 Integrated debugging', '📊 Git integration', '🌐 Remote development'],
                'install_method': 'apt_package',
                'default': False
            }
        }

    def show_editor_selection(self):
        """Zeigt Editor-Auswahl-Dialog"""
        print("\n" + "="*70)
        print("🎨 CHOOSE YOUR DEVELOPMENT EDITOR")
        print("="*70)
        print()

        for i, (key, editor) in enumerate(self.available_editors.items(), 1):
            default_marker = " (RECOMMENDED)" if editor['default'] else ""
            print(f"{i}. {editor['name']}{default_marker}")
            print(f"   {editor['description']}")

            for feature in editor['features']:
                print(f"   {feature}")
            print()

        while True:
            try:
                choice = input("Select editor (1-2) [1 for Zed]: ").strip()

                if not choice:  # Default zu Zed
                    choice = "1"

                choice_num = int(choice)
                if 1 <= choice_num <= len(self.available_editors):
                    selected_key = list(self.available_editors.keys())[choice_num - 1]
                    selected_editor = self.available_editors[selected_key]

                    print(f"\n✅ Selected: {selected_editor['name']}")
                    return selected_key, selected_editor
                else:
                    print("❌ Invalid choice. Please select 1 or 2.")

            except ValueError:
                print("❌ Please enter a number (1 or 2).")

    def create_editor_config(self, editor_choice):
        """Erstellt Editor-spezifische Konfiguration"""
        config_dir = Path("desktop/editor-config")
        config_dir.mkdir(parents=True, exist_ok=True)

        # Editor-Auswahl in Konfigurationsdatei speichern
        config = {
            'selected_editor': editor_choice,
            'install_method': self.available_editors[editor_choice]['install_method']
        }

        with open(config_dir / "editor-choice.json", 'w') as f:
            json.dump(config, f, indent=2)

        print(f"✅ Editor configuration saved: {editor_choice}")
        return config

def create_zed_configuration():
    """Erstellt Zed-spezifische Konfiguration für Container-Development"""

    zed_config_dir = Path("desktop/editor-config/zed")
    zed_config_dir.mkdir(parents=True, exist_ok=True)

    # Zed Settings für Container-Development
    zed_settings = {
        "theme": "Ayu Dark",
        "buffer_font_family": "JetBrains Mono",
        "buffer_font_size": 14,
        "ui_font_size": 16,
        "terminal": {
            "shell": {
                "program": "/bin/bash"
            },
            "working_directory": "current_project_directory"
        },
        "lsp": {
            "rust-analyzer": {
                "binary": {
                    "path": "/usr/local/bin/rust-analyzer"
                }
            },
            "typescript-language-server": {
                "binary": {
                    "path": "/usr/local/bin/typescript-language-server"
                }
            },
            "python-lsp-server": {
                "binary": {
                    "path": "/usr/local/bin/pylsp"
                }
            }
        },
        "languages": {
            "JavaScript": {
                "language_servers": ["typescript-language-server"],
                "format_on_save": "on"
            },
            "TypeScript": {
                "language_servers": ["typescript-language-server"],
                "format_on_save": "on"
            },
            "Python": {
                "language_servers": ["python-lsp-server"],
                "format_on_save": "on"
            },
            "Rust": {
                "language_servers": ["rust-analyzer"],
                "format_on_save": "on"
            },
            "Dockerfile": {
                "language_servers": ["docker-langserver"]
            }
        },
        "project_panel": {
            "dock": "left"
        },
        "outline_panel": {
            "dock": "right"
        },
        "collaboration_panel": {
            "dock": "left"
        },
        "git": {
            "inline_blame": {
                "enabled": true
            }
        },
        "vim_mode": False,
        "autosave": "on_focus_change",
        "tab_size": 2,
        "soft_wrap": "preferred_line_length",
        "preferred_line_length": 100,
        "show_whitespaces": "selection",
        "relative_line_numbers": False,
        "seed_search_query_from_cursor": "always"
    }

    with open(zed_config_dir / "settings.json", 'w') as f:
        json.dump(zed_settings, f, indent=2)

    # Keymap für Container-Development
    zed_keymap = [
        {
            "context": "Editor",
            "bindings": {
                "ctrl-shift-p": "command_palette::Toggle",
                "ctrl-p": "file_finder::Toggle",
                "ctrl-shift-f": "project_search::ToggleFocus",
                "ctrl-`": "terminal_panel::ToggleFocus",
                "ctrl-shift-e": "project_panel::ToggleFocus",
                "ctrl-shift-o": "outline::Toggle",
                "ctrl-shift-g": "collaboration_panel::ToggleFocus"
            }
        },
        {
            "context": "Terminal",
            "bindings": {
                "ctrl-shift-c": "terminal::Copy",
                "ctrl-shift-v": "terminal::Paste"
            }
        }
    ]

    with open(zed_config_dir / "keymap.json", 'w') as f:
        json.dump(zed_keymap, f, indent=2)

    # Zed-Extensions für AI/Container-Development
    zed_extensions = {
        "auto_install": [
            "docker",
            "python",
            "javascript",
            "typescript",
            "rust",
            "json",
            "yaml",
            "toml",
            "markdown",
            "html",
            "css"
        ]
    }

    with open(zed_config_dir / "extensions.json", 'w') as f:
        json.dump(zed_extensions, f, indent=2)

    print("✅ Zed configuration created for container development")

def create_vscode_configuration():
    """Erstellt VS Code Konfiguration für Container-Development"""

    vscode_config_dir = Path("desktop/editor-config/vscode")
    vscode_config_dir.mkdir(parents=True, exist_ok=True)

    # VS Code Settings
    vscode_settings = {
        "workbench.colorTheme": "Dark+ (default dark)",
        "editor.fontFamily": "JetBrains Mono, Consolas, monospace",
        "editor.fontSize": 14,
        "editor.lineHeight": 22,
        "editor.tabSize": 2,
        "editor.insertSpaces": True,
        "editor.detectIndentation": True,
        "editor.renderWhitespace": "selection",
        "editor.rulers": [80, 100],
        "editor.formatOnSave": True,
        "editor.codeActionsOnSave": {
            "source.fixAll": True,
            "source.organizeImports": True
        },
        "files.autoSave": "onFocusChange",
        "explorer.confirmDelete": False,
        "git.enableSmartCommit": True,
        "git.confirmSync": False,
        "terminal.integrated.shell.linux": "/bin/bash",
        "python.defaultInterpreterPath": "/usr/bin/python3",
        "python.linting.enabled": True,
        "python.linting.pylintEnabled": True,
        "python.formatting.provider": "black"
    }

    with open(vscode_config_dir / "settings.json", 'w') as f:
        json.dump(vscode_settings, f, indent=2)

    # Empfohlene Extensions für AI-Development
    vscode_extensions = {
        "recommendations": [
            "ms-python.python",
            "ms-python.black-formatter",
            "ms-vscode.vscode-typescript-next",
            "bradlc.vscode-tailwindcss",
            "ms-vscode.vscode-json",
            "redhat.vscode-yaml",
            "ms-vscode-remote.remote-containers",
            "ms-vscode.docker",
            "rust-lang.rust-analyzer",
            "github.copilot",
            "ms-toolsai.jupyter",
            "ms-python.pylint"
        ]
    }

    with open(vscode_config_dir / "extensions.json", 'w') as f:
        json.dump(vscode_extensions, f, indent=2)

    print("✅ VS Code configuration created for container development")

def main():
    """Hauptfunktion für Editor-Setup"""
    print("🎨 Setting up development editor for Workspace-in-a-Box...")

    # Editor-Auswahl
    editor_setup = EditorSetup()
    selected_key, selected_editor = editor_setup.show_editor_selection()

    # Konfiguration erstellen
    config = editor_setup.create_editor_config(selected_key)

    # Editor-spezifische Konfiguration
    if selected_key == 'zed':
        create_zed_configuration()
    elif selected_key == 'vscode':
        create_vscode_configuration()

    print(f"\n🎉 {selected_editor['name']} has been configured for your workspace!")
    print(f"📁 Configuration saved in: desktop/editor-config/{selected_key}/")

    return selected_key

if __name__ == "__main__":
    selected_editor = main()
    print(f"\n✨ Your workspace will be configured with {selected_editor.upper()}")
