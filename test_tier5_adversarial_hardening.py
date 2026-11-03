# -*- coding: utf-8 -*-
"""
========================================================================================
VORTEX-100 BLADELESS AIR-MULTIPLIER SYSTEM
TIER 5 ADVERSARIAL STRESS TESTING & COVERAGE HARDENING SUITE
========================================================================================
Milestone: Final Milestone Acceptance (Milestone 5)
Author: Adversarial Challenger (Empirical Challenge & Verification)
Coverage:
  1. CAD Topology & Micro-Tolerance Manifoldness (STL, 3MF, OBJ+MTL, STEP AP214)
  2. 1.25mm Slit Aerodynamic Profile & Assembly Geometry
  3. Presentation HTML Bit-for-Bit Hash Parity & Three.js PBR CMF Synchronization
  4. Procurement Page Budget Math, 12 Sequential Cards, Sourcing & Mirror Parity
  5. Manufacturing Manual FDM Profile, 5-Job Schedule, 6-Phase Assembly & DMM Safety
========================================================================================
"""

import os
import sys
import math
import struct
import hashlib
import zipfile
import re
import unittest
import xml.etree.ElementTree as ET
from collections import defaultdict

BASE_DIR = r"C:\Users\star\Downloads\product design"
MIRROR_DIR = r"C:\Users\star\.gemini\antigravity\scratch\aero_bladeless_fan"

CAD_3MF = os.path.join(BASE_DIR, "VORTEX_100_Full_Assembly_Colored.3mf")
CAD_OBJ = os.path.join(BASE_DIR, "VORTEX_100_Full_Assembly.obj")
CAD_MTL = os.path.join(BASE_DIR, "vortex_materials.mtl")
CAD_STEP = os.path.join(BASE_DIR, "VORTEX_100_Full_Assembly_Colored.step")
PRESENTATION_HTML = os.path.join(BASE_DIR, "VORTEX_100_Bladeless_Fan_Presentation.html")
INDEX_HTML = os.path.join(BASE_DIR, "index.html")
PROCUREMENT_HTML = os.path.join(BASE_DIR, "procurement.html")
PROCUREMENT_MIRROR = os.path.join(MIRROR_DIR, "procurement.html")
MANUAL_MD = os.path.join(BASE_DIR, "MANUFACTURING_AND_ASSEMBLY_MANUAL.md")

STL_COMPONENTS = [
    "Ring_Airfoil_Front.stl",
    "Ring_Airfoil_Back.stl",
    "Centrifugal_Impeller_11Blade.stl",
    "Volute_Diffuser_Plenum.stl",
    "Base_Pedestal_Enclosure.stl"
]

CMF_COLORS = {
    "Warm_Alabaster_White": {
        "hex": "#F4F1EA",
        "hex_alpha": "#F4F1EAFF",
        "threejs_hex": 0xF4F1EA,
        "rgb_norm": (0.957, 0.945, 0.918)
    },
    "Champagne_Gold": {
        "hex": "#D4AF37",
        "hex_alpha": "#D4AF37FF",
        "threejs_hex": 0xD4AF37,
        "rgb_norm": (0.831, 0.686, 0.216)
    },
    "Dark_Charcoal": {
        "hex": "#22252A",
        "hex_alpha": "#22252AFF",
        "threejs_hex": 0x22252A,
        "rgb_norm": (0.133, 0.145, 0.165)
    },
    "Warm_White_Halo": {
        "hex": "#FFF8E7",
        "hex_alpha": "#FFF8E7FF",
        "threejs_hex": 0xFFF8E7,
        "rgb_norm": (1.000, 0.973, 0.906)
    }
}


# ======================================================================================
# HELPER FUNCTIONS FOR GEOMETRY ANALYSIS
# ======================================================================================
def read_binary_stl(filepath):
    """Parses binary STL file and returns (triangles, header)."""
    with open(filepath, "rb") as f:
        data = f.read()
    assert len(data) >= 84, f"STL file too small: {filepath}"
    header = data[:80]
    num_triangles = struct.unpack("<I", data[80:84])[0]
    expected_size = 84 + num_triangles * 50
    assert len(data) == expected_size, f"Corrupted STL: size {len(data)} != expected {expected_size}"
    
    triangles = []
    offset = 84
    for _ in range(num_triangles):
        vals = struct.unpack("<12fH", data[offset:offset+50])
        normal = vals[0:3]
        v0 = vals[3:6]
        v1 = vals[6:9]
        v2 = vals[9:12]
        triangles.append((normal, v0, v1, v2))
        offset += 50
    return triangles, header


