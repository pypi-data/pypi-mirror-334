from .base import BaseSegmenter

class FigureSegmenter(BaseSegmenter):
    def __init__(
        self,
        margin=15,
        overlap_margin=2,
        caption_margin=30,
        min_dimension=20,
        caption_keywords=["figure", "fig"],
        fig_scale=4,
    ):
        super().__init__()

        self.margin = margin
        self.caption_keywords = caption_keywords
        self.min_dimension = min_dimension
        self.fig_scale = fig_scale
        self.overlap_margin = overlap_margin
        self.caption_margin = caption_margin

    def get_image_segments(self, page, blocks):
        """Extract image segments from the page."""
        image_segments = []

        for block in blocks:
            if "image" in block:
                bbox = block["bbox"]
                image_segments.append(self.new_segment(bbox, page=page, image="png"))

        return image_segments

    def get_caption_segments(self, page, blocks):
        """Extract caption segments from the page."""
        caption_segments = []

        for block in blocks:
            if "lines" in block:

                combined_text = []
                block_bboxes = []
                for line in block["lines"]:
                    for span in line["spans"]:
                        combined_text.append(span["text"])
                        block_bboxes.append(span["bbox"])

                # Combine all text into a paragraph
                paragraph_text = " ".join(combined_text)

                bbox = self.merge_bounding_boxes(block_bboxes)

                if any(
                    [
                        paragraph_text[:15].lower().startswith(keyword)
                        for keyword in self.caption_keywords
                    ]
                ):
                    
                    caption_segments.append(
                        self.new_segment(bbox, page=page, text=paragraph_text)
                    )
                    

        return caption_segments

    def get_text_segments(self, page, blocks):
        """Extract text segments from the page."""
        text_segments = []

        for block in blocks:
            if "lines" in block:

                combined_text = []
                block_bboxes = []
                for line in block["lines"]:
                    for span in line["spans"]:
                        combined_text.append(span["text"])
                        block_bboxes.append(span["bbox"])

                # Combine all text into a paragraph
                paragraph_text = " ".join(combined_text)

                bbox = self.merge_bounding_boxes(block_bboxes)

                text_segments.append(
                    self.new_segment(bbox, page=page, text=paragraph_text)
                )

        return text_segments

    def get_shape_segments(self, page):
        """Extract shape segments from the page."""
        shapes = page.get_drawings()
        shape_segments = []

        for shape in shapes:
            bbox = shape["rect"]
            shape_segments.append(self.new_segment(bbox, page=page))

        return shape_segments

    def merge_segments(
        self, page, image_segments, caption_segments, shape_segments, text_segments
    ):
        """Try to combine image and caption segments into figure segments.

        This function tries to merge image and catption segments.
        Image segments are first combined with possible overlapping image and shape segments.
        If a caption is close to an image segment, they are combined also.
        """

        # first group image and shape segments
        graphical_segments = image_segments + shape_segments

        # order the graphical segments by size
        graphical_segments = sorted(
            graphical_segments,
            key=lambda x: (
                x["position"]["boundingRect"]["x2"]
                - x["position"]["boundingRect"]["x1"]
            )
            * (
                x["position"]["boundingRect"]["y2"]
                - x["position"]["boundingRect"]["y1"]
            ),
            reverse=True,
        )

        # condense the bounding boxes, by iterating over the graphical segments. If they overlap within
        # the margin, they are combined.
        found_overlap = True
        while found_overlap:
            found_overlap = False
            for i, segment in enumerate(graphical_segments):
                for j, other_segment in enumerate(graphical_segments):
                    if i != j:
                        bbox = segment["position"]["boundingRect"]
                        other_bbox = other_segment["position"]["boundingRect"]
                        if (
                            bbox["x1"] - self.margin < other_bbox["x2"]
                            and bbox["x2"] + self.margin > other_bbox["x1"]
                            and bbox["y1"] - self.margin < other_bbox["y2"]
                            and bbox["y2"] + self.margin > other_bbox["y1"]
                        ):
                            combined_segment = self.combine_segments(
                                segment, other_segment
                            )
                            graphical_segments[i] = combined_segment
                            graphical_segments.pop(j)
                            found_overlap = True
                            break
                if found_overlap:
                    break

        # remove segments that are too small
        def segment_bigh_enough(segment):
            bbox = segment["position"]["boundingRect"]
            delta_x = bbox["x2"] - bbox["x1"]
            delta_y = bbox["y2"] - bbox["y1"]
            return delta_x > self.min_dimension and delta_y > self.min_dimension

        graphical_segments = [
            segment for segment in graphical_segments if segment_bigh_enough(segment)
        ]

        # if there are text_segments that overlap with graphical segments, extend the bounding box
        for segment in graphical_segments:
            bbox = segment["position"]["boundingRect"]
            for text_segment in text_segments:
                text_bbox = text_segment["position"]["boundingRect"]
                if (
                    bbox["x1"] - self.overlap_margin < text_bbox["x2"]
                    and bbox["x2"] + self.overlap_margin > text_bbox["x1"]
                    and bbox["y1"] - self.overlap_margin < text_bbox["y2"]
                    and bbox["y2"] + self.overlap_margin > text_bbox["y1"]
                ):
                    combined_bbox = self.merge_pdfjs_bounding_boxes([bbox, text_bbox])
                    segment["position"]["boundingRect"] = combined_bbox
                    # add the text to the graphical segment
                    if "text" not in segment["content"]:
                        segment["content"]["text"] = text_segment["content"]["text"]
                    else:
                        segment["content"]["text"] += (
                            "\n" + text_segment["content"]["text"]
                        )

        # now try to combine the graphical segments with the caption segments
        closest_caption_segment_index = [None] * len(graphical_segments)
        for segment in graphical_segments:

            graphical_bbox = segment["position"]["boundingRect"]

            # find the closest graphical segment
            closest_segment = None
            closest_distance = float("inf")
            closest_index = None
            for i, caption_segment in enumerate(caption_segments):
                bbox = caption_segment["position"]["boundingRect"]
                # use a minimum distance of the caption margin
                distance = min(
                    min(
                        abs(bbox["x1"] - graphical_bbox["x2"]),
                        abs(bbox["x2"] - graphical_bbox["x1"]),
                    ),
                    min(
                        abs(bbox["y1"] - graphical_bbox["y2"]),
                        abs(bbox["y2"] - graphical_bbox["y1"]),
                    ),
                )
                if distance < closest_distance:
                    closest_distance = distance
                    closest_segment = caption_segment
                    closest_index = i

            # if a closest segment is found and it is close enough, combine the caption with the graphical segment
            if closest_segment is None:
                continue

            closest_caption_segment_index[graphical_segments.index(segment)] = (
                closest_index
            )

        # if there are graphical segments with same closest_caption_segment_index, combine them
        for i, segment in enumerate(graphical_segments):
            closest_index = closest_caption_segment_index[i]
            if closest_index is not None:
                # update the caption text accordingly
                if "text" not in segment["content"]:
                    segment["content"]["text"] = caption_segments[closest_index][
                        "content"
                    ]["text"]
                else:
                    segment["content"]["text"] = (
                        caption_segments[closest_index]["content"]["text"]
                        + "\n\n" + segment["content"]["text"]
                    )
                # add the rects
                if "rects" in caption_segments[closest_index]["position"]:
                    bbrect = caption_segments[closest_index]["position"]["boundingRect"]
                    bbrect["extra"] = "caption"
                    segment["position"]["rects"].append(bbrect)

                for j, other_segment in enumerate(graphical_segments):
                    if i != j and closest_caption_segment_index[j] == closest_index:
                        combined_segment = self.combine_segments(segment, other_segment)
                        graphical_segments[i] = combined_segment
                        graphical_segments.pop(j)
                        closest_caption_segment_index.pop(j)
                        break

        return graphical_segments

    def calculate_figure_segments(self, page, combined_segments):
        import pymupdf as fitz
        import base64

        def encode_image_to_base64(image_bytes):
            return base64.b64encode(image_bytes).decode("utf-8")

        def get_image_segment(segment):

            bbox = segment["position"]["boundingRect"]

            bbox = fitz.Rect(bbox["x1"], bbox["y1"], bbox["x2"], bbox["y2"])
            image = page.get_pixmap(
                matrix=fitz.Matrix(self.fig_scale, self.fig_scale), clip=bbox
            )

            # image is a Pixmap object, convert it to raw image bytes
            image_bytes = image.tobytes()

            # encode the image as base64
            image_base64 = encode_image_to_base64(image_bytes)

            segment["content"]["image"] = f"data:image/png;base64,{image_base64}"

            return segment

        return [get_image_segment(segment) for segment in combined_segments]

    def run_page(self, page):

        blocks = page.get_text("dict")["blocks"]

        image_segments = self.get_image_segments(page, blocks)
        caption_segments = self.get_caption_segments(page, blocks)
        shape_segments = self.get_shape_segments(page)
        text_segments = self.get_text_segments(page, blocks)

        combined_segments = self.merge_segments(
            page, image_segments, caption_segments, shape_segments, text_segments
        )
        figure_segments = self.calculate_figure_segments(page, combined_segments)

        return figure_segments

    def _run(self, doc, excluded_boxes):

        if len(excluded_boxes) > 0:
            raise NotImplementedError(
                "FigureSegmenter does not support excluded_boxes yet."
            )

        self.figure_segments = []

        for page in doc:
            self.figure_segments.extend(self.run_page(page))

        return self.figure_segments
