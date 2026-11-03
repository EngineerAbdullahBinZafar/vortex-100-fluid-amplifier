"""
========================================================================================
CHALLENGER 1 EMPIRICAL STRESS TEST HARNESS: CAD GEOMETRY & FORMATS
Milestone: Milestone 1 (CAD Geometry & Format Stress Testing)
Target: VORTEX-100 CAD Assets (3MF, OBJ+MTL, STEP AP214, Binary STLs)
Standards: ISO 10303-21, 3MF Core/Material Specification, Wavefront OBJ/MTL, Binary STL
========================================================================================
"""

import os
import sys
import math
import struct
import zipfile
import re
import xml.etree.ElementTree as ET

BASE_DIR = r"C:\Users\star\Downloads\product design"
CAD_STL_DIR = os.path.join(BASE_DIR, "cad_stl")

CAD_3MF = os.path.join(BASE_DIR, "VORTEX_100_Full_Assembly_Colored.3mf")
CAD_OBJ = os.path.join(BASE_DIR, "VORTEX_100_Full_Assembly.obj")
CAD_MTL = os.path.join(BASE_DIR, "vortex_materials.mtl")
CAD_STEP = os.path.join(BASE_DIR, "VORTEX_100_Full_Assembly_Colored.step")

STL_COMPONENTS = [
    "Ring_Airfoil_Front.stl",
    "Ring_Airfoil_Back.stl",
    "Centrifugal_Impeller_11Blade.stl",
    "Volute_Diffuser_Plenum.stl",
    "Base_Pedestal_Enclosure.stl",
    "VORTEX_100_Full_Assembly.stl"
]

CMF_EXPECTED = {
    "Warm_Alabaster_White": {
        "hex_alpha": "#F4F1EAFF",
        "rgb_norm": (0.957, 0.945, 0.918),
        "tolerance": 0.01
    },
    "Champagne_Gold": {
        "hex_alpha": "#D4AF37FF",
        "rgb_norm": (0.831, 0.686, 0.216),
        "tolerance": 0.01
    },
    "Dark_Charcoal": {
        "hex_alpha": "#22252AFF",
        "rgb_norm": (0.133, 0.145, 0.165),
        "tolerance": 0.01
    },
    "Warm_White_Halo": {
        "hex_alpha": "#FFF8E7FF",
        "rgb_norm": (1.000, 0.973, 0.906),
        "tolerance": 0.01
    }
}