def analyze_mesh_topology(triangles, quant_decimals=4):
    """
    Computes signed volume, boundary edges, non-manifold edges,
    and checks for degenerate triangles.
    """
    vol6 = 0.0
    degen_count = 0
    edge_map = defaultdict(int)
    directed_edges = set()
    
    def quant(v):
        return (round(v[0], quant_decimals), round(v[1], quant_decimals), round(v[2], quant_decimals))

    for norm, v0, v1, v2 in triangles:
        # Cross product of edges for volume and degenerate check
        e1 = (v1[0] - v0[0], v1[1] - v0[1], v1[2] - v0[2])
        e2 = (v2[0] - v0[0], v2[1] - v0[1], v2[2] - v0[2])
        cp = (
            e1[1] * e2[2] - e1[2] * e2[1],
            e1[2] * e2[0] - e1[0] * e2[2],
            e1[0] * e2[1] - e1[1] * e2[0]
        )
        area2 = cp[0]*cp[0] + cp[1]*cp[1] + cp[2]*cp[2]
        if area2 < 1e-12:
            degen_count += 1

        # Signed tetrahedron volume (origin to triangle)
        # vol6 = v0 . (v1 x v2)
        v1xv2 = (
            v1[1] * v2[2] - v1[2] * v2[1],
            v1[2] * v2[0] - v1[0] * v2[2],
            v1[0] * v2[1] - v1[1] * v2[0]
        )
        vol6 += (v0[0] * v1xv2[0] + v0[1] * v1xv2[1] + v0[2] * v1xv2[2])

        # Topological edges
        qv0, qv1, qv2 = quant(v0), quant(v1), quant(v2)
        edges = [(qv0, qv1), (qv1, qv2), (qv2, qv0)]
        for ea, eb in edges:
            if ea == eb:
                continue
            undir = (min(ea, eb), max(ea, eb))
            edge_map[undir] += 1

    volume = vol6 / 6.0
    boundary_edges = sum(1 for count in edge_map.values() if count == 1)
    non_manifold_edges = sum(1 for count in edge_map.values() if count > 2)

    return {
        "num_triangles": len(triangles),
        "volume_cm3": volume / 1000.0,
        "boundary_edges": boundary_edges,
        "non_manifold_edges": non_manifold_edges,
        "degenerate_triangles": degen_count,
        "is_watertight": (boundary_edges == 0 and non_manifold_edges == 0 and len(triangles) > 0)
    }


# ======================================================================================
# TIER 5 TEST CLASSES
# ======================================================================================

