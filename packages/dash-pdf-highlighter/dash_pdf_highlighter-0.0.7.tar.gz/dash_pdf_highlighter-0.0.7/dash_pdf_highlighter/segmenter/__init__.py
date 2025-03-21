from .base import BaseSegmenter
from .figure import FigureSegmenter
from .semantic import SemanticSegmenter
from .sentence import SentenceSegmenter



class Segmenter(BaseSegmenter):

    def __init__(self,
                 chached=True,
                 calc_embedding=True,
                 max_char_joined_segments=1000,
                 max_joined_segments=50,
                 debug=False
                ):
        super().__init__()
        self.cached = chached
        self.use_embedding = calc_embedding
        self.debug = debug

        self.figure_segmenter = FigureSegmenter()
        self.sentence_segmenter = SemanticSegmenter(
            max_char_joined_segments=max_char_joined_segments,
            max_joined_segments=max_joined_segments
        )



    def _run(self, doc, excluded_boxes=[]):
        if self.cached:
            result = self.get_from_cache()
            if len(result) > 0:
                print("Returning from cache")
                return self.stripped_output(result, debug=self.debug)

        # run the figure segmenter
        self.figure_segments = self.figure_segmenter._run(doc, [])

        # run the sentence segmenter
        self.sentence_segments = self.sentence_segmenter._run(
            doc, excluded_boxes=[])

        output = self.figure_segments + self.sentence_segments



        if self.use_embedding:
            for segment in output:
                if "text" in segment["content"] and len(segment["content"]["text"]) > 2:
                    segment["embedding"] = self.get_embedding(
                        segment["content"]["text"]
                    )
            
        if self.cached:
            self.save_to_cache(output)

        
        return self.stripped_output(output, debug=self.debug)
    

def search_segments(text, filter={}, limit=10):
    from .mongo import MongoDBConnection
    from .base import get_embedding

    with MongoDBConnection() as mg:

        embedding = get_embedding(text, mg)


        return mg.vector_search(
            embedding,
            extra_filters=filter,
            limit=limit
        )