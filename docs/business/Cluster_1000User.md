

# 🧱 **Cluster-Ziel: 1000 aktive Nutzer, skalierbar, selbstbetrieben**

## **Gesamtkonzept: 4 Gruppen von Nodes**

* **Control Nodes** (OpenStack Core)
* **GPU Compute Nodes** (LLMs mit Ollama)
* **Ceph Storage Nodes** (RBD, CephFS, S3)
* **Service Nodes** (zentrale Dienste, WebApps, CI/CD)

---

## 🖥️ **1. Control Nodes (3×)**

**Zweck:** Keystone, Glance, Neutron, Horizon, MariaDB, RabbitMQ, HAProxy

| Komponente      | Modell / Empfehlung                  | Einzelpreis |
| --------------- | ------------------------------------ | ----------- |
| CPU             | Intel Xeon Silver 4310 (2×10c)       | \~400 €     |
| Mainboard       | Supermicro X12 Series (BMC, IPMI)    | \~350 €     |
| RAM             | 64 GB ECC DDR4 (2×32 GB)             | \~250 €     |
| Storage (OS)    | 2× Samsung PM893 SSD (RAID1, 480 GB) | \~140 €     |
| Netzteil + Case | 500W Gold + 2U Rack oder Tower       | \~150 €     |
| Netzwerkkarte   | 2× 1 Gbit (Onboard reicht)           | –           |

**Summe pro Node:** \~1.250 €
**3 Nodes:** \~3.750 €

---

## ⚡ **2. GPU Compute Nodes (4–6×)**

**Zweck:** LLM-Inferenz mit Ollama (z. B. Mistral, LLaMA, Codellama)

| Komponente         | Modell / Empfehlung                     | Einzelpreis   |
| ------------------ | --------------------------------------- | ------------- |
| CPU                | AMD Threadripper Pro 3955WX (16c/32t)   | \~800 €       |
| Mainboard          | WRX80 Pro WS (ASUS / Supermicro)        | \~600 €       |
| RAM                | 128 GB DDR4 ECC (8×16 GB)               | \~500 €       |
| GPU                | NVIDIA RTX A6000 (48 GB) / L40S / 3090  | 2.000–4.000 € |
| Storage (OS)       | 2× Samsung PM9A3 NVMe (RAID1, 1 TB)     | \~300 €       |
| Netzwerkkarte      | 10 Gbit SFP+ Dual-Port (Intel X520)     | \~100 €       |
| Kühlung + Netzteil | 1200W Platinum + Workstation-Tower/Rack | \~300 €       |

**Summe pro Node:** 4.500–5.000 €
**4 Nodes (RTX A6000):** \~18.000–20.000 €

---

## 🗃️ **3. Ceph Storage Nodes (3–5×)**

**Zweck:** RBD für VMs, CephFS für `/shared`, RGW für S3

| Komponente     | Modell / Empfehlung                           | Einzelpreis |
| -------------- | --------------------------------------------- | ----------- |
| CPU            | Intel Xeon Silver 4310                        | \~400 €     |
| RAM            | 64–128 GB ECC DDR4                            | \~300 €     |
| Boot SSDs      | 2× Samsung 870 EVO (RAID1, 500 GB)            | \~120 €     |
| OSD Disks      | 2× 8 TB Seagate Exos HDD (SATA 7200 RPM)      | \~300 €     |
| Journaling SSD | 1× Samsung PM9A3 NVMe (1 TB)                  | \~150 €     |
| Netzwerkkarte  | Intel X550 10 Gbit Dual-Port (SFP+ oder RJ45) | \~100 €     |
| Gehäuse + PSU  | 3U Rack 8-Bay HotSwap, 750W Redundant PSU     | \~400 €     |

**Summe pro Node:** \~1.300–1.600 €
**3–5 Nodes:** \~5.000–8.000 €

---

## ⚙️ **4. Service Nodes (6–10×)**

**Zweck:** GitLab, Qdrant, Langfuse, N8N, Web UIs, Supabase, etc.

| Komponente    | Modell / Empfehlung                | Einzelpreis |
| ------------- | ---------------------------------- | ----------- |
| CPU           | AMD EPYC 7302P (16c/32t)           | \~650 €     |
| RAM           | 64 GB DDR4 ECC                     | \~250 €     |
| Storage (OS)  | 2× Samsung PM893 SSD (RAID1, 1 TB) | \~200 €     |
| Netzwerkkarte | Intel i350 1 Gbit Quad-Port        | \~80 €      |
| Gehäuse + PSU | 2U Rack, 600W Gold                 | \~150 €     |

**Summe pro Node:** \~1.200 €
**6 Nodes:** \~7.200 €

---

## 🧮 **Gesamtkalkulation (Konservativ)**

| Kategorie         | Anzahl | Preis (ca.)            |
| ----------------- | ------ | ---------------------- |
| Control Nodes     | 3×     | 3.750 €                |
| GPU Nodes (A6000) | 4×     | 18.000 €               |
| Ceph Nodes        | 3×     | 5.000 €                |
| Service Nodes     | 6×     | 7.200 €                |
| **Gesamt**        |        | **\~33.950 €** (netto) |

> Mit 20 % Reserve und Netzwerk-/USV-Infrastruktur: **\~40.000–45.000 € Brutto**

---