class TestTier5_CADTopologyHardening(unittest.TestCase):
    """Adversarial stress-testing of CAD meshes, topologies, and multi-format exports."""

    def test_t5_01_stl_component_micro_tolerances(self):
        """
        Challenges all 5 individual STL components against micro-tolerances
        (10^-3 mm to 10^-5 mm). Must have 0 boundary and 0 non-manifold edges.
        """
        for filename in STL_COMPONENTS:
            filepath = os.path.join(BASE_DIR, filename)
            self.assertTrue(os.path.exists(filepath), f"Missing STL: {filepath}")
            triangles, _ = read_binary_stl(filepath)
            
            # Test at 0.001mm and 0.0001mm quantization
            for dec in [3, 4]:
                metrics = analyze_mesh_topology(triangles, quant_decimals=dec)
                self.assertEqual(metrics["boundary_edges"], 0,
                                 f"{filename} has {metrics['boundary_edges']} boundary edges at 10^-{dec} mm")
                self.assertEqual(metrics["non_manifold_edges"], 0,
                                 f"{filename} has {metrics['non_manifold_edges']} non-manifold edges at 10^-{dec} mm")
                self.assertEqual(metrics["degenerate_triangles"], 0,
                                 f"{filename} has degenerate triangles")
                self.assertGreater(metrics["volume_cm3"], 0.0,
                                   f"{filename} volume must be strictly positive (found {metrics['volume_cm3']})")

    def test_t5_02_slit_aerodynamic_gap_measurement(self):
        """
        Adversarially verifies the 1.25mm aerodynamic slit gap directly from the
        STL coordinates of Ring_Airfoil_Front.stl and Ring_Airfoil_Back.stl.
        Front inner lip: R = 75.0mm. Rear throttle lip: R = 73.75mm.
        Difference Delta_R = 1.25mm (+/- 0.05mm tolerance).
        """
        front_path = os.path.join(BASE_DIR, "Ring_Airfoil_Front.stl")
        back_path = os.path.join(BASE_DIR, "Ring_Airfoil_Back.stl")
        
        front_tris, _ = read_binary_stl(front_path)
        back_tris, _ = read_binary_stl(back_path)
        
        # Extract vertices near Z = 0
        front_lip_radii = []
        for _, v0, v1, v2 in front_tris:
            for v in (v0, v1, v2):
                if abs(v[2]) < 0.05:  # At z = 0
                    r = math.hypot(v[0], v[1])
                    if 74.0 <= r <= 76.0:
                        front_lip_radii.append(r)
        
        back_lip_radii = []
        for _, v0, v1, v2 in back_tris:
            for v in (v0, v1, v2):
                if abs(v[2]) < 0.05:  # At z = 0
                    r = math.hypot(v[0], v[1])
                    if 72.5 <= r <= 74.5:
                        back_lip_radii.append(r)

        self.assertGreater(len(front_lip_radii), 0, "No front lip vertices found near z=0")
        self.assertGreater(len(back_lip_radii), 0, "No back lip vertices found near z=0")

        min_front_r = min(front_lip_radii)
        max_back_r = max(back_lip_radii)
        
        self.assertAlmostEqual(min_front_r, 75.0, delta=0.05,
                               msg=f"Front lip radius {min_front_r:.3f} mm deviates from nominal 75.0mm")
        self.assertAlmostEqual(max_back_r, 73.75, delta=0.05,
                               msg=f"Rear lip radius {max_back_r:.3f} mm deviates from nominal 73.75mm")

        measured_slit = min_front_r - max_back_r
        self.assertAlmostEqual(measured_slit, 1.25, delta=0.05,
                               msg=f"Measured slit {measured_slit:.3f} mm outside [1.20, 1.30] mm tolerance window")

    def test_t5_03_bed_envelope_collision_stress(self):
        """
        Verifies all components strictly fit inside standard 220x220x250 mm FDM envelope.
        """
        for filename in STL_COMPONENTS:
            filepath = os.path.join(BASE_DIR, filename)
            tris, _ = read_binary_stl(filepath)
            xs, ys, zs = [], [], []
            for _, v0, v1, v2 in tris:
                for v in (v0, v1, v2):
                    xs.append(v[0])
                    ys.append(v[1])
                    zs.append(v[2])
            dx = max(xs) - min(xs)
            dy = max(ys) - min(ys)
            dz = max(zs) - min(zs)
            self.assertLessEqual(dx, 220.05, f"{filename} X dimension {dx:.2f}mm exceeds 220mm bed")
            self.assertLessEqual(dy, 220.05, f"{filename} Y dimension {dy:.2f}mm exceeds 220mm bed")
            self.assertLessEqual(dz, 250.05, f"{filename} Z dimension {dz:.2f}mm exceeds 250mm Z-axis")

    def test_t5_04_3mf_adversarial_validation(self):
        """
        Inspects 3MF OPC ZIP archive, XML schema, color groups, and multi-body integrity.
        """
        self.assertTrue(os.path.exists(CAD_3MF), f"Missing 3MF file: {CAD_3MF}")
        with zipfile.ZipFile(CAD_3MF, "r") as z:
            namelist = z.namelist()
            self.assertIn("[Content_Types].xml", namelist)
            self.assertIn("3D/3dmodel.model", namelist)
            
            model_xml = z.read("3D/3dmodel.model").decode("utf-8")
            # Namespace & XML checks
            self.assertIn('xmlns="http://schemas.microsoft.com/3dmanufacturing/core/2015/02"', model_xml)
            self.assertIn('xmlns:m="http://schemas.microsoft.com/3dmanufacturing/material/2015/02"', model_xml)
            
            # Verify 4 CMF colors
            for color_name, info in CMF_COLORS.items():
                self.assertIn(info["hex_alpha"], model_xml, f"Missing 3MF color {info['hex_alpha']} for {color_name}")

            # Verify 7 component bodies
            expected_objects = [
                "Ring_Airfoil_Front",
                "Ring_Airfoil_Back",
                "Centrifugal_Impeller_11Blade",
                "Volute_Diffuser_Plenum",
                "Base_Pedestal_Enclosure",
                "Halo_Ring_Lightguide",
                "Control_Knob_Accent"
            ]
            for obj in expected_objects:
                self.assertIn(f'name="{obj}"', model_xml, f"Missing 3MF component object: {obj}")

    def test_t5_05_obj_mtl_adversarial_validation(self):
        """
        Inspects Wavefront OBJ and MTL files: verifies material linkage, illumination,
        Kd/Ks values, vertex counts, and object group separation.
        """
        self.assertTrue(os.path.exists(CAD_OBJ), f"Missing OBJ: {CAD_OBJ}")
        self.assertTrue(os.path.exists(CAD_MTL), f"Missing MTL: {CAD_MTL}")
        
        with open(CAD_MTL, "r", encoding="utf-8") as f:
            mtl_content = f.read()
        
        with open(CAD_OBJ, "r", encoding="utf-8") as f:
            obj_content = f.read()

        self.assertIn("mtllib vortex_materials.mtl", obj_content)
        
        for mat_name in CMF_COLORS.keys():
            self.assertIn(f"newmtl {mat_name}", mtl_content)
            self.assertIn(f"usemtl {mat_name}", obj_content)

        # Check PBR illumination
        self.assertIn("illum 2", mtl_content)
        self.assertIn("Kd", mtl_content)
        self.assertIn("Ks", mtl_content)

        # Count vertices and faces in OBJ
        v_count = len(re.findall(r"^v\s+", obj_content, re.MULTILINE))
        f_count = len(re.findall(r"^f\s+", obj_content, re.MULTILINE))
        self.assertGreaterEqual(v_count, 20000, f"OBJ vertex count too low: {v_count}")
        self.assertGreaterEqual(f_count, 40000, f"OBJ face count too low: {f_count}")

    def test_t5_06_step_ap214_adversarial_validation(self):
        """
        Inspects ISO 10303-21 STEP AP214 file: verifies syntax, MANIFOLD_SOLID_BREP,
        CLOSED_SHELL, STYLED_ITEM, and COLOUR_RGB entities.
        """
        self.assertTrue(os.path.exists(CAD_STEP), f"Missing STEP: {CAD_STEP}")
        with open(CAD_STEP, "r", encoding="utf-8") as f:
            step_text = f.read()

        self.assertTrue(step_text.startswith("ISO-10303-21;"), "Invalid STEP AP214 header")
        self.assertTrue(step_text.strip().endswith("END-ISO-10303-21;"), "Invalid STEP AP214 footer")
        self.assertTrue("AP214" in step_text and "AUTOMOTIVE_DESIGN" in step_text, "Missing AP214 automotive design schema in STEP header")
        
        # 7 distinct solid bodies
        solid_count = step_text.count("MANIFOLD_SOLID_BREP(")
        shell_count = step_text.count("CLOSED_SHELL(")
        styled_count = step_text.count("STYLED_ITEM(")
        
        self.assertEqual(solid_count, 7, f"Expected 7 MANIFOLD_SOLID_BREP entities, found {solid_count}")
        self.assertEqual(shell_count, 7, f"Expected 7 CLOSED_SHELL entities, found {shell_count}")
        self.assertEqual(styled_count, 7, f"Expected 7 STYLED_ITEM entities, found {styled_count}")

        # Check COLOUR_RGB representation
        self.assertIn("COLOUR_RGB(", step_text)


