**Stabilitäts- und Skalierbarkeitsgründen absolut zu empfehlen**. 
OpenStack ist auf mindestens **3 Control-Plane-Hosts** + verteilte Komponenten ausgelegt – auf 2 Nodes ist es nicht HA-fähig. Durch das Verlegen des Clusters in die Cloud kannst du:

* mit standardisierten VMs und Images arbeiten,
* einfacher skalieren,
* sauber deine Ceph-, GPU- und Worker-Rollen trennen,
* dein Setup später on-prem replizieren (Infrastructure as Code),
* **und deine zwei lokalen Server als Compute-Nodes hinzufügen**, sobald OpenStack läuft.

---

## ✅ Empfohlener Plan: OpenStack in der Cloud bereitstellen

### **Optionen für Cloud-Hosting von OpenStack**

| Provider                          | Typ                        | Vorteil                                             |
| --------------------------------- | -------------------------- | --------------------------------------------------- |
| **AWS EC2**                       | Self-managed VMs           | Voller Zugriff, flexible Netze, einfache Skalierung |
| **Hetzner Cloud**                 | Bare Metal + StorageBox    | Preisgünstig, europäisch, feste IPs                 |
| **OVH / IONOS**                   | Bare Metal mit Root-Zugang | Günstig bei viel Storage & Bandbreite               |
| **Terraform + OpenStack-Ansible** | Plattformunabhängig        | Sauber versionierbar, wiederholbar                  |

---

## 🧠 Strategievorschlag: **Cloud-gehosteter OpenStack Core + lokale Erweiterung**

### **1. Architekturmodell (Cloud)**

| Rolle         | Anzahl | Cloud-Ressourcen               |
| ------------- | ------ | ------------------------------ |
| Control Plane | 3x     | 3 EC2 VMs (4 vCPU, 8–16 GB)    |
| Ceph Cluster  | 3x     | EBS + Ceph auf 3 Nodes         |
| GPU Worker    | 1–2x   | EC2 G4/G5 oder p3/p4 instances |
| Service Nodes | 2–3x   | Standard VMs (8 vCPU, 16 GB)   |

> Du kannst alle VMs mit Terraform erzeugen, mit OpenStack-Ansible provisionieren und via VPN mit deinen On-Prem Nodes verbinden.

---

## ⚙️ Empfohlenes Setup-Tool: **OpenStack-Ansible (OSA)**

### Vorteile:

* Vollständige OpenStack-Installation in VMs
* Rollenbasiert (keystone, glance, nova, neutron, horizon…)
* YAML-Driven, CI-fähig
* Unterstützt Ceph-Backend nativ
* Später auf Bare Metal übertragbar

**Repo:** [https://opendev.org/openstack/openstack-ansible](https://opendev.org/openstack/openstack-ansible)

---

## 🧱 Setup-Strategie in der Cloud

### A. Infrastruktur bereitstellen (z. B. mit Terraform)

```hcl
resource "aws_instance" "controller_1" {
  ami           = "ami-xyz"
  instance_type = "t3.large"
  ...
}
```

### B. OpenStack mit OSA installieren

1. Base-VM mit Ubuntu 22.04
2. Git Clone von `openstack-ansible`
3. Run Book:

   ```bash
   scripts/bootstrap-ansible.sh
   openstack-ansible playbooks/setup-hosts.yml
   openstack-ansible playbooks/setup-infrastructure.yml
   openstack-ansible playbooks/setup-openstack.yml
   ```

---

## 🌐 Netzwerk & Zugriff

| Komponente            | Empfehlung                         |
| --------------------- | ---------------------------------- |
| OpenStack API         | Floating IP + Security Group       |
| Horizon               | HTTPS über LB                      |
| Internal API Net      | VXLAN oder flannel                 |
| VPN (lokal <-> Cloud) | WireGuard / OpenVPN (Site-to-Site) |

---

## ☁️ Cloud-Setup Vorteile

| Vorteil                              | Bedeutung für dich                         |
| ------------------------------------ | ------------------------------------------ |
| Reproduzierbar mit Terraform/Ansible | → später on-prem identisch einsetzbar      |
| Hochverfügbar & sicher               | → produktionsfähig                         |
| Trennung von Storage / Compute       | → realistische Enterprise-Architektur      |
| Skalierbarkeit nach Bedarf           | → Test- vs. Produktionsumgebungen trennbar |

---
