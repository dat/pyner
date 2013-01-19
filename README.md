# PyNER 

The Python interface to the [Stanford Named Entity Recognizer](https://github.com/dat/stanford-ner).

## Project Homepage

* [Stanford Named Entity Recognizer](http://nlp.stanford.edu/software/CRF-NER.shtml)

## Installation

    $ python setup.py install

## Basic Usage

    >>> import ner
    >>> tagger = ner.HttpNER(host='localhost', port=8080)
    >>> tagger.get_entities("University of California is located in California, United States")
    {'LOCATION': ['California', 'United States'],
     'ORGANIZATION': ['University of California']}
    >>> tagger.json_entities("Alice went to the Museum of Natural History.")
    '{"ORGANIZATION": ["Museum of Natural History"], "PERSON": ["Alice"]}'

## Online Demo

* [Graphical demo of several models](http://nlp.stanford.edu:8080/ner/)

## License

BSD License

## Author

PyNER is developed by maintained by Dat Hoang.
It can be found here: http://github.com/dat/pyner

