#!/usr/bin/python
import time, urlparse, os.path
from marionette import Marionette
from marionette_driver import By, Actions


def open_page(client, post):
    while len(client.window_handles) == 1:
#        client.find_element(By.CSS_SELECTOR, 'body').click()
        print('click')
        Actions(client).middle_click(post).perform()
        time.sleep(1)


# Connect to Firefox
client = Marionette(host='localhost', port=2828)
client.start_session()


def export_list(client):
    with client.using_context('content'):
        posts = client.find_elements(By.CSS_SELECTOR, 'td.title a.row-title')

        for post in posts:
            open_page(client, post)
            time.sleep(5)
            # Switch to the tab opened
            client.switch_to_window(client.window_handles[-1])
            post_url = urlparse.urlparse(client.get_url())
            post_id = str(urlparse.parse_qs(post_url.query)['post'][0])
            path = './export-html/post-' + post_id + '.html'
            if not os.path.isfile(path):
                # Export the HTMl
                export = open(path, 'w+')
                export.write(client.page_source.encode('utf-8'))
                export.close()
                print('Exported ' + post_id + ' ID')
            else:
                print('Already exported ' + post_id)
            client.close()
            client.switch_to_window(client.window_handles[0])
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
