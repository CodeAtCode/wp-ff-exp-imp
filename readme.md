# WordPress Firefox Exporter Importer

It is a suite of tools to export posts from the HTML on the backend area of every post using Firefox, JSON and WXR.  

### Why this strange workaround or hack?
I will tell you a story, there was an our customer and we are doing a new website, after months of working he discovered that the old agency that done the actual website don't want to give to them the data backup.  
We discovered that the RSS feed has incomplete content, XML-RPC enabled only in write-mode, REST API disabled so we had no choice to import the content of the old site in the new one.  
Also the behaviour of the old agency is not very good, because they are not the owner of the website but we don't know the contract made with them so we had only a chance to have in reasonable times the backup.   
So we had the access on the website as editor, so we used the Firefox unit testing system to paginate every post list in the admin area and download all the HTML version of the editing page of the post. In that way we have all the settings and the tool is compatible with other WordPress sites. Next we parse all the HTML files and generate a json with the data to import, next merged all the JSON in an unique file and next converted to a XML file using the WXR standard. 

## export-html.py

Connect with Firefox (with Marionette enabled), go the page `/wp-admin/edit.php`, the script will use the pagination and will export all the `HTML` files on the `export-html` folder.

Require some times and need to be executed few times to download everything!

## export-json.py

Convert the HTML exported from the first script in a `JSON` files on the folder `export-json`.

## single-json.sh

Create a single `JSON` file merging all the files using `jq` on the folder `json-result`.

## json2wxr.js

```
npm install https://github.com/mte90/node-wxr
```

Use the `node-wxr` module (with patches for bugs) to convert the JSON generated with the previous script in the same folder with a xml file using the `WXR` standard.

## wxr-split.py

```
./wxr-split.py ./json-result/export.xml 3
```

Split the `XML` exported file of the previous step in 3 files.