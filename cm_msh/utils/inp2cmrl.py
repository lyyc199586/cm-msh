"""
inp2cmrl.py

This script provides functionality to convert ABAQUS .inp files into CMRL input format.
It parses the .inp file to extract nodes, elements, node sets, and element sets, and writes
them into separate files in the required format for CMRL.

Author: Yangyuanchen Liu
Date: 2025-05-19

Functions:
    parse_data_file: Parses the .inp file and extracts relevant data.
    inp2cmrl: Converts the .inp file into CMRL input format and writes output files.
    _find_duplicates: Checks for duplicate IDs in a given list and logs warnings.
    _write_coordinates_nodal: Writes node coordinates to a file.
    _write_connectivities_elements: Writes element connectivity data to a file.
    _write_set_nodes: Writes node set data to a file.
    _write_set_elements: Writes element set data to a file.
"""

from pathlib import Path
import re
from collections import Counter
from typing import List, Tuple, Dict


def parse_data_file(filename: Path) -> Tuple[
    List[Tuple[int, float, float, float]],
    List[Tuple[int, int, int, int, int]],
    Dict[str, Dict[str, List[int]]],
    Dict[str, Dict[str, List[int]]],
    int
]:
    """
    Parses an ABAQUS .inp file to extract nodes, elements, node sets, and element sets.

    Args:
        filename (Path): Path to the .inp file.

    Returns:
        Tuple: A tuple containing:
            - List of nodes as tuples (node_id, x, y, z).
            - List of elements as tuples (element_id, node1, node2, node3, node4).
            - Dictionary of node sets with set names as keys and node data as values.
            - Dictionary of element sets with set names as keys and element data as values.
            - Minimum element ID.
    """
    nodes = []
    elements = []
    Allelement_ID = []
    node_sets = {}
    element_sets = {}

    with open(filename, 'r') as file:
        lines = file.readlines()

    current_set = None
    is_generate = False
    reading_nodes = False
    reading_elements = False
    reading_node_set = False
    reading_element_set = False

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Section control
        if line.startswith("*NODE"):
            current_set = None
            is_generate = False
            reading_nodes = True
            reading_elements = reading_node_set = reading_element_set = False
            continue

        elif line.startswith("*ELEMENT, type=C3D4"):
            current_set = None
            is_generate = False
            reading_elements = True
            reading_nodes = reading_node_set = reading_element_set = False
            continue

        elif line.startswith("*NSET"):
            current_set = line.split("NSET=")[1].split(",")[0]
            is_generate = "generate" in line.lower()
            reading_node_set = True
            reading_nodes = reading_elements = reading_element_set = False
            node_sets[current_set] = {"nodes": [], "generate": is_generate}
            continue

        elif line.startswith("*ELSET"):
            current_set = line.split("ELSET=")[1].split(",")[0]
            if re.match(r"^Vol_\w+", current_set):
                is_generate = "generate" in line.lower()
                reading_element_set = True
                reading_nodes = reading_elements = reading_node_set = False
                element_sets[current_set] = {"elements": [], "generate": is_generate}
            continue

        elif line.startswith("*"):
            reading_nodes = reading_elements = reading_node_set = reading_element_set = False
            current_set = None
            is_generate = False
            continue

        # Actual content reading
        if reading_nodes:
            parts = line.split(",")
            if len(parts) == 4:
                try:
                    node_id = int(parts[0].strip())
                    x, y, z = map(float, parts[1:])
                    nodes.append((node_id, x, y, z))
                except ValueError:
                    continue

        elif reading_elements:
            parts = line.split(",")
            if len(parts) == 5:
                try:
                    element_id = int(parts[0].strip())
                    node_ids = list(map(int, parts[1:]))
                    elements.append((element_id, *node_ids))
                    Allelement_ID.append(element_id)
                except ValueError:
                    continue

        elif reading_node_set and current_set in node_sets:
            parts = [p.strip() for p in line.split(",") if p.strip()]
            if parts:
                try:
                    node_sets[current_set]["nodes"].extend(map(int, parts))
                except ValueError:
                    continue

        elif reading_element_set and current_set in element_sets:
            parts = [p.strip() for p in line.split(",") if p.strip()]
            if parts:
                try:
                    element_sets[current_set]["elements"].extend(map(int, parts))
                except ValueError:
                    continue

    # Summary and check
    min_element_id = min(Allelement_ID)
    _find_duplicates(Allelement_ID, "element connectivities")
    return nodes, elements, node_sets, element_sets, min_element_id


