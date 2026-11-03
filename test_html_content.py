with open('VORTEX_100_Bladeless_Fan_Presentation.html', 'r', encoding='utf-8') as f:
    text = f.read()

checks = {
    'Student Name': 'ABDULLAH BIN ZAFAR' in text,
    'Reg No': '2023-MC-292' in text,
    'Dept': 'Mechatronics & Control Engineering' in text,
    'Three.js script': 'three.min.js' in text,
    'OrbitControls': 'OrbitControls.js' in text,
    'Canvas Container': 'threejs-canvas-wrap' in text,
    'initThreeJsEngine': 'initThreeJsEngine' in text,
    '6 STL Cards': 'VORTEX_100_Full_Assembly.stl' in text,
    '2D SVG Drawings': 'Front Elevation & Slit Geometry' in text,
    'Fastener Architecture': 'M3 Brass Heat-Set Inserts' in text,
    'Bayonet Bottom Lid': 'Bayonet Twist-Lock' in text,
    'Vibration Grommets': 'Shore-40A' in text,
    'CMF Guide': 'Matte Alabaster Cream' in text,
    'Assembly Manual': '10-Step Production Assembly' in text,
    'Student Defense Banner': 'Student Capstone Defense Edition' in text,
    'VORTEX-100 Engraved': 'VORTEX-100' in text
}

all_pass = True
for k, v in checks.items():
    status = "PASS" if v else "FAIL"
    if not v:
        all_pass = False
    print(f"{k:25}: {status}")

print("\nOVERALL STATUS:", "ALL PASSED!" if all_pass else "SOME FAILED")
