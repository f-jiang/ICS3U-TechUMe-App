
import json

settings_json = json.dumps([
    {'type': 'title',
     'title': 'example title'},
    {'type': 'bool',
     'title': 'Music',
     'desc': 'Toggle Music',
     'section': 'settings',
     'key': 'music'},
    {'type': 'bool',
     'title': 'Sound Effects',
     'desc': 'Toggle Sound Effects',
     'section': 'settings',
     'key': 'sfx'}
])
