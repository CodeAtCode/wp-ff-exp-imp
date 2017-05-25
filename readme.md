# WordPress Firefox Exporter Importer

A suite of tools to export posts from WordPress using the HTML on the backend area of every post using Firefox, JSON and WXR.  

## Why this strange workaround or hack?
I will tell you a story... there was a customer and there was a new website in progress, after months of working he discovered that the old agency that done the actual website don't want to give to them the backup of the data.  
So there was only two option for the customer: Scream running in a circle or call someone to leave to him the problems and claiming with this unlucky guy.   
Flash forward to us as the unlucky guys that have to find a solution for this not simple problem.  
So we discovered in the actual website:

* The RSS feed has incomplete content
* XML-RPC enabled only in write-mode
* REST API disabled
* we had access as `editor` in the actual WordPress site
* there was 420 posts to export with categories, tags and featured images

This was our turn to run in circle in the room because the only solution was do it manually!  

The only way that we saw was pretty simple, download the HTML of every backend page of the posts and then parse to generate a WXR file for WordPress to do the magic and we done it.  
Why the backend? Because contain all the data in a unique format that can be compatible across other websites (you can never know what the future can say) and at the same time that data are in a easy way to convert for the WXR file.   

A little note: the behaviour of the old agency was not very good, because they are not the owner of the website but we don't know the contract made with them so we had only a chance to have in reasonable times the backup.   

### How do you did it?

* Using Firefox for access to the page and with the Firefox Nightly edition with the Marionette (unit test system of Firefox) enabled we scripted the pagination of the post list and opening of all of them and downloading
* Generate an HTML file and convert with another script as JSON with the data that we really need (content, featured image, categories etc)
* Merge all the JSON files in an unique file to improve the next script workflow
* Convert that JSON as WXR xml file
* Split that file in little chunks because hosting can has limits in file uploads or WordPress can crash for the huge amount of things to do 
* Enjoy of the importing on first run!

PS: Remember that if you are using WPML that on importing the media don't have languages so in the media list the page is empty (we lost 2 hours of debug to understand that behaviour).

## The suite

### export-html.py

Connect with Firefox (with Marionette enabled), go the page `/wp-admin/edit.php`, the script will use the pagination and will export all the `HTML` files on the `export-html` folder.

Require some times and need to be executed few times to download everything!

### export-json.py

Convert the HTML exported from the first script in a `JSON` files on the folder `export-json`.

### single-json.sh

Create a single `JSON` file merging all the files using `jq` on the folder `json-result`.

### json2wxr.js

```
npm install https://github.com/mte90/node-wxr
```

Use the `node-wxr` module (with patches for bugs and other new features) to convert the JSON generated with the previous script in the same folder with a xml file using the `WXR` standard.

### wxr-split.py

```
./wxr-split.py ./json-result/export.xml 3
```

Split the `XML` exported file of the previous step in 3 files.