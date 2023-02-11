# Musical analysis

In this work, I used some datasets provided by my teachers at my master's degree and try to analyze them using Python's packaging tools, in order to create a complete Python project structure. A test structure is also developped.

## Tasks

This work was made in the context of one of my courses and therefore the following goals were to be reached in order to pass. I was asked to:

+ De-normalize the original files, getting a coherent structure and correcting some of the mistakes the original data contains.
+ Use alternative ways of reading .csv files aiming to be capable of handling data of more than 1Gb.
+ Create some filtering and basic counters answering to a series of questions (the info given in the #3 section of the main file answers these questions).
+ Analyze the audio features, getting some statistical markers of the data and some graphs.
+ Get the (normalized) histogram of a feature of a certain artist.
+ Get a visual comparison with 2 types of distance between two artists' features.

## Method & structure

For this work, I implemented a complete project structure, where the main.py script is in charge of calling the auxiliar functions. The helpers.py script does all the auxiliar work, and the plotters.py file executes the graphing functions.

The project is structured as follows:
+ songs
  + main
    + __init__.py
    + helpers.py
    + plotters.py
    + PEC4.py
    + data
      + data.zip
    + plots
  + tests
    + __init__.py
    + tests.py
  + LICENSE
  + setup.py
  + requirements.txt
  + README.md

## Tests 

The code is tested to see if it works as intended. 5 classes are created to see if the formatting, reading, calculations, and operations are correctly implemented. The package has been released once every test has been verified.

## Results

The results are mainly expressed with plots, as it can be seen in the following two examples.

![audio_feature_histogram](https://user-images.githubusercontent.com/81832365/218278525-3cd2eb7c-7a34-4f58-86df-a169312e3b3b.png)

![cosinus_heatmap](https://user-images.githubusercontent.com/81832365/218278526-a5fa12b4-a6b8-4ffc-9b87-d56cd8620475.png)

## Bibliography

In order to create the project, the following websites have been consulted:

+ https://kiwidamien.github.io/making-a-python-package.html
+ https://matplotlib.org/stable/index.html
+ https://python-packaging-tutorial.readthedocs.io/en/latest/setup_py.html
+ https://stackoverflow.com/
+ https://numpy.org/doc/stable/index.html
+ https://pandas.pydata.org/

