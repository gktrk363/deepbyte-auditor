# 🔍 DeepByte Auditor

<p align="center">
  <img src="https://img.shields.io/github/v/release/gktrk363/deepbyte-auditor?style=for-the-badge&color=red" />
  <img src="https://img.shields.io/badge/Platform-Windows-0078D4?style=for-the-badge&logo=windows&logoColor=white" />
  <img src="https://img.shields.io/badge/Python-3.10+-yellow?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" />
</p>

### **Advanced Project Analytics & Disk Optimization Suite**
### **Gelişmiş Proje Analiz ve Disk Optimizasyon Paketi**

**DeepByte Auditor**, özellikle büyük ölçekli yazılım ekosistemleri ve oyun geliştirme süreçleri için tasarlanmış, yüksek performanslı bir veri denetleme ve görselleştirme aracıdır. Gereksiz proje şişkinliklerini (binary artifacts, cache files, untracked logs) saniyeler içinde analiz ederek geliştirme verimliliğini artırır.

---

## 📸 Preview | Önizleme

<p align="center">
  <img src="DeepByteAuditor.png" width="850" alt="DeepByte Auditor Dashboard" />
  <br>
  <i>Crimson Dashboard: Real-time project indexing and hierarchical distribution analysis.</i>
</p>

---

## 🚀 Core Capabilities | Temel Yetenekler

| Feature | TR Açıklama | EN Description |
| :--- | :--- | :--- |
| **Concurrent Indexing** | Çok izlekli (multi-threaded) tarama motoru ile sıfır gecikme. | Non-blocking data indexing via asynchronous thread architecture. |
| **Heuristic Identification** | Uzantısız veya gizli dosyaları akıllı algoritmalarla tanımlama. | Identifies untracked binary data using smart heuristic classification. |
| **Analytical Visuals** | Matplotlib tabanlı derinlemesine veri görselleştirme paneli. | High-fidelity data visualization and distribution charts. |
| **Optimized UX** | Düşük kaynak tüketimli, statik ve profesyonel "Crimson" arayüzü. | Performance-centric, zero-hover static production UI. |

---

## ⚙️ Technical Workflow | Çalışma Prensibi

1. **Scan Phase:** Uygulama, belirtilen kök dizini asenkron olarak tarayarak dosya meta verilerini toplar.
2. **Analysis Phase:** Toplanan veriler **Pandas** dataframe yapısına aktarılır ve boyut/tür analizi yapılır.
3. **Visualization:** Analiz sonuçları **Matplotlib** üzerinden hiyerarşik ve dairesel grafiklere dönüştürülür.
4. **Reporting:** Kullanıcıya en çok yer kaplayan dizinler ve dosya türleri anlık olarak raporlanır.

---

## 📥 Deployment | Kurulum ve Kullanım

**TR:** Hiçbir bağımlılık yüklemeden kullanmak için [Releases](https://github.com/gktrk363/deepbyte-auditor/releases) sayfasından `.exe` sürümünü indirin ve çalıştırın.

**EN:** For standalone production usage, download the latest `.exe` from the [Releases](https://github.com/gktrk363/deepbyte-auditor/releases) section. No Python environment required.

---

## 🛡️ License | Lisans

This project is licensed under the **MIT License**.

---
<p align="right">
  Developed by <b>gktrk363</b>
</p>
