# Email Image to text conversion.

#### Instructions -

The OCR API solution is split into 4 step for 100% accuracy.

1) Filter all email images links
2) Consume OCR API using PHP script and save response in MySQL table
3) Review and clean the email data (if found any garbage in it)
4) Add below code in spider script to consume PHP web service


1) Filter all email images links

Use below code to filter the all email image links.

```
	#list images urls
        for image_file in imagesB_generated:
            if ("/emailimages/" in image_file):
                data = [image_file]
                self.csv_writer(data, "email_images_url_list.csv")
```

Please add above snippet in all parse functions in the migration script [Example](https://github.com/greenpeace/planet4-gpi-export/blob/master/Canada/canada_spider.py#L460)
This will generate a csv file with a list of all the email image URLs.


2) Consume OCR API using PHP script and save response in MySQL table

Please copy the `planet4-gpi-export/OCR_webservice` folder to local web server.

Create the database on your local system, name as **_gp_ca_email_img_to_text_**(here I use 'gp_ca' prefix but you can use any name.)

Import the tables from [here](https://github.com/greenpeace/planet4-gpi-export/blob/master/OCR_webservice/email_img_to_text_schema.sql)

As per local MySQL database credentials, please update planet4-gpi-export/OCR_webservice/connection.php file.

Now we have the list of links but there are so many of duplicate entries.

Filter those links and get the unique list of links.

Copy the list of images in `email_img_to_text_function.php` file in `$url_list` array.

3) Review and clean the email data (using script)

browse the `review_parsed_email_id.php` file on local. here you can check and fix if you found any issue with parsed data by editing database table raws.


4) Add below code in spider script to consume PHP webservice

Please replace/comment the code snippet added in step1 with below one -

```
	# Filter email id image and replace it with email text.
        delete_images = list()
        for image_file in imagesB_generated:
            if ("/emailimages/" in image_file):
                # PHP webservice script url.
                api_url = "http://localhost_test/PHP_webservice/email_img_to_text.php"
                end_point_url = api_url + "?url=" + image_file
                emailid = urllib2.urlopen(end_point_url).read(1000)
                delete_images.append(image_file)
                # Remove the email images from Post body and replace it with email text.
                body_text = re.sub(
                    '<img[a-zA-Z0-9="\s\_]*src=\"' + image_file + '\"[a-zA-Z0-9="\s]*>',
                    emailid, body_text)

        # Remove the email images from list.
        for image_file in delete_images:
            imagesB_generated.remove(image_file)
```
This code will replace the images of each post for its corresponding email text between <a> tags.

###### Note: 
- please replace the `api_url` path with your local server path.
- The OCR API has **500 calls/DAY / IP** Rate limit.

Now the OCR API set up in a script is ready for migration.

API reference: https://ocr.space/ocrapi