def stress_test_stl_mesh(filepath, quant_tolerances=(3, 4, 5)):
    assert os.path.exists(filepath), f"STL file not found: {filepath}"
    size = os.path.getsize(filepath)
    assert size >= 84, f"STL file {filepath} smaller than 84-byte header: {size}"

    with open(filepath, "rb") as f:
        header = f.read(80)
        n_tris = struct.unpack("<I", f.read(4))[0]
        expected_size = 84 + n_tris * 50
        assert size == expected_size, (
            f"File size mismatch for {filepath}: got {size}, expected {expected_size} "
            f"({n_tris} triangles)"
        )
        raw_records = f.read(n_tris * 50)

    min_b = [float("inf"), float("inf"), float("inf")]
    max_b = [float("-inf"), float("-inf"), float("-inf")]
    vol = 0.0
    surface_area = 0.0
    degenerate_count = 0
    inverted_normal_count = 0
    zero_normal_count = 0

    triangles = []
    offset = 0

    for i in range(n_tris):
        rec = struct.unpack_from("<ffffffffffffH", raw_records, offset)
        offset += 50
        nx, ny, nz = rec[0], rec[1], rec[2]
        v0 = (rec[3], rec[4], rec[5])
        v1 = (rec[6], rec[7], rec[8])
        v2 = (rec[9], rec[10], rec[11])

        for v in (v0, v1, v2):
            for d in range(3):
                if v[d] < min_b[d]:
                    min_b[d] = v[d]
                if v[d] > max_b[d]:
                    max_b[d] = v[d]

        ax, ay, az = v1[0] - v0[0], v1[1] - v0[1], v1[2] - v0[2]
        bx, by, bz = v2[0] - v0[0], v2[1] - v0[1], v2[2] - v0[2]
        cx = ay * bz - az * by
        cy = az * bx - ax * bz
        cz = ax * by - ay * bx
        c_len = math.sqrt(cx * cx + cy * cy + cz * cz)
        area = 0.5 * c_len
        surface_area += area

        if area < 1e-7:
            degenerate_count += 1

        vol += (v0[0] * cx + v0[1] * cy + v0[2] * cz) / 6.0

        n_len = math.sqrt(nx * nx + ny * ny + nz * nz)
        if n_len < 1e-6:
            zero_normal_count += 1
        elif c_len > 1e-6:
            calc_nx = cx / c_len
            calc_ny = cy / c_len
            calc_nz = cz / c_len
            dot = (nx * calc_nx + ny * calc_ny + nz * calc_nz) / n_len
            if dot < 0.0:
                inverted_normal_count += 1

        triangles.append((v0, v1, v2))

    quant_results = {}
    for decimals in quant_tolerances:
        vert_map = {}
        unique_verts = 0
        edge_counts = {}

        for v0, v1, v2 in triangles:
            idx = []
            for v in (v0, v1, v2):
                key = (round(v[0], decimals), round(v[1], decimals), round(v[2], decimals))
                if key not in vert_map:
                    vert_map[key] = unique_verts
                    unique_verts += 1
                idx.append(vert_map[key])

            for e_i in range(3):
                ia = idx[e_i]
                ib = idx[(e_i + 1) % 3]
                if ia != ib:
                    edge = (min(ia, ib), max(ia, ib))
                    edge_counts[edge] = edge_counts.get(edge, 0) + 1

        b_edges = sum(1 for c in edge_counts.values() if c == 1)
        nm_edges = sum(1 for c in edge_counts.values() if c > 2)
        watertight = (b_edges == 0 and nm_edges == 0)
        quant_results[decimals] = {
            "boundary_edges": b_edges,
            "non_manifold_edges": nm_edges,
            "unique_vertices": unique_verts,
            "watertight": watertight
        }

    return {
        "filepath": filepath,
        "triangles": n_tris,
        "bounding_box_min": min_b,
        "bounding_box_max": max_b,
        "dimensions": [round(max_b[d] - min_b[d], 4) for d in range(3)],
        "surface_area_mm2": surface_area,
        "volume_mm3": vol,
        "volume_cm3": vol / 1000.0,
        "outward_normals": vol > 0.0,
        "degenerate_triangles": degenerate_count,
        "inverted_facet_normals": inverted_normal_count,
        "zero_header_normals": zero_normal_count,
        "quant_results": quant_results
    }


