# Project: VORTEX-100 Bladeless Fan Engineering & Presentation System

## Architecture
- **Hardware Architecture**: Dyson Gen1 Centrifugal Air Multiplier (~5.5k–6k PKR total BOM) powered by a 12V high-static centrifugal blower (7530 or 9733 model), stepless analog rotary potentiometer with integrated switch, warm white 3000K halo LED ring, 110x70mm cylindrical H13 HEPA + activated carbon filter, and 12V 2A DC power adapter.
- **CAD & 3D Modeling Pipeline**: Pure-Python standard library multi-format generator creating multi-material colored 3MF, Wavefront OBJ + MTL, colored STEP AP214 (ISO 10303-21), and manifold binary STL assets with exact CMF metadata and 0 boundary/non-manifold defects.
- **Aerodynamic Airfoil Loop**: 2-piece split assembly (Front Airfoil Lip + Rear Shell Cowl) featuring continuous tongue-and-groove joint, 6x conical registration dowels, 6x M3 heat-set fastener bosses, and a calibrated 1.25mm continuous discharge slit that prints 100% support-free on FDM beds.
- **Pedestal Base Mounting**: Rigid internal mounting architecture with 4x Shore-40A silicone vibration-damping stanchions for the blower, airtight HEPA compression shelf with 1.5mm gasket preloading, anti-rotation front potentiometer collar boss, and rear 5.5x2.1mm DC barrel jack port.
- **Interactive WebGL Presentation**: Responsive Three.js (r128) WebGL 3D viewer in `VORTEX_100_Bladeless_Fan_Presentation.html` and `index.html` synchronized with photorealistic PBR materials matching CMF colors, OrbitControls, exploded views, dynamic Coandă particle simulation, and cross-section clipping.
- **Procurement & Sourcing Guide**: `procurement.html` featuring 12 sequential component cards, ~Rs. 5,780 PKR student budget, verified Pakistani checkout links (Digilog.pk, Electrobes.com, Daraz.pk), and Hall Road / Brandreth Road / Montgomery Road Lahore offline sourcing directory.
- **Manufacturing & Assembly Manual**: Calibrated 220x220x250mm FDM profile (0.2mm layer height, 4 walls, 20-25% gyroid infill, PETG/PLA), 5-job print sequence (~28.2 hrs), and 6-phase step-by-step physical assembly and electrical safety commissioning procedure.

## Feature Inventory
| # | Feature | Description | Milestone | Source |
|---|---------|-------------|-----------|--------|
| 1 | Multi-Material Colored CAD Models | Export 3MF, OBJ+MTL, and colored STEP AP214 alongside STL with distinct bodies and CMF colors | M1 | Survey 1 (R1) |
| 2 | Watertight Base Pedestal CAD | Eliminate 240 non-manifold edges in Base_Pedestal_Enclosure.stl (boundary_edges=0, non_manifold=0) | M1 | Survey 1 (R1) |
| 3 | Three.js PBR CMF Synchronization | Synchronize WebGL 3D viewer in presentation & index with Warm Alabaster, Champagne Gold, Dark Charcoal, Warm Halo | M1 | Survey 2 (R1) |
| 4 | Non-Regression on Test Scripts | Retain 'Matte Alabaster Cream' text, 12 cards, isolated images, and mirror file so all existing tests pass | M1 / M3 | Survey 2 (R1/R3) |
| 5 | Split Airfoil Ring (Front & Rear) | 2-piece split (Front Lip R=75.0mm, Rear Cowl R=73.75mm) preserving 1.25mm slit with 0 internal supports | M2 | Survey 1/3 (R2) |
| 6 | Airfoil Interlock & Alignment | Continuous tongue-and-groove joint, 6x conical pins, and 6x M3 heat-set bosses for rigid seal | M2 | Survey 1 (R2) |
| 7 | Blower Cradle & Vibration Isolation | Rigid internal stanchions and Shore-40A silicone damping seats for 12V blower fan (7530/9733) | M2 | Survey 1/3 (R2) |
| 8 | Cylindrical HEPA Sealing Chamber | Internal annular shelf & bottom lid compressing 110x70mm filter gaskets by 1.5mm to eliminate bypass | M2 | Survey 3 (R2) |
| 9 | Control Knob & DC Jack Bosses | Front panel 7.2mm boss with anti-rotation notch and rear 11.2mm DC barrel jack port in pedestal base | M2 | Survey 1/3 (R2) |
| 10 | Presentation Dyson Gen1 Architecture | Update technical presentation & index with Dyson Gen1 rationale, aerodynamic equations, and acoustic models | M3 | Survey 2/3 (R3) |
| 11 | Reconciled 5.5k-6k PKR Procurement Guide | Update procurement.html to ~Rs. 5,780 PKR BOM with verified PK links and Hall Road vendor directory | M3 | Survey 2/3 (R3) |
| 12 | Mirror File Sync | Synchronize procurement.html changes to C:\Users\star\.gemini\antigravity\scratch\aero_bladeless_fan\ | M3 | Survey 2 (R3) |
| 13 | FDM 220x220x250mm Slicing Profile | Slicer specs for Ender-3/Neptune profile: 0.2mm layer, 4 walls, 20-25% gyroid infill, 0-support orientation | M4 | Survey 3 (R4) |
| 14 | Chronological 3D Printing Schedule | 5-job print sequence (~28.2 hrs total) enabling parallel electrical testing while long prints run | M4 | Survey 3 (R4) |
| 15 | 6-Phase Physical Assembly Manual | Step-by-step mechanical fastening, wiring diagram, DMM pre-power check, and live commissioning guide | M4 | Survey 3 (R4) |
| 16 | E2E Testing Suite (Tiers 1-4) | Opaque-box test suite verifying CAD files, WebGL scripts, procurement budget, live links, and assembly | E2E Track | Dual Track |
| 17 | Final Acceptance & Adversarial Hardening | 100% pass of E2E test suite + Tier 5 white-box adversarial stress testing | M5 (Final) | Dual Track |

