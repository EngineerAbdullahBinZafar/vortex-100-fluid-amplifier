# Test Infrastructure Architecture — VORTEX-100 Bladeless Fan System

**Document Version**: 1.0.0  
**Target Project**: VORTEX-100 Bladeless Fan Engineering & Presentation System  
**Test Suite Path**: `C:\Users\star\Downloads\product design\test_e2e_vortex.py`  
**Author**: E2E Test Writer (`teamwork_test_writer_e2e`)  
**Environment**: Pure Python 3.11 Standard Library (Zero external dependencies)  

---

## 1. Executive Summary & Architecture Overview

The VORTEX-100 E2E Test Suite (`test_e2e_vortex.py`) establishes an opaque-box, requirement-driven automated verification pipeline covering all functional tiers of the VORTEX-100 engineering project. It validates the multi-material CAD geometry pipeline, aerodynamic 2-piece split loop, internal mounting structures, interactive Three.js WebGL presentation, ~Rs. 5,780 PKR student procurement BOM, Hall Road Lahore sourcing directory, FDM 3D printing parameters, and step-by-step physical assembly procedures.

```
                              ┌──────────────────────────────────────┐
                              │     VORTEX-100 E2E TEST RUNNER       │
                              │       (test_e2e_vortex.py)           │
                              └──────────────────┬───────────────────┘
                                                 │
         ┌───────────────────┬───────────────────┼───────────────────┬───────────────────┐
         │                   │                   │                   │                   │
         ▼                   ▼                   ▼                   ▼                   ▼
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│     TIER 1      │ │     TIER 2      │ │     TIER 3      │ │     TIER 4      │ │   REGRESSION    │
│Feature Coverage │ │Boundary & Corner│ │  Cross-Feature  │ │ Real-World Work-│ │Legacy Test Suite│
│  (9 Modules)    │ │   (5 Areas)     │ │  Interactions   │ │ flows (5 Scen.) │ │  Integration    │
└─────────────────┘ └─────────────────┘ └─────────────────┘ └─────────────────┘ └─────────────────┘
```

---

## 2. Test Architecture Tiers

### 2.1 Tier 1: Feature Coverage (>=5 test cases per feature)
Tier 1 verifies that each standalone feature in the project specification functions correctly:

| Feature ID | Feature Name | Test Class | Min Cases | Scope & Assertions |
|---|---|---|---|---|
| **F1** | Multi-Material CAD Exports | `TestTier1_CADExports` | 5 | 3MF OPC ZIP container, Wavefront OBJ geometry, MTL material definitions, ISO 10303-21 STEP AP214 B-Rep schema, binary STL files. |
| **F2** | Watertight Mesh Geometry | `TestTier1_WatertightGeometry` | 5 | Topological edge analysis: `boundary_edges == 0`, `non_manifold_edges == 0`, `degenerate_triangles == 0`, positive enclosed volume, outward normals. |
| **F3** | CMF Color Tokens | `TestTier1_CMFColorTokens` | 5 | Hex strings, Three.js integers, normalized sRGB, 8-bit RGB, roughness, metalness, and emissive intensity across 4 CMF tokens. |
| **F4** | Three.js WebGL Viewer | `TestTier1_ThreeJsViewer` | 5 | Three.js r128 CDN script, OrbitControls.js, `#threejs-canvas-wrap` DOM container, `initThreeJsEngine()` JS function, and presentation/index parity. |
| **F5** | Dyson Gen1 Architecture | `TestTier1_DysonGen1Architecture` | 5 | 12V 7530/9733 centrifugal blower, stepless rotary potentiometer, 110x70mm HEPA filter, Coandă equations, and acoustic models. |
| **F6** | Procurement BOM (~5.5k-6k) | `TestTier1_ProcurementBOM` | 5 | Exactly 12 horizontal cards (`data-step="1"` to `"12"`), direct buy links (no `/catalog/?q=` or `/tag/`), isolated images, scratch mirror sync. |
| **F7** | Hall Road Lahore Sourcing | `TestTier1_HallRoadSourcing` | 5 | Hall Road master offline directory, Champion RC / Al-Rehman / Brandreth Road shops, Pakistani e-commerce domains, interactive JS tools. |
| **F8** | FDM 3D Printing Profile | `TestTier1_FDMProfile` | 5 | 220x220x250mm bed envelope, 0.20mm layer height, 4 walls (1.6mm solid shell), 20-25% gyroid infill, PETG/PLA thermal ranges. |
| **F9** | Chronological Assembly | `TestTier1_AssemblySteps` | 5 | 5-job print schedule (~28.2 hours), M3 brass heat-set inserts, Shore-40A silicone damping grommets, bayonet twist-lock bottom lid. |

