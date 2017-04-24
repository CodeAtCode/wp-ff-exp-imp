#!/usr/bin/nodejs
var Importer = require('wxr');
var fs = require('fs');
var importer = new Importer();
var json_file = fs.readFileSync('./json-result/export.json', 'utf8');
var json_file = json_file.replace(/<script[^>]*>.*?<\/script>/gi,'').replace(/<blockquote[^>]*>.*?<\/blockquote>/gi,'')
var obj = JSON.parse(json_file);

var wpcat = {}

for (var i = 0; i < obj.length; ++i) {
  console.log("ID: " + obj[i].ID);
  var cat_post = {};
  // Category
  for (var z = 0; z < obj[i].category.length; ++z) {
	if (wpcat[obj[i].category[z]] !== undefined) {
	  importer.addCategory({
		id: z,
		title: obj[i].category[z]
	  });
	  cat_post[z] = obj[i].category[z];
	}
  }
  var tag_post = {};
  // Tag
  for (var z = 0; z < obj[i].tag.length; ++z) {
	tag_post[z] = obj[i].tag[z];
  }
  // Import
  importer.addPost({
	id: obj[i].ID,
	title: obj[i].post_title,
	name: obj[i].post_name,
	date: obj[i].post_date,
	status: obj[i].post_status,
	post: obj[i].post_type,
	author: "wp_user_replace",
	contentEncoded: obj[i].post_content.trim(),
	categories: cat_post,
	tags: tag_post
  });
  // Add attachment
  importer.addAttachment({
	id: obj[i].featured_image_is,
	date: obj[i].post_date,
	title: obj[i].featured_image_desc,
	author: "admin",
	description: obj[i].featured_image_desc,
	status: "wp_user_replace",
	parent: obj[i].ID,
	attachmentURL: obj[i].featured_image
  });
}

var file_xml = importer.stringify();

fs.writeFile("./json-result/export.xml", file_xml, function (err) {
  if (err) {
	return console.log(err);
  }

  console.log("The file was generated!");
});
