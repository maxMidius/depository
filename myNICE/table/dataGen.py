import pandas as pd
import os

def generate_multiline_xlsx(directory="sample_data"):

    os.makedirs(directory, exist_ok=True)

    # ---------- File 1: Plain multi-line ----------
    df_plain = pd.DataFrame([
        {
            "ID": 1,
            "Notes": "Line 1\nLine 2\nLine 3",
        },
        {
            "ID": 2,
            "Notes": "First line\nSecond line\nThird line\nFourth line",
        },
        {
            "ID": 3,
            "Notes": "Single line",
        },
    ])
    df_plain.to_excel(f"{directory}/multiline_plain.xlsx", index=False)

    # ---------- File 2: HTML multi-line ----------
    df_html = pd.DataFrame([
        {
            "ID": 1,
            "Description": "Line 1<br>Line 2<br>Line 3",
        },
        {
            "ID": 2,
            "Description": "<p>Paragraph A</p><p>Paragraph B</p>",
        },
        {
            "ID": 3,
            "Description": "<div style='color:blue'>Blue text line 1</div>"
                           "<div style='color:green'>Green text line 2</div>",
        },
    ])
    df_html.to_excel(f"{directory}/multiline_html.xlsx", index=False)

    print("Generated multi-line test XLSX files in:", directory)


# Run this once:
if __name__ == "__main__":
    generate_multiline_xlsx()

