from pathlib import Path
import markdown
from xhtml2pdf import pisa

SRC = Path('docs/RAPPORT_TEMPLATE.md')
DST = Path('docs/RAPPORT_TEMPLATE.pdf')

CSS = '''
<style>
body { font-family: DejaVu Sans, Arial, Helvetica, sans-serif; font-size: 12pt; line-height: 1.5; margin: 24px; }
h1, h2, h3, h4, h5 { font-weight: bold; margin-top: 24px; margin-bottom: 12px; }
h1 { font-size: 24pt; }
h2 { font-size: 20pt; }
h3 { font-size: 16pt; }
p { margin: 6px 0; }
blockquote { margin: 12px 24px; padding-left: 12px; border-left: 4px solid #888; color: #444; }
pre, code { font-family: Consolas, Courier, monospace; background: #f6f6f6; padding: 4px; }
pre { white-space: pre-wrap; word-wrap: break-word; padding: 12px; margin: 8px 0; }
code { display: inline; }
ul, ol { margin: 6px 0 6px 24px; }
table { border-collapse: collapse; width: 100%; margin: 12px 0; }
th, td { border: 1px solid #666; padding: 6px 8px; }
th { background-color: #e7e7e7; }
hr { border: 0; border-top: 1px solid #ccc; margin: 20px 0; }
</style>
'''

if not SRC.exists():
    raise FileNotFoundError(f'Markdown source not found: {SRC}')

DST.parent.mkdir(parents=True, exist_ok=True)
text = SRC.read_text(encoding='utf-8')
html = markdown.markdown(text, extensions=['extra', 'tables', 'fenced_code', 'codehilite'])
html_full = f'<html><head><meta charset="utf-8">{CSS}</head><body>{html}</body></html>'
with DST.open('wb') as f:
    pisa_status = pisa.CreatePDF(html_full, dest=f)
if pisa_status.err:
    raise RuntimeError('PDF generation failed')
print('PDF generated:', DST.resolve())