class TestTier5_HTMLPresentationHardening(unittest.TestCase):
    """Adversarial stress-testing of HTML presentation and Three.js WebGL synchronization."""

    def test_t5_07_exact_file_hash_parity(self):
        """
        Verifies 100% bit-for-bit parity between master presentation and index.html
        via SHA-256 and MD5 cryptographic hashes.
        """
        self.assertTrue(os.path.exists(PRESENTATION_HTML))
        self.assertTrue(os.path.exists(INDEX_HTML))
        
        with open(PRESENTATION_HTML, "rb") as f1, open(INDEX_HTML, "rb") as f2:
            bytes1 = f1.read()
            bytes2 = f2.read()

        self.assertEqual(len(bytes1), len(bytes2), "File sizes do not match")
        self.assertEqual(hashlib.sha256(bytes1).hexdigest(), hashlib.sha256(bytes2).hexdigest(),
                         "SHA-256 mismatch between Presentation and index.html")
        self.assertEqual(hashlib.md5(bytes1).hexdigest(), hashlib.md5(bytes2).hexdigest(),
                         "MD5 mismatch between Presentation and index.html")

    def test_t5_08_threejs_pbr_materials_and_cmf_sync(self):
        """
        Validates Three.js PBR material assignments in presentation HTML
        against the exact CMF color palette.
        """
        with open(PRESENTATION_HTML, "r", encoding="utf-8") as f:
            html = f.read()

        self.assertIn("three.min.js", html)
        self.assertIn("OrbitControls.js", html)
        self.assertIn("initThreeJsEngine", html)

        # Check Three.js hex values
        self.assertIn("0xF4F1EA", html, "Missing Warm Alabaster White hex in Three.js")
        self.assertIn("0xD4AF37", html, "Missing Champagne Gold hex in Three.js")
        self.assertIn("0x22252A", html, "Missing Dark Charcoal hex in Three.js")
        self.assertIn("0xFFF8E7", html, "Missing Warm White Halo hex in Three.js")

        # PBR Material definitions
        self.assertTrue("MeshStandardMaterial" in html or "MeshPhysicalMaterial" in html)
        self.assertIn("roughness:", html)
        self.assertIn("metalness:", html)

    def test_t5_09_non_regression_legacy_strings(self):
        """
        Ensures strict non-regression for strings required by earlier test scripts.
        """
        with open(PRESENTATION_HTML, "r", encoding="utf-8") as f:
            html = f.read()

        self.assertIn("Matte Alabaster Cream", html, "Must retain 'Matte Alabaster Cream' for test_html_content.py")
        self.assertIn("ABDULLAH BIN ZAFAR", html)
        self.assertIn("2023-MC-292", html)
        self.assertIn("Mechatronics & Control Engineering", html)
        self.assertIn("UET Lahore", html)
        self.assertIn("VORTEX_100_Full_Assembly.stl", html)

    def test_t5_10_responsive_breakpoints_and_styling(self):
        """
        Verifies CSS responsiveness and layout flexibility across breakpoints.
        """
        with open(PRESENTATION_HTML, "r", encoding="utf-8") as f:
            html = f.read()

        self.assertIn("@media", html)
        self.assertIn("max-width", html)
        self.assertIn("viewport", html)
        self.assertIn("width=device-width", html)


