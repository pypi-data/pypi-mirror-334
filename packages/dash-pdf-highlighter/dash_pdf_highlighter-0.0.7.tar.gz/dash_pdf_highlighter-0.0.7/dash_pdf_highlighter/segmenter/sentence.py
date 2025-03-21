from .base import BaseSegmenter

class SentenceSegmenter(BaseSegmenter):

    def __init__(self):
        super().__init__()

    def split_into_sentences(self, text):
        """Split into sentences using regex and keeps the sentence ending punctuation."""
        import regex as re

        # prevent splitting on decimal numbers
        text = re.sub(r"(\d)\.(\d)", r"\1<prd>\2", text)

        # fix i.e. and e.g. and etc.
        text = re.sub(r"e\.g\.", "e<prd>g<prd>", text)
        text = re.sub(r"i\.e\.", "i<prd>e<prd>", text)
        text = re.sub(r"etc\.", "etc<prd>", text)
        text = re.sub(r"vs\.", "vs<prd>", text)
        text = re.sub(r"et al\.", "et al<prd>", text)

        # if we get a name like "V. Krueckl" we don't want to split it
        text = re.sub(r"([A-Z])\.", r"\1<prd>", text)

        # special abbreviations: Fig and Eq etc e.g.
        special = [
            "Fig",
            "Eq",
            "Dr",
            "Mr",
            "Ms",
            "Mrs",
            "Prof",
            "St",
            "Ave",
            "Inc",
            "Ltd",
            "Jr",
            "Sr",
            "Co",
            "Corp",
            "Dept",
            "Univ",
            "Assn",
            "Apt",
            "Blvd",
            "Cie",
            "Cir",
            "Col",
            "Dist",
            "Fed",
            "Ft",
            "Hwy",
            "Ln",
            "Mt",
            "Op",
            "Pl",
            "Rd",
            "Sq",
            "St",
            "Tce",
            "Ter",
            "Univ",
            "Apt",
            "Dept",
            "Est",
            "Figs",
            "Eqs",
            "Dr",
            "Mr",
            "Ms",
            "Mrs",
            "Prof",
            "St",
            "Ave",
            "Inc",
            "Ltd",
            "Jr",
            "Sr",
            "Co",
            "Corp",
            "Dept",
            "Univ",
            "Assn",
            "Apt",
            "Blvd",
            "Cie",
            "Cir",
            "Col",
            "Dist",
            "Fed",
            "Ft",
            "Hwy",
            "Ln",
            "Mt",
            "Op",
            "Pl",
            "Rd",
            "Sq",
            "St",
            "Tce",
            "Ter",
            "Univ",
            "Apt",
            "Dept",
            "Est",
            "Figs",
            "Eqs",
        ]
        for el in special:
            text = re.sub(r"\b" + el + r"\.", el + "<prd>", text)

        # remove trailing whitespace and also special whitespace characters
        text = re.sub(r"\s+", " ", text.strip())

        sentence_endings = re.findall(r"[^\.!\?]+[\.!\?]*", text)
        if len(sentence_endings) == 0:
            output = [text]
        else:
            output = sentence_endings

        return output

    def ends_with_sentence_ending(self, text):
        import regex as re

        return re.match(r".*[\.\?\!]\s*$", text)
    
    def transform_special_ligature_characters(self, text):
        import unicodedata
        import re

        # replace ligature characters
        text = unicodedata.normalize("NFKD", text)
        text = re.sub(r"ﬁ", "fi", text)
        text = re.sub(r"ﬂ", "fl", text)
        text = re.sub(r"ﬀ", "ff", text)
        text = re.sub(r"ﬃ", "ffi", text)
        text = re.sub(r"ﬄ", "ffl", text)
        text = re.sub(r"ﬅ", "ft", text)
        text = re.sub(r"ﬆ", "st", text)
        
        return text
    
    def is_in_excluded_box(self, span, excluded_boxes, page_number):
        # check if the line is in an excluded box
        # excluded_boxes is in the pdfjs format
        # span uses the pymupdf format

        bbox = span["bbox"]

        for excluded_box in excluded_boxes:
            if (
                bbox[0] >= excluded_box["x1"]
                and bbox[1] <= excluded_box["x2"]
                and bbox[2] >= excluded_box["y1"]
                and bbox[3] <= excluded_box["y2"]
                and "pageNumber" in excluded_box
                and page_number == excluded_box["pageNumber"] - 1
            ):
                return True
            
        return False

    def _run(self, doc, excluded_boxes):


        sentences = []

        current_text = ""
        current_bboxes = []

        for page in doc:
            blocks = page.get_text("dict")["blocks"]

            for block in blocks:
                if "lines" in block:
                    for line in block["lines"]:
                        for span in line["spans"]:

                            # skip if the line is in an excluded box
                            if self.is_in_excluded_box(span, excluded_boxes, page.number):
                                continue

                            # get the text and apply some transformations
                            raw_text = span["text"]
                            text = self.transform_special_ligature_characters(raw_text)
                            splits = self.split_into_sentences(text)

                            # handle empty text
                            if current_text == "" or current_text == " ":
                                current_text = ""
                                current_bboxes = []

                            # loop over the splits
                            for chunk in splits:

                                if len(current_text) > 0:
                                    if current_text[-1] in ["-", "–", "—"]:
                                        current_text = current_text[:-1]
                                    else:
                                        current_text += " "
                                current_text += chunk
                                num_chunk_words = len(current_text.split())
                                current_bboxes.append(span["bbox"])

                                if (
                                    self.ends_with_sentence_ending(chunk)
                                    and len(current_text) > 6
                                    and num_chunk_words > 2
                                ):

                                    bbox = self.merge_bounding_boxes(current_bboxes)
                                    sentences.append(
                                        self.new_segment(
                                            bbox,
                                            page=page,
                                            text=current_text,
                                            rects=current_bboxes,
                                        )
                                    )
                                    current_text = ""
                                    current_bboxes = []

        return sentences
