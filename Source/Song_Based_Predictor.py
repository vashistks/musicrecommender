import math
#This is the item based predictor program
class SongBasedPredictor:
    def __init__(self,song_user_map, alpha = 0.5,similarity_measure=0,q=2):
        """:arg
                song_user_map       - Represents the song_to_user index map
                alpha               - determines the weight that needs to be given while calculating the similarity measure
                similarity_measure  - 0 represents cosine similarity
                                      1 represents conditional based similarity
        """
        self.song_user_map = song_user_map
        self.alpha = alpha
        self.similarity_measure = similarity_measure
        self.q = q

    def find_cosine_similarity(self, song1, song2):
        """This method is used to find cosine similarity between song1 and song2"""
        similarity = 0
        count_song1 = len(self.song_user_map[song1])
        count_song2 = len(self.song_user_map[song2])
        count_song1_song2 =  float(len(self.song_user_map[song1].intersection(self.song_user_map[song2])))

        if count_song1_song2 > 0:
            similarity = count_song1_song2/(math.pow(count_song1, self.alpha) * math.pow(count_song2, 1-self.alpha))
        return similarity

    def find_score(self,user_listened_songs, all_possible_songs):
        """This method finds the score for each of the user_songs from
        the listening history by finding similarity between the song and all_songs"""
        scores_map = dict()
        for song_id in all_possible_songs:
            scores_map[song_id] = 0.0
        #check to make sure song is present in song_user_map
            if song_id in self.song_user_map:
                for user_listened_song in user_listened_songs:
                    if(user_listened_song in self.song_user_map):
                        #get the similarity measure type
                        if self.similarity_measure == 0:
                            #call cosine similarity
                            similarity = self.find_cosine_similarity(song_id,user_listened_song)
                        if self.similarity_measure == 1:
                            #call conditional probability similarity
                            similarity = self.find_conditional_based_similarity(song_id,user_listened_song)
                            # locality-sensitive param gamma is 2
                        scores_map[song_id] += math.pow(similarity, self.q)
        return scores_map