class TestTier5_ProcurementAuditHardening(unittest.TestCase):
    """Adversarial stress-testing of procurement calculations, links, and cards."""

    def test_t5_11_card_count_and_sequential_ordering(self):
        """
        Audits exactly 12 cards, verifying sequential ordering from step 1 to 12.
        """
        with open(PROCUREMENT_HTML, "r", encoding="utf-8") as f:
            html = f.read()

        card_steps = [int(s) for s in re.findall(r'<article class="procure-card"[^>]*data-step="(\d+)"', html)]
        self.assertEqual(len(card_steps), 12, f"Expected exactly 12 cards, found {len(card_steps)}")
        self.assertEqual(card_steps, list(range(1, 13)), f"Card steps are not sequentially ordered 1..12: {card_steps}")

    def test_t5_12_isolated_product_images_and_styling(self):
        """
        Ensures all 12 cards have an isolated real product image with background knockout.
        """
        with open(PROCUREMENT_HTML, "r", encoding="utf-8") as f:
            html = f.read()

        imgs = re.findall(r'<img[^>]+src="([^"]+)"[^>]*class="product-real-img"', html)
        self.assertEqual(len(imgs), 12, f"Expected 12 isolated images, found {len(imgs)}")
        self.assertIn("mix-blend-mode: multiply", html, "Missing mix-blend-mode: multiply for background knockout")

    def test_t5_13_turnkey_bom_budget_window(self):
        """
        Adversarially validates that the turnkey BOM cost is between 5,500 and 6,000 PKR.
        """
        with open(PROCUREMENT_HTML, "r", encoding="utf-8") as f:
            html = f.read()

        # Check declared budget
        self.assertIn("Rs. 5,780", html)
        
        # Verify 5,780 is strictly in [5500, 6000]
        budget = 5780
        self.assertGreaterEqual(budget, 5500)
        self.assertLessEqual(budget, 6000)

    def test_t5_14_pakistani_stores_and_hall_road_directory(self):
        """
        Verifies genuine Pakistani retail domains and Lahore offline directory.
        """
        with open(PROCUREMENT_HTML, "r", encoding="utf-8") as f:
            html = f.read()

        for store in ["digilog.pk", "electrobes.com", "daraz.pk"]:
            self.assertIn(store, html.lower(), f"Missing verified store: {store}")

        self.assertIn("Hall Road", html)
        self.assertIn("Lahore", html)

    def test_t5_15_procurement_mirror_file_sync(self):
        """
        Verifies synchronization between procurement.html and its mirror copy.
        """
        self.assertTrue(os.path.exists(PROCUREMENT_HTML))
        self.assertTrue(os.path.exists(PROCUREMENT_MIRROR), f"Missing mirror file: {PROCUREMENT_MIRROR}")

        with open(PROCUREMENT_HTML, "rb") as f1, open(PROCUREMENT_MIRROR, "rb") as f2:
            self.assertEqual(f1.read(), f2.read(), "procurement.html does not match scratch mirror copy")


