#!/usr/bin/python
import lxml.html, os, json
from lxml.cssselect import CSSSelector

source = './export-html'
for root, dirs, filenames in os.walk(source):
    for f in filenames:
        fullpath = os.path.join(source, f)
        data = {}
        html = open(fullpath, 'r')
        # Parser the html
        tree = lxml.html.fromstring(html)
        sel = CSSSelector('#title')
        results = sel(tree)
        data['post_title'] = results[0].text
        # This is the slug
        sel = CSSSelector('#editable-post-name-full')
        data['post_name'] = results[0].text
        data['post_type'] = 'post'
        sel = CSSSelector('#hidden_post_status')
        data['post_status'] = results[0].value
        sel = CSSSelector('.wp-editor-area')
        data['post_content'] = results[0].value
        sel = CSSSelector('#post_ID')
        data['ID'] = results[0].value
        
        archive = open('export-json/' + f + '.json', 'w')
        archive.write(json.dumps(data, indent=4, sort_keys=True))
        archive.close()
        exit