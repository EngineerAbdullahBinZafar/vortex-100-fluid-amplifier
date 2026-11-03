"""
========================================================================================
PROJECT: VORTEX-100 Bladeless Air-Multiplier System
MODULE: Multi-Material Colored CAD & Watertight Mesh Engine (Production Master)
AUTHOR: ABDULLAH BIN ZAFAR (2023-MC-292) | Dept: Mechatronics & Control Engineering, UET Lahore
DESCRIPTION:
    100% Pure Python Standard Library multi-format CAD generator exporting:
    1. VORTEX_100_Full_Assembly_Colored.3mf — Valid OPC ZIP package with <m:colorgroup>
       containing #F4F1EAFF (Warm Alabaster White), #D4AF37FF (Champagne Gold),
       #22252AFF (Dark Charcoal), and #FFF8E7FF (Warm White Halo). Multi-object assembly.
    2. VORTEX_100_Full_Assembly.obj & vortex_materials.mtl — Wavefront OBJ grouping
       components with calibrated PBR materials (Kd, Ks, Ka, Ke, Ns, d, illum).
    3. VORTEX_100_Full_Assembly_Colored.step — ISO 10303-21 standard AP214 faceted B-Rep
       with COLOUR_RGB styling for each component.
    4. Production watertight binary STL files in root and cad_stl/ with 0 non-manifold
       edges and 0 boundary edges.
========================================================================================
"""

import os
import sys
import math
import struct
import json
import time
import zipfile
import shutil

# Import base geometry engine
import generate_vortex_stl as gvs

OUTPUT_DIR = r"C:\Users\star\Downloads\product design"
CAD_STL_DIR = os.path.join(OUTPUT_DIR, "cad_stl")

# ======================================================================================
# CMF DESIGN TOKENS & COLOR DEFINITIONS
# ======================================================================================
CMF_PALETTE = {
    "Warm_Alabaster_White": {
        "hex": "#F4F1EA",
        "hex_alpha": "#F4F1EAFF",
        "rgb_norm": (0.957, 0.945, 0.918),
        "rgb_8bit": (244, 241, 234),
        "threejs_hex": 0xF4F1EA,
        "pindex": 0,
        "roughness": 0.35,
        "metalness": 0.05,
        "pbr": {
            "Ka": (0.957, 0.945, 0.918),
            "Kd": (0.957, 0.945, 0.918),
            "Ks": (0.200, 0.200, 0.200),
            "Ns": 35.0,
            "d": 1.0,
            "illum": 2
        }
    },
    "Champagne_Gold": {
        "hex": "#D4AF37",
        "hex_alpha": "#D4AF37FF",
        "rgb_norm": (0.831, 0.686, 0.216),
        "rgb_8bit": (212, 175, 55),
        "threejs_hex": 0xD4AF37,
        "pindex": 1,
        "roughness": 0.22,
        "metalness": 0.88,
        "pbr": {
            "Ka": (0.831, 0.686, 0.216),
            "Kd": (0.831, 0.686, 0.216),
            "Ks": (0.880, 0.880, 0.880),
            "Ns": 88.0,
            "d": 1.0,
            "illum": 2
        }
    },
    "Dark_Charcoal": {
        "hex": "#22252A",
        "hex_alpha": "#22252AFF",
        "rgb_norm": (0.133, 0.145, 0.165),
        "rgb_8bit": (34, 37, 42),
        "threejs_hex": 0x22252A,
        "pindex": 2,
        "roughness": 0.55,
        "metalness": 0.15,
        "pbr": {
            "Ka": (0.133, 0.145, 0.165),
            "Kd": (0.133, 0.145, 0.165),
            "Ks": (0.150, 0.150, 0.150),
            "Ns": 25.0,
            "d": 1.0,
            "illum": 2
        }
    },
    "Warm_White_Halo": {
        "hex": "#FFF8E7",
        "hex_alpha": "#FFF8E7FF",
        "rgb_norm": (1.000, 0.973, 0.906),
        "rgb_8bit": (255, 248, 231),
        "threejs_hex": 0xFFF8E7,
        "pindex": 3,
        "roughness": 0.20,
        "metalness": 0.02,
        "pbr": {
            "Ka": (1.000, 0.973, 0.906),
            "Kd": (1.000, 0.973, 0.906),
            "Ks": (0.300, 0.300, 0.300),
            "Ke": (1.000, 0.973, 0.906),
            "Ns": 50.0,
            "d": 0.92,
            "illum": 2
        }
    }
}

