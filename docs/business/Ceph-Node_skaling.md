## Geplantes Ceph-Setup mit:

* **System-SSD (OS, Ceph-Dienste)**
* **2× 4TB HDDs für OSDs pro Node**

---

## 📦 **Empfohlene Größe für die System-SSD je Ceph-Node**

| System-SSD | Größe (empfohlen) | Begründung                                                       |
| ---------- | ----------------- | ---------------------------------------------------------------- |
| **Min.**   | **120 GB**        | Funktioniert für reinen Ceph-Testbetrieb ohne zusätzliche Rollen |
| **Empf.**  | **240–480 GB**    | Genug für:                                                       |

* OS (Ubuntu Server)
* `cephadm` Daten
* Ceph Logs
* Ceph MON, MGR, MDS, RGW
* ggf. Crash Dumps, Prometheus-Lokale Daten
* Paket-Cache
* Docker/Podman Layer (wenn nicht ausgelagert) |
  \| **Optimal** | **>480 GB (z. B. 1 TB)** | Reserven für zukünftige Erweiterungen (RGW Cache, Grafana, Node Exporter, etc.) |

---

## 📁 **Platzbedarf im Detail (Erfahrung aus realem Cluster)**

| Pfad                   | Typ             | Typischer Platzbedarf           |
| ---------------------- | --------------- | ------------------------------- |
| `/var/lib/ceph/`       | Ceph-Dienste    | 2–10 GB je Rolle                |
| `/var/log/ceph/`       | Logs            | 500 MB – mehrere GB             |
| `/var/lib/docker/`     | (falls genutzt) | >10 GB schnell möglich          |
| `/var/lib/ceph/crash/` | Crash Reports   | bis 10 GB (wächst ohne Cleanup) |
| `/var/lib/ceph/mon/`   | MON Daten       | ca. 500 MB – 1 GB               |
| `/var/lib/ceph/mgr/`   | MGR Daten       | <1 GB                           |

---

## 💡 **Empfehlungen für dein Setup**

Da du:

* 2× 4TB HDDs als OSD pro Node hast,
* und sicher Ceph MON, MGR, evtl. MDS + RGW auf der SSD betreiben willst,

empfehle ich:

### ✅ **System-SSD: Mindestens 240 GB, besser 480–512 GB**

* SSD sollte *nicht* als OSD verwendet werden – das würde Systemstabilität riskieren
* Nutze *eine separate Partition für `/var/lib/ceph`*, wenn möglich

---

## 🔒 Zusatztipp: SSD Haltbarkeit

* Setze **Consumer-SSDs mit guter TBW** (z. B. Samsung 870 EVO) oder besser: **Enterprise SSDs (Intel DC, Samsung PM-Serie)**
* **Aktiviere TRIM**:

  ```bash
  sudo systemctl enable fstrim.timer
  ```

---

## 📌 Zusammengefasst

| Frage                        | Antwort                                         |
| ---------------------------- | ----------------------------------------------- |
| **Wie groß?**                | 240–512 GB SSD (besser 480+ für Reserve)        |
| **Warum?**                   | Ausreichend für Ceph-Dienste, Logs, Container   |
| **Was nicht tun?**           | System-SSD als OSD benutzen                     |
| **Was zusätzlich bedenken?** | TRIM, Log-Rotation, ggf. extra `/var` Partition |

---

