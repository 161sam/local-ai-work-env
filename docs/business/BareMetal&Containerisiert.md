
* **OpenStack: Bare Metal-Installation aller Control-/Compute-Komponenten**
* **User-Services: Containerisiert (Docker/Podman) innerhalb der VMs**

Das ergibt ein leistungsfähiges, modular wartbares Setup. Hier ist dein **konkreter Fahrplan**, um **OpenStack manuell auf deinen zwei Nodes + 1 NAS aufzusetzen**, **ohne DevStack oder Kolla**, aber mit produktionsnahem Fokus.

---

## 🧱 **Setup-Ziel: Bare-Metal OpenStack mit Containerisierten User-Desktops**

---

## 🔧 **1. Voraussetzungen / Planung**

| Hostname | Rolle                      | Hardware           |
| -------- | -------------------------- | ------------------ |
| `node1`  | Control + Compute          | i7, 64GB RAM       |
| `node2`  | GPU Compute Node           | i9, 64GB RAM + GPU |
| `rpi4`   | Shared Storage (NFS/MinIO) | 8GB, SSD/USB       |

**OS-Empfehlung:** `Ubuntu Server 22.04 LTS` (kein Desktop)

---

## 🛠️ **2. Netzwerkplan**

| Interface | Zweck            | IP-Bereich         | Beispiel-IP       |
| --------- | ---------------- | ------------------ | ----------------- |
| `eth0`    | Management + API | `192.168.100.0/24` | `192.168.100.10`  |
| `br-ex`   | External Network | `192.168.1.0/24`   | Floating IP Range |

🧠 Wir nutzen `Open vSwitch (OVS)` für externes Bridging.

---

## 🧰 **3. OpenStack Services auf node1 (Controller + Compute)**

### Komponenten:

| Service              | Zweck                          |
| -------------------- | ------------------------------ |
| Keystone             | Auth / Identity                |
| Glance               | VM Images                      |
| Nova (API + Compute) | VM-Provisionierung             |
| Neutron              | Netzwerk                       |
| Cinder (optional)    | Block Storage (lokal oder NFS) |
| Horizon              | Web UI                         |
| Placement            | Ressourcenplanung              |
| MariaDB              | Backend-DB für OpenStack       |
| RabbitMQ             | Messaging                      |
| Memcached            | Caching für Tokens             |

---

## 🚀 **4. Installationsanleitung (Zusammenfassung)**

### 🔸 **\[A] Node vorbereiten (node1 + node2)**

```bash
sudo apt update
sudo apt install software-properties-common
sudo add-apt-repository cloud-archive:yoga  # oder antelope
sudo apt update && sudo apt dist-upgrade
```

```bash
# Netzwerk vorbereiten
sudo apt install openvswitch-switch
ovs-vsctl add-br br-ex
ovs-vsctl add-port br-ex eth0
```

---

### 🔸 **\[B] MariaDB, RabbitMQ, Memcached (node1)**

```bash
sudo apt install mariadb-server rabbitmq-server memcached
# Konfigurationsdateien sichern + anpassen
```

---

### 🔸 **\[C] Keystone – Identity Service**

```bash
sudo apt install keystone apache2 libapache2-mod-wsgi-py3
# Datenbank anlegen
mysql -u root -p
CREATE DATABASE keystone;
GRANT ALL PRIVILEGES ON keystone.* TO 'keystone'@'localhost' IDENTIFIED BY 'KEYSTONE_PASS';
```

Konfiguriere `/etc/keystone/keystone.conf` → DB, Token Provider (`fernet`)

---

### 🔸 **\[D] Glance – Image Service**

```bash
sudo apt install glance
# DB: CREATE DATABASE glance;
# Konfiguration: /etc/glance/glance-api.conf
```

Upload Beispiel-Image:

```bash
openstack image create "Ubuntu AI-Desktop" --file ubuntu-desktop-ai.qcow2 --disk-format qcow2 --container-format bare --public
```

---

### 🔸 **\[E] Nova – Compute & API (node1 + node2)**

Install auf beiden Nodes:

```bash
sudo apt install nova-compute
```

Nur auf `node1`:

```bash
sudo apt install nova-api nova-scheduler nova-conductor nova-novncproxy
```

Konfiguriere `/etc/nova/nova.conf` auf beiden:

* DB, Keystone, Glance, Neutron
* \[gpu] section (nur auf `node2`):

  ```
  [pci]
  alias = { "name": "gpu", "product_id": "1eb8", "vendor_id": "10de", "device_type": "type-PCI" }
  ```

---

### 🔸 **\[F] Neutron – Netzwerk (VXLAN)**

```bash
sudo apt install neutron-server neutron-plugin-ml2 neutron-linuxbridge-agent neutron-dhcp-agent neutron-metadata-agent
```

Konfiguriere:

* `/etc/neutron/plugins/ml2/ml2_conf.ini`
* `/etc/neutron/neutron.conf`
* `/etc/neutron/plugins/ml2/linuxbridge_agent.ini`

---

### 🔸 **\[G] Horizon – Web UI**

```bash
sudo apt install openstack-dashboard
# Zugriff via https://<node1_ip>/horizon
```

---

### 🔸 **\[H] Optional: Cinder mit NFS oder LVM**

```bash
sudo apt install cinder-volume
# Cinder Backend: /dev/sdX oder NFS vom Pi4
```

---

## 🧠 **5. User-Desktops mit Docker-Containern**

**Image (per Glance): Ubuntu 22.04 + XFCE + cloud-init**

> Bereitgestellte Container im Image:

* `docker-compose.yml` enthält:

  * `ollama` (GPU via `--gpus all`)
  * `n8n`
  * `qdrant`
  * `open-webui`
  * `flowise`
  * `supabase`
  * `searxng`
  * `zed`
  * `gitlab` (optional lightweight oder Runner)

→ Alles vorinstalliert, automatisch gestartet via cloud-init oder Systemd:

```yaml
#cloud-config
write_files:
  - path: /opt/start-ai.sh
    permissions: '0755'
    content: |
      #!/bin/bash
      docker compose -f /opt/docker-compose.yml up -d
runcmd:
  - /opt/start-ai.sh
```

---

## 🌐 **6. Netzwerk: Floating IPs + Neutron VXLAN**

* Floating IP Bereich: z. B. `192.168.1.100-192.168.1.120`
* Neutron verbindet interne Netze → Extern über `br-ex`
* SSH + Guacamole über Floating IP erreichbar

---

## 📁 **7. Shared Storage (rpi4)**

> Pi4 als **NFS-Server** oder **MinIO (S3)**

```bash
# NFS:
sudo apt install nfs-kernel-server
sudo mkdir -p /export/shared
sudo chown nobody:nogroup /export/shared
echo "/export/shared *(rw,sync,no_subtree_check)" >> /etc/exports
exportfs -a
```

Mount in den VMs:

```bash
sudo mount -t nfs 192.168.100.30:/export/shared /shared
```

---

## ✅ Fazit: Du erreichst damit...

| Feature                           | Umsetzung (jetzt)           | Skalierbar (später)  |
| --------------------------------- | --------------------------- | -------------------- |
| **Bare Metal OpenStack**          | Direkt auf node1/node2      | +15 Nodes später     |
| **GPU-Support für Ollama etc.**   | Docker mit NVIDIA Runtime   | Multi-GPU Nodes      |
| **User Desktop-VMs mit Services** | cloud-init + docker-compose | Templates skalierbar |
| **Storage via Pi4**               | NFS oder MinIO              | → Ceph später        |

---

