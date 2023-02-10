from helpers import *
from plotters import *


if __name__ == "__main__":

    # 1. DENORMALIZATION

    # File path management
    p = os.getcwd()
    file_path_1 = os.path.join(p, 'data/data.zip')
    file_path_2 = os.path.join(p, 'data')

    # Unzip data
    unzipper(file_path_1, 'data')

    # Read data
    albums = reader('data/albums_norm.csv', ';')
    artists = reader('data/artists_norm.csv', ';')
    tracks = reader('data/tracks_norm.csv', ';')

    # Capitalization
    artists = capitalizer(artists, "name")

    # Empty value handling
    tracks = empty_handler(tracks, "popularity")

    # Joining the datasets
    # Renaming columns with same names
    albums = albums.rename(columns={'name': 'album_name', 'popularity': 'album_popularity'})
    artists = artists.rename(columns={'name': 'artist_name', 'popularity': 'artist_popularity'})
    tracks = tracks.rename(columns={'name': 'track_name', 'popularity': 'track_popularity'})

    # Merging
    tracks = pd.merge(tracks, artists, on='artist_id', how='left')
    tracks = pd.merge(tracks, albums, on=['album_id', 'artist_id'], how='left')

    # Final dataset info
    num_tracks = len(tracks.index)
    num_cols = len(tracks.columns)
    num_empty_pop = len(tracks[tracks.track_popularity == ''])
    print("Number of tracks: " + str(num_tracks))
    print("Number of columns: " + str(num_cols))
    print("Number of empty popularity values: " + str(num_empty_pop))

    # 2. READING COMPARISON

    # Path management
    file_path_3 = ["data/artists_norm.csv", "data/tracks_norm.csv", "data/albums_norm.csv"]
    col_name = ["artist_id", "track_id", "album_id"]

    # Plotting and saving
    bar_plotter(file_path_3, col_name)

    # 3. FILTERING AND BASIC COUNTERS

    # Printing of the comments
    # A:
    print(value_count("Radiohead", "artist_name", tracks, "Radiohead songs"))

    # B:
    print(contain_count("police|Police", "track_name", tracks, "track titles containing the 'police' word"))

    # C:
    print(contain_count("^199", "release_year", tracks, "tracks published in the 90s"))

    # D:
    print(get_top_value("track_popularity", "track_name", tracks, "most popular track",
                        (tracks['release_year'] >= 2012)))

    # E:
    print(decade("release_year", "artist_name", 1960, 2020, tracks,
                 "of artists with tracks in each decade since the 1960s"))

    # 4. INITIAL ANALYSIS

    # A: Energy feature, Metallica
    print(min_mean_max_feature("energy", (tracks['artist_name'] == "Metallica"), tracks,
                               "the energy feature of Metallica"))

    # B: Danceability means, Coldplay, by album (plot)
    means = get_means("danceability", (tracks['artist_name'] == "Coldplay"), "album_name", tracks)

    # Plotting and saving
    group_mean_feature_plotter("Danceability of Coldplay tracks grouped by album",
    "Album", "Danceability", means[0], means[1])

    # 5. AUDIO FEATURE HISTOGRAM

    # Ed Sheeran's acousticness: plotting and saving
    audio_feature_histogram("acousticness", (tracks['artist_name'] == "Ed Sheeran"),
                            tracks, "Acousticness probability density of Ed Sheeran tracks")

    # 6. ARTIST VISUAL COMPARISON

    # Adele - Extremoduro energy comparison: plotting and saving
    density_prob_comparison_plot("energy", (tracks['artist_name'] == "Adele"),
                                 "energy",(tracks['artist_name'] == "Extremoduro"),
                                 tracks,"Adele - Extremoduro energy comparison", "Adele", "Extremoduro")

    # 7. ARTIST SIMILARITY CALCULATION

    # Creation of a list with the numeric features
    feat = ["danceability", "energy", "key", "loudness", "mode", "speechiness", "acousticness", "instrumentalness",
            "liveness", "valence", "tempo", "duration_ms"]

    # Heatmap of the artist's comparison (euclidean distance)
    heatmap(["Metallica", "Extremoduro", "AC/DC", "Hans Zimmer"], feat, tracks, "euclidean", "artist_name")

    # Heatmap of the artist's comparison (cosinus distance)
    heatmap(["Metallica", "Extremoduro", "AC/DC", "Hans Zimmer"], feat, tracks, "cosinus", "artist_name")