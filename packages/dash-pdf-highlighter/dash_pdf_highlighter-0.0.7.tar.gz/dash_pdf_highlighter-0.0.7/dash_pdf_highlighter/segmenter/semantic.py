from .base import BaseSegmenter
from .sentence import SentenceSegmenter
from .mongo import MongoDBConnection


class SemanticSegmenter(BaseSegmenter):
    def __init__(self, max_char_joined_segments=1000, max_joined_segments=50):
        super().__init__()

        self.sentence_segmenter = SentenceSegmenter()
        self.max_char_joined_segments = max_char_joined_segments
        self.max_joined_segments = max_joined_segments

    def get_similarity_matrix(self, segments):
        import numpy as np

        max_length = self.max_char_joined_segments
        band = self.max_joined_segments

        similarity_matrix = np.zeros((len(segments), len(segments)))

        embedding_vectors = [np.array(el["embedding"]) for el in segments]

        segment_lengths = [len(el["content"]["text"]) for el in segments]

        for i in range(len(segments)):
            similarity_matrix[i][i] = 1.0
            for j in range(i+1, min(len(segments), i+band)):
                length_sum = np.sum(segment_lengths[i:j+1])

                if length_sum > max_length:
                    break

                similarity = np.dot(embedding_vectors[i], embedding_vectors[j]) / (
                    np.linalg.norm(embedding_vectors[i]) * np.linalg.norm(embedding_vectors[j]))
                similarity_matrix[i][j] = similarity
                similarity_matrix[j][i] = similarity

        return similarity_matrix

    def find_best_segmentation(self, similarity):
        import numpy as np

        if isinstance(similarity, list):
            similarity = np.array(similarity)

        # neglect non calculated values
        similarity[similarity == 0] = np.nan

        # calculate the running median of the similarity matrix on a 20x20 window
        def running_quantile(data, window_size=40, quantile=0.4):
            data = np.array(data)
            data = np.pad(data, (window_size//2, window_size//2),
                          mode='constant', constant_values=np.nan)
            data = np.array([np.nanquantile(data[i-window_size//2:i+window_size//2+1], quantile)
                            for i in range(window_size//2, len(data)-window_size//2)])
            return data
        median_similiarty = running_quantile(similarity)

        # use the median as a threshold for possible grouping
        matching_similarity = similarity > median_similiarty

        # find maximale blocks
        def find_max_blocks(matching_similarity, window_size=50):
            blocks = []
            for i in range(len(matching_similarity)):
                for j in range(i, len(matching_similarity)):
                    if any(~matching_similarity[i:j, i:j].flatten()):
                        blocks.append(j-i-1)
                        break

            blocks.append(1)
            blocks.append(1)

            return blocks
        blocks = find_max_blocks(matching_similarity)

        # generate the first join recipy with maximal sized blocks
        to_join = []

        while max(blocks) > 0:
            current_max = max(blocks)

            # find all matching indices
            idx = [i for i, el in enumerate(blocks) if el == current_max]

            # add the matching indices to the to_join array
            to_join.extend([list(range(el, el+current_max)) for el in idx])

            # make a set of the indices in to join
            found_indices = set(
                [item for sublist in to_join for item in sublist])

            # set the values in the blocks array to 0 for the indices in the to_join array
            for i in found_indices:
                blocks[i] = 0

        # sort the to_join array by the first element of each sublist
        to_join = sorted(to_join, key=lambda x: x[0])


        # some indices might apprear multiple times, we create a clever algorithm to remove them :D
        def remove_duplicate_indices(to_join):

            to_join = sorted(to_join, key=lambda x: x[0])

            # get a list of the indices that is found multiple times
            to_join_flat = [item for sublist in to_join for item in sublist]
            mutliple_indices = list(set([item for item in to_join_flat if to_join_flat.count(item) > 1]))

            # group the multiple indices in groups with consecutive indices
            multiple_groups = []
            for i in mutliple_indices:
                if not multiple_groups:
                    multiple_groups.append([i])
                else:
                    if i == multiple_groups[-1][-1] + 1:
                        multiple_groups[-1].append(i)
                    else:
                        multiple_groups.append([i])    

            found_elements_to_remove = False

            for el in multiple_groups:
                num_indices = len(el)
                lower_indices = el[0:num_indices//2]
                upper_indices = el[num_indices//2:]     

                if len(lower_indices) > 0:
                    # searchin the to_join array if a group starts with lower_indices, if yes, remove them
                    for i in range(len(to_join)):
                        if len(to_join[i]) < len(lower_indices):
                            continue

                        if to_join[i][0] == lower_indices[0]:
                            to_join[i] = to_join[i][len(lower_indices):]
                            found_elements_to_remove = True

                            

                if len(upper_indices) > 0:
                    # searchin the to_join array if a group ends with upper_indices, if yes, remove them
                    for i in range(len(to_join)):
                        if len(to_join[i]) < len(upper_indices):
                            continue

                        if to_join[i][-1] == upper_indices[-1]:
                            to_join[i] = to_join[i][:-len(upper_indices)]
                            found_elements_to_remove = True

            # remove empty lists
            to_join = [el for el in to_join if el]

            return to_join, found_elements_to_remove
        
        found_duplicates = True
        while found_duplicates:
            to_join, found_duplicates = remove_duplicate_indices(to_join)


        # add back indices that are not in the to_join array
        flat_to_join = [item for sublist in to_join for item in sublist]
        for i in range(len(similarity)):
            if i not in flat_to_join:
                to_join.append([i])

        return to_join


    def _run(self, doc, excluded_boxes):
        import numpy as np
        import json

        self.sentence_segments = self.sentence_segmenter._run(doc, excluded_boxes)

        # use embedding model to calculate for each sentence a vector
        for segment in self.sentence_segments:
            segment["embedding"] = self.get_embedding(
                segment["content"]["text"])

        # calculate a similarity matrix between all sentences
        similarity_matrix = self.get_similarity_matrix(self.sentence_segments)
        
        # find the best segmentation
        to_join = self.find_best_segmentation(similarity_matrix)

        # check if the to_join array can be right
        # 1. no duplicates:
        flat_to_join = [item for sublist in to_join for item in sublist]
        assert len(flat_to_join) == len(set(flat_to_join)), "Duplicates found in to_join array"

        # 2. all indices are in the range of the sentence_segments
        assert len(flat_to_join) == len(self.sentence_segments), "Not all indices are in the range of the sentence_segments"
        
        segments = []

        for join in to_join:
            if len(join) == 1:
                segments.append(self.sentence_segments[join[0]])
            else:
                new_segment = self.sentence_segments[join[0]]
                for idx in join[1:]:
                    new_segment = self.combine_segments(
                        new_segment, self.sentence_segments[idx]
                    )
                segments.append(new_segment)

        return segments
                    