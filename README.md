# sitegen - a Static Site Generator written in Python

... or: if Golang has Hugo, could this be *Victor* instead? :)

**sitegen** is a static generator written in Python, using almost exlusively the Python Standard Library. 

It can create a complete site from scratch, with an optional blog entry and full support for template extensibility and SEO enhancements very quickly and with as little manual intervention as possible. In fact, sitegen's goal during development was: **from zero to web in five minutes or less**.

## Quickly deploy a website with sitegen

1. Clone this repository:

```
git clone https://github.com/raspibrasil/sitegen
```

2. Install the markdown module (if not present):

```
pip install --user markdown
```

3. Specify your site's domain and publication directory in `sitegen/settings.py`:

```
DOMAIN = 'https://mysupersite.net'
raw_pubdir = 'mysupersite'
```

4. Create your basic page structure in `sitegen/settings.py`:

```
SITE_PAGES = [
    ('About this site', 'about'),
    ('Get in touch', 'contact'),
    ('Privacy Policy', 'privacy'),
    ('My qualifications', 'resume'),
]
```

5. Edit the template fields in `sitegen/settings.py`:

```
TEMPLATE_FIELDS = {
    'title': "",        # reserved
    'description': "",  # reserved
    'canonical' : "",   # reserved
    'content': "",      # reserved
    'footer_notice': "Copyright 2021 - me - all rights reserved",
    'navbar_top': "",
}

TEMPLATE_FIELDS['navbar_top'] = '<ul><li><a href="/">Home</a></li></ul>'
```

6. Edit the `template.html` file to taste.

7. Create the site's structure in the publication directory:

```
./init
```

8. Edit the `index.md` files in each of the site pages with your content, and publish them:

```
./publish mysupersite/index.md mysupersite/*/index.md
```

9. Deploy the website:

```
scp -r mysupersite/* you@your_server:/var/www/
```

And that's it!