def _find_duplicates(ids: List[int], context: str) -> None:
    """
    Checks for duplicate IDs in a given list and logs warnings.

    Args:
        ids (List[int]): List of IDs to check for duplicates.
        context (str): Contextual description of the IDs being checked.
    """
    counter = Counter(ids)
    duplicates = {k: v for k, v in counter.items() if v > 1}
    if duplicates:
        print(f"[WARNING] Duplicates found in {context}: {duplicates}")
    else:
        print(f"[OK] No duplicates in {context}.")


def _write_coordinates_nodal(nodes: List[Tuple[int, float, float, float]], path: Path) -> None:
    """
    Writes node coordinates to a file.

    Args:
        nodes (List[Tuple[int, float, float, float]]): List of nodes with coordinates.
        path (Path): Path to the output file.
    """
    with open(path, "w") as f:
        f.write(f"{len(nodes)}\n")
        for node_id, x, y, z in nodes:
            f.write(f"  {node_id} {x} {y} {z}\n")


def _write_connectivities_elements(elements: List[Tuple[int, int, int, int, int]], min_id: int, path: Path) -> None:
    """
    Writes element connectivity data to a file.

    Args:
        elements (List[Tuple[int, int, int, int, int]]): List of elements with connectivity data.
        min_id (int): Minimum element ID for ID shifting.
        path (Path): Path to the output file.
    """
    with open(path, "w") as f:
        f.write(f"{len(elements)} Tet4\n")
        for eid, n1, n2, n3, n4 in elements:
            shifted_id = eid - min_id + 1
            f.write(f"  {shifted_id} {n1} {n2} {n3} {n4}\n")


def _write_set_nodes(node_sets: Dict[str, Dict[str, List[int]]], path: Path) -> None:
    """
    Writes node set data to a file.

    Args:
        node_sets (Dict[str, Dict[str, List[int]]]): Dictionary of node sets.
        path (Path): Path to the output file.
    """
    with open(path, "w") as f:
        f.write(f"{len(node_sets)}\n")
        for i, (name, data) in enumerate(node_sets.items(), start=1):
            nodes = data["nodes"]
            if data["generate"]:
                first, last, step = nodes[0], nodes[1], nodes[2]
                f.write(f"{i} {name} incremental\n")
                f.write(f"   {first} {last} {step}\n")
            else:
                f.write(f"{i} {name} explicit\n")
                f.write(f"{len(nodes)} ")
                for j in range(0, len(nodes), 16):
                    f.write("     " + "\t".join(map(str, nodes[j:j + 16])) + "\n")


def _write_set_elements(element_sets: Dict[str, Dict[str, List[int]]], min_id: int, path: Path) -> None:
    """
    Writes element set data to a file.

    Args:
        element_sets (Dict[str, Dict[str, List[int]]]): Dictionary of element sets.
        min_id (int): Minimum element ID for ID shifting.
        path (Path): Path to the output file.
    """
    with open(path, "w") as f:
        f.write(f"{len(element_sets)}\n")
        for i, (name, data) in enumerate(element_sets.items(), start=1):
            elems = [eid - min_id + 1 for eid in data["elements"]]
            _find_duplicates(elems, f"element set {name}")
            if data["generate"]:
                first, last, step = elems[0], elems[1], elems[2]
                f.write(f"{i} {name} incremental\n")
                f.write(f"   {first} {last} {step}\n")
            else:
                f.write(f"{i} {name} explicit\n")
                f.write(f"   {len(elems)} ")
                for j in range(0, len(elems), 16):
                    f.write("     " + "\t".join(map(str, elems[j:j + 16])) + "\n")


def inp2cmrl(input_path: Path, output_dir: Path) -> None:
    """
    Converts an ABAQUS .inp file to CMRL input format and writes output files.

    Args:
        input_path (Path): Path to the .inp file.
        output_dir (Path): Directory to write output files.
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    nodes, elements, node_sets, element_sets, min_id = parse_data_file(input_path)

    _write_coordinates_nodal(nodes, output_dir / "coordinatesNodal.inp")
    _write_connectivities_elements(elements, min_id, output_dir / "connectivitiesElement.inp")
    _write_set_nodes(node_sets, output_dir / "setsNode.inp")
    _write_set_elements(element_sets, min_id, output_dir / "setsElement.inp")

    print(f"[DONE] Conversion complete. Files written to: {output_dir}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Convert ABAQUS .inp to CMRL input format.")
    parser.add_argument("input", type=Path, help="Path to the ABAQUS .inp file")
    parser.add_argument("output", type=Path, help="Output directory for CMRL files")

    args = parser.parse_args()
    inp2cmrl(args.input, args.output)

