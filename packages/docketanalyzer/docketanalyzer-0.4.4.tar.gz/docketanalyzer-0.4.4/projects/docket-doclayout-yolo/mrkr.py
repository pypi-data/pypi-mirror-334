from pathlib import Path
from PIL import Image
from surya.recognition import RecognitionPredictor
from surya.detection import DetectionPredictor
from docketanalyzer_ocr import pdf_document


def fitz_page_to_pil_image(page):
    """Converts a fitz.Page object to a PIL Image object."""
    pix = page.get_pixmap()
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    return img


data_dir = Path('data/docs')
path = data_dir / 'ared__2_16-cv-00080__doc.pdf.17_0.pdf'
example_path = Path('data/example/doc.pdf')
example_path.write_bytes(path.read_bytes())
doc = pdf_document(path)

if 1:
    img = fitz_page_to_pil_image(doc[0].fitz)
    recognition_predictor = RecognitionPredictor()
    detection_predictor = DetectionPredictor()

    predictions = recognition_predictor([img], [["en"]], detection_predictor)[0]
    for line in predictions.text_lines:
        pass#print(line.text)

    recognition_predictor = RecognitionPredictor()
    detection_predictor = DetectionPredictor()

    predictions = recognition_predictor([img], [["en"]], detection_predictor)[0]
    for line in predictions.text_lines:
        pass#print(line.text)
