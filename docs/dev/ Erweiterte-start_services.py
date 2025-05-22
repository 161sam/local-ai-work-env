#!/usr/bin/env python3
"""
start_services.py (Extended Version)

Erweitert das Original-Skript um Desktop-, Produktivitäts- und Entwicklungsfeatures
Behält vollständige Rückwärtskompatibilität bei
"""

import os
import subprocess
import shutil
import time
import argparse
import platform
import sys

def run_command(cmd, cwd=None):
    """Run a shell command and print it."""
    print("Running:", " ".join(cmd))
    subprocess.run(cmd, cwd=cwd, check=True)

def clone_supabase_repo():
    """Clone the Supabase repository using sparse checkout if not already present."""
    if not os.path.exists("supabase"):
        print("Cloning the Supabase repository...")
        run_command([
            "git", "clone", "--filter=blob:none", "--no-checkout",
            "https://github.com/supabase/supabase.git"
        ])
        os.chdir("supabase")
        run_command(["git", "sparse-checkout", "init", "--cone"])
        run_command(["git", "sparse-checkout", "set", "docker"])
        run_command(["git", "checkout", "master"])
        os.chdir("..")
    else:
        print("Supabase repository already exists, updating...")
        os.chdir("supabase")
        run_command(["git", "pull"])
        os.chdir("..")

def prepare_supabase_env():
    """Copy .env to .env in supabase/docker."""
    env_path = os.path.join("supabase", "docker", ".env")
    env_example_path = os.path.join(".env")
    print("Copying .env in root to .env in supabase/docker...")
    shutil.copyfile(env_example_path, env_path)

def setup_guacamole_db():
    """Setup Guacamole database initialization if needed."""
    init_dir = "guacamole/init"
    init_file = os.path.join(init_dir, "initdb.sql")

    if not os.path.exists(init_file):
        print("Setting up Guacamole database initialization...")
        os.makedirs(init_dir, exist_ok=True)
        try:
            # Generate Guacamole DB init script
            cmd = [
                "docker", "run", "--rm", "guacamole/guacamole:latest",
                "/opt/guacamole/bin/initdb.sh", "--postgres"
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)

            with open(init_file, 'w') as f:
                f.write(result.stdout)
            print(f"✅ Created Guacamole init script: {init_file}")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to generate Guacamole init script: {e}")
            print("You may need to create it manually later.")

def setup_desktop_environment():
    """Setup desktop shared directories."""
    directories = [
        "desktop-shared",
        "shared"  # Ensure original shared dir exists
    ]

    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
            print(f"✅ Created directory: {directory}")

def stop_existing_containers(profile=None, features=None):
    """Stop existing containers with profile and feature support."""
    print("Stopping and removing existing containers for project 'localai'...")
    cmd = ["docker", "compose", "-p", "localai", "-f", "docker-compose.yml"]

    # Add profiles
    if profile and profile != "none":
        cmd.extend(["--profile", profile])

    # Add feature profiles
    if features:
        for feature in features:
            if feature != "none":
                cmd.extend(["--profile", feature])

    cmd.append("down")
    run_command(cmd)

def start_services(profile=None, features=None):
    """Start services with profile and feature support."""
    print("Starting services...")
    cmd = ["docker", "compose", "-p", "localai", "-f", "docker-compose.yml"]

    # Add profiles
    if profile and profile != "none":
        cmd.extend(["--profile", profile])

    # Add feature profiles
    if features:
        for feature in features:
            if feature != "none":
                cmd.extend(["--profile", feature])

    cmd.extend(["up", "-d"])
    run_command(cmd)

def wait_for_service(service_name, port, timeout=120):
    """Wait for a service to be ready."""
    print(f"⏳ Waiting for {service_name} to be ready on port {port}...")
    start_time = time.time()

    while time.time() - start_time < timeout:
        try:
            result = subprocess.run(
                ["curl", "-s", f"http://localhost:{port}"],
                capture_output=True,
                timeout=5
            )
            if result.returncode == 0:
                print(f"✅ {service_name} is ready!")
                return True
        except subprocess.TimeoutExpired:
            pass
        except FileNotFoundError:
            # curl not available, skip health check
            print(f"⚠️ curl not available, skipping health check for {service_name}")
            return True

        time.sleep(5)

    print(f"❌ {service_name} failed to start within {timeout} seconds")
    return False

def show_service_urls(features):
    """Display service URLs based on enabled features."""
    print("\n" + "="*60)
    print("🎉 Local AI Package is now running!")
    print("="*60)

    # Core services (always available)
    print("\n📋 Core Services:")
    print("🧠 N8N:                   http://localhost:5678")
    print("💬 Open WebUI:            http://localhost:3000")
    print("🤖 Ollama API:            http://localhost:11434")
    print("📊 Qdrant:                http://localhost:6333")
    print("🗄️  Supabase:             http://localhost:8000")
    print("🌐 Langfuse:              http://localhost:3002")
    print("🔍 SearXNG:               http://localhost:8080")

    # Feature-specific services
    if features and 'desktop' in features:
        print("\n🖥️  Desktop Services:")
        print("🖥️  Guacamole Desktop:    http://localhost:8080")
        print("🖥️  Desktop VNC (direct): http://localhost:6901")
        print("   Default Login:        guacadmin / guacadmin")
        print("   Desktop User:         kasm-user / password")

    if features and 'productivity' in features:
        print("\n📝 Productivity Services:")
        print("📝 AppFlowy:              http://localhost:8081")
        print("✨ AFFINE:                http://localhost:3010")

    if features and 'development' in features:
        print("\n🛠️  Development Services:")
        print("🦊 GitLab:                http://localhost:8082")
        print("🔧 N8N Extended:          http://localhost:5679")
        print("   GitLab Login:         root / (check container logs)")

    print("\n📁 Shared Folders:")
    print("   N8N Shared:           ./shared")
    if features and 'desktop' in features:
        print("   Desktop Shared:       ./desktop-shared")

    print("\n🚀 Setup Complete! Access your services using the URLs above.")

