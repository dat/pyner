#!/usr/bin/env python

try:
    import http.client as httplib
    from urllib.parse import urlencode
except ImportError:
    import httplib
    from urllib import urlencode

import json
import re
import socket

from itertools import groupby
from operator import itemgetter

from .exceptions import (
    NERError,
)

from .utils import (
    tcpip4_socket,
    http_connection,
)


#regex patterns for various tagging options for entity parsing
SLASHTAGS_EPATTERN  = re.compile(r'(.+?)/([A-Z]+)?\s*')
XML_EPATTERN        = re.compile(r'<wi num=".+?" entity="(.+?)">(.+?)</wi>')
INLINEXML_EPATTERN  = re.compile(r'<([A-Z]+?)>(.+?)</\1>')


class NER(object):
    """Wrapper for server-based Stanford NER tagger."""

    def tag_text(self, text):
        pass

    def __slashTags_parse_entities(self, tagged_text):
        """Return a list of token tuples (entity_type, token) parsed
        from slashTags-format tagged text.

        :param tagged_text: slashTag-format entity tagged text
        """
        return (match.groups()[::-1] for match in
            SLASHTAGS_EPATTERN.finditer(tagged_text))

    def __xml_parse_entities(self, tagged_text):
        """Return a list of token tuples (entity_type, token) parsed
        from xml-format tagged text.

        :param tagged_text: xml-format entity tagged text
        """
        return (match.groups() for match in
            XML_EPATTERN.finditer(tagged_text))

    def __inlineXML_parse_entities(self, tagged_text):
        """Return a list of entity tuples (entity_type, entity) parsed
        from inlineXML-format tagged text.

        :param tagged_text: inlineXML-format tagged text
        """
        return (match.groups() for match in
            INLINEXML_EPATTERN.finditer(tagged_text))

    def __collapse_to_dict(self, pairs):
        """Return a dictionary mapping the first value of every pair
        to a collapsed list of all the second values of every pair.

        :param pairs: list of (entity_type, token) tuples
        """
        return dict((first, list(map(itemgetter(1), second))) for (first, second)
            in groupby(sorted(pairs, key=itemgetter(0)), key=itemgetter(0)))

    def get_entities(self, text):
        """Return all the named entities in text as a dict.

        :param text: string to parse entities
        :returns: a dict of entity type to list of entities of that type
        """
        tagged_text = self.tag_text(text)
        if self.oformat == 'slashTags':
            entities = self.__slashTags_parse_entities(tagged_text)
            entities = ((etype, " ".join(t[1] for t in tokens)) for (etype, tokens) in
                groupby(entities, key=itemgetter(0)))
        elif self.oformat == 'xml':
            entities = self.__xml_parse_entities(tagged_text)
            entities = ((etype, " ".join(t[1] for t in tokens)) for (etype, tokens) in
                groupby(entities, key=itemgetter(0)))
        else: #inlineXML
            entities = self.__inlineXML_parse_entities(tagged_text)
        return self.__collapse_to_dict(entities)

    def json_entities(self, text):
        """Return a JSON encoding of named entities in text.

        :param text: string to parse entities
        :returns: a JSON dump of entities parsed from text
        """
        return json.dumps(self.get_entities(text))


class SocketNER(NER):
    """Stanford NER over simple TCP/IP socket."""

    def __init__(self, host='localhost', port=1234, output_format='inlineXML'):
        if output_format not in ('slashTags', 'xml', 'inlineXML'):
            raise ValueError('Output format %s is invalid.' % output_format)
        self.host = host
        self.port = port
        self.oformat = output_format

    def tag_text(self, text):
        """Tag the text with proper named entities token-by-token.

        :param text: raw text string to tag
        :returns: tagged text in given output format
        """
        for s in ('\f', '\n', '\r', '\t', '\v'): #strip whitespaces
            text = text.replace(s, '')
        text += '\n' #ensure end-of-line
        with tcpip4_socket(self.host, self.port) as s:
            if not isinstance(text, bytes):
                text = text.encode('utf-8')
            s.sendall(text)
            tagged_text = s.recv(10*len(text))
        return tagged_text.decode('utf-8')


class HttpNER(NER):
    """Stanford NER using HTTP protocol."""

    def __init__(self, host='localhost', port=1234, location='/stanford-ner/ner',
            classifier=None, output_format='inlineXML', preserve_spacing=True):
        if output_format not in ('slashTags', 'xml', 'inlineXML'):
            raise ValueError('Output format %s is invalid.' % output_format)
        self.host = host
        self.port = port
        self.location = location
        self.oformat = output_format
        self.classifier = classifier
        self.spacing = preserve_spacing

    def tag_text(self, text):
        """Tag the text with proper named entities token-by-token.

        :param text: raw text strig to tag
        :returns: tagged text in given output format
        """
        for s in ('\f', '\n', '\r', '\t', '\v'): #strip whitespaces
            text = text.replace(s, '')
        text += '\n' #ensure end-of-line
        with http_connection(self.host, self.port) as c:
            headers = {'Content-type': 'application/x-www-form-urlencoded', 'Accept' : 'text/plain'}
            if self.classifier:
                params = urlencode(
                    {'input': text, 'outputFormat': self.oformat,
                    'preserveSpacing': self.spacing,
                    'classifier': self.classifier})
            else:
                params = urlencode(
                    {'input': text, 'outputFormat': self.oformat,
                    'preserveSpacing': self.spacing})
            try:
                c.request('POST', self.location, params, headers)
                response = c.getresponse()
                tagged_text = response.read()
            except httplib.HTTPException as e:
                print("Failed to post HTTP request.")
                raise e
        return tagged_text


