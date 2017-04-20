#!/usr/bin/python
import time, urlparse, os.path
from marionette import Marionette
from marionette_driver import By

# Connect to Firefox
client = Marionette(host='localhost', port=2828)
client.start_session()


def export_list(client):
    # Open in a new tab
    addTarget = "var anchors = document.querySelectorAll('a.row-title');for (var i=0; i<anchors.length; i++){anchors[i].setAttribute('target', '_blank');}"
    client.execute_script(addTarget)

    posts = client.find_elements(By.CSS_SELECTOR, 'td.title a.row-title')

    for post in posts:
        post.click()
        time.sleep(5)
        all_tab = client.window_handles
        # Switch to the tab opened
        client.switch_to_window(all_tab[-1])
        post_url = urlparse.urlparse(client.get_url())
        post_id = str(urlparse.parse_qs(post_url.query)['post'][0])
        path = './export-html/post-' + post_id + '.html'
        if not os.path.isfile(path):
            # Export the HTMl
            export = open(path, 'w+')
            export.write(client.page_source.encode('utf-8'))
            export.close()
            client.close()
            print('Exported ' + post_id + ' ID')
            client.switch_to_window(all_tab[0])
            # Repeat the process

    export_pages(client)


def export_pages(client):
    print('Finished the page!')

    try:
        print('Move to the next one!')
        next_page = client.find_element(By.CSS_SELECTOR, 'a.next-page')
        next_page.click()
        time.sleep(2)
        export_list(client)
    except:
        print('Export finished')


export_list(client)
