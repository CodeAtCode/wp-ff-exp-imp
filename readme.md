# WordPress Firefox Exporter Importer

It is a suite of tools to export posts from the HTML on the backend area of every post using Firefox, JSON and WXR.  

### Why this strange workaround or hack?
I will tell you a story, there was an our customer where we are doing a new website and after months of working he discovered that the old agency that done the actual website don't want to give to them the backup.  
We discovered that the RSS feed have content incomplete, XML-RPC enabled only for posting and not reading, REST API disabled so we had no choice to import the content of old site in the new one.  
Also the behaviour of the old agency is not very good, because they are not the owner of the website but we don't know the contract made with them so we had only a chance to have in reasonable times the backup.   
So we had the access on the website as editor, so 

## export-html.py

Connect with Firefox, need to be on the list of post like `/wp-admin/edit.php`, will use the pagination and will export all the HTML file on the `export-html` folder.

Require some times and need to be executed few times to download everything!

## export-json.py

Convert the HTML exported from the first script in a JSON files on the folder `export-json`.

## single-json.sh

Create a single JSON file merging from all the rest using `jq` on the folder `json-result`.

## json2wxr.js

```
npm install https://github.com/mte90/node-wxr:patch-1
```

Use the `node-wxr` module (with patches for bugs) to convert the JSON generated with the previous script in the same folder with a xml file using the `wxr` standard.

## wxr-split.py

```
./wxr-split.py ./json-result/export.xml 3
```

Split the xml exported file of the previous step in less minor files.