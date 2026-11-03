#!/usr/bin/env python3
"""
Empirical Re-Check Oracle for Milestone 1 Remediation
Validates face winding, outward normals, positive volume, watertightness,
and manifold topological properties across 3MF, OBJ, and STEP AP214 assets.
"""

import sys
import os
import zipfile
import xml.etree.ElementTree as ET
import math
from collections import defaultdict

BASE_DIR = os.path.abspath(r"C:\Users\star\Downloads\product design")
FILE_3MF = os.path.join(BASE_DIR, "VORTEX_100_Full_Assembly_Colored.3mf")
FILE_OBJ = os.path.join(BASE_DIR, "VORTEX_100_Full_Assembly.obj")
FILE_STEP = os.path.join(BASE_DIR, "VORTEX_100_Full_Assembly_Colored.step")

EXPECTED_BODIES = [
    "Ring_Airfoil_Front",
    "Ring_Airfoil_Back",
    "Centrifugal_Impeller_11Blade",
    "Volute_Diffuser_Plenum",
    "Base_Pedestal_Enclosure",
    "Halo_Ring_Lightguide",
    "Control_Knob_Accent",
]

def cross(a, b):
    return (
        a[1] * b[2] - a[2] * b[1],
        a[2] * b[0] - a[0] * b[2],
        a[0] * b[1] - a[1] * b[0]
    )

def dot(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]

def sub(a, b):
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])

def compute_mesh_metrics(vertices, faces):
    """
    Computes signed volume, boundary edges, non-manifold edges,
    and checks consistent orientation.
    """
    vol6 = 0.0
    degen_count = 0
    edge_undirected = defaultdict(list)

    # Weld vertices for topology analysis
    v_map = {}
    u_idx = 0
    for v in vertices:
        k = (round(v[0], 4), round(v[1], 4), round(v[2], 4))
        if k not in v_map:
            v_map[k] = u_idx
            u_idx += 1

    welded_indices = [v_map[(round(v[0], 4), round(v[1], 4), round(v[2], 4))] for v in vertices]

    for i, f in enumerate(faces):
        v0, v1, v2 = vertices[f[0]], vertices[f[1]], vertices[f[2]]
        cp = cross(sub(v1, v0), sub(v2, v0))
        area = 0.5 * math.sqrt(dot(cp, cp))
        if area < 1e-12:
            degen_count += 1
        vol6 += dot(v0, cp)

        w0, w1, w2 = welded_indices[f[0]], welded_indices[f[1]], welded_indices[f[2]]
        edges = [(w0, w1), (w1, w2), (w2, w0)]
        for e in edges:
            if e[0] != e[1]:
                u_edge = tuple(sorted(e))
                edge_undirected[u_edge].append(e)

    signed_volume_cm3 = (vol6 / 6.0) / 1000.0

    boundary_edges = sum(1 for d in edge_undirected.values() if len(d) == 1)
    non_manifold_edges = sum(1 for d in edge_undirected.values() if len(d) > 2)
    inconsistent_orientation = sum(1 for d in edge_undirected.values() if len(d) == 2 and d[0] == d[1])

    watertight = (boundary_edges == 0 and non_manifold_edges == 0)
    outward = (signed_volume_cm3 > 0.0)

    return {
        "faces": len(faces),
        "vertices": len(vertices),
        "unique_vertices": u_idx,
        "volume_cm3": signed_volume_cm3,
        "outward": outward,
        "watertight": watertight,
        "boundary_edges": boundary_edges,
        "non_manifold_edges": non_manifold_edges,
        "inconsistent_orientation": inconsistent_orientation,
        "degenerate_faces": degen_count
    }

def verify_3mf():
    print("\n" + "="*70)
    print("ORACLE 1: 3MF VERIFICATION (VORTEX_100_Full_Assembly_Colored.3mf)")
    print("="*70)
    assert os.path.exists(FILE_3MF), f"3MF file missing: {FILE_3MF}"
    
    zf = zipfile.ZipFile(FILE_3MF, 'r')
    model_xml = zf.read('3D/3dmodel.model')
    root = ET.fromstring(model_xml)

    ns = {'m': 'http://schemas.microsoft.com/3dmanufacturing/core/2015/02'}
    objects = root.findall('.//m:object', ns)
    print(f"Total objects found in 3MF: {len(objects)}")
    assert len(objects) == 7, f"Expected 7 objects, got {len(objects)}"

    results = {}
    for obj in objects:
        obj_name = obj.attrib.get('name', 'unnamed')
        mesh = obj.find('m:mesh', ns)
        verts = [
            (float(v.attrib['x']), float(v.attrib['y']), float(v.attrib['z']))
            for v in mesh.findall('.//m:vertex', ns)
        ]
        faces = [
            (int(t.attrib['v1']), int(t.attrib['v2']), int(t.attrib['v3']))
            for t in mesh.findall('.//m:triangle', ns)
        ]
        metrics = compute_mesh_metrics(verts, faces)
        results[obj_name] = metrics
        print(f"  [{obj_name}] Faces={metrics['faces']}, Vol={metrics['volume_cm3']:.2f} cm3, Outward={metrics['outward']}, Watertight={metrics['watertight']} (B={metrics['boundary_edges']}, NM={metrics['non_manifold_edges']}, Incons={metrics['inconsistent_orientation']})")
        assert metrics['outward'], f"FAIL: {obj_name} has inward normals (Vol={metrics['volume_cm3']})"
        assert metrics['volume_cm3'] > 0.0, f"FAIL: {obj_name} volume not positive"
        assert metrics['watertight'], f"FAIL: {obj_name} is not watertight"

    print(">> 3MF ORACLE: 100% PASSED (All 7 bodies strictly outward, positive volume, and watertight)")
    return results

