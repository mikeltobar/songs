import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import unittest
from pathlib import Path
from PEC4.helpers import *

class TestFilesAndProcessing(unittest.TestCase):


    def test_unzipper(self):
        p = Path(__file__).parents[1]
        file_path_1 = os.path.join(p, 'PEC4/data/albums_norm.csv')
        file_path_2 = os.path.join(p, 'PEC4/data/artists_norm.csv')
        file_path_3 = os.path.join(p, 'PEC4/data/tracks_norm.csv')
        try:
            os.remove(file_path_1)
            os.remove(file_path_2)
            os.remove(file_path_3)
        except FileNotFoundError:
            pass
        file_path_4 = os.path.join(p, 'PEC4/data/data.zip')
        file_path_5 = os.path.join(p, 'PEC4/data')
        unzipper(file_path_4, file_path_5)
        print(file_path_1)
        self.assertTrue(os.path.isfile(file_path_1))
        self.assertTrue(os.path.isfile(file_path_2))
        self.assertTrue(os.path.isfile(file_path_3))

    def test_reader(self):
        p = Path(__file__).parents[1]
        file_path_1 = os.path.join(p, 'PEC4/data/albums_norm.csv')
        self.assertTrue(reader(file_path_1, ';').equals(pd.read_csv(file_path_1, on_bad_lines='skip', sep=";")))


    def test_capitalizer(self):
        data = [['luciano pavarotti'], ['KISS'], ['Freddy Mercury']]
        ok_data = [['Luciano Pavarotti'], ['KISS'], ['Freddy Mercury']]
        df = pd.DataFrame(data, columns=['Name'])
        ok_df = pd.DataFrame(ok_data, columns=['Name'])
        self.assertTrue(capitalizer(df, 'Name').equals(ok_df))

    def test_empty_handler(self):
        data = [[4.0], [2.0], []]
        ok_data = [[4.0], [2.0], [3.0]]
        df = pd.DataFrame(data, columns=['Total'])
        ok_df = pd.DataFrame(ok_data, columns=['Total'])
        self.assertTrue(empty_handler(df, 'Total').equals(ok_df))


class TestReturnColumn(unittest.TestCase):


    def test_pandas_reading(self):
        p = Path(__file__).parents[1]
        file_path_1 = os.path.join(p, 'PEC4/data/albums_norm.csv')
        file_path_2 = os.path.join(p, 'PEC4/data/artists_norm.csv')
        file_path_3 = os.path.join(p, 'PEC4/data/tracks_norm.csv')
        df1 = pd.read_csv(file_path_1, sep=";")
        df2 = pd.read_csv(file_path_2, sep=";")
        df3 = pd.read_csv(file_path_3, sep=";")
        col1 = df1["album_id"].to_frame()
        col2 = df2["artist_id"].to_frame()
        col3 = df3["track_id"].to_frame()
        self.assertTrue(col1.equals(get_column_pandas(file_path_1, "album_id")))
        self.assertTrue(col2.equals(get_column_pandas(file_path_2, "artist_id")))
        self.assertTrue(col3.equals(get_column_pandas(file_path_3, "track_id")))

    def test_csv_reading(self):
        p = Path(__file__).parents[1]
        file_path_1 = os.path.join(p, 'PEC4/data/albums_norm.csv')
        file_path_2 = os.path.join(p, 'PEC4/data/artists_norm.csv')
        file_path_3 = os.path.join(p, 'PEC4/data/tracks_norm.csv')
        df1 = pd.read_csv(file_path_1, sep=";")
        df2 = pd.read_csv(file_path_2, sep=";")
        df3 = pd.read_csv(file_path_3, sep=";")
        col1 = df1["album_id"].to_frame()
        col2 = df2["artist_id"].to_frame()
        col3 = df3["track_id"].to_frame()
        col4 = pd.DataFrame(get_column_csv_dictreader(file_path_1, "album_id"))
        col5 = pd.DataFrame(get_column_csv_dictreader(file_path_2, "artist_id"))
        col6 = pd.DataFrame(get_column_csv_dictreader(file_path_3, "track_id"))
        self.assertTrue(col1.equals(col4.rename(columns={0: "album_id"})))
        self.assertTrue(col2.equals(col5.rename(columns={0: "artist_id"})))
        self.assertTrue(col3.equals(col6.rename(columns={0: "track_id"})))

    def test_compare_pandas_csv(self):
        p = Path(__file__).parents[1]
        file_path_1 = os.path.join(p, 'PEC4/data/albums_norm.csv')
        file_path_2 = os.path.join(p, 'PEC4/data/artists_norm.csv')
        file_path_3 = os.path.join(p, 'PEC4/data/tracks_norm.csv')
        col1 = get_column_pandas(file_path_1, "album_id")
        col2 = get_column_pandas(file_path_2, "artist_id")
        col3 = get_column_pandas(file_path_3, "track_id")
        col4 = pd.DataFrame(get_column_csv_dictreader(file_path_1, "album_id"))
        col5 = pd.DataFrame(get_column_csv_dictreader(file_path_2, "artist_id"))
        col6 = pd.DataFrame(get_column_csv_dictreader(file_path_3, "track_id"))
        self.assertTrue(col1.equals(col4.rename(columns={0: "album_id"})))
        self.assertTrue(col2.equals(col5.rename(columns={0: "artist_id"})))
        self.assertTrue(col3.equals(col6.rename(columns={0: "track_id"})))