### 2.2 Tier 2: Boundary & Corner Cases (>=5 per feature area)
Tier 2 stress-tests tolerances, geometric limits, numeric bounds, and format syntax:

| Area ID | Focus Area | Test Class | Min Cases | Boundary Limits & Corner Conditions Tested |
|---|---|---|---|---|
| **B1** | Slit Tolerance Bounds | `TestTier2_SlitTolerance` | 5 | Nominal $\Delta R = 1.25\text{ mm}$, lower limit $1.20\text{ mm}$, upper limit $1.30\text{ mm}$, extreme rejection ($<1.0\text{ mm}$ choking, $>1.5\text{ mm}$ detachment), zero slit singularity rejection. |
| **B2** | Build Envelope Bounds | `TestTier2_BuildVolumeBounds` | 5 | Front Lip ($218 \le 220\text{ mm}$), Rear Cowl ($218 \le 220\text{ mm}$), Pedestal Base ($Z = 180 \le 250\text{ mm}$), turbomachinery compactness, build plate margin ($\ge 1.0\text{ mm}$). |
| **B3** | Budget Limits | `TestTier2_BudgetLimits` | 5 | Lower bound $\ge 5,500\text{ PKR}$, upper bound $\le 6,000\text{ PKR}$, positive item prices ($p > 0$), rejection of negative/zero/NaN prices, currency denomination check. |
| **B4** | Color Hex & RGB Bounds | `TestTier2_ColorHexBounds` | 5 | Hex syntax regex `^#[0-9A-Fa-f]{6}$`, normalized range $[0.0, 1.0]$, 8-bit integer range $[0, 255]$, round-trip conversion precision, malformed hex string rejection. |
| **B5** | File Format Headers | `TestTier2_FileFormatHeaders` | 5 | 3MF zip magic bytes `PK\x03\x04`, OBJ valid prefix tokens (`v`, `f`, `vn`, `o`, `mtllib`), MTL tokens (`newmtl`, `Kd`, etc.), STEP `ISO-10303-21;` header, STL exact 50-byte record alignment. |

### 2.3 Tier 3: Cross-Feature Interactions (Pairwise Compatibility)
Tier 3 tests integration contracts between independent modules:
- **CAD CMF Tokens ↔ Three.js WebGL Parameters**: Validates that material colors in CAD formats (3MF, OBJ/MTL, STEP) match Three.js WebGL shaders bit-for-bit.
- **Airfoil Split Mating Geometry**: Validates that Front Airfoil Lip ($R=75.0\text{ mm}$) and Rear Cowl ($R=73.75\text{ mm}$) create the exact $1.25\text{ mm}$ slit, continuous tongue (2.2mm) and groove (3.2mm) with 0.5mm gasket clearance, 6 conical dowel pins at $R=98\text{ mm}$ ($\theta = 30^\circ, 90^\circ, \dots$), and 6 M3 fastener screw bosses ($\theta = 0^\circ, 60^\circ, \dots$).
- **Procurement BOM ↔ Chassis Mechanical Interfaces**: Validates that the 12V 7530 blower fits the internal cradle stanchions, 110x70mm HEPA fits the bottom compression ledge, 16mm potentiometer fits the 7.2mm front collar boss, and DC barrel jack fits the 11.2mm rear chassis port.
- **Slicer Profile ↔ Assembly Manual Workflow**: Validates that the 13.5-hour base pedestal print window allows parallel bench wiring and electrical testing before final mechanical assembly.
- **Presentation ↔ Index Parity & Navigation**: Validates bit-for-bit file parity between presentation copies and bidirectional hyperlinks between presentation and procurement guide.

