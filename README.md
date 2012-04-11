# PyNER 

The Python interface to the Stanford Named Entity Recognizer.

## Installation

    $ python setup.py install

## Getting Started

    >>> import ner
    >>> tagger = ner.HttpNER(host='localhost', port='8080')
    >>> tagger.get_entities("University of California is located in California, United States")
    {'LOCATION': ['California', 'United States'],
     'ORGANIZATION': ['University of California']}
    >>> tagger.json_entities("Alice wants to the Museum of Natural History.")
    '{"ORGANIZATION": ["Museum of Natural History"], "PERSON": ["Alice"]}'

## Online Demo

* [Stanford Named Entity Tagger](http://nlp.stanford.edu:8080/ner/)

## License

BSD License

## Author

PyNER is developed by maintained by Dat Hoang
It can be found here: http://github.com/dat/pyner

