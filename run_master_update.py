# -*- coding: utf-8 -*-
"""
Master Presentation Upgrade Script for VORTEX-100
"""

import os
import sys
import re

OUTPUT_DIR = r"C:\Users\star\Downloads\product design"
SCRATCH_DIR = r"C:\Users\star\.gemini\antigravity\scratch\aero_bladeless_fan"

src_path = os.path.join(OUTPUT_DIR, "generate_presentation.py")
with open(src_path, "r", encoding="utf-8") as f:
    code = f.read()

print("Original code length:", len(code))
