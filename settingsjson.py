
import json

settings_json = json.dumps([
    {'type': 'title',
     'title': 'example title'},
    {'type': 'bool',
     'title': 'Music',
     'desc': 'Boolean description text',
     'section': 'example',
     'key': 'music'},
    {'type': 'bool',
     'title': 'Sound Effects',
     'desc': 'Numeric description text',
     'section': 'example',
     'key': 'sfx'}
])
