import PyPDF2
import re

class PDFSentenceExtractor:
    def __init__(self, pdf_name:str):
        self.pdf_name = pdf_name
        
    def extractor(self, start_page=1, end_page=15):
        sentences = list()
        abbreviations = ["Mr.", "Mrs.", "Ms.", "Dr.", "Jr.", "Sr.", "No.", "Fig.", "Eq.", "Ref.", "et al."]
        with open(self.pdf_name, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page_num in range(start_page-1, end_page):
                if page_num > len(reader.pages):
                    break
                page = reader.pages[page_num]
                text = page.extract_text()
                if text:
                    text = text.replace("\n"," ")
                    text = re.sub(r'^\s*\d+\s*', '', text)
                for abbr in abbreviations:
                    safe_abbr = abbr.replace(".", "<DOT>")
                    text = text.replace(abbr, safe_abbr)
                pattern = r'\.(?=\s+[A-Z])'
                parts = re.split(pattern, text)
                for sentence in parts:
                    sentence = sentence.replace("<DOT>", ".").strip()
                    if sentence:
                      sentences.append(sentence)
        return sentences
            