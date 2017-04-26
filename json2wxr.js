#!/usr/bin/nodejs
var Importer = require('wxr');
var fs = require('fs');
var importer = new Importer();
var json_file = fs.readFileSync('./json-result/export.json', 'utf8');
var json_file = json_file.replace(/<script[^>]*>.*?<\/script>/gi, '').replace(/<blockquote[^>]*>.*?<\/blockquote>/gi, '');
var obj = JSON.parse(json_file);
var wpcat = {};

var string_to_slug = function (str) {
  str = str.replace(/^\s+|\s+$/g, ''); // trim
  str = str.toLowerCase();
  // remove accents, swap ñ for n, etc
  var from = "àáäâèéëêìíïîòóöôùúüûñç·/_,:;";
  var to = "aaaaeeeeiiiioooouuuunc------";
  for (var i = 0, l = from.length; i < l; i++) {
	str = str.replace(new RegExp(from.charAt(i), 'g'), to.charAt(i));
  }
  str = str.replace(/[^a-z0-9 -]/g, '') // remove invalid chars
		  .replace(/\s+/g, '-') // collapse whitespace and replace by -
		  .replace(/-+/g, '-'); // collapse dashes
  return str;
};

for (var i = 0; i < obj.length; ++i) {
  console.log("ID: " + obj[i].ID);
  var cat_posts = [];
  var tag_posts = [];
  var cat_post = '';
  var tag_post = '';
  // Category
  for (var cat_id in obj[i].category) {
	if (obj.hasOwnProperty(cat_id)) {
	  cat_post = {
		id: cat_id,
		title: obj[i].category[cat_id],
		slug: string_to_slug(obj[i].category[cat_id])
	  };
	  if (wpcat[obj[i].category[cat_id]] === undefined) {
		importer.addCategory(cat_post);
	  }
	  cat_posts.push(cat_post);
	}
  }
  // Tag
  for (var tag_id in obj[i].tag) {
	tag_post = {
	  title: obj[i].tag[tag_id],
	  slug: string_to_slug(obj[i].tag[tag_id])
	};
	importer.addCategory(tag_post);
	tag_posts.push(tag_post);
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
	categories: cat_posts,
	tags: tag_posts
  });
  // Add attachment
  importer.addAttachment({
	id: obj[i].featured_image_is,
	date: obj[i].post_date,
	title: obj[i].featured_image_desc,
	author: "wp_user_replace",
	description: obj[i].featured_image_desc,
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
