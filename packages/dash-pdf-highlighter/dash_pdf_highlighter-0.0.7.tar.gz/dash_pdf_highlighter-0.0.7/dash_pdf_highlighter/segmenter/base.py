from .mongo import MongoDBConnection



def get_embedding(text, mg, model="text-embedding-ada-002"):
    """
    Get the embedding of a text using the OpenAI API.
    
    """
    import openai

    res = mg.embeddings.find_one({"text": text}) or {}

    if res:
        return res["embedding"]

    response = openai.embeddings.create(
        input=text,
        model=model,
    )

    embedding = response.data[0].embedding

    mg.embeddings.insert_one({"text": text, "embedding": embedding})

    return embedding
    


class BaseSegmenter:
    def __init__(self):
        pass

    def convert_coordinates_from_pymupdf_to_pdfjs(
        self, bbox, page_height, page_width, page_number=None
    ):
        self.file_mode = ""
        self.file_id = ""

        output = {
            "x1": bbox[0],
            "y1": bbox[1],
            "x2": bbox[2],
            "y2": bbox[3],
            "width": page_width,
            "height": page_height,
        }
        if page_number is not None:
            output["pageNumber"] = page_number
        return output

    def merge_pdfjs_bounding_boxes(self, bboxes):
        """Calculate the union of multiple bounding boxes."""
        x1 = min(box["x1"] for box in bboxes)
        y1 = min(box["y1"] for box in bboxes)
        x2 = max(box["x2"] for box in bboxes)
        y2 = max(box["y2"] for box in bboxes)
        return {
            "x1": x1,
            "y1": y1,
            "x2": x2,
            "y2": y2,
            "width": bboxes[0]["width"],
            "height": bboxes[0]["height"],
        }

    def merge_bounding_boxes(self, bboxes):
        """Calculate the union of multiple bounding boxes."""
        x1 = min(box[0] for box in bboxes)
        y1 = min(box[1] for box in bboxes)
        x2 = max(box[2] for box in bboxes)
        y2 = max(box[3] for box in bboxes)
        return (x1, y1, x2, y2)


    def generate_id(self, segment):
        import hashlib
        import uuid
        if "content" in segment:
            if "text" in segment["content"]:
                content_hash = hashlib.sha256(segment["content"]["text"].encode()).hexdigest()
            elif "image" in segment["content"]:
                content_hash = hashlib.sha256(segment["content"]["image"].encode()).hexdigest()
            else:
                content_hash = str(uuid.uuid4())
        else:
            content_hash = str(uuid.uuid4())
    
        return content_hash        

    def new_segment(
        self,
        bbox,
        page=None,
        text=None,
        image=None,
        comment=None,
        page_number=None,
        page_width=None,
        page_height=None,
        rects=None,
        id=None,
    ):

        if page_width is None:
            page_width = page.rect.width
        if page_height is None:
            page_height = page.rect.height
        if page_number is None:
            page_number = page.number

        if "x1" not in bbox:
            bounding_box = self.convert_coordinates_from_pymupdf_to_pdfjs(
                bbox, page_height, page_width, page_number + 1
            )
        else:
            bounding_box = bbox

        if rects is None:
            rects = [bounding_box]

        # check if rects is of the pdfjs format
        if "x1" not in rects[0]:
            rects = [
                self.convert_coordinates_from_pymupdf_to_pdfjs(
                    rect, page_height, page_width, page_number + 1
                )
                for rect in rects
            ]

        output = {
            "content": {},
            "position": {
                "boundingRect": bounding_box,
                "rects": rects,
                "pageNumber": page_number + 1,
            },
            "comment": {"text": "", "emoji": ""},
        }

        if text is not None:
            text = text.replace("<prd>", ".")
            output["content"]["text"] = text
        if image is not None:
            output["content"]["image"] = image
        if comment is not None:
            if isinstance(comment, str):
                output["comment"]["text"] = comment
            else:
                output["comment"] = comment

        if id is None:
            output["id"] = self.generate_id(output)
        else:
            output["id"] = id
        return output

    def combine_segments(self, sA, sB):
        # take the first image
        image = None
        if "image" in sA["content"]:
            image = sA["content"]["image"]
        elif "image" in sB["content"]:
            image = sB["content"]["image"]

        # combine the text if it exists
        text = None
        if "text" in sA["content"]:
            text = sA["content"]["text"]
        if "text" in sB["content"]:
            if text is None:
                text = sB["content"]["text"]
            else:
                text += " " + sB["content"]["text"]
                # remove double spaces
                text = text.replace("  ", " ")

        # combine the comments
        comment = None
        if "comment" in sA:
            comment = sA["comment"]
        if "comment" in sB:
            if comment is None:
                comment = sB["comment"]

        # combine the bounding boxes
        bounding_boxes = [
            sA["position"]["boundingRect"],
            sB["position"]["boundingRect"],
        ]
        bounding_box = self.merge_pdfjs_bounding_boxes(bounding_boxes)

        # combine the rects
        rects = sA["position"]["rects"] + sB["position"]["rects"]

        return self.new_segment(
            bounding_box,
            text=text,
            image=image,
            comment=comment,
            page_number=sA["position"]["pageNumber"] - 1,
            page_width=sA["position"]["boundingRect"]["width"],
            page_height=sA["position"]["boundingRect"]["height"],
            rects=rects
        )


    def get_embedding(self, text, model="text-embedding-ada-002"):
        """ Get the embedding of a text using the OpenAI API.
                """
        with MongoDBConnection() as mg:
            return get_embedding(text, mg, model)


    def run(self, doc, excluded_boxes=[]):
        import pymupdf as fitz
        import requests

        if isinstance(doc, fitz.Document):
            self.file_mode = "local"
            self.file_id = doc.name
            return self._run(doc, excluded_boxes)

        elif isinstance(doc, str):
            if doc.startswith("http"):
                res = requests.get(doc, stream=True)

                self.file_mode = "remote"
                self.file_id = doc

                if res.status_code != 200:
                    raise Exception(f"Failed to download the file from {doc}")

                fitz_doc = fitz.open(stream=res.content, filetype="pdf")
            else:
                fitz_doc = fitz.open(doc)

            return self._run(fitz_doc, excluded_boxes)

        raise NotImplementedError("Subclasses must implement this method.")
    

    def save_to_cache(self, segments):
        with MongoDBConnection() as mg:
            for segment in segments:
                segment["file_id"] = self.file_id
                segment["file_mode"] = self.file_mode
                mg.segments.insert_one(segment)


    def get_from_cache(self, embedding=False):
        with MongoDBConnection() as mg:
            res = mg.segments.find(
                {"file_id": self.file_id, "file_mode": self.file_mode},
                {"_id": 0, "file_id": 0, "file_mode": 0, "embedding": 1 if embedding else 0},
            )
            return list(res)
        
    def stripped_output(self, segments, debug=False):
        stripped_segments = []
        for segment in segments:

            position = {
                "boundingRect": segment["position"]["boundingRect"],
                "rects": [] if "image" in segment["content"] else segment["position"]["rects"],
                "pageNumber": segment["position"]["pageNumber"],
            }

            stripped_segment = {
                "content": segment["content"],
                "position": position,
                "comment": segment["comment"],
                "id": segment["id"],
            }
            if debug:
                stripped_segment["comment"]["text"] = f"""ID: {segment["id"]}

{segment["content"]["text"]}"""
            stripped_segments.append(stripped_segment)
        return stripped_segments