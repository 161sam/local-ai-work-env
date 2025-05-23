

# 🧱 **1. Zielsystemüberblick**

| Typ                 | Anzahl                                        | Beschreibung               |
| ------------------- | --------------------------------------------- | -------------------------- |
| **Rack Units (RU)** | \~35–38                                       | 42U-Schrank empfohlen      |
| **Strombedarf**     | \~5–6 kW (Peak)                               | GPU + Ceph + Service Nodes |
| **Kühlung**         | ≥20.000 BTU/h                                 | bei 24/7 Dauerbetrieb      |
| **Netz**            | 1× 10 Gbit Backbone, 1 Gbit User Access       |                            |
| **Redundanz**       | USV (≥6 kVA), 2× Switch, RAID/OSD Replikation |                            |


---
![grafik](https://github.com/user-attachments/assets/16cfca9d-6506-48a7-9e1d-2b746bd031ff)

---

# 🗂️ **2. Rack-Layout (42U Vorschlag)**

```text
| U | Komponente                    | Typ           |
|----|-------------------------------|---------------|
| 42 | Patchpanel                   | Netzwerk      |
| 41 | Switch 2 (Redundanz)        | 10G L2+        |
| 40 | Switch 1 (Main)             | 10G L3 Managed |
| 39 | KVM Console Tray (optional) | Admin-Zugriff |
| 38 | Power Distribution Unit (PDU) | 2× IEC 32A    |
| 37 | Rack USV (APC, Eaton)       | ≥6kVA, 2U+     |
| 36 | Leer / Luftstrom            | –             |
| 35 | GPU Node 1                  | 4U Workstation|
| 31 | GPU Node 2                  | 4U Workstation|
| 27 | GPU Node 3                  | 4U Workstation|
| 23 | GPU Node 4                  | 4U Workstation|
| 19 | Ceph Node 1 (HotSwap)       | 2U            |
| 17 | Ceph Node 2 (HotSwap)       | 2U            |
| 15 | Ceph Node 3 (HotSwap)       | 2U            |
| 13 | Control Node 1              | 1U            |
| 12 | Control Node 2              | 1U            |
| 11 | Control Node 3              | 1U            |
| 10 | Service Node 1              | 1U            |
| 9  | Service Node 2              | 1U            |
| 8  | Service Node 3              | 1U            |
| 7  | Service Node 4              | 1U            |
| 6  | Service Node 5              | 1U            |
| 5  | Service Node 6              | 1U            |
| 4–1| Luftstrom / Reserve         | –             |
```

---

# ⚡ **3. Strombedarf & USV-Kalkulation**

## Verbrauch je Node-Typ (realistisch):

| Node-Typ     | Watt idle | Watt peak | Stück |
| ------------ | --------- | --------- | ----- |
| GPU Node     | 250–350 W | 600–800 W | 4     |
| Ceph Node    | 80–120 W  | 150–200 W | 3     |
| Control Node | 60–90 W   | 120 W     | 3     |
| Service Node | 80–100 W  | 120–150 W | 6     |

### **Gesamtleistung (Peak): \~5.5–6 kW**

* → **USV-Anlage mit mind. 6.000 VA** (z. B. APC SRT 6kVA)
* Stromzuleitung: **2× IEC 32A 230V**, besser: getrennte Phasen (A/B)
* PDU: 2× intelligent (Messung & Remote Power Switch)

---

# ❄️ **4. Kühlung (Thermische Last)**

| Leistung   | BTU/h Berechnung                     |
| ---------- | ------------------------------------ |
| 6.000 W    | 6.000 W × 3.41 = **\~20.500 BTU/h**  |
| Empfehlung | 24.000–30.000 BTU/h bei 24/7-Betrieb |
| Lösung     | Klimaschrank, Split-Klima, Kaltgang  |

> Wichtig: Luftstrom von unten nach oben, Kaltluft vorne / Warm hinten

---

# 🌐 **5. Netzwerkplanung (10G Core)**

| Komponente            | Beschreibung                         |
| --------------------- | ------------------------------------ |
| **Switch 1 (Main)**   | 24×1G + 4×10G SFP+ Managed (L3 VLAN) |
| **Switch 2 (Backup)** | für HA, Redundanz (STP/VRRP)         |
| **Verkabelung**       | Cat6A + DAC für 10G SFP+ Ports       |
| **Trunk VLANs**       | für Ceph, OpenStack, VM-Traffic      |
| **Management VLAN**   | IPMI / BMC für Remote-Access         |

---

# ✅ **Empfohlene Hardware für Strom & Netz**

| Komponente | Modell / Empfehlung                      | Preis ca.   |
| ---------- | ---------------------------------------- | ----------- |
| USV        | APC SRT 6kVA oder Eaton 9PX 6000VA       | \~2.000 €   |
| Switch     | Mikrotik CRS326-24S+2Q+ / Ubiquiti UniFi | \~400 €     |
| Rack       | Digitus 42U 800×1000 mm, Mesh-Door       | \~700 €     |
| PDUs       | Rittal iPDU (intelligent, 16–32A)        | \~300–500 € |
| Klima      | Split-Klima 24k BTU (Mitsubishi, Daikin) | \~1.500 €   |

---

## ✅ Als Nächstes lieferbar:

1. ✅ Visuelles Rack-Diagramm als PNG oder PDF
2. ✅ Einkaufsliste mit Bezugsquellen (DE/EU)
3. ✅ Konfigurierbares Rack-Plan-Template (CSV/Excel)
4. ✅ Kühl- und USV-Sizing-Skript zur Anpassung

Was darf ich dir zuerst ausarbeiten?