## Milestones
| # | Name | Scope | Dependencies | Status |
|---|------|-------|-------------|--------|
| M1 | Multi-Material Colored CAD & WebGL CMF Sync | Export 3MF, OBJ+MTL, STEP AP214; fix non-manifold edges in base STL; sync Three.js PBR materials in presentation & index | None | DONE |
| M2 | Rigid Internal Mounting Architecture & Split Airfoil | Model blower cradle with vibration dampers, HEPA seal, pot/DC bosses, and 2-piece split airfoil with 1.25mm slit | M1 | DONE |
| M3 | Web Presentation & 5.5k-6k PKR Procurement Guide | Update presentation, index, and procurement.html with Dyson Gen1 architecture, calculations, and Hall Road directory | M1 | DONE |
| M4 | Chronological 3D Printing & Physical Assembly Manual | Deliver calibrated 220x220x250mm slicing profile, 5-job print sequence, and 6-phase assembly/inspection guide | M2, M3 | DONE |
| M5 | Final Milestone: 100% E2E Verification & Adversarial Hardening | Pass 100% of E2E test suite (Tiers 1-4) + Tier 5 adversarial stress testing | M1-M4, TEST_READY | DONE |
| E2E | E2E Testing Track | Develop test harness, test cases (Tiers 1-4), and publish TEST_INFRA.md and TEST_READY.md | None | DONE |

## Interface Contracts
### CAD Generator ↔ WebGL 3D Viewer
- **CMF Tokens**:
  - `Warm Alabaster White`: Hex `#F4F1EA`, Three.js `0xF4F1EA`, sRGB `(0.957, 0.945, 0.918)`.
  - `Champagne Gold`: Hex `#D4AF37`, Three.js `0xD4AF37`, sRGB `(0.831, 0.686, 0.216)`.
  - `Dark Charcoal`: Hex `#22252A`, Three.js `0x22252A`, sRGB `(0.133, 0.145, 0.165)`.
  - `Warm White Halo`: Hex `#FFF8E7`, Three.js `0xFFF8E7`, Emissive `0xFFF8E7`, Intensity `0.85`.
- **Component Geometry Bounds**:
  - Front Airfoil Lip: Outer Diameter 218.0mm, Aperture $R = 75.0\text{ mm}$, Depth 31.5mm.
  - Rear Airfoil Cowl: Outer Diameter 218.0mm, Throttle Lip $R = 73.75\text{ mm}$, Depth 22.0mm.
  - Aerodynamic Slit Width: Exactly $1.25\text{ mm}$ ($\Delta R = 75.00 - 73.75\text{ mm}$).
  - Pedestal Base: Outer Diameter 130.0mm, Height 180.0mm, Wall Thickness 3.5mm.

### Presentation Files ↔ Test Suites
- `test_html_content.py`: Requires `'Matte Alabaster Cream'`, `'ABDULLAH BIN ZAFAR'`, `'2023-MC-292'`, `'three.min.js'`, `'OrbitControls.js'`, `'VORTEX_100_Full_Assembly.stl'`.
- `test_procurement_page.py`: Requires exactly 12 cards, 12 isolated images with `mix-blend-mode: multiply`, verified Pakistani domains, and mirror file in `C:\Users\star\.gemini\antigravity\scratch\aero_bladeless_fan\procurement.html`.
- `test_live_links.py`: Requires 13 active checkout URLs and 12 product image URLs returning HTTP 200.

## Code Layout
- `C:\Users\star\Downloads\product design\`
  - `generate_vortex_colored_cad.py` — Pure-Python multi-format CAD generator (3MF, OBJ+MTL, STEP AP214, binary STL).
  - `generate_vortex_stl.py` — Baseline CAD generator script.
  - `VORTEX_100_Full_Assembly_Colored.3mf` — Multi-material colored 3MF assembly.
  - `VORTEX_100_Full_Assembly.obj` & `vortex_materials.mtl` — Wavefront OBJ+MTL assembly with CMF colors.
  - `VORTEX_100_Full_Assembly_Colored.step` — ISO 10303-21 AP214 colored STEP assembly.
  - `cad_stl/` & root — Watertight binary STL component files.
  - `VORTEX_100_Bladeless_Fan_Presentation.html` — Master interactive technical presentation.
  - `index.html` — Synchronized master presentation copy.
  - `procurement.html` — Procurement guide & local sourcing directory.
  - `test_html_content.py`, `test_procurement_page.py`, `test_live_links.py` — Existing regression test suite.
  - `test_e2e_vortex.py` — E2E test runner covering Tiers 1-4.
  - `MANUFACTURING_AND_ASSEMBLY_MANUAL.md` — Standalone chronological 3D printing and physical assembly manual.
