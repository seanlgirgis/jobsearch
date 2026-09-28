from pathlib import Path
import pdfplumber

out = Path(__file__).resolve().parents[1] / "resume_output"
for stem in (
    "Sean_Girgis_Part_Time_Consulting_Resume",
    "Sean_Girgis_Senior_Career_Resume",
):
    with pdfplumber.open(out / f"{stem}.pdf") as pdf:
        text = "\n\n".join((page.extract_text(x_tolerance=2, y_tolerance=3) or "") for page in pdf.pages)
    (out / f"{stem}.txt").write_text(text.strip() + "\n", encoding="utf-8")
