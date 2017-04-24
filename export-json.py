#!/usr/bin/python
import lxml.html, os, json, re
from lxml.cssselect import CSSSelector

source = './export-html/'
for root, dirs, filenames in os.walk(source):
    for f in filenames:
        fullpath = os.path.join(source, f)
        print('Parsed ' + f)
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
        # Assemble the date
        sel = CSSSelector('#hidden_jj')
        results = sel(tree)
        day = str(results[0].value)
        sel = CSSSelector('#hidden_mm')
        results = sel(tree)
        month = str(results[0].value)
        sel = CSSSelector('#hidden_aa')
        results = sel(tree)
        year = str(results[0].value)
        sel = CSSSelector('#hidden_hh')
        results = sel(tree)
        hour = str(results[0].value)
        sel = CSSSelector('#hidden_mn')
        results = sel(tree)
        minute = str(results[0].value)
        data['post_date'] = year + '-' + month + '-' + day + ' ' + hour + ':' + minute + ':00'
        sel = CSSSelector('.attachment-266x266')
        results = sel(tree)
        if len(results) > 0:
            data['featured_image'] = results[0].get('src').replace('-300x300', '')
            data['featured_image_desc'] = results[0].get('alt')
            sel = CSSSelector('#_thumbnail_id')
            results = sel(tree)
            data['featured_image_id'] = results[0].value
        # Get the category
        sel = CSSSelector('.selectit input[checked="checked"]')
        results = sel(tree)
        data['category'] = {}
        for cat in results:
            if cat.value != 'open':
                sel = CSSSelector('#category-' + cat.value + ' .selectit')
                results_cat = sel(tree)
                if len(results_cat) > 0:
                    cat_name = lxml.html.tostring(results_cat[0])
                    data['category'][cat.value] = re.sub(re.compile('<.*?>'), '', cat_name).strip()
        # Get the tags
        sel = CSSSelector('.tagchecklist span')
        results = sel(tree)
        data['tag'] = []
        if len(results) > 0:
            for tag in results:
                tag_name = lxml.html.tostring(tag).replace('&#160;', '')
                data['tag'].append(re.sub(re.compile('<.*?>'), '', tag_name).replace('X', '').strip())
        archive = open('export-json/' + f.replace('.html', '') + '.json', 'w')
        archive.write(json.dumps(data, indent=4, sort_keys=True))
        archive.close()