def stress_test_3mf(filepath):
    assert os.path.exists(filepath), f"3MF file not found: {filepath}"
    assert zipfile.is_zipfile(filepath), f"File is not a valid ZIP: {filepath}"

    with zipfile.ZipFile(filepath, "r") as zf:
        namelist = zf.namelist()
        assert "[Content_Types].xml" in namelist, "3MF missing [Content_Types].xml"
        assert "_rels/.rels" in namelist, "3MF missing _rels/.rels"
        assert "3D/3dmodel.model" in namelist, "3MF missing 3D/3dmodel.model"

        ct_bytes = zf.read("[Content_Types].xml")
        ct_root = ET.fromstring(ct_bytes)
        assert ct_root.tag.endswith("Types"), f"Invalid Content_Types root: {ct_root.tag}"
        defaults = {el.attrib.get("Extension"): el.attrib.get("ContentType") for el in ct_root}
        assert "rels" in defaults, "Missing 'rels' default in Content_Types"
        assert "model" in defaults, "Missing 'model' default in Content_Types"
        assert "3dmanufacturing-3dmodel+xml" in defaults["model"], f"Unexpected model content type: {defaults['model']}"

        rels_bytes = zf.read("_rels/.rels")
        rels_root = ET.fromstring(rels_bytes)
        targets = [el.attrib.get("Target") for el in rels_root]
        assert any("3dmodel.model" in t for t in targets), f"No 3dmodel.model target in rels: {targets}"

        model_bytes = zf.read("3D/3dmodel.model")
        root = ET.fromstring(model_bytes)

        ns_core = "http://schemas.microsoft.com/3dmanufacturing/core/2015/02"
        ns_mat = "http://schemas.microsoft.com/3dmanufacturing/material/2015/02"

        assert root.tag == f"{{{ns_core}}}model", f"Invalid root tag: {root.tag}"
        assert root.attrib.get("unit") == "millimeter", f"Invalid or missing unit: {root.attrib.get('unit')}"

        colorgroups = root.findall(f".//{{{ns_mat}}}colorgroup")
        assert len(colorgroups) >= 1, "Missing <m:colorgroup> definition"
        cg = colorgroups[0]
        cg_id = cg.attrib.get("id")
        assert cg_id is not None, "Colorgroup missing id"

        colors = [el.attrib.get("color") for el in cg.findall(f"{{{ns_mat}}}color")]
        assert len(colors) == 4, f"Expected 4 colors in colorgroup, found {len(colors)}"

        for mat_name, mat_spec in CMF_EXPECTED.items():
            expected_hex = mat_spec["hex_alpha"]
            assert expected_hex in colors, f"Colorgroup missing expected color {expected_hex} for {mat_name}"

        objects = root.findall(f".//{{{ns_core}}}object")
        assert len(objects) >= 5, f"Expected at least 5 component objects in 3MF, found {len(objects)}"

        object_ids = set()
        object_topologies = {}

        for obj in objects:
            oid = obj.attrib.get("id")
            oname = obj.attrib.get("name", "unnamed")
            opid = obj.attrib.get("pid")
            opindex = obj.attrib.get("pindex")
            assert oid is not None, f"Object {oname} missing id"
            assert oid not in object_ids, f"Duplicate object id {oid}"
            object_ids.add(oid)

            mesh = obj.find(f"{{{ns_core}}}mesh")
            assert mesh is not None, f"Object {oname} (id={oid}) missing <mesh>"
            verts_el = mesh.find(f"{{{ns_core}}}vertices")
            tris_el = mesh.find(f"{{{ns_core}}}triangles")
            assert verts_el is not None, f"Object {oname} missing <vertices>"
            assert tris_el is not None, f"Object {oname} missing <triangles>"

            vertices = []
            for v_el in verts_el.findall(f"{{{ns_core}}}vertex"):
                x = float(v_el.attrib["x"])
                y = float(v_el.attrib["y"])
                z = float(v_el.attrib["z"])
                vertices.append((x, y, z))

            faces = []
            for t_el in tris_el.findall(f"{{{ns_core}}}triangle"):
                v1 = int(t_el.attrib["v1"])
                v2 = int(t_el.attrib["v2"])
                v3 = int(t_el.attrib["v3"])
                assert 0 <= v1 < len(vertices), f"Triangle vertex v1={v1} out of bounds ({len(vertices)} verts)"
                assert 0 <= v2 < len(vertices), f"Triangle vertex v2={v2} out of bounds ({len(vertices)} verts)"
                assert 0 <= v3 < len(vertices), f"Triangle vertex v3={v3} out of bounds ({len(vertices)} verts)"
                faces.append((v1, v2, v3))

            vert_map = {}
            unique_verts = 0
            edge_counts = {}
            vol = 0.0

            for v1, v2, v3 in faces:
                idx = []
                for vi in (v1, v2, v3):
                    v = vertices[vi]
                    k = (round(v[0], 4), round(v[1], 4), round(v[2], 4))
                    if k not in vert_map:
                        vert_map[k] = unique_verts
                        unique_verts += 1
                    idx.append(vert_map[k])

                for e_i in range(3):
                    ia = idx[e_i]
                    ib = idx[(e_i + 1) % 3]
                    if ia != ib:
                        edge = (min(ia, ib), max(ia, ib))
                        edge_counts[edge] = edge_counts.get(edge, 0) + 1

                p0 = vertices[v1]
                p1 = vertices[v2]
                p2 = vertices[v3]
                cx = (p1[1] - p0[1]) * (p2[2] - p0[2]) - (p1[2] - p0[2]) * (p2[1] - p0[1])
                cy = (p1[2] - p0[2]) * (p2[0] - p0[0]) - (p1[0] - p0[0]) * (p2[2] - p0[2])
                cz = (p1[0] - p0[0]) * (p2[1] - p0[1]) - (p1[1] - p0[1]) * (p2[0] - p0[0])
                vol += (p0[0] * cx + p0[1] * cy + p0[2] * cz) / 6.0

            b_edges = sum(1 for c in edge_counts.values() if c == 1)
            nm_edges = sum(1 for c in edge_counts.values() if c > 2)

            object_topologies[oname] = {
                "id": oid,
                "vertices": len(vertices),
                "faces": len(faces),
                "boundary_edges": b_edges,
                "non_manifold_edges": nm_edges,
                "watertight": (b_edges == 0 and nm_edges == 0),
                "volume_cm3": vol / 1000.0,
                "outward_normals": vol > 0.0
            }

        build_el = root.find(f"{{{ns_core}}}build")
        assert build_el is not None, "3MF missing <build> section"
        items = build_el.findall(f"{{{ns_core}}}item")
        assert len(items) >= len(objects), f"Mismatch: {len(objects)} objects but only {len(items)} build items"
        for item in items:
            ref_oid = item.attrib.get("objectid")
            assert ref_oid in object_ids, f"Build item references non-existent objectid: {ref_oid}"

    return {
        "valid": True,
        "colorgroup_colors": colors,
        "object_count": len(objects),
        "object_topologies": object_topologies
    }


