# WordPress Firefox Exporter Importer

It is a suite of tools to export posts from the html on the backend area of every post using Firefox and a plugin importer from JSON.  
Why this trange workaround or hack? Because sometimes old owner of the website don't give to you access to a db or Rest api or feed rss (with text) or xml rpc.

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