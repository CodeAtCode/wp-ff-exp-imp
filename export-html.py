#!/usr/bin/python
import time, urlparse, os.path
from marionette_driver.marionette import Marionette
from marionette_driver import By, Actions

# Connect to Firefox
client = Marionette(host='localhost', port=2828)
client.start_session()


def open_page(client, post):
    while len(client.window_handles) == 1:
        # Fuzzy is required to enable the browser to lost the focus and a click that work
        # To use only if the website lags a lot and is full of js trash
        # removeOtherStrings = "window.scrollTo(0,(Math.floor(Math.random() * (document.documentElement.scrollHeight))))"
        # client.execute_script(removeOtherStrings)
        Actions(client).middle_click(post).perform()
        time.sleep(0.4)


def export_html(client, post):
    open_page(client, post)
    time.sleep(4)
    # Switch to the tab opened
    client.switch_to_window(client.window_handles[-1])
    post_url = urlparse.urlparse(client.get_url())
    try:
        post_id = str(urlparse.parse_qs(post_url.query)['post'][0])
    except:
        # switch to the tab sometimes not work, with this we retry it
        export_html(client, post)
        return False
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


def export_list(client):
    with client.using_context('content'):
        posts = client.find_elements(By.CSS_SELECTOR, 'td.title a.row-title')

        for post in posts:
            export_html(client, post)
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
client.close()