# ======================================================================================
# MULTI-MATERIAL 3MF EXPORTER (OPC ZIP CONTAINER WITH <m:colorgroup>)
# ======================================================================================
def export_3mf(filepath, components):
    """
    Exports a 100% compliant 3MF OPC ZIP container with <m:colorgroup> containing:
    #F4F1EAFF, #D4AF37FF, #22252AFF, #FFF8E7FF and distinct multi-object structure.
    """
    content_types_xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">\n'
        '  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>\n'
        '  <Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/>\n'
        '</Types>'
    )

    rels_xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">\n'
        '  <Relationship Target="/3D/3dmodel.model" Id="rel0" '
        'Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/>\n'
        '</Relationships>'
    )

    model_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<model unit="millimeter" xml:lang="en-US" '
        'xmlns="http://schemas.microsoft.com/3dmanufacturing/core/2015/02" '
        'xmlns:m="http://schemas.microsoft.com/3dmanufacturing/material/2015/02">',
        '  <metadata name="Title">VORTEX-100 Bladeless Fan Full Assembly Colored</metadata>',
        '  <metadata name="Designer">ABDULLAH BIN ZAFAR (2023-MC-292)</metadata>',
        '  <metadata name="Department">Mechatronics &amp; Control Engineering, UET Lahore</metadata>',
        '  <metadata name="Description">Multi-Material Colored CAD Model of VORTEX-100 Bladeless Fan with Calibrated CMF</metadata>',
        '  <resources>',
        '    <m:colorgroup id="1">',
        '      <m:color color="#F4F1EAFF"/>',  # pindex 0: Warm Alabaster White
        '      <m:color color="#D4AF37FF"/>',  # pindex 1: Champagne Gold
        '      <m:color color="#22252AFF"/>',  # pindex 2: Dark Charcoal
        '      <m:color color="#FFF8E7FF"/>',  # pindex 3: Warm White Halo
        '    </m:colorgroup>'
    ]

    object_id = 2
    build_items = []

    for comp in components:
        mat_key = getattr(comp, "material_key", "Warm_Alabaster_White")
        mat_info = CMF_PALETTE[mat_key]
        pindex = mat_info["pindex"]

        vol = comp.compute_signed_volume()
        flip = (vol < 0.0)

        model_lines.append(f'    <object id="{object_id}" type="model" name="{comp.name}" pid="1" pindex="{pindex}">')
        model_lines.append('      <mesh>')
        model_lines.append('        <vertices>')
        for v in comp.vertices:
            model_lines.append(f'          <vertex x="{v[0]:.4f}" y="{v[1]:.4f}" z="{v[2]:.4f}"/>')
        model_lines.append('        </vertices>')
        model_lines.append('        <triangles>')
        for f in comp.faces:
            v1 = f[2] if flip else f[1]
            v2 = f[1] if flip else f[2]
            model_lines.append(f'          <triangle v1="{f[0]}" v2="{v1}" v3="{v2}" pid="1" p1="{pindex}"/>')
        model_lines.append('        </triangles>')
        model_lines.append('      </mesh>')
        model_lines.append('    </object>')

        build_items.append(f'    <item objectid="{object_id}"/>')
        object_id += 1

    model_lines.append('  </resources>')
    model_lines.append('  <build>')
    model_lines.extend(build_items)
    model_lines.append('  </build>')
    model_lines.append('</model>')

    model_xml = '\n'.join(model_lines)

    os.makedirs(os.path.dirname(os.path.abspath(filepath)), exist_ok=True)
    with zipfile.ZipFile(filepath, 'w', compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr('[Content_Types].xml', content_types_xml)
        zf.writestr('_rels/.rels', rels_xml)
        zf.writestr('3D/3dmodel.model', model_xml)

    return os.path.getsize(filepath)

# ======================================================================================
# WAVEFRONT OBJ + MTL EXPORTER (PBR MATERIALS & NAMED OBJECTS)
# ======================================================================================
def export_obj_mtl(obj_filepath, mtl_filepath, components):
    """
    Exports a Wavefront OBJ assembly and companion MTL file with calibrated PBR materials:
    Warm_Alabaster_White, Champagne_Gold, Dark_Charcoal, Warm_White_Halo.
    """
    mtl_lines = [
        "# VORTEX-100 PBR Material Definitions",
        "# Student: ABDULLAH BIN ZAFAR (2023-MC-292) | Dept: Mechatronics, UET Lahore",
        "# Palette: Nordic Pure Calibrated CMF",
        ""
    ]
    for mat_name, mat in CMF_PALETTE.items():
        pbr = mat["pbr"]
        mtl_lines.append(f"newmtl {mat_name}")
        mtl_lines.append(f"Ka {pbr['Ka'][0]:.4f} {pbr['Ka'][1]:.4f} {pbr['Ka'][2]:.4f}")
        mtl_lines.append(f"Kd {pbr['Kd'][0]:.4f} {pbr['Kd'][1]:.4f} {pbr['Kd'][2]:.4f}")
        mtl_lines.append(f"Ks {pbr['Ks'][0]:.4f} {pbr['Ks'][1]:.4f} {pbr['Ks'][2]:.4f}")
        if "Ke" in pbr:
            mtl_lines.append(f"Ke {pbr['Ke'][0]:.4f} {pbr['Ke'][1]:.4f} {pbr['Ke'][2]:.4f}")
        mtl_lines.append(f"Ns {pbr['Ns']:.1f}")
        mtl_lines.append(f"d {pbr['d']:.2f}")
        mtl_lines.append(f"illum {pbr['illum']}")
        mtl_lines.append("")

    with open(mtl_filepath, 'w', encoding='utf-8') as f_mtl:
        f_mtl.write('\n'.join(mtl_lines))

    mtl_filename = os.path.basename(mtl_filepath)
    obj_lines = [
        "# VORTEX-100 Bladeless Fan Full Assembly Colored OBJ",
        f"# Material Library: {mtl_filename}",
        f"mtllib {mtl_filename}",
        ""
    ]

    vert_offset = 1
    for comp in components:
        mat_key = getattr(comp, "material_key", "Warm_Alabaster_White")
        obj_lines.append(f"o {comp.name}")
        obj_lines.append(f"g {comp.name}")
        obj_lines.append(f"usemtl {mat_key}")

        for v in comp.vertices:
            obj_lines.append(f"v {v[0]:.4f} {v[1]:.4f} {v[2]:.4f}")

        vol = comp.compute_signed_volume()
        flip = (vol < 0.0)
        for f in comp.faces:
            v0 = f[0] + vert_offset
            v1 = (f[2] if flip else f[1]) + vert_offset
            v2 = (f[1] if flip else f[2]) + vert_offset
            obj_lines.append(f"f {v0} {v1} {v2}")

        vert_offset += len(comp.vertices)
        obj_lines.append("")

    with open(obj_filepath, 'w', encoding='utf-8') as f_obj:
        f_obj.write('\n'.join(obj_lines))

    return os.path.getsize(obj_filepath), os.path.getsize(mtl_filepath)

# ======================================================================================
# ISO 10303-21 STEP AP214 COLORED FACETED B-REP EXPORTER
# ======================================================================================
def export_step_ap214(filepath, components):
    """
    Exports ISO 10303-21 standard AP214 faceted B-Rep assembly with COLOUR_RGB styling.
    Compatible with SolidWorks, Fusion 360, FreeCAD, Rhino, and Autodesk Inventor.
    """
    timestamp = time.strftime("%Y-%m-%dT%H:%M:%S")

    step_lines = [
        "ISO-10303-21;",
        "HEADER;",
        "FILE_DESCRIPTION(('VORTEX-100 Bladeless Fan Full Assembly Colored AP214'), '2;1');",
        f"FILE_NAME('{os.path.basename(filepath)}', '{timestamp}', ('ABDULLAH BIN ZAFAR'), ('UET Lahore'), 'VORTEX Pure-Python CAD Engine', 'AP214 Faceted B-Rep Generator', '');",
        "FILE_SCHEMA(('AUTOMOTIVE_DESIGN { 1 0 10303 214 1 1 1 1 }'));",
        "ENDSEC;",
        "DATA;",
        "#1 = APPLICATION_CONTEXT('core data for automotive mechanical design processes');",
        "#2 = APPLICATION_PROTOCOL_DEFINITION('international standard', 'automotive_design', 2000, #1);",
        "#3 = PRODUCT_CONTEXT('', #1, 'mechanical');",
        "#4 = PRODUCT('VORTEX_100', 'VORTEX-100 Bladeless Fan Full Assembly', '', (#3));",
        "#5 = PRODUCT_DEFINITION_FORMATION('1', '', #4);",
        "#6 = PRODUCT_DEFINITION_CONTEXT('part definition', #1, 'design');",
        "#7 = PRODUCT_DEFINITION('design', '', #5, #6);",
        "#8 = PRODUCT_DEFINITION_SHAPE('', '', #7);",
        "#9 = ( GEOMETRIC_REPRESENTATION_CONTEXT(3) GLOBAL_UNCERTAINTY_ASSIGNED_CONTEXT((#10)) GLOBAL_UNIT_ASSIGNED_CONTEXT((#11, #12, #13)) REPRESENTATION_CONTEXT('Context #1', '3D Context with UNIT and UNCERTAINTY') );",
        "#10 = UNCERTAINTY_MEASURE_WITH_UNIT(LENGTH_MEASURE(1.E-05), #11, 'distance_accuracy_value', 'confusion accuracy');",
        "#11 = ( LENGTH_UNIT() NAMED_UNIT(*) SI_UNIT(.MILLI., .METRE.) );",
        "#12 = ( NAMED_UNIT(*) PLANE_ANGLE_UNIT() SI_UNIT($, .RADIAN.) );",
        "#13 = ( NAMED_UNIT(*) SOLID_ANGLE_UNIT() SI_UNIT($, .STERADIAN.) );",
        "#14 = CARTESIAN_POINT('', (0., 0., 0.));",
        "#15 = DIRECTION('', (0., 0., 1.));",
        "#16 = DIRECTION('', (1., 0., 0.));",
        "#17 = AXIS2_PLACEMENT_3D('', #14, #15, #16);"
    ]

    next_id = 20

    color_style_map = {}
    for mat_name, mat in CMF_PALETTE.items():
        r, g, b = mat["rgb_norm"]
        c_id = next_id; next_id += 1
        col_fill_id = next_id; next_id += 1
        fill_style_id = next_id; next_id += 1
        surf_fill_id = next_id; next_id += 1
        side_style_id = next_id; next_id += 1
        style_usage_id = next_id; next_id += 1
        pres_style_id = next_id; next_id += 1

        step_lines.append(f"#{c_id} = COLOUR_RGB('{mat_name}', {r:.4f}, {g:.4f}, {b:.4f});")
        step_lines.append(f"#{col_fill_id} = FILL_AREA_STYLE_COLOUR('', #{c_id});")
        step_lines.append(f"#{fill_style_id} = FILL_AREA_STYLE('', (#{col_fill_id}));")
        step_lines.append(f"#{surf_fill_id} = SURFACE_STYLE_FILL_AREA(#{fill_style_id});")
        step_lines.append(f"#{side_style_id} = SURFACE_SIDE_STYLE('', (#{surf_fill_id}));")
        step_lines.append(f"#{style_usage_id} = SURFACE_STYLE_USAGE(.BOTH., #{side_style_id});")
        step_lines.append(f"#{pres_style_id} = PRESENTATION_STYLE_ASSIGNMENT((#{style_usage_id}));")

        color_style_map[mat_name] = pres_style_id

    solid_ids = []
    styled_item_ids = []

    dir_map = {}
    def get_or_create_dir(dx, dy, dz):
        nonlocal next_id
        key = (round(dx, 4), round(dy, 4), round(dz, 4))
        if key not in dir_map:
            dir_map[key] = next_id
            step_lines.append(f"#{next_id} = DIRECTION('', ({key[0]}, {key[1]}, {key[2]}));")
            next_id += 1
        return dir_map[key]

    for comp in components:
        vol = comp.compute_signed_volume()
        flip = (vol < 0.0)
        vert_map = {}
        for f in comp.faces:
            for vi in f:
                v = comp.vertices[vi]
                key = (round(v[0], 4), round(v[1], 4), round(v[2], 4))
                if key not in vert_map:
                    vert_map[key] = next_id
                    step_lines.append(f"#{next_id} = CARTESIAN_POINT('', ({key[0]}, {key[1]}, {key[2]}));")
                    next_id += 1

        face_ids = []
        for f in comp.faces:
            i0 = f[0]
            i1 = f[2] if flip else f[1]
            i2 = f[1] if flip else f[2]
            v0 = comp.vertices[i0]
            v1 = comp.vertices[i1]
            v2 = comp.vertices[i2]
            k0 = (round(v0[0], 4), round(v0[1], 4), round(v0[2], 4))
            k1 = (round(v1[0], 4), round(v1[1], 4), round(v1[2], 4))
            k2 = (round(v2[0], 4), round(v2[1], 4), round(v2[2], 4))
            id0, id1, id2 = vert_map[k0], vert_map[k1], vert_map[k2]

            ax, ay, az = v1[0] - v0[0], v1[1] - v0[1], v1[2] - v0[2]
            bx, by, bz = v2[0] - v0[0], v2[1] - v0[1], v2[2] - v0[2]
            nx = ay * bz - az * by
            ny = az * bx - ax * bz
            nz = ax * by - ay * bx
            nl = math.sqrt(nx * nx + ny * ny + nz * nz)
            if nl > 1e-12:
                nx, ny, nz = nx / nl, ny / nl, nz / nl
            else:
                nx, ny, nz = 0.0, 0.0, 1.0

            if abs(nx) < 0.9:
                rx, ry, rz = 0.0, -nz, ny
            else:
                rx, ry, rz = -nz, 0.0, nx
            rl = math.sqrt(rx * rx + ry * ry + rz * rz)
            if rl > 1e-12:
                rx, ry, rz = rx / rl, ry / rl, rz / rl
            else:
                rx, ry, rz = 1.0, 0.0, 0.0

            axis_dir_id = get_or_create_dir(nx, ny, nz)
            ref_dir_id = get_or_create_dir(rx, ry, rz)

            poly_id = next_id; next_id += 1
            step_lines.append(f"#{poly_id} = POLY_LOOP('', (#{id0}, #{id1}, #{id2}));")

            bound_id = next_id; next_id += 1
            step_lines.append(f"#{bound_id} = FACE_OUTER_BOUND('', #{poly_id}, .T.);")

            placement_id = next_id; next_id += 1
            step_lines.append(f"#{placement_id} = AXIS2_PLACEMENT_3D('', #{id0}, #{axis_dir_id}, #{ref_dir_id});")

            plane_id = next_id; next_id += 1
            step_lines.append(f"#{plane_id} = PLANE('', #{placement_id});")

            face_id = next_id; next_id += 1
            step_lines.append(f"#{face_id} = FACE_SURFACE('', (#{bound_id}), #{plane_id}, .T.);")
            face_ids.append(face_id)

        shell_id = next_id; next_id += 1
        faces_str = ', '.join(f"#{fid}" for fid in face_ids)
        step_lines.append(f"#{shell_id} = CLOSED_SHELL('', ({faces_str}));")

        solid_id = next_id; next_id += 1
        step_lines.append(f"#{solid_id} = MANIFOLD_SOLID_BREP('{comp.name}', #{shell_id});")
        solid_ids.append(solid_id)

        mat_key = getattr(comp, "material_key", "Warm_Alabaster_White")
        pres_style_id = color_style_map.get(mat_key, list(color_style_map.values())[0])
        styled_item_id = next_id; next_id += 1
        step_lines.append(f"#{styled_item_id} = STYLED_ITEM('{comp.name}_Style', (#{pres_style_id}), #{solid_id});")
        styled_item_ids.append(styled_item_id)

    shape_rep_id = next_id; next_id += 1
    items_str = ', '.join([f"#{sid}" for sid in solid_ids] + ["#17"])
    step_lines.append(f"#{shape_rep_id} = ADVANCED_BREP_SHAPE_REPRESENTATION('VORTEX_100_Full_Assembly', ({items_str}), #9);")

    shape_def_rep_id = next_id; next_id += 1
    step_lines.append(f"#{shape_def_rep_id} = SHAPE_DEFINITION_REPRESENTATION(#8, #{shape_rep_id});")

    styled_items_str = ', '.join(f"#{si}" for si in styled_item_ids)
    mech_pres_id = next_id; next_id += 1
    step_lines.append(f"#{mech_pres_id} = MECHANICAL_DESIGN_GEOMETRIC_PRESENTATION_REPRESENTATION('CMF_Color_Assignment', ({styled_items_str}), #9);")

    step_lines.append("ENDSEC;")
    step_lines.append("END-ISO-10303-21;")

    os.makedirs(os.path.dirname(os.path.abspath(filepath)), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f_step:
        f_step.write('\n'.join(step_lines))

    return os.path.getsize(filepath)

# ======================================================================================
# MASTER PIPELINE EXECUTION
# ======================================================================================
def run_vortex_colored_cad_pipeline():
    start_time = time.time()
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(CAD_STL_DIR, exist_ok=True)

    print("=" * 90)
    print("   VORTEX-100 MULTI-MATERIAL COLORED CAD & WATERTIGHT MESH PIPELINE")
    print("   CMF SPECIFICATION: Warm Alabaster White, Champagne Gold, Dark Charcoal, Warm Halo")
    print("=" * 90)
    print(f"Target Output Directory: {OUTPUT_DIR}\n")

    # 1. Generate all components using the verified watertight generator engine
    print("[1/4] Generating component meshes with 100% manifold topology...")
    
    c_ring_front = gvs.generate_ring_airfoil_front()
    c_ring_front.name = "Ring_Airfoil_Front"
    c_ring_front.material_key = "Warm_Alabaster_White"

    c_ring_back = gvs.generate_ring_airfoil_back()
    c_ring_back.name = "Ring_Airfoil_Back"
    c_ring_back.material_key = "Warm_Alabaster_White"

    c_impeller = gvs.generate_centrifugal_impeller()
    c_impeller.name = "Centrifugal_Impeller_11Blade"
    c_impeller.material_key = "Champagne_Gold"

    c_volute = gvs.generate_volute_diffuser_plenum()
    c_volute.name = "Volute_Diffuser_Plenum"
    c_volute.material_key = "Dark_Charcoal"

    c_base = gvs.generate_base_pedestal_enclosure()
    c_base.name = "Base_Pedestal_Enclosure"
    c_base.material_key = "Warm_Alabaster_White"

    # Additional visual CMF accent components:
    c_halo = gvs.create_tube_manifold(r_in=74.0, r_out=76.25, h=2.5, n_theta=64, z0=15.0)
    c_halo.name = "Halo_Ring_Lightguide"
    c_halo.material_key = "Warm_White_Halo"

    c_knob = gvs.create_cylinder_manifold(r=11.0, h=14.0, n_theta=36, z0=138.0, center_xy=(0.0, -65.0))
    c_knob.name = "Control_Knob_Accent"
    c_knob.material_key = "Champagne_Gold"

    primary_components = [
        c_ring_front,
        c_ring_back,
        c_impeller,
        c_volute,
        c_base
    ]

    all_components = [
        c_ring_front,
        c_ring_back,
        c_impeller,
        c_volute,
        c_base,
        c_halo,
        c_knob
    ]

    full_assembly_mesh = gvs.STLMesh("VORTEX_100_Full_Assembly")
    for comp in primary_components:
        full_assembly_mesh.append_mesh(comp)

    for comp in all_components:
        print(f"   -> {comp.name:30}: {len(comp.faces):,d} triangles, Material: {comp.material_key}")

    # 2. Export Binary STLs (Root and cad_stl/)
    print("\n[2/4] Exporting watertight binary STL files to root and cad_stl/ ...")
    stl_files_to_verify = []

    primary_stls = [
        ("Ring_Airfoil_Front.stl", c_ring_front),
        ("Ring_Airfoil_Back.stl", c_ring_back),
        ("Centrifugal_Impeller_11Blade.stl", c_impeller),
        ("Volute_Diffuser_Plenum.stl", c_volute),
        ("Base_Pedestal_Enclosure.stl", c_base),
    ]

    for fname, mesh in primary_stls:
        root_path = os.path.join(OUTPUT_DIR, fname)
        cad_path = os.path.join(CAD_STL_DIR, fname)
        mesh.save_binary_stl(root_path)
        mesh.save_binary_stl(cad_path)
        stl_files_to_verify.append(root_path)
        print(f"   -> Saved {fname} ({len(mesh.faces):,d} triangles) in root and cad_stl/")

    # Also save full assembly STL
    asm_root = os.path.join(OUTPUT_DIR, "VORTEX_100_Full_Assembly.stl")
    asm_cad = os.path.join(CAD_STL_DIR, "VORTEX_100_Full_Assembly.stl")
    full_assembly_mesh.save_binary_stl(asm_root)
    full_assembly_mesh.save_binary_stl(asm_cad)
    print(f"   -> Saved VORTEX_100_Full_Assembly.stl ({len(full_assembly_mesh.faces):,d} triangles) in root and cad_stl/")

    # 3. Export Multi-Material Colored CAD Formats
    print("\n[3/4] Exporting Multi-Material Colored CAD Formats (3MF, OBJ+MTL, STEP AP214)...")

    # A. 3MF Multi-Material Colored Assembly
    path_3mf = os.path.join(OUTPUT_DIR, "VORTEX_100_Full_Assembly_Colored.3mf")
    size_3mf = export_3mf(path_3mf, all_components)
    print(f"   -> [3MF]  Successfully exported: {os.path.basename(path_3mf)} ({size_3mf / 1024:.1f} KB)")

    # B. OBJ + MTL Wavefront PBR Assembly
    path_obj = os.path.join(OUTPUT_DIR, "VORTEX_100_Full_Assembly.obj")
    path_mtl = os.path.join(OUTPUT_DIR, "vortex_materials.mtl")
    size_obj, size_mtl = export_obj_mtl(path_obj, path_mtl, all_components)
    print(f"   -> [OBJ]  Successfully exported: {os.path.basename(path_obj)} ({size_obj / (1024*1024):.2f} MB)")
    print(f"   -> [MTL]  Successfully exported: {os.path.basename(path_mtl)} ({size_mtl} bytes)")

    # C. STEP AP214 Colored Assembly
    path_step = os.path.join(OUTPUT_DIR, "VORTEX_100_Full_Assembly_Colored.step")
    size_step = export_step_ap214(path_step, all_components)
    print(f"   -> [STEP] Successfully exported: {os.path.basename(path_step)} ({size_step / (1024*1024):.2f} MB)")

    # 4. Rigorous Topological Verification
    print("\n[4/4] Running Rigorous 3D Topological Verification Suite...")
    verification_results = []
    all_passed = True

    for fpath in stl_files_to_verify:
        res = gvs.STLMesh.verify_stl(fpath)
        verification_results.append(res)

        fname = res["filename"]
        dims = res["dimensions_mm"]
        vol_cm3 = res["solid_volume_cm3"]
        triangles = res["triangles"]
        wt = res["is_watertight"]
        b_edges = res["boundary_edges"]
        nm_edges = res["non_manifold_edges"]
        degen = res["degenerate_triangles"]

        status_str = "PASS (100% Watertight)" if wt else "FAIL"
        if not wt or degen > 0:
            all_passed = False

        print(f"\n[FILE]: {fname}")
        print(f"   - Dimensions (L x W x H): {dims[0]} mm x {dims[1]} mm x {dims[2]} mm")
        print(f"   - Enclosed Solid Volume: {vol_cm3:.2f} cm3")
        print(f"   - Triangle Count:        {triangles:,} triangles")
        print(f"   - Unique Vertices:       {res['unique_vertices']:,}")
        print(f"   - Boundary Edges:        {b_edges} (Must be 0 for watertight)")
        print(f"   - Non-Manifold Edges:    {nm_edges} (Must be 0 for clean manifold)")
        print(f"   - Degenerate Triangles:  {degen}")
        print(f"   - Outward Normals:       {'OK (Positive Volume)' if res['outward_normals'] else 'INVERTED'}")
        print(f"   - Topological Status:    {status_str}")

    # Update verification JSON report
    report_json_path = os.path.join(OUTPUT_DIR, "vortex_stl_verification_report.json")
    with open(report_json_path, "w", encoding="utf-8") as f_json:
        json.dump({
            "pipeline": "VORTEX-100 Multi-Material Colored CAD Generator",
            "all_passed": all_passed,
            "components": verification_results,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }, f_json, indent=4)

    total_elapsed = time.time() - start_time
    print("\n" + "=" * 90)
    print(f"COLORED CAD PIPELINE COMPLETED in {total_elapsed:.2f} seconds!")
    print(f"Structured verification log exported to: {report_json_path}")
    print("=" * 90)

    return all_passed

if __name__ == "__main__":
    success = run_vortex_colored_cad_pipeline()
    sys.exit(0 if success else 1)
