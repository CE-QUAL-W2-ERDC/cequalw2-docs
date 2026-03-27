#!/usr/bin/env python3
"""
PSU Manual Differencing Tool

Extracts text from PSU CE-QUAL-W2 manual PDFs and generates a structured
diff report to identify changes between versions.

Usage:
    python diff_psu_manuals.py old_manual.pdf new_manual.pdf [--output report.md]

Requirements:
    pip install pymupdf
"""

import argparse
import difflib
import re
import sys
from pathlib import Path

try:
    import fitz  # PyMuPDF
except ImportError:
    print("Error: PyMuPDF is required. Install with: pip install pymupdf")
    sys.exit(1)


def extract_text_by_page(pdf_path: str) -> list[dict]:
    """Extract text from each page of a PDF, with page numbers."""
    doc = fitz.open(pdf_path)
    pages = []
    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text("text")
        pages.append({
            "page": page_num + 1,
            "text": text.strip(),
        })
    doc.close()
    return pages


def extract_full_text(pdf_path: str) -> str:
    """Extract all text from a PDF as a single string."""
    pages = extract_text_by_page(pdf_path)
    return "\n\n".join(
        f"--- PAGE {p['page']} ---\n{p['text']}" for p in pages
    )


def normalize_text(text: str) -> list[str]:
    """Normalize text for comparison: collapse whitespace, split into lines."""
    # Collapse multiple spaces and normalize line endings
    text = re.sub(r'[ \t]+', ' ', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    lines = text.splitlines()
    # Strip each line and remove empty lines
    lines = [line.strip() for line in lines if line.strip()]
    return lines


def compute_diff(old_lines: list[str], new_lines: list[str]) -> list[str]:
    """Compute a unified diff between old and new text."""
    diff = difflib.unified_diff(
        old_lines,
        new_lines,
        fromfile="Previous PSU Manual",
        tofile="New PSU Manual",
        lineterm="",
        n=3,  # Context lines
    )
    return list(diff)


def classify_change(change_block: str) -> str:
    """Heuristically classify a change block."""
    lower = change_block.lower()
    if any(w in lower for w in ["equation", "=", "coefficient", "formula"]):
        return "equation_or_parameter"
    elif any(w in lower for w in ["figure", "fig.", "table"]):
        return "figure_or_table"
    elif any(w in lower for w in ["new", "added", "additional", "feature"]):
        return "new_content"
    elif len(change_block) < 50:
        return "minor_edit"
    else:
        return "text_revision"


def generate_report(
    diff_lines: list[str],
    old_path: str,
    new_path: str,
) -> str:
    """Generate a Markdown report from the diff output."""
    report = []
    report.append("# PSU Manual Change Report")
    report.append("")
    report.append(f"- **Previous version:** `{Path(old_path).name}`")
    report.append(f"- **New version:** `{Path(new_path).name}`")
    report.append("")

    if not diff_lines:
        report.append("No differences detected.")
        return "\n".join(report)

    # Count changes
    additions = sum(1 for l in diff_lines if l.startswith("+") and not l.startswith("+++"))
    deletions = sum(1 for l in diff_lines if l.startswith("-") and not l.startswith("---"))

    report.append("## Summary")
    report.append("")
    report.append(f"- Lines added: {additions}")
    report.append(f"- Lines removed: {deletions}")
    report.append("")

    report.append("## Detailed Changes")
    report.append("")
    report.append("```diff")
    for line in diff_lines:
        report.append(line)
    report.append("```")
    report.append("")

    # Extract change blocks for triage
    report.append("## Change Triage")
    report.append("")
    report.append(
        "Review each change below and create GitHub issues for "
        "substantive updates that should be incorporated into the "
        "ERDC documentation."
    )
    report.append("")

    # Group hunks
    current_hunk = []
    hunk_num = 0
    for line in diff_lines:
        if line.startswith("@@"):
            if current_hunk:
                hunk_num += 1
                block_text = "\n".join(current_hunk)
                category = classify_change(block_text)
                report.append(f"### Change {hunk_num} ({category})")
                report.append("")
                report.append("```diff")
                for hl in current_hunk[-10:]:  # Limit output per hunk
                    report.append(hl)
                report.append("```")
                report.append("")
                report.append(f"- [ ] Reviewed")
                report.append(f"- [ ] Issue created")
                report.append("")
            current_hunk = [line]
        else:
            current_hunk.append(line)

    # Last hunk
    if current_hunk:
        hunk_num += 1
        block_text = "\n".join(current_hunk)
        category = classify_change(block_text)
        report.append(f"### Change {hunk_num} ({category})")
        report.append("")
        report.append("```diff")
        for hl in current_hunk[-10:]:
            report.append(hl)
        report.append("```")
        report.append("")
        report.append(f"- [ ] Reviewed")
        report.append(f"- [ ] Issue created")
        report.append("")

    return "\n".join(report)


def save_extracted_text(pdf_path: str, output_dir: Path) -> Path:
    """Extract and save text from a PDF for version tracking."""
    text = extract_full_text(pdf_path)
    stem = Path(pdf_path).stem
    output_path = output_dir / f"{stem}.txt"
    output_path.write_text(text, encoding="utf-8")
    print(f"Extracted text saved to: {output_path}")
    return output_path


def main():
    parser = argparse.ArgumentParser(
        description="Compare two versions of the PSU CE-QUAL-W2 manual PDF."
    )
    parser.add_argument("old_pdf", help="Path to the previous PSU manual PDF")
    parser.add_argument("new_pdf", help="Path to the new PSU manual PDF")
    parser.add_argument(
        "--output", "-o",
        default="psu_manual_changes.md",
        help="Output report path (default: psu_manual_changes.md)",
    )
    parser.add_argument(
        "--save-text",
        action="store_true",
        help="Save extracted text files for version control",
    )
    parser.add_argument(
        "--text-dir",
        default="psu-manual-tracking",
        help="Directory for extracted text files (default: psu-manual-tracking/)",
    )
    args = parser.parse_args()

    # Validate inputs
    for pdf in [args.old_pdf, args.new_pdf]:
        if not Path(pdf).exists():
            print(f"Error: File not found: {pdf}")
            sys.exit(1)

    print(f"Extracting text from: {args.old_pdf}")
    old_text = extract_full_text(args.old_pdf)
    old_lines = normalize_text(old_text)

    print(f"Extracting text from: {args.new_pdf}")
    new_text = extract_full_text(args.new_pdf)
    new_lines = normalize_text(new_text)

    print("Computing differences...")
    diff_lines = compute_diff(old_lines, new_lines)

    print("Generating report...")
    report = generate_report(diff_lines, args.old_pdf, args.new_pdf)

    output_path = Path(args.output)
    output_path.write_text(report, encoding="utf-8")
    print(f"Report saved to: {output_path}")

    if args.save_text:
        text_dir = Path(args.text_dir)
        text_dir.mkdir(parents=True, exist_ok=True)
        save_extracted_text(args.old_pdf, text_dir)
        save_extracted_text(args.new_pdf, text_dir)

    # Print summary
    additions = sum(1 for l in diff_lines if l.startswith("+") and not l.startswith("+++"))
    deletions = sum(1 for l in diff_lines if l.startswith("-") and not l.startswith("---"))
    print(f"\nSummary: {additions} lines added, {deletions} lines removed")


if __name__ == "__main__":
    main()