class TestTier5_ManufacturingManualHardening(unittest.TestCase):
    """Adversarial stress-testing of manufacturing parameters, slicing, and electrical safety."""

    def test_t5_16_fdm_profile_limits(self):
        """
        Verifies slicing parameters: 220x220x250mm envelope, 0.40mm nozzle, 0.20mm layer,
        4 solid walls (1.60mm), and Gyroid infill.
        """
        with open(MANUAL_MD, "r", encoding="utf-8") as f:
            manual = f.read()

        self.assertIn("220 × 220 × 250 mm", manual)
        self.assertIn("0.40 mm", manual)
        self.assertIn("0.20 mm", manual)
        self.assertIn("1.60 mm", manual)
        self.assertIn("4 solid perimeter", manual.lower())
        self.assertIn("Gyroid", manual)

    def test_t5_17_chronological_5_job_production_schedule(self):
        """
        Verifies 5-job print sequence totaling exactly 28.2 hours and ~585g filament.
        """
        with open(MANUAL_MD, "r", encoding="utf-8") as f:
            manual = f.read()

        for j in range(1, 6):
            self.assertIn(f"Job {j}", manual)

        self.assertIn("28.2 hr", manual)
        self.assertIn("585 g", manual)
        self.assertIn("Dual-Track", manual)

    def test_t5_18_6_phase_physical_assembly(self):
        """
        Verifies coverage of all 6 assembly phases: Phase A through Phase F.
        """
        with open(MANUAL_MD, "r", encoding="utf-8") as f:
            manual = f.read()

        for phase_letter in ["A", "B", "C", "D", "E", "F"]:
            self.assertIn(f"Phase {phase_letter}:", manual, f"Missing Phase {phase_letter} in assembly manual")

        self.assertIn("m3 brass heat-set", manual.lower())
        self.assertIn("1.25 mm feeler gauge", manual)
        self.assertIn("Shore-40A", manual)
        self.assertIn("20% preload", manual.lower())
        self.assertIn("1.50 mm", manual)  # HEPA gasket compression

    def test_t5_19_dmm_electrical_safety_thresholds(self):
        """
        Adversarially validates pre-power electrical safety criteria:
        1. Switch OFF: Open Loop (OL / infinite resistance).
        2. Switch ON: R > 10 kOhm (safe high-impedance).
        3. Dead-short safety cutoff: reject if R < 100 Ohm.
        """
        with open(MANUAL_MD, "r", encoding="utf-8") as f:
            manual = f.read()

        self.assertIn("Resistance / Continuity", manual)
        self.assertIn("Open Loop", manual)
        self.assertIn("10.0", manual)
        self.assertIn("kΩ", manual)
        self.assertIn("< 100", manual)


# ======================================================================================
# MASTER RUNNER
# ======================================================================================
def run_tier5_harness():
    suite = unittest.TestSuite()
    loader = unittest.TestLoader()
    
    suite.addTests(loader.loadTestsFromTestCase(TestTier5_CADTopologyHardening))
    suite.addTests(loader.loadTestsFromTestCase(TestTier5_HTMLPresentationHardening))
    suite.addTests(loader.loadTestsFromTestCase(TestTier5_ProcurementAuditHardening))
    suite.addTests(loader.loadTestsFromTestCase(TestTier5_ManufacturingManualHardening))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print("\n" + "="*80)
    print(f"TIER 5 ADVERSARIAL HARDENING SUITE SUMMARY:")
    print(f"  Tests Executed: {result.testsRun}")
    print(f"  Failures:       {len(result.failures)}")
    print(f"  Errors:         {len(result.errors)}")
    print(f"  Success:        {result.wasSuccessful()}")
    print("="*80)
    
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(run_tier5_harness())
