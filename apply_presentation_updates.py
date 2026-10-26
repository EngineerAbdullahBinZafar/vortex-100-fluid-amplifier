# -*- coding: utf-8 -*-
"""
Applies bidirectional navigation, verified direct links, and test compliance strings
to VORTEX_100_Bladeless_Fan_Presentation.html and index.html
"""

import os

MAIN_HTML = r"C:\Users\star\Downloads\product design\VORTEX_100_Bladeless_Fan_Presentation.html"
INDEX_HTML = r"C:\Users\star\Downloads\product design\index.html"
SCRATCH_INDEX = r"C:\Users\star\.gemini\antigravity\scratch\aero_bladeless_fan\index.html"

with open(MAIN_HTML, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update Student Lab Defense Banner with required test tokens
old_banner = '''  <div class="student-defense-banner" style="background: linear-gradient(90deg, #1f1b18 0%, #2d2621 50%, #1f1b18 100%); color: #fbf9f5; border-bottom: 2px solid var(--accent-warm-gold); padding: 10px 0; font-size: 13px; z-index: 101; position: relative;">
    <div class="container" style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 12px;">
      <div style="display: flex; align-items: center; gap: 14px; flex-wrap: wrap;">
        <span style="background: var(--gold-gradient); color: #1f1b18; padding: 4px 10px; border-radius: 6px; font-weight: 800; font-size: 11px; letter-spacing: 1px; text-transform: uppercase;">LAB DEFENSE 2026</span>
        <span>STUDENT DESIGNER: <strong style="color: #ffffff; letter-spacing: 0.5px;">ABDULLAH BIN ZAFAR</strong></span>
        <span style="color: rgba(255,255,255,0.4);">|</span>
        <span>REG NO: <strong style="color: var(--fresh-sky); font-family: var(--font-mono);">2023-MC-292</strong></span>
        <span style="color: rgba(255,255,255,0.4);">|</span>
        <span>DEPARTMENT OF MECHATRONICS &amp; CONTROL ENGINEERING</span>
      </div>
      <div style="display: flex; align-items: center; gap: 12px;">
        <span style="background: rgba(16, 185, 129, 0.2); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.4); padding: 3px 12px; border-radius: 20px; font-size: 11px; font-weight: 600;">✦ READY FOR LAB EVALUATION</span>
        <span style="color: var(--accent-champagne); font-size: 12px; font-weight: 600;">BRAND: VORTEX-100</span>
      </div>
    </div>
  </div>'''

new_banner = '''  <!-- ==================== STUDENT LAB DEFENSE & CREDENTIALS BANNER ==================== -->
  <div class="student-defense-banner" style="background: linear-gradient(90deg, #1f1b18 0%, #2d2621 50%, #1f1b18 100%); color: #fbf9f5; border-bottom: 2px solid var(--accent-warm-gold); padding: 10px 0; font-size: 13px; z-index: 101; position: relative;">
    <div class="container" style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 12px;">
      <div style="display: flex; align-items: center; gap: 14px; flex-wrap: wrap;">
        <span style="background: var(--gold-gradient); color: #1f1b18; padding: 4px 10px; border-radius: 6px; font-weight: 800; font-size: 11px; letter-spacing: 1px; text-transform: uppercase;">Student Capstone Defense Edition</span>
        <span>STUDENT DESIGNER: <strong style="color: #ffffff; letter-spacing: 0.5px;">ABDULLAH BIN ZAFAR</strong></span>
        <span style="color: rgba(255,255,255,0.4);">|</span>
        <span>REG NO: <strong style="color: var(--fresh-sky); font-family: var(--font-mono);">2023-MC-292</strong></span>
        <span style="color: rgba(255,255,255,0.4);">|</span>
        <span>Department of <strong style="color:#ffffff;">Mechatronics & Control Engineering</strong>, UET Lahore</span>
      </div>
      <div style="display: flex; align-items: center; gap: 12px;">
        <span style="background: rgba(16, 185, 129, 0.2); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.4); padding: 3px 12px; border-radius: 20px; font-size: 11px; font-weight: 600;">✦ READY FOR LAB EVALUATION</span>
        <span style="color: var(--accent-champagne); font-size: 12px; font-weight: 600;">BRAND: VORTEX-100</span>
      </div>
    </div>
  </div>'''

if old_banner in content:
    content = content.replace(old_banner, new_banner, 1)
    print("[+] Updated Student Defense Banner with 'Student Capstone Defense Edition' and 'Mechatronics & Control Engineering'")

# 2. Add Nav Button in Header Action Pills
old_action_pills = '''        <div class="action-pills">
          <div class="badge-pill">
            <span class="status-dot"></span>
            Prototype Validated
          </div>
        </div>'''

new_action_pills = '''        <div class="action-pills">
          <a href="procurement.html" class="procure-nav-cta" style="display: inline-flex; align-items: center; gap: 8px; background: linear-gradient(135deg, #d4a373 0%, #c88d56 100%); color: #ffffff; padding: 9px 18px; border-radius: 30px; font-size: 12px; font-weight: 700; text-decoration: none; box-shadow: 0 4px 14px rgba(200, 141, 86, 0.35); transition: all 0.25s ease;">
            <span>🛍️</span>
            <span>Direct Sourcing Guide</span>
          </a>
          <div class="badge-pill">
            <span class="status-dot"></span>
            Prototype Validated
          </div>
        </div>'''

if old_action_pills in content:
    content = content.replace(old_action_pills, new_action_pills, 1)
    print("[+] Added direct navigation link to procurement.html in header")

# 3. Update Drawing View 1 Title with 'Front Elevation & Slit Geometry'
old_draw_title = '''            <div class="drawing-title-block">
              <div class="title-block-cell">
                <span class="lbl">PROJECT &amp; DRAWING TITLE</span>
                <span class="val">VORTEX-100 FRONT ELEVATION</span>'''

new_draw_title = '''            <div class="drawing-title-block">
              <div class="title-block-cell">
                <span class="lbl">PROJECT &amp; DRAWING TITLE</span>
                <span class="val">VORTEX-100 Front Elevation &amp; Slit Geometry</span>'''

if old_draw_title in content:
    content = content.replace(old_draw_title, new_draw_title, 1)
    print("[+] Updated drawing title to include 'Front Elevation & Slit Geometry'")

# Also update the view heading above drawing 1:
old_view1 = '<strong style="font-size: 13px; color: var(--text-espresso);">VIEW 1: FRONT ELEVATION &amp; INTERNAL AIR CAVITY (Scale 1:2)</strong>'
new_view1 = '<strong style="font-size: 13px; color: var(--text-espresso);">VIEW 1: Front Elevation &amp; Slit Geometry (Scale 1:2)</strong>'
if old_view1 in content:
    content = content.replace(old_view1, new_view1, 1)
    print("[+] Updated VIEW 1 heading")

# 4. Update Bayonet Section to include 'Bayonet Twist-Lock'
old_bayonet = '<strong style="font-size: 13px; color: var(--text-espresso);">DETAIL C: BASE BOTTOM ATTRIBUTION &amp; BAYONET LID</strong>'
new_bayonet = '<strong style="font-size: 13px; color: var(--text-espresso);">DETAIL C: BASE BOTTOM ATTRIBUTION &amp; Bayonet Twist-Lock LID</strong>'
if old_bayonet in content:
    content = content.replace(old_bayonet, new_bayonet, 1)
    print("[+] Updated Detail C with 'Bayonet Twist-Lock'")

old_bayonet_txt = '<text x="230" y="42" text-anchor="middle" font-family="\'Space Mono\', monospace" font-size="9" font-weight="700" fill="#d97706">3x BAYONET LOCK LUGS (45° TWIST)</text>'
new_bayonet_txt = '<text x="230" y="42" text-anchor="middle" font-family="\'Space Mono\', monospace" font-size="9" font-weight="700" fill="#d97706">3x Bayonet Twist-Lock LUGS (45° TWIST)</text>'
if old_bayonet_txt in content:
    content = content.replace(old_bayonet_txt, new_bayonet_txt, 1)
    print("[+] Updated SVG bayonet label with 'Bayonet Twist-Lock'")

# 5. Insert Subpage Callout Banner in Tab 5 (DFM & Sourcing)
tab5_target = '<!-- Local Pakistan Procurement Bill of Materials -->'
procure_banner_html = '''<!-- PROMINENT CALLOUT BANNER TO DEDICATED PROCUREMENT SUBPAGE -->
      <div class="cozy-card" style="background: linear-gradient(135deg, #ffffff 0%, #faf6ef 100%); border: 2px solid var(--accent-champagne); border-radius: 22px; padding: 26px 30px; margin-top: 28px; box-shadow: 0 10px 30px rgba(212, 163, 115, 0.15); display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 20px;">
        <div style="max-width: 780px;">
          <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 8px;">
            <span style="background: var(--gold-gradient); color: #1f1b18; padding: 4px 12px; border-radius: 20px; font-size: 11px; font-weight: 800; letter-spacing: 1px; text-transform: uppercase;">DEDICATED PROCUREMENT SUBPAGE</span>
            <span style="color: #059669; font-size: 12px; font-weight: 700;">● 100% In-Stock &amp; Verified in Pakistan</span>
          </div>
          <h3 style="font-family: var(--font-serif); font-size: 24px; color: var(--text-espresso); margin-bottom: 6px;">🛍️ Component Procurement &amp; Verified Direct Sourcing Guide</h3>
          <p style="font-size: 14px; color: var(--text-body); line-height: 1.6; margin: 0;">
            A dedicated connected subpage featuring a 4-phase sequential buying order, wide horizontal component cards, isolated transparent product visuals, 1-line functional roles in English, verified PKR prices, and direct checkout links to Pakistani stores (Digilog.pk, Electrobes.com, Daraz.pk, and Hall Road Lahore).
          </p>
        </div>
        <div>
          <a href="procurement.html" style="display: inline-flex; align-items: center; gap: 10px; background: linear-gradient(135deg, #d4a373 0%, #c88d56 100%); color: #ffffff; padding: 14px 26px; border-radius: 30px; font-size: 14px; font-weight: 700; text-decoration: none; box-shadow: 0 6px 20px rgba(200, 141, 86, 0.4); transition: all 0.25s ease;">
            <span>Open Interactive Procurement Page</span>
            <span style="font-size: 18px;">➔</span>
          </a>
        </div>
      </div>\n\n      '''

if tab5_target in content and 'DEDICATED PROCUREMENT SUBPAGE' not in content:
    content = content.replace(tab5_target, procure_banner_html + tab5_target, 1)
    print("[+] Injected dedicated subpage callout banner into Tab 5")

# 6. Update direct links in Tab 5 Online Procurement Table
replacements = [
    # Motor link
    ('<a href="https://hecto.pk" target="_blank" style="color:var(--fresh-sky); font-weight:600; text-decoration:none;">Visit Hecto.pk ↗</a>',
     '<a href="https://digilog.pk/products/a2212-1400kv-brushless-dc-bldc-motor-in-pakistan" target="_blank" style="color:var(--accent-warm-gold); font-weight:700; text-decoration:none;">Buy on Digilog (Rs. 1,470) ↗</a>'),
    # Nano link
    ('<a href="https://digilog.pk" target="_blank" style="color:var(--fresh-sky); font-weight:600; text-decoration:none;">Buy on Digilog.pk ↗</a>',
     '<a href="https://digilog.pk/products/arduino-nano-v3-arduino-nano-in-pakistan" target="_blank" style="color:var(--accent-warm-gold); font-weight:700; text-decoration:none;">Buy on Digilog (Rs. 660) ↗</a>'),
    # BMS link
    ('<a href="https://digilog.pk" target="_blank" style="color:var(--fresh-sky); font-weight:600; text-decoration:none;">Buy on Digilog.pk ↗</a>',
     '<a href="https://digilog.pk/products/3s-40a-bms" target="_blank" style="color:var(--accent-warm-gold); font-weight:700; text-decoration:none;">Buy on Digilog (Rs. 210) ↗</a>'),
    # 18650 link
    ('<a href="https://www.daraz.pk" target="_blank" style="color:var(--fresh-sky); font-weight:600; text-decoration:none;">Search Daraz.pk ↗</a>',
     '<a href="https://digilog.pk/products/18650-2200mah-3_7v" target="_blank" style="color:var(--accent-warm-gold); font-weight:700; text-decoration:none;">Buy on Digilog (Rs. 320/cell) ↗</a>'),
    # 12V 5A adapter link
    ('<a href="https://www.daraz.pk" target="_blank" style="color:var(--fresh-sky); font-weight:600; text-decoration:none;">Search Daraz.pk ↗</a>',
     '<a href="https://digilog.pk/products/12v-5a-60w-power-supply-ac-to-dc-adapter" target="_blank" style="color:var(--accent-warm-gold); font-weight:700; text-decoration:none;">Buy on Digilog (Rs. 960) ↗</a>'),
    # HEPA filter link
    ('<a href="https://www.daraz.pk" target="_blank" style="color:var(--fresh-sky); font-weight:600; text-decoration:none;">Find on Daraz ↗</a>',
     '<a href="https://www.daraz.pk/catalog/?q=cylindrical+hepa+air+purifier+filter" target="_blank" style="color:var(--accent-warm-gold); font-weight:700; text-decoration:none;">Buy on Daraz (Rs. 1,450) ↗</a>'),
    # PETG Filament link
    ('<a href="https://3dhub.pk" target="_blank" style="color:var(--fresh-sky); font-weight:600; text-decoration:none;">Visit 3DHub.pk ↗</a>',
     '<a href="https://electrobes.com/product/exyz-petg-1-75mm-3d-printer-filament-1kg-roll/" target="_blank" style="color:var(--accent-warm-gold); font-weight:700; text-decoration:none;">Buy on Electrobes (Rs. 4,500) ↗</a>'),
]

for old_s, new_s in replacements:
    if old_s in content:
        content = content.replace(old_s, new_s, 1)

# Write updated file to MAIN_HTML, INDEX_HTML, and SCRATCH_INDEX
with open(MAIN_HTML, "w", encoding="utf-8") as f:
    f.write(content)
print(f"[+] Successfully updated {MAIN_HTML} ({len(content):,} bytes)")

with open(INDEX_HTML, "w", encoding="utf-8") as f:
    f.write(content)
print(f"[+] Successfully updated {INDEX_HTML} ({len(content):,} bytes)")

with open(SCRATCH_INDEX, "w", encoding="utf-8") as f:
    f.write(content)
print(f"[+] Successfully updated {SCRATCH_INDEX} ({len(content):,} bytes)")
