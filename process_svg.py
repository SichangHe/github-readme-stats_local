"""Validate and atomically publish a generated language-card SVG."""

from pathlib import Path
import sys
import xml.etree.ElementTree as ET


candidate_path = Path(sys.argv[1])
target_path = Path(sys.argv[2])
svg = candidate_path.read_text()

try:
    root = ET.fromstring(svg)
except ET.ParseError as error:
    raise SystemExit(f"Invalid SVG XML: {error}") from error

if root.tag != "{http://www.w3.org/2000/svg}svg":
    raise SystemExit("Response root is not an SVG element")
if not any(element.get("data-testid") == "lang-items" for element in root.iter()):
    raise SystemExit("Response is not a language card")
headers = [
    "".join(element.itertext()).strip()
    for element in root.iter()
    if element.get("data-testid") == "header"
]
if not any(
    header in {"Most Used Languages", "Most Owned Languages"} for header in headers
):
    raise SystemExit("Response does not have the expected language-card header")

_ = candidate_path.write_text(svg.replace("Most Used", "Most Owned"))
_ = candidate_path.replace(target_path)