def generate_searxng_secret_key():
    """Generate a secret key for SearXNG based on the current platform."""
    # Original function from start_services.py (unchanged)
    print("Checking SearXNG settings...")

    settings_path = os.path.join("searxng", "settings.yml")
    settings_base_path = os.path.join("searxng", "settings-base.yml")

    if not os.path.exists(settings_base_path):
        print(f"Warning: SearXNG base settings file not found at {settings_base_path}")
        return

    if not os.path.exists(settings_path):
        print(f"SearXNG settings.yml not found. Creating from {settings_base_path}...")
        try:
            shutil.copyfile(settings_base_path, settings_path)
            print(f"Created {settings_path} from {settings_base_path}")
        except Exception as e:
            print(f"Error creating settings.yml: {e}")
            return
    else:
        print(f"SearXNG settings.yml already exists at {settings_path}")

    print("Generating SearXNG secret key...")
    system = platform.system()

    try:
        if system == "Windows":
            ps_command = [
                "powershell", "-Command",
                "$randomBytes = New-Object byte[] 32; " +
                "(New-Object Security.Cryptography.RNGCryptoServiceProvider).GetBytes($randomBytes); " +
                "$secretKey = -join ($randomBytes | ForEach-Object { \"{0:x2}\" -f $_ }); " +
                "(Get-Content searxng/settings.yml) -replace 'ultrasecretkey', $secretKey | Set-Content searxng/settings.yml"
            ]
            subprocess.run(ps_command, check=True)
        elif system == "Darwin":  # macOS
            openssl_cmd = ["openssl", "rand", "-hex", "32"]
            random_key = subprocess.check_output(openssl_cmd).decode('utf-8').strip()
            sed_cmd = ["sed", "-i", "", f"s|ultrasecretkey|{random_key}|g", settings_path]
            subprocess.run(sed_cmd, check=True)
        else:  # Linux
            openssl_cmd = ["openssl", "rand", "-hex", "32"]
            random_key = subprocess.check_output(openssl_cmd).decode('utf-8').strip()
            sed_cmd = ["sed", "-i", f"s|ultrasecretkey|{random_key}|g", settings_path]
            subprocess.run(sed_cmd, check=True)

        print("SearXNG secret key generated successfully.")
    except Exception as e:
        print(f"Error generating SearXNG secret key: {e}")

def main():
    parser = argparse.ArgumentParser(description='Start the Extended Local AI Package')

    # Original arguments (unchanged)
    parser.add_argument('--profile',
                       choices=['cpu', 'gpu-nvidia', 'gpu-amd', 'none'],
                       default='cpu',
                       help='Profile to use for Docker Compose (default: cpu)')

    # New feature arguments
    parser.add_argument('--features',
                       choices=['desktop', 'productivity', 'development'],
                       nargs='*',
                       default=[],
                       help='Additional features to enable (can specify multiple)')

    # Convenience flags
    parser.add_argument('--with-desktop',
                       action='store_true',
                       help='Include desktop environment (same as --features desktop)')

    parser.add_argument('--full-stack',
                       action='store_true',
                       help='Enable all features (desktop, productivity, development)')

    args = parser.parse_args()

    # Process convenience flags
    if args.with_desktop and 'desktop' not in args.features:
        args.features.append('desktop')

    if args.full_stack:
        args.features = ['desktop', 'productivity', 'development']

    # Validate .env file
    if not os.path.exists('.env'):
        print("❌ No .env file found. Please create one based on .env.example")
        print("💡 You can copy .env.example to .env and modify the values")
        sys.exit(1)

    print("🚀 Starting Extended Local AI Package...")
    print(f"📊 GPU Profile: {args.profile}")
    print(f"🔧 Features: {args.features if args.features else 'None (core only)'}")

    # Original setup functions
    clone_supabase_repo()
    prepare_supabase_env()
    generate_searxng_secret_key()

    # Extended setup functions
    setup_desktop_environment()
    if 'desktop' in args.features:
        setup_guacamole_db()

    # Stop existing containers
    stop_existing_containers(args.profile, args.features)

    # Start Supabase first (original behavior)
    print("Starting Supabase services...")
    run_command([
        "docker", "compose", "-p", "localai",
        "-f", "supabase/docker/docker-compose.yml",
        "up", "-d"
    ])

    print("Waiting for Supabase to initialize...")
    time.sleep(10)

    # Start main services
    start_services(args.profile, args.features)

    # Health checks for core services
    wait_for_service("N8N", 5678)
    wait_for_service("Open WebUI", 3000)

    # Feature-specific health checks
    if 'desktop' in args.features:
        wait_for_service("Guacamole", 8080, timeout=180)
        wait_for_service("Desktop", 6901, timeout=180)

    if 'productivity' in args.features:
        wait_for_service("AppFlowy", 8081)
        wait_for_service("AFFINE", 3010)

    if 'development' in args.features:
        wait_for_service("GitLab", 8082, timeout=300)  # GitLab takes longer
        wait_for_service("N8N Extended", 5679)

    # Display service information
    show_service_urls(args.features)

if __name__ == "__main__":
    main()
