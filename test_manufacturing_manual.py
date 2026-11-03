# -*- coding: utf-8 -*-
"""
Verification Suite for VORTEX-100 Manufacturing & Physical Assembly Manual
Validates comprehensive coverage of FDM slicer profile, 5-job print sequence,
6-phase physical assembly, and HTML presentation parity.
"""

import os
import re
import unittest

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
MANUAL_PATH = os.path.join(BASE_DIR, "MANUFACTURING_AND_ASSEMBLY_MANUAL.md")
PRESENTATION_PATH = os.path.join(BASE_DIR, "VORTEX_100_Bladeless_Fan_Presentation.html")
INDEX_PATH = os.path.join(BASE_DIR, "index.html")


class TestManufacturingAndAssemblyManual(unittest.TestCase):
    """Verifies content, structure, and technical metrics of the manual."""

    @classmethod
    def setUpClass(cls):
        self_path = MANUAL_PATH
        assert os.path.exists(self_path), f"Manual missing at {self_path}"
        with open(self_path, "r", encoding="utf-8") as f:
            cls.manual_text = f.read()

        with open(PRESENTATION_PATH, "r", encoding="utf-8") as f:
            cls.presentation_text = f.read()

        with open(INDEX_PATH, "r", encoding="utf-8") as f:
            cls.index_text = f.read()

    # --- SECTION 1: FDM SLICER PROFILE ---

    def test_sec1_bed_envelope_and_kinematics(self):
        """Verifies 220x220x250mm bed envelope, 0.4mm nozzle, and layer heights."""
        text = self.manual_text
        self.assertIn("220 × 220 × 250 mm", text)
        self.assertIn("0.40 mm", text)
        self.assertIn("0.20 mm", text)
        self.assertIn("0.16 mm", text)  # adaptive for Coanda ramp

    def test_sec1_perimeters_and_acoustic_damping(self):
        """Verifies 4 solid perimeters (1.6mm total shell) and gyroid infill."""
        text = self.manual_text
        self.assertIn("4 solid perimeter", text.lower())
        self.assertIn("1.60 mm", text)
        self.assertIn("Gyroid", text)
        self.assertIn("20%", text)
        self.assertIn("25%", text)
        self.assertIn("35%", text)  # Blower cradle infill

    def test_sec1_thermal_profiles_petg_vs_pla(self):
        """Verifies PETG (238C / 78C) vs PLA+ (210C / 60C) thermal parameters."""
        text = self.manual_text
        self.assertIn("238°C", text)
        self.assertIn("78°C", text)
        self.assertIn("210°C", text)
        self.assertIn("60°C", text)
        self.assertIn("73°C", text)  # HDT PETG

    def test_sec1_zero_support_orientation_strategy(self):
        """Verifies 0-support strategy for airfoil front lip, rear cowl, and bottom lid."""
        text = self.manual_text
        self.assertIn("Ring Airfoil Front Lip", text)
        self.assertIn("Ring Airfoil Rear Cowl", text)
        self.assertIn("Base Bottom Lid", text)
        self.assertIn("0 Supports Required", text)

    # --- SECTION 2: 5-JOB CHRONOLOGICAL PRINT SEQUENCE ---

    def test_sec2_5_job_breakdown_and_totals(self):
        """Verifies 5 sequential print jobs totaling ~28.2 hours and ~585g filament."""
        text = self.manual_text
        self.assertIn("Job 1", text)
        self.assertIn("Job 2", text)
        self.assertIn("Job 3", text)
        self.assertIn("Job 4", text)
        self.assertIn("Job 5", text)
        self.assertIn("28.2", text)
        self.assertIn("585", text)

    def test_sec2_parallel_bench_assembly_scheduling(self):
        """Verifies dual-track parallel workflow during long prints."""
        text = self.manual_text
        self.assertIn("Parallel Bench Assembly", text)
        self.assertIn("Dual-Track", text)
        self.assertIn("bench", text.lower())

    # --- SECTION 3: 6-PHASE PHYSICAL ASSEMBLY MANUAL ---

    def test_sec3_phase_a_brass_inserts(self):
        """Verifies Phase A: M3 brass heat-set insert thermal installation."""
        text = self.manual_text
        self.assertIn("Phase A", text)
        self.assertIn("M3", text)
        self.assertIn("heat-set", text.lower())
        self.assertIn("235°C", text)

    def test_sec3_phase_b_airfoil_and_feeler_gauge(self):
        """Verifies Phase B: 1.25mm feeler gauge verification and halo LED integration."""
        text = self.manual_text
        self.assertIn("Phase B", text)
        self.assertIn("1.25 mm", text)
        self.assertIn("feeler gauge", text.lower())
        self.assertIn("Halo LED", text)
        self.assertIn("rtv silicone", text.lower())

    def test_sec3_phase_c_blower_and_grommets(self):
        """Verifies Phase C: 12V blower installation on Shore-40A grommets with 20% preload."""
        text = self.manual_text
        self.assertIn("Phase C", text)
        self.assertIn("Shore-40A", text)
        self.assertIn("20%", text)
        self.assertIn("5.20 mm", text)  # compressed height from 6.5mm
        self.assertIn("EPDM", text)

    def test_sec3_phase_d_pedestal_and_wiring(self):
        """Verifies Phase D: DC barrel jack, rotary potentiometer, point-to-point wiring."""
        text = self.manual_text
        self.assertIn("Phase D", text)
        self.assertIn("5.5 × 2.1 mm", text)
        self.assertIn("Rotary Potentiometer", text)
        self.assertIn("POINT-TO-POINT SCHEMATIC", text)
        self.assertIn("NET-01", text)

    def test_sec3_phase_e_hepa_and_bayonet_compression(self):
        """Verifies Phase E: cylindrical HEPA filter and 1.5mm bayonet compression."""
        text = self.manual_text
        self.assertIn("Phase E", text)
        self.assertIn("HEPA", text)
        self.assertIn("110 mm OD", text)
        self.assertIn("1.50 mm", text)  # compression
        self.assertIn("Bayonet", text)

    def test_sec3_phase_f_dmm_safety_and_commissioning(self):
        """Verifies Phase F: pre-power DMM check (R > 10 kOhm) and live commissioning."""
        text = self.manual_text
        self.assertIn("Phase F", text)
        self.assertIn("Digital Multimeter", text)
        self.assertIn("10.0", text)  # R > 10.0 kOhm
        self.assertIn("Open Loop", text)
        self.assertIn("Commissioning", text)

    # --- PRESENTATION HTML INTEGRATION & PARITY ---

    def test_html_presentation_incorporates_assembly_details(self):
        """Verifies presentation HTML includes 6 phases, 5-job print sequence, and manual link."""
        pres = self.presentation_text
        self.assertIn("Phase A: Pre-Assembly Inspection", pres)
        self.assertIn("Phase B: Airfoil Ring Subassembly", pres)
        self.assertIn("Phase C: 12V Blower Installation", pres)
        self.assertIn("Phase D: Pedestal Installation", pres)
        self.assertIn("Phase E: Cylindrical HEPA Filter", pres)
        self.assertIn("Phase F: Airfoil Mating", pres)
        self.assertIn("28.2 Hours", pres)
        self.assertIn("MANUFACTURING_AND_ASSEMBLY_MANUAL.md", pres)

    def test_presentation_and_index_bit_for_bit_parity(self):
        """Verifies VORTEX_100_Bladeless_Fan_Presentation.html and index.html are identical."""
        with open(PRESENTATION_PATH, "rb") as f1, open(INDEX_PATH, "rb") as f2:
            d1 = f1.read()
            d2 = f2.read()
        self.assertEqual(len(d1), len(d2), "Byte size mismatch between presentation and index")
        self.assertEqual(d1, d2, "Content mismatch: presentation and index must be 100% bit-for-bit identical")


if __name__ == "__main__":
    unittest.main()
