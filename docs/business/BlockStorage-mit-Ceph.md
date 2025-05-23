

## 🧠 **Ziel:** Ceph als Ersatz für Pi-basierte NFS/MinIO in deiner späteren OpenStack-Produktionsumgebung

📦 *Ceph soll dienen für: RBD (Block Storage), CephFS (/shared), RGW (S3)*

---

## 💡 **Minimale Hardware-Anforderungen (für Test + kleine Produktion)**

| Rolle        | CPU    | RAM  | Disk Setup              | Kommentar                          |
| ------------ | ------ | ---- | ----------------------- | ---------------------------------- |
| **Ceph MON** | 2 vCPU | 4 GB | SSD                     | Metadata/Quorum, kein Datenvolumen |
| **Ceph MGR** | 2 vCPU | 2 GB | –                       | Verwaltungs-Dienst                 |
| **Ceph OSD** | 4 vCPU | 8 GB | 1× SSD oder HDD per OSD | Haupt-Storage pro Device           |
| **Ceph MDS** | 2 vCPU | 4 GB | –                       | Nur nötig für CephFS               |
| **Ceph RGW** | 2 vCPU | 2 GB | optional                | S3-kompatibles Objekt-Storage      |

---

### 🔸 **Empfohlene Node-Größe pro Ceph-Node (Minimum):**

| Ressource    | Empfehlung pro Node                   |
| ------------ | ------------------------------------- |
| **CPU**      | ≥ 4 vCPU                              |
| **RAM**      | ≥ 16 GB                               |
| **Storage**  | 1 SSD für System, 1+ HDD/SSD für OSDs |
| **Netzwerk** | 1 Gbit/s (10 Gbit/s empfohlen)        |

> Du brauchst mindestens **3 Nodes** für ein stabiles Ceph-Cluster mit MON-Quorum!

---

## 📐 Beispiel: Minimal-Ceph-Cluster für dich (3 Nodes)

| Node    | Rolle              | Geräte                     |
| ------- | ------------------ | -------------------------- |
| `ceph1` | MON, MGR, OSD      | 1x System-SSD + 1x 2TB HDD |
| `ceph2` | MON, OSD           | 1x System-SSD + 1x 2TB HDD |
| `ceph3` | MON, MDS, OSD, RGW | 1x System-SSD + 1x 2TB HDD |

---

## 📊 **Ressourcenverbrauch pro Dienst (realistisch)**

| Dienst   | RAM idle | RAM unter Last | CPU idle | CPU Last |
| -------- | -------- | -------------- | -------- | -------- |
| MON      | \~150 MB | \~300 MB       | <5%      | \~15%    |
| MGR      | \~200 MB | \~400 MB       | <5%      | \~20%    |
| OSD (1x) | \~800 MB | 2–4 GB         | 10–40%   | bis 80%  |
| MDS      | \~500 MB | 1–2 GB         | 5–20%    | bis 50%  |
| RGW      | \~400 MB | 1 GB           | 5–15%    | bis 30%  |

---

## ⚠️ Wenn du *jetzt* Ceph testen willst, aber nur 2 Nodes hast:

> Du **kannst temporär** mit einem **reduzierten 1-Node-Ceph-Cluster** arbeiten, **ABER**:

* ❌ Kein Redundanz
* ⚠️ Nicht fehlertolerant
* ✅ Gut für Funktionstests mit CephFS/RBD/RGW

Beispiel auf `node1`:

```bash
# mit cephadm:
cephadm bootstrap --mon-ip 192.168.100.10
ceph orch apply osd --all-available-devices
ceph fs volume create sharedfs
```

---

## 🧾 **Fazit: Was brauchst du für produktiven Ceph-Storage?**

| Ziel                     | Hardware-Anforderung                      |
| ------------------------ | ----------------------------------------- |
| **Testbetrieb (1 Node)** | 4 vCPU, 16GB RAM, 2 SSD/HDD               |
| **Produktiv (3 Nodes)**  | je Node: 4–8 vCPU, 16–32GB RAM, 2–4 Disks |
| **High-Performance**     | 10 Gbit Netz, SSD/PCIe/NVMe für OSDs      |

---

## ✅ Vorschlag

Wenn du Ceph *ernsthaft produktiv* betreiben willst:

* Warte bis du **mind. 3 Nodes mit >16 GB RAM + SSD/HDD-Kombi** hast
* Nutze **`cephadm` oder `ceph-ansible`** für automatisiertes Setup
* Beginne mit **RBD + CephFS**, RGW (S3) später

---