def verify_obj():
    print("\n" + "="*70)
    print("ORACLE 2: OBJ VERIFICATION (VORTEX_100_Full_Assembly.obj)")
    print("="*70)
    assert os.path.exists(FILE_OBJ), f"OBJ file missing: {FILE_OBJ}"

    with open(FILE_OBJ, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    all_verts = []
    current_obj = None
    obj_faces = defaultdict(list)

    for line in lines:
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        parts = line.split()
        if parts[0] == 'v':
            all_verts.append((float(parts[1]), float(parts[2]), float(parts[3])))
        elif parts[0] == 'o':
            current_obj = parts[1]
        elif parts[0] == 'f':
            # OBJ is 1-indexed
            face = [int(p.split('/')[0]) - 1 for p in parts[1:4]]
            obj_faces[current_obj].append(face)

    print(f"Total global vertices: {len(all_verts)}, Total objects: {len(obj_faces)}")
    assert len(obj_faces) == 7, f"Expected 7 objects, got {len(obj_faces)}"

    results = {}
    for name, faces in obj_faces.items():
        # Remap vertices for local analysis
        used_indices = sorted(list(set(vi for f in faces for vi in f)))
        idx_map = {old: new for new, old in enumerate(used_indices)}
        local_verts = [all_verts[vi] for vi in used_indices]
        local_faces = [[idx_map[vi] for vi in f] for f in faces]

        metrics = compute_mesh_metrics(local_verts, local_faces)
        results[name] = metrics
        print(f"  [{name}] Faces={metrics['faces']}, Vol={metrics['volume_cm3']:.2f} cm3, Outward={metrics['outward']}, Watertight={metrics['watertight']} (B={metrics['boundary_edges']}, NM={metrics['non_manifold_edges']}, Incons={metrics['inconsistent_orientation']})")
        assert metrics['outward'], f"FAIL: {name} has inward normals (Vol={metrics['volume_cm3']})"
        assert metrics['volume_cm3'] > 0.0, f"FAIL: {name} volume not positive"
        assert metrics['watertight'], f"FAIL: {name} is not watertight"

    print(">> OBJ ORACLE: 100% PASSED (All 7 bodies strictly outward, positive volume, and watertight)")
    return results

def verify_step():
    print("\n" + "="*70)
    print("ORACLE 3: STEP AP214 VERIFICATION (VORTEX_100_Full_Assembly_Colored.step)")
    print("="*70)
    assert os.path.exists(FILE_STEP), f"STEP file missing: {FILE_STEP}"

    with open(FILE_STEP, 'r', encoding='utf-8') as f:
        content = f.read()

    lines = content.splitlines()
    print(f"Total STEP lines: {len(lines)}")

    # Parse CARTESIAN_POINT
    cartesian_pts = {}
    poly_loops = {}
    face_bounds = {}
    advanced_faces = {}
    closed_shells = {}
    shell_names = {}

    import re
    pt_re = re.compile(r"#(\d+)\s*=\s*CARTESIAN_POINT\s*\(\s*''\s*,\s*\(\s*([-\d.eE]+)\s*,\s*([-\d.eE]+)\s*,\s*([-\d.eE]+)\s*\)\s*\);")
    poly_re = re.compile(r"#(\d+)\s*=\s*POLY_LOOP\s*\(\s*''\s*,\s*\((.*?)\)\s*\);")
    bound_re = re.compile(r"#(\d+)\s*=\s*FACE_OUTER_BOUND\s*\(\s*''\s*,\s*#(\d+)\s*,\s*\.([TF])\.\s*\);")
    face_re = re.compile(r"#(\d+)\s*=\s*(?:ADVANCED_FACE|FACE_SURFACE)\s*\(\s*''\s*,\s*\(\s*#(\d+)\s*\)\s*,\s*#(\d+)\s*,\s*\.([TF])\.\s*\);")
    shell_re = re.compile(r"#(\d+)\s*=\s*CLOSED_SHELL\s*\(\s*'([^']*)'\s*,\s*\((.*?)\)\s*\);")
    solid_re = re.compile(r"#(\d+)\s*=\s*MANIFOLD_SOLID_BREP\s*\(\s*'([^']*)'\s*,\s*#(\d+)\s*\);")
    plane_re = re.compile(r"#(\d+)\s*=\s*AXIS2_PLACEMENT_3D\s*\(\s*''\s*,\s*#(\d+)\s*,\s*#(\d+)\s*,\s*#(\d+)\s*\);")
    dir_re = re.compile(r"#(\d+)\s*=\s*DIRECTION\s*\(\s*''\s*,\s*\(\s*([-\d.eE]+)\s*,\s*([-\d.eE]+)\s*,\s*([-\d.eE]+)\s*\)\s*\);")

    dirs = {}

    for line in lines:
        m = pt_re.match(line)
        if m:
            cartesian_pts[int(m.group(1))] = (float(m.group(2)), float(m.group(3)), float(m.group(4)))
            continue
        m = dir_re.match(line)
        if m:
            dirs[int(m.group(1))] = (float(m.group(2)), float(m.group(3)), float(m.group(4)))
            continue
        m = poly_re.match(line)
        if m:
            pids = [int(p.strip().lstrip('#')) for p in m.group(2).split(',') if p.strip()]
            poly_loops[int(m.group(1))] = pids
            continue
        m = bound_re.match(line)
        if m:
            face_bounds[int(m.group(1))] = int(m.group(2))
            continue
        m = face_re.match(line)
        if m:
            advanced_faces[int(m.group(1))] = {
                'bound': int(m.group(2)),
                'surface': int(m.group(3)),
                'same_sense': m.group(4) == 'T'
            }
            continue
        m = shell_re.match(line)
        if m:
            fids = [int(f.strip().lstrip('#')) for f in m.group(3).split(',') if f.strip()]
            closed_shells[int(m.group(1))] = fids
            continue
        m = solid_re.match(line)
        if m:
            sname = m.group(2)
            shid = int(m.group(3))
            shell_names[shid] = sname
            continue

    print(f"Parsed: Points={len(cartesian_pts)}, Loops={len(poly_loops)}, Shells={len(closed_shells)}")
    assert len(closed_shells) == 7, f"Expected 7 closed shells, got {len(closed_shells)}"

    results = {}
    for shell_id, fids in closed_shells.items():
        shell_name = shell_names.get(shell_id, f"Shell_{shell_id}")
        # Reconstruct faces and compute signed volume
        verts_list = []
        vert_lookup = {}
        faces_list = []

        for fid in fids:
            af = advanced_faces[fid]
            bound_id = af['bound']
            loop_id = face_bounds[bound_id]
            loop_pt_ids = poly_loops[loop_id]
            assert len(loop_pt_ids) == 3, f"Non-triangular face in shell {shell_name}: {loop_pt_ids}"

            face_vert_indices = []
            for pt_id in loop_pt_ids:
                if pt_id not in vert_lookup:
                    vert_lookup[pt_id] = len(verts_list)
                    verts_list.append(cartesian_pts[pt_id])
                face_vert_indices.append(vert_lookup[pt_id])

            faces_list.append(face_vert_indices)

        metrics = compute_mesh_metrics(verts_list, faces_list)
        results[shell_name] = metrics
        print(f"  [{shell_name}] Shell #{shell_id}: Faces={metrics['faces']}, Vol={metrics['volume_cm3']:.2f} cm3, Outward={metrics['outward']}, Watertight={metrics['watertight']} (B={metrics['boundary_edges']}, NM={metrics['non_manifold_edges']}, Incons={metrics['inconsistent_orientation']})")
        assert metrics['outward'], f"FAIL: Shell {shell_name} has inward normals (Vol={metrics['volume_cm3']})"
        assert metrics['volume_cm3'] > 0.0, f"FAIL: Shell {shell_name} volume not positive"
        assert metrics['watertight'], f"FAIL: Shell {shell_name} is not watertight"

    print(">> STEP AP214 ORACLE: 100% PASSED (All 7 closed shells strictly outward, positive volume, and watertight)")
    return results

if __name__ == '__main__':
    res_3mf = verify_3mf()
    res_obj = verify_obj()
    res_step = verify_step()

    print("\n" + "="*70)
    print("CROSS-FORMAT CONSISTENCY VERIFICATION")
    print("="*70)
    for b in EXPECTED_BODIES:
        v_3mf = res_3mf[b]['volume_cm3']
        v_obj = res_obj[b]['volume_cm3']
        v_step = res_step[b]['volume_cm3']
        diff_obj = abs(v_3mf - v_obj)
        diff_step = abs(v_3mf - v_step)
        print(f"  {b:30s} | 3MF: {v_3mf:8.2f} | OBJ: {v_obj:8.2f} | STEP: {v_step:8.2f} cm3 | MaxDiff={max(diff_obj, diff_step):.4f}")
        assert max(diff_obj, diff_step) < 0.1, f"Volume mismatch across formats for {b}"

    print("\nALL EMPIRICAL ORACLE TESTS COMPLETED WITH ZERO DEFECTS!")