class TestFilteringAndBasicCounters(unittest.TestCase):

    def test_value_count(self):
        data = [['peter'], ['mike'], ['fred'], ['peter'], ['mike'], ['josh'], ['bert'], ['peter']]
        df = pd.DataFrame(data, columns=['name'])
        msg_1 = 'There are 3 occurrences of peter.'
        msg_2 = 'There are 2 occurrences of mike.'
        msg_3 = value_count('peter', 'name', df, 'peter')
        msg_4 = value_count('mike', 'name', df, 'mike')
        self.assertEqual(msg_1, msg_3)
        self.assertEqual(msg_2, msg_4)

    def test_containing_count(self):
        data = [['jackson parker'], ['mike parker'], ['fred jackson'], ['peter jackson'], ['parker parks']]
        df = pd.DataFrame(data, columns=['name'])
        msg_1 = 'There are 3 occurrences of parker.'
        msg_2 = 'There are 3 occurrences of jackson.'
        msg_3 = contain_count('parker', 'name', df, 'parker')
        msg_4 = contain_count('jackson', 'name', df, 'jackson')
        self.assertEqual(msg_1, msg_3)
        self.assertEqual(msg_2, msg_4)


    def test_get_top_value(self):
        data = [['Tom', 10, 'no'], ['Frank', 2, 'yes'], ['Nick', 7 ,'yes'], ['Rachel', 3, 'no']]
        df = pd.DataFrame(data, columns=['name', 'mark', 'international'])
        msg_1 = 'The student with the top mark is Tom.'
        msg_2 = 'The international student with the top mark is Nick.'
        msg_3 = get_top_value('mark', 'name', df, 'student with the top mark', None)
        msg_4 = get_top_value('mark', 'name', df, 'international student with the top mark',
                              df['international'] == 'yes')
        self.assertEqual(msg_1, msg_3)
        self.assertEqual(msg_2, msg_4)

    def test_decades(self):
        data = [[1992, 'AC/DC'], [2000, 'AC/DC'], [2010, 'AC/DC'], [1994, 'David Bowie'], [2000, 'David Bowie'],
                [2010, 'Fito y fitipaldis']]
        df = pd.DataFrame(data, columns=['year', 'artist'])
        msg_1 = 'The values of artists with tracks in each decade since the 1990s until the 2010s are: '\
                'AC/DC, according to the given dataframe.'
        msg_2 = 'The values of artists with tracks in each decade since the 1990s until the 2000s are: '\
                'AC/DC, David Bowie, according to the given dataframe.'
        msg_3 = decade('year', 'artist', 1990, 2010, df,
                'of artists with tracks in each decade since the 1990s until the 2010s')
        msg_4 = decade('year', 'artist', 1990, 2000, df,
                'of artists with tracks in each decade since the 1990s until the 2000s')
        self.assertEqual(msg_1, msg_3)
        self.assertEqual(msg_2, msg_4)

class TestInitialAnalysis(unittest.TestCase):

    def test_min_mean_max_feature(self):
        data = [[1.55, 'petrol'], [1.43, 'diesel'], [1.35, 'petrol'], [1.46, 'diesel'], [1.34, 'petrol'],
                [1.65, 'diesel']]
        df = pd.DataFrame(data, columns=['price', 'type'])
        msg_1 = 'For the price feature min value is: 1.34, max value is: 1.65, & mean value is: 1.46.'
        msg_2 = 'For the price feature min value is: 1.43, max value is: 1.65, & mean value is: 1.51.'
        msg_3 = min_mean_max_feature('price', None, df, 'the price feature')
        msg_4 = min_mean_max_feature('price', (df['type'] == 'diesel'), df, 'the price feature')
        self.assertEqual(msg_1, msg_3)
        self.assertEqual(msg_2, msg_4)

    def test_means(self):
        data = [[2, 'album1'], [2, 'album2'], [2, 'album1'], [4, 'album2']]
        df = pd.DataFrame(data, columns=['number', 'album'])
        out_1 = [2.0, 3.0]
        out_2 = get_means('number', None, 'album', df)
        self.assertEqual(out_1, out_2[0])

class TestFeatures(unittest.TestCase):

    def test_features_mean(self):
        data = [['Bowie', 2, 4, 3], ['Bowie', 2, 0, 3], ['Bowie', 2, 2, 3], ['Elton John', 4, 2, 0]]
        df = pd.DataFrame(data, columns=['name', 'a', 'b', 'c'])
        feat_1 = ['a', 'b']
        feat_2 = ['a', 'b', 'c']
        out_1 = [2.0, 2.0]
        out_2 = [2.0, 2.0, 3.0]
        out_3 = features_mean('Bowie', df, feat_1, 'name')
        out_4 = features_mean('Bowie', df, feat_2, 'name')
        self.assertEqual(out_1, out_3)
        self.assertEqual(out_2, out_4)

# coverage run --source PEC4.helpers -m unittest discover && coverage report (from PEC4 folder)
