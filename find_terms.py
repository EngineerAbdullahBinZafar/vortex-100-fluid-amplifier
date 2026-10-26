with open('VORTEX_100_Bladeless_Fan_Presentation.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if any(k in line for k in ['Student', 'Defense', '2023-MC-292', 'Orthographic', 'Bayonet']):
        print(f"Line {i+1}: {line.strip()[:140]}")