### 2.4 Tier 4: Real-World Application Scenarios
Tier 4 simulates end-to-end user workflows:
1. **Scenario 1: Student Capstone Defense Evaluation**: Simulates university defense panel validating student name, registration number, department, capstone defense banner, 2D technical drawings, 3D WebGL viewer, and acoustic calculations.
2. **Scenario 2: FDM Slicer Production Importing**: Simulates slicer import engine (Cura/PrusaSlicer) checking STL binary integrity, watertightness, manifold edges, and positive normal orientation.
3. **Scenario 3: Hall Road Lahore Shopping & Substitution**: Simulates student shopping at Hall Road Lahore, checking offline vendor directories and verifying budget headroom for part substitutions (e.g., 7530 vs 9733 blower).
4. **Scenario 4: Physical Bench Assembly & DMM Safety Commissioning**: Validates physical fastening order, silicone damping grommets, bayonet twist-lock lid, and simulated pre-power DMM short-circuit resistance testing ($R > 10\ \text{k}\Omega$).
5. **Scenario 5: Full Regression Harness**: Programmatically executes and validates existing project test suites (`test_html_content.py` and `test_procurement_page.py`), confirming zero regressions.

---

## 3. Pure Standard Library Analytical Engines

To avoid external C-extension binary dependencies (e.g., numpy, trimesh, cadquery), `test_e2e_vortex.py` implements four high-speed topological analyzers in standard Python:

### 3.1 `STLAnalyzer`
- Reads binary STL files using Python `struct` module.
- Computes enclosed volume via the 3D divergence theorem:
  $$V = \frac{1}{6} \sum_{i=1}^{N} \mathbf{v}_{0,i} \cdot (\mathbf{v}_{1,i} \times \mathbf{v}_{2,i})$$
- Computes surface area:
  $$A = \frac{1}{2} \sum_{i=1}^{N} \| (\mathbf{v}_{1,i} - \mathbf{v}_{0,i}) \times (\mathbf{v}_{2,i} - \mathbf{v}_{0,i}) \|$$
- Quantizes vertices to $10^{-4}\text{ mm}$ and counts occurrences of undirected edges:
  $$\text{boundary\_edges} = \sum [c_e = 1], \quad \text{non\_manifold\_edges} = \sum [c_e > 2]$$
  A mesh is **100% watertight** if and only if $\text{boundary\_edges} = 0$ and $\text{non\_manifold\_edges} = 0$.

### 3.2 `ThreeMFAnalyzer`
- Inspects 3MF Open Packaging Convention (OPC) ZIP containers.
- Validates XML namespaces, `[Content_Types].xml`, `_rels/.rels`, and `3D/3dmodel.model`.
- Validates `<m:colorgroup>` definitions, material IDs, and `<object>` meshes.

### 3.3 `OBJMTLAnalyzer`
- Parses Wavefront OBJ vertex coordinates (`v`), vertex normals (`vn`), and face index polygons (`f`).
- Parses companion MTL material definitions (`newmtl`, `Kd`, `Ka`, `Ks`, `d`).

### 3.4 `STEPAnalyzer`
- Analyzes ISO 10303-21 Part 21 clear text encoding.
- Verifies `HEADER;`, `FILE_SCHEMA(('AUTOMOTIVE_DESIGN'))`, `DATA;`, `MANIFOLD_SOLID_BREP`, and `COLOUR_RGB`.

---

## 4. Execution & CLI Options

The test suite can be executed from terminal or automated CI/CD runners:

```powershell
# Run the complete test suite (all tiers)
python test_e2e_vortex.py

# Run individual tiers
python test_e2e_vortex.py --tier1    # Feature Coverage only
python test_e2e_vortex.py --tier2    # Boundary & Corner cases only
python test_e2e_vortex.py --tier3    # Cross-Feature interactions only
python test_e2e_vortex.py --tier4    # Real-World scenarios only

# Run with machine-readable JSON output
python test_e2e_vortex.py --json

# Run via standard unittest runner
python -m unittest test_e2e_vortex.py -v
```
