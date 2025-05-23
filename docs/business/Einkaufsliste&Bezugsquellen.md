Hier ist eine **Einkaufsliste für deine OpenStack AI-Cluster-Hardware**, optimiert für den **Eigenbetrieb in Deutschland/EU**. Ich habe Komponenten ausgewählt, die bei bekannten Anbietern wie **ServerShop24, Mindfactory, Alternate, Thomas-Krenn, Jacob Elektronik, Reichelt** oder **eBay Business** verfügbar sind.

---

# 🛒 **Einkaufsliste nach Node-Typ (mit Bezugsquellen)**

---

## 🖥️ **1. Control Nodes (3×)**

| Komponente | Empfehlung                      | Bezugsquelle                                 | Einzelpreis (ca.)  |
| ---------- | ------------------------------- | -------------------------------------------- | ------------------ |
| Server     | Supermicro 1U SYS-5019C-MR      | [Thomas-Krenn](https://www.thomas-krenn.com) | 950 €              |
| RAM        | 2×32 GB DDR4 ECC                | \[Mindfactory / Alternate]                   | 250 €              |
| SSDs (OS)  | 2× Samsung PM893 480 GB (RAID1) | \[Jacob Elektronik]                          | 130 €              |
| Gesamt     |                                 |                                              | \~1.250 € pro Node |

---

## ⚡ **2. GPU Nodes (4–6×)**

| Komponente          | Empfehlung                              | Bezugsquelle               | Einzelpreis (ca.) |
| ------------------- | --------------------------------------- | -------------------------- | ----------------- |
| Workstation Chassis | Fractal Design Define 7 XL (Silent)     | \[Caseking / Mindfactory]  | 180 €             |
| Mainboard           | ASUS WRX80 PRO WS / Supermicro H12SSL   | \[ServerShop24 / eBay Pro] | 550–700 €         |
| CPU                 | AMD Threadripper PRO 3955WX (16c/32t)   | \[eBay Pro / Mindfactory]  | 800–1000 €        |
| RAM                 | 8×16 GB DDR4 ECC                        | \[Mindfactory]             | 450–500 €         |
| GPU                 | NVIDIA RTX A6000 (48 GB)                | \[eBay Business / Jacob]   | 3.500–4.500 €     |
| SSD NVMe            | 2× Samsung 980 Pro / PM9A3 (RAID1)      | \[Reichelt / Mindfactory]  | 250 €             |
| Netzteil            | 1000–1200W Platinum (BeQuiet, Seasonic) | \[Caseking]                | 220 €             |
| Gesamt              |                                         |                            | \~4.500–5.000 €   |

---

## 🗃️ **3. Ceph Storage Nodes (3–5×)**

| Komponente       | Empfehlung                           | Bezugsquelle                | Einzelpreis (ca.) |
| ---------------- | ------------------------------------ | --------------------------- | ----------------- |
| 2U Servergehäuse | Supermicro CSE-826 (8× 3.5" HotSwap) | \[ServerShop24 / Reuse]     | 350 €             |
| CPU              | Intel Xeon Silver 4210 / 4310        | \[Thomas-Krenn]             | 400–500 €         |
| RAM              | 64 GB ECC DDR4                       | \[Mindfactory]              | 250–300 €         |
| SSDs (OS)        | 2× Samsung PM893 500 GB              | \[Jacob / MF]               | 120 €             |
| HDDs (OSDs)      | 2× Seagate Exos 8–16 TB              | \[Mindfactory / Reichelt]   | 250–300 €         |
| Journal SSD      | 1× Samsung PM9A3 1 TB                | \[Mindfactory / ServerShop] | 140 €             |
| NIC              | Intel X550-T2 (10 Gbit Dual Port)    | \[Reichelt / Jacob]         | 100–120 €         |
| Gesamt           |                                      |                             | \~1.300–1.500 €   |

---

## ⚙️ **4. Service Nodes (6×)**

| Komponente | Empfehlung                       | Bezugsquelle                   | Einzelpreis (ca.) |
| ---------- | -------------------------------- | ------------------------------ | ----------------- |
| 1U Server  | Supermicro SYS-5019S / Dell R240 | \[ServerShop24 / Thomas-Krenn] | 950 €             |
| CPU        | Intel Xeon E-2288G (8c/16t)      | \[eBay Pro / MF]               | 350 €             |
| RAM        | 64 GB DDR4 ECC                   | \[Alternate / MF]              | 250 €             |
| SSD        | 2× Samsung PM9A3 1 TB            | \[Reichelt / Jacob]            | 240 €             |
| Gesamt     |                                  |                                | \~1.200 €         |

---

## 🧵 **5. Infrastruktur**

| Komponente            | Empfehlung                              | Bezugsquelle             | Preis       |
| --------------------- | --------------------------------------- | ------------------------ | ----------- |
| Rack (42U)            | Digitus / Triton 800×1000 mm            | \[Reichelt / eBay]       | \~700 €     |
| PDU (intelligent)     | Rittal / APC iPDU                       | \[Voelkner / Jacob]      | \~400–500 € |
| USV                   | APC SRT 6kVA Online                     | \[APC / Reichelt]        | \~2.000 €   |
| Switch                | Mikrotik CRS326-24S+2Q+ / Unifi 48-Port | \[MSK Computer / Amazon] | \~400 €     |
| Klimaanlage (24k BTU) | Mitsubishi Split 7 kW / Daikin          | \[klimaworld.de]         | \~1.500 €   |

---

# ✅ Gesamtprojekteinkauf (abgerundet)

| Komponente                                | Preis (netto)  |
| ----------------------------------------- | -------------- |
| Nodes (GPU + Storage + Control + Service) | \~34.000 €     |
| Infrastruktur (Rack, Switches, USV)       | \~5.000 €      |
| Reserve / Ersatzteile / Kühlung           | \~5.000 €      |
| **Gesamt**                                | **\~44.000 €** |

---

