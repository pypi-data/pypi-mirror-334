from pathlib import Path
import simplejson as json
from docketanalyzer import load_docket_index
from docketanalyzer.ocr import pdf_document
import regex as re
import fitz


data_dir = Path('data')
doc_dir = data_dir / "docs"
anno_dir = data_dir / "annos"
doc_dir.mkdir(parents=True, exist_ok=True)
anno_dir.mkdir(parents=True, exist_ok=True)


def collect_data():
    index = load_docket_index()

    docket_ids = index.load_cached_ids(shuffle=True)
    docket_ids = docket_ids[:1000]
    for docket_id in docket_ids:
        manager = index[docket_id]
        for pdf_path in manager.pdf_paths:
            data, _ = manager.apply_ocr(pdf_path, overwrite=True, remote=True)
            out_path = doc_dir / f"{docket_id}__{pdf_path.stem}.json"
            out_path.write_text(json.dumps(data, indent=2))
            out_path.with_suffix('.pdf').write_bytes(pdf_path.read_bytes())


def has_pattern(text, pattern):
    return bool(re.search(pattern, text))


paths = list(sorted(doc_dir.glob("*.pdf")))
paths = list(sorted(doc_dir.glob("*.pdf")))
i = 5
#paths = paths[i:i+1]
#paths = [Path('data/docs/caed__1_17-cv-01479__doc.pdf.13_0.pdf')]

color_map = {
    "ignore": (1, 0, 0),
    "abandon": (0, 1, 1),
    "title": (0, 1, 0),
    "text": (0, 0, 1),
}
for path in paths[:25]:
    out_path = anno_dir / path.name
    doc = pdf_document(path, load=out_path.with_suffix('.json'))
    doc = pdf_document(path).process(batch_size=64).postprocess_court_doc()
    for page in doc:
        for block in reversed(page):
            color = color_map.get(block.block_type)
            if color:
                page.draw(
                    block.bbox,  fill=color, fill_opacity=0.2,
                )
    doc.doc.save(out_path)
    doc.save(out_path.with_suffix('.json'))
    doc.close()
    print(path)
