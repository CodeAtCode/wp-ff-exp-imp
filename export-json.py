#!/usr/bin/python
import lxml.html, os, json
from lxml.cssselect import CSSSelector

source = './export-html/'
for root, dirs, filenames in os.walk(source):
    for f in filenames:
        fullpath = os.path.join(source, f)
        data = {}
        html = open(fullpath, 'r').read()
        # Parser the html
        tree = lxml.html.fromstring(html)
        sel = CSSSelector('#title')
        results = sel(tree)
        data['post_title'] = results[0].value
        # This is the slug
        sel = CSSSelector('#editable-post-name-full')
        results = sel(tree)
        data['post_name'] = results[0].text
        data['post_type'] = 'post'
        sel = CSSSelector('#hidden_post_status')
        results = sel(tree)
        data['post_status'] = results[0].value
        sel = CSSSelector('.wp-editor-area')
        results = sel(tree)
        data['post_content'] = results[0].value
        sel = CSSSelector('#post_ID')
        results = sel(tree)
        data['ID'] = results[0].value

        archive = open('export-json/' + f.replace('.html', '') + '.json', 'w')
        archive.write(json.dumps(data, indent=4, sort_keys=True))
        archive.close()