def stress_test_obj_mtl(obj_path, mtl_path):
    assert os.path.exists(obj_path), f"OBJ file not found: {obj_path}"
    assert os.path.exists(mtl_path), f"MTL file not found: {mtl_path}"

    materials = {}
    current_mat = None
    with open(mtl_path, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split()
            token = parts[0]
            if token == "newmtl":
                current_mat = parts[1]
                materials[current_mat] = {}
            elif current_mat:
                if token in ("Ka", "Kd", "Ks", "Ke"):
                    materials[current_mat][token] = tuple(float(x) for x in parts[1:4])
                elif token in ("Ns", "d"):
                    materials[current_mat][token] = float(parts[1])
                elif token == "illum":
                    materials[current_mat][token] = int(parts[1])

    for mat_name, mat_spec in CMF_EXPECTED.items():
        assert mat_name in materials, f"MTL missing material: {mat_name}"
        kd = materials[mat_name].get("Kd")
        assert kd is not None, f"Material {mat_name} missing Kd declaration"
        exp_rgb = mat_spec["rgb_norm"]
        for c_i in range(3):
            diff = abs(kd[c_i] - exp_rgb[c_i])
            assert diff <= mat_spec["tolerance"], (
                f"Material {mat_name} Kd component {c_i} ({kd[c_i]}) differs from "
                f"expected ({exp_rgb[c_i]}) by {diff}"
            )

    all_vertices = []
    objects = {}
    current_obj = "default"
    current_usemtl = None
    has_mtllib = False

    with open(obj_path, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split()
            token = parts[0]
            if token == "mtllib":
                has_mtllib = True
                mtl_ref = parts[1]
                assert mtl_ref == os.path.basename(mtl_path), f"mtllib reference mismatch: {mtl_ref} vs {os.path.basename(mtl_path)}"
            elif token == "o":
                current_obj = parts[1]
                if current_obj not in objects:
                    objects[current_obj] = {"faces": [], "material": current_usemtl}
            elif token == "usemtl":
                current_usemtl = parts[1]
                assert current_usemtl in materials, f"OBJ references undefined material: {current_usemtl} at line {line_num}"
                if current_obj in objects:
                    objects[current_obj]["material"] = current_usemtl
            elif token == "v":
                v = (float(parts[1]), float(parts[2]), float(parts[3]))
                all_vertices.append(v)
            elif token == "f":
                if current_obj not in objects:
                    objects[current_obj] = {"faces": [], "material": current_usemtl}
                f_indices = []
                for p in parts[1:]:
                    v_idx = int(p.split("/")[0])
                    assert 1 <= v_idx <= len(all_vertices), f"Face vertex {v_idx} out of range (1..{len(all_vertices)})"
                    f_indices.append(v_idx - 1)
                assert len(f_indices) == 3, f"Non-triangular face found at line {line_num}: {len(f_indices)} vertices"
                objects[current_obj]["faces"].append(tuple(f_indices))

    assert has_mtllib, "OBJ file missing mtllib reference"
    assert len(objects) >= 5, f"Expected >= 5 objects in OBJ, found {len(objects)}"

    obj_topologies = {}
    for oname, odata in objects.items():
        faces = odata["faces"]
        vert_map = {}
        unique_verts = 0
        edge_counts = {}
        vol = 0.0

        for v0_i, v1_i, v2_i in faces:
            idx = []
            for vi in (v0_i, v1_i, v2_i):
                v = all_vertices[vi]
                k = (round(v[0], 4), round(v[1], 4), round(v[2], 4))
                if k not in vert_map:
                    vert_map[k] = unique_verts
                    unique_verts += 1
                idx.append(vert_map[k])

            for e_i in range(3):
                ia = idx[e_i]
                ib = idx[(e_i + 1) % 3]
                if ia != ib:
                    edge = (min(ia, ib), max(ia, ib))
                    edge_counts[edge] = edge_counts.get(edge, 0) + 1

            p0 = all_vertices[v0_i]
            p1 = all_vertices[v1_i]
            p2 = all_vertices[v2_i]
            cx = (p1[1] - p0[1]) * (p2[2] - p0[2]) - (p1[2] - p0[2]) * (p2[1] - p0[1])
            cy = (p1[2] - p0[2]) * (p2[0] - p0[0]) - (p1[0] - p0[0]) * (p2[2] - p0[2])
            cz = (p1[0] - p0[0]) * (p2[1] - p0[1]) - (p1[1] - p0[1]) * (p2[0] - p0[0])
            vol += (p0[0] * cx + p0[1] * cy + p0[2] * cz) / 6.0

        b_edges = sum(1 for c in edge_counts.values() if c == 1)
        nm_edges = sum(1 for c in edge_counts.values() if c > 2)

        obj_topologies[oname] = {
            "material": odata["material"],
            "faces": len(faces),
            "boundary_edges": b_edges,
            "non_manifold_edges": nm_edges,
            "watertight": (b_edges == 0 and nm_edges == 0),
            "volume_cm3": vol / 1000.0,
            "outward_normals": vol > 0.0
        }

    return {
        "valid": True,
        "materials": materials,
        "total_vertices": len(all_vertices),
        "objects": obj_topologies
    }


def stress_test_step_ap214(filepath):
    assert os.path.exists(filepath), f"STEP file not found: {filepath}"
    size = os.path.getsize(filepath)
    assert size > 100000, f"STEP file too small ({size} bytes)"

    with open(filepath, "r", encoding="utf-8", errors="replace") as f:
        content = f.read()

    assert content.startswith("ISO-10303-21;"), "STEP missing ISO-10303-21 signature"
    assert "HEADER;" in content, "STEP missing HEADER;"
    assert "ENDSEC;" in content, "STEP missing ENDSEC;"
    assert "DATA;" in content, "STEP missing DATA;"
    assert content.strip().endswith("END-ISO-10303-21;"), "STEP missing END-ISO-10303-21;"

    assert "FILE_SCHEMA(('AUTOMOTIVE_DESIGN" in content or "AUTOMOTIVE_DESIGN" in content, (
        "STEP missing AP214 AUTOMOTIVE_DESIGN schema"
    )

    ref_regex = re.compile(r"#(\d+)")

    entity_map = {}
    entity_types = {}
    lines = content.split(";\n")

    for line in lines:
        line = line.strip()
        if not line.startswith("#"):
            continue
        line_clean = line + ";" if not line.endswith(";") else line
        eq_pos = line_clean.find("=")
        if eq_pos != -1:
            eid_str = line_clean[1:eq_pos].strip()
            rest = line_clean[eq_pos + 1:].strip()
            if rest.endswith(";"):
                rest = rest[:-1].strip()
            try:
                eid = int(eid_str)
            except ValueError:
                continue
            entity_map[eid] = rest
            if rest.startswith("("):
                entity_types[eid] = "COMPLEX_INSTANCE"
            else:
                etype_m = re.match(r"^([A-Za-z0-9_]+)", rest)
                entity_types[eid] = etype_m.group(1) if etype_m else "UNKNOWN"

    assert len(entity_map) > 1000, f"Expected > 1,000 entities in STEP, found {len(entity_map)}"

    dangling_refs = []
    for eid, eargs in entity_map.items():
        refs = ref_regex.findall(eargs)
        for r in refs:
            r_int = int(r)
            if r_int not in entity_map:
                dangling_refs.append((eid, r_int))

    assert len(dangling_refs) == 0, f"Found {len(dangling_refs)} dangling entity references in STEP! First 5: {dangling_refs[:5]}"

    solids = [eid for eid, etype in entity_types.items() if etype == "MANIFOLD_SOLID_BREP"]
    assert len(solids) >= 5, f"Expected >= 5 MANIFOLD_SOLID_BREP entities, found {len(solids)}"

    shells = [eid for eid, etype in entity_types.items() if etype == "CLOSED_SHELL"]
    assert len(shells) >= 5, f"Expected >= 5 CLOSED_SHELL entities, found {len(shells)}"

    colours = {}
    for eid, etype in entity_types.items():
        if etype == "COLOUR_RGB":
            args = entity_map[eid]
            name_m = re.search(r"'([^']+)'", args)
            name = name_m.group(1) if name_m else "unnamed"
            floats = re.findall(r"[-+]?\d*\.\d+|\d+", args)
            r, g, b = float(floats[-3]), float(floats[-2]), float(floats[-1])
            colours[name] = {"eid": eid, "rgb": (r, g, b)}

    for mat_name, mat_spec in CMF_EXPECTED.items():
        assert mat_name in colours, f"STEP missing COLOUR_RGB for {mat_name}"
        col_rgb = colours[mat_name]["rgb"]
        exp_rgb = mat_spec["rgb_norm"]
        for c_i in range(3):
            diff = abs(col_rgb[c_i] - exp_rgb[c_i])
            assert diff <= mat_spec["tolerance"], (
                f"STEP COLOUR_RGB for {mat_name} component {c_i} ({col_rgb[c_i]}) "
                f"differs from expected ({exp_rgb[c_i]}) by {diff}"
            )

    styled_items = [eid for eid, etype in entity_types.items() if etype == "STYLED_ITEM"]
    assert len(styled_items) >= len(solids), f"Expected >= {len(solids)} STYLED_ITEM entities, found {len(styled_items)}"

    points = {}
    for eid, etype in entity_types.items():
        if etype == "CARTESIAN_POINT":
            args = entity_map[eid]
            floats = re.findall(r"[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?", args)
            if len(floats) >= 3:
                points[eid] = (float(floats[-3]), float(floats[-2]), float(floats[-1]))

    poly_loops = {}
    for eid, etype in entity_types.items():
        if etype == "POLY_LOOP":
            args = entity_map[eid]
            v_refs = [int(x) for x in ref_regex.findall(args)]
            if len(v_refs) == 3:
                poly_loops[eid] = tuple(v_refs)

    bounds = {}
    for eid, etype in entity_types.items():
        if etype == "FACE_OUTER_BOUND":
            args = entity_map[eid]
            p_refs = [int(x) for x in ref_regex.findall(args)]
            if p_refs:
                bounds[eid] = p_refs[0]

    faces = {}
    for eid, etype in entity_types.items():
        if etype == "FACE_SURFACE":
            args = entity_map[eid]
            f_refs = [int(x) for x in ref_regex.findall(args)]
            if f_refs and f_refs[0] in bounds:
                faces[eid] = bounds[f_refs[0]]

    shells_map = {}
    for eid, etype in entity_types.items():
        if etype == "CLOSED_SHELL":
            args = entity_map[eid]
            sh_refs = [int(x) for x in ref_regex.findall(args)]
            shells_map[eid] = sh_refs

    solid_topologies = {}
    for eid in solids:
        args = entity_map[eid]
        name_m = re.search(r"'([^']*)'", args)
        sname = name_m.group(1) if name_m else f"Solid_{eid}"
        sh_refs = [int(x) for x in ref_regex.findall(args)]
        if not sh_refs:
            continue
        shell_id = sh_refs[0]
        face_list = shells_map.get(shell_id, [])
        vol = 0.0
        for fid in face_list:
            if fid not in faces:
                continue
            pid = faces[fid]
            if pid not in poly_loops:
                continue
            v0_id, v1_id, v2_id = poly_loops[pid]
            p0 = points[v0_id]
            p1 = points[v1_id]
            p2 = points[v2_id]
            cx = (p1[1] - p0[1]) * (p2[2] - p0[2]) - (p1[2] - p0[2]) * (p2[1] - p0[1])
            cy = (p1[2] - p0[2]) * (p2[0] - p0[0]) - (p1[0] - p0[0]) * (p2[2] - p0[2])
            cz = (p1[0] - p0[0]) * (p2[1] - p0[1]) - (p1[1] - p0[1]) * (p2[0] - p0[0])
            vol += (p0[0] * cx + p0[1] * cy + p0[2] * cz) / 6.0

        solid_topologies[sname] = {
            "id": eid,
            "shell_id": shell_id,
            "faces": len(face_list),
            "volume_cm3": vol / 1000.0,
            "outward_normals": vol > 0.0
        }

    return {
        "valid": True,
        "total_entities": len(entity_map),
        "manifold_solids": len(solids),
        "closed_shells": len(shells),
        "colours": colours,
        "styled_items": len(styled_items),
        "solid_topologies": solid_topologies
    }


def main():
    print("=" * 80)
    print("STARTING EMPIRICAL CAD STRESS TEST SUITE")
    print("=" * 80)

    # 1. STL Meshes
    print("\n--- 1. EMPIRICAL BINARY STL STRESS TESTS ---")
    stl_reports = {}
    for sname in STL_COMPONENTS:
        root_path = os.path.join(BASE_DIR, sname)
        cad_path = os.path.join(CAD_STL_DIR, sname)

        assert os.path.exists(root_path), f"Missing root STL {root_path}"
        assert os.path.exists(cad_path), f"Missing cad_stl STL {cad_path}"
        with open(root_path, "rb") as f1, open(cad_path, "rb") as f2:
            assert f1.read() == f2.read(), f"Content mismatch between {root_path} and {cad_path}"

        res = stress_test_stl_mesh(root_path)
        stl_reports[sname] = res

        print(f"\n[STL] {sname}:")
        print(f"  Triangles:            {res['triangles']:,}")
        print(f"  Dimensions (mm):      {res['dimensions']}")
        print(f"  Volume:               {res['volume_cm3']:.2f} cm3")
        print(f"  Outward Normals:      {res['outward_normals']}")
        print(f"  Degenerate Triangles: {res['degenerate_triangles']}")
        print(f"  Inverted Facet Norms: {res['inverted_facet_normals']}")
        for tol, qres in res["quant_results"].items():
            print(f"  Quant {10**(-tol)}mm: Boundary={qres['boundary_edges']}, Non-Manifold={qres['non_manifold_edges']}, Watertight={qres['watertight']}")

        if sname != "VORTEX_100_Full_Assembly.stl":
            assert res["degenerate_triangles"] == 0, f"Found degenerate triangles in {sname}"
            assert res["outward_normals"], f"Inverted volume/normals in {sname}"
            assert res["quant_results"][4]["boundary_edges"] == 0, f"Seams/boundary holes in {sname}"
            assert res["quant_results"][4]["non_manifold_edges"] == 0, f"Non-manifold edges in {sname}"
            assert res["quant_results"][4]["watertight"], f"{sname} is not watertight!"

    # 2. 3MF File
    print("\n--- 2. EMPIRICAL 3MF MULTI-MATERIAL STRESS TESTS ---")
    res_3mf = stress_test_3mf(CAD_3MF)
    print(f"[3MF] Status: PASS (Structure & Namespaces)")
    print(f"  Colors defined: {res_3mf['colorgroup_colors']}")
    print(f"  Objects parsed: {res_3mf['object_count']}")
    for oname, otop in res_3mf["object_topologies"].items():
        print(f"  -> Object '{oname}': {otop['faces']:,} faces, Watertight: {otop['watertight']} (B={otop['boundary_edges']}, NM={otop['non_manifold_edges']}), Vol={otop['volume_cm3']:.2f} cm3, Outward={otop['outward_normals']}")
        assert otop['outward_normals'], f"3MF Object '{oname}' has inverted normals: Vol={otop['volume_cm3']:.2f} cm3"
        assert otop['volume_cm3'] > 0.0, f"3MF Object '{oname}' has non-positive volume: {otop['volume_cm3']:.2f} cm3"
        assert otop['watertight'], f"3MF Object '{oname}' is not watertight!"

    # 3. OBJ + MTL Pair
    print("\n--- 3. EMPIRICAL OBJ + MTL STRESS TESTS ---")
    res_obj = stress_test_obj_mtl(CAD_OBJ, CAD_MTL)
    print(f"[OBJ+MTL] Status: PASS (Structure & Materials)")
    print(f"  Materials parsed: {list(res_obj['materials'].keys())}")
    print(f"  Total Vertices:   {res_obj['total_vertices']:,}")
    for oname, otop in res_obj["objects"].items():
        print(f"  -> Object '{oname}': Mat={otop['material']}, Faces={otop['faces']:,}, Watertight: {otop['watertight']} (B={otop['boundary_edges']}, NM={otop['non_manifold_edges']}), Vol={otop['volume_cm3']:.2f} cm3, Outward={otop['outward_normals']}")
        assert otop['outward_normals'], f"OBJ Object '{oname}' has inverted normals: Vol={otop['volume_cm3']:.2f} cm3"
        assert otop['volume_cm3'] > 0.0, f"OBJ Object '{oname}' has non-positive volume: {otop['volume_cm3']:.2f} cm3"
        assert otop['watertight'], f"OBJ Object '{oname}' is not watertight!"

    # 4. STEP AP214
    print("\n--- 4. EMPIRICAL STEP AP214 STRESS TESTS ---")
    res_step = stress_test_step_ap214(CAD_STEP)
    print(f"[STEP AP214] Status: PASS (ISO 10303-21 Syntax & Entities)")
    print(f"  Total Entities:     {res_step['total_entities']:,}")
    print(f"  Manifold Solids:    {res_step['manifold_solids']}")
    print(f"  Closed Shells:      {res_step['closed_shells']}")
    print(f"  Colors Mapped:      {list(res_step['colours'].keys())}")
    print(f"  Styled Items:       {res_step['styled_items']}")
    for sname, stop in res_step["solid_topologies"].items():
        print(f"  -> Solid '{sname}': Faces={stop['faces']:,}, Vol={stop['volume_cm3']:.2f} cm3, Outward={stop['outward_normals']}")
        assert stop['outward_normals'], f"STEP Solid '{sname}' has inverted normals: Vol={stop['volume_cm3']:.2f} cm3"
        assert stop['volume_cm3'] > 0.0, f"STEP Solid '{sname}' has non-positive volume: {stop['volume_cm3']:.2f} cm3"

    print("\n" + "=" * 80)
    print(">>> EMPIRICAL CHALLENGER STRESS TESTS COMPLETE <<<")
    print("=" * 80)


if __name__ == "__main__":
    main()
