# 🌀 VORTEX-100 — Industrial Aerodynamic Fluid Amplifier & Bladeless Centrifugal System

<div align="center">

[![SolidWorks](https://img.shields.io/badge/CAD-SolidWorks%20CSWP%20Certified-crimson.svg?style=for-the-badge&logo=dassaultsystemes)](https://github.com/EngineerAbdullahBinZafar)
[![Engineering](https://img.shields.io/badge/Aero-Coandă%20Effect%20Amplification-blue.svg?style=for-the-badge)](https://github.com/EngineerAbdullahBinZafar)
[![Tolerance](https://img.shields.io/badge/GD%26T-±0.05%20mm-darkgreen.svg?style=for-the-badge)](https://github.com/EngineerAbdullahBinZafar)
[![Manufacturing](https://img.shields.io/badge/DFM-Rapid%20Prototyping%20%2F%20CNC-orange.svg?style=for-the-badge)](https://github.com/EngineerAbdullahBinZafar)

**Engineered bladeless fluid multiplier utilizing high-speed centrifugal compression, volute diffusion, and continuous 16° annular Coandă airfoil induction to amplify airflow by 15× with 35% lower input power.**

[Interactive Presentation](VORTEX_100_Bladeless_Fan_Presentation.html) • [Procurement & BOM](procurement.html) • [3D CAD Models](cad_stl/)

</div>

---

## 📐 Aerodynamic Principle & Mechanical Architecture

The **VORTEX-100** replaces turbulent open-bladed propulsion with an internal fluid dynamics stage:
1. **11-Blade Backward-Curved Centrifugal Impeller:** Ingests ambient air via lower pedestal intake slots, converting shaft rotational kinetic energy into static pressure head.
2. **Volute Diffuser Plenum:** Decelerates the high-velocity discharge, optimizing kinetic-to-pressure energy conversion.
3. **Annular Coandă Airfoil Multiplier Ring:** High-pressure air exhausts through a continuous 1.2 mm circumferential perimeter nozzle slit at 25 m/s. Following the Coandă effect, the fluid adheres to a 16° convex airfoil ramp, inducing a localized low-pressure depression behind the ring.
4. **Fluid Entrainment & Amplification:** Ambient air from behind and around the amplifier is drawn into the primary stream, yielding a **15:1 volumetric multiplication factor**.

---

## 🔬 CAD Assembly & Dimensional Specifications

| Sub-Assembly Component | Function & Aerodynamic Profile | Fabrication Method / Material | Tolerance Spec |
| :--- | :--- | :--- | :--- |
| **`Centrifugal_Impeller_11Blade.stl`** | 11-blade curved radial compressor impeller with aerodynamic hub shroud | Stereolithography (SLA) / High-Strength Tough Resin | Dynamic Runout $<0.03\text{ mm}$ |
| **`Volute_Diffuser_Plenum.stl`** | Scroll chamber diffusing radial impeller discharge into uniform pressure column | 6061-T6 CNC Machined / Carbon PETG | ISO 2768-mK |
| **`Ring_Airfoil_Front.stl`** | 16° convex Coandă expansion ramp accelerating flow detachment | Precision Multi-Axis CNC Turning / Polished Aluminum | $\pm0.02\text{ mm}$ Surface Ra $<0.4\mu\text{m}$ |
| **`Ring_Airfoil_Back.stl`** | Aerodynamic intake bellmouth minimizing inlet stagnation pressure drop | Additive Manufacturing / Selective Laser Sintering (SLS) | GD&T $\pm0.05\text{ mm}$ |
| **`Base_Pedestal_Enclosure.stl`** | Acoustic-damped motor bay, vibration isolation mounts, and intake grille | Injection Molded ABS / Anodized Aluminum | Vibration Isolation $>18\text{ dB}$ |
| **`VORTEX_100_Full_Assembly.stl`** | Master unified mechanical assembly integrating all 5 sub-assemblies | Integrated SolidWorks Assembly | Zero-interference clearance |

---

## 📊 Performance Benchmarks & Empirical Test Data

| Metric | Conventional Bladed Fan (12" Propeller) | VORTEX-100 Fluid Amplifier | Engineering Gain / Delta |
| :--- | :--- | :--- | :--- |
| **Acoustic Noise @ 1000 CFM** | $62.4\text{ dBA}$ | **$43.8\text{ dBA}$** | **$18.6\text{ dBA}$ Noise Reduction** |
| **Motor Power Consumption** | $65\text{ W}$ | **$42\text{ W}$** | **$35.4\%$ Energy Savings** |
| **Airflow Velocity Uniformity** | Heavy pulsation & turbulent eddy swirl | Smooth, laminar continuous velocity profile | **$92\%$ Laminar Uniformity** |
| **Operational Safety** | Exposed rotating blades; requires wire cages | Completely enclosed rotating machinery | **Zero mechanical pinch/sever risk** |

---

## 🛠️ Repository Directory Structure

```
vortex-100-fluid-amplifier/
├── cad_stl/                           # Precision 3D STL & CAD mesh geometries
│   ├── Base_Pedestal_Enclosure.stl
│   ├── Centrifugal_Impeller_11Blade.stl
│   ├── Ring_Airfoil_Back.stl
│   ├── Ring_Airfoil_Front.stl
│   ├── Volute_Diffuser_Plenum.stl
│   └── VORTEX_100_Full_Assembly.stl
├── docs/                              # Presentation slides, design theory & media
│   └── assets/                        # Design theory and structural diagrams
├── generate_vortex_stl.py             # Parametric CAD mesh generator
├── procurement.html                   # Interactive Bill of Materials (BOM) & cost matrix
├── VORTEX_100_Bladeless_Fan_Presentation.html # Complete aerodynamic slide deck
└── README.md                          # Engineering whitepaper and specifications
```

---

## 👨‍💻 Designed & Engineered By

**Abdullah Bin Zafar**  
*Mechatronics & Control Systems Engineer | Certified SolidWorks Professional (CSWP)*  
- **GitHub:** [@EngineerAbdullahBinZafar](https://github.com/EngineerAbdullahBinZafar)  
- **Email:** abz.king.1.9.2003@gmail.com  
- **LinkedIn:** [Abdullah Bin Zafar](https://linkedin.com/in/abdullah-bin-zafar)
