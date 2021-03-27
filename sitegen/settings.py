# Core settings of sitegen

import os
from markdown import markdown

# Should debug messages be printed to stdout?
DEBUG = True

# -- Site structure -- #

# Site root (where all the dev files are present)
SITEROOT = os.path.realpath('.')

# Path to where the site should be published (put in production):
PUBDIR = SITEROOT + '/testsite/'

# Your site's domain for linking, etc, with the https:// bit:
DOMAIN = 'https://example.com/'

# "Static" pages of the site (i.e. root pages)
# Add them as tuples in the format of ("page title", "URL"):
SITE_PAGES = [
    ('About this site', 'about'),
    ('Get in touch', 'contact'),
    ('Privacy Policy', 'privacy'),
]

# What's the name of the "blog" subfolder of the site?
# This will be appended to PUBDIR
BLOG_SUBDIR = 'blog/'
BLOG = PUBDIR + BLOG_SUBDIR


# -- Page structure --
#
# This section contains enumerates the "holes" and other structures that our
# site's template has.
#

# Path to the template file
TEMPLATE = SITEROOT + '/template.html'

# The fields (holes) for our page's template. 
# Some are fields are 'reserved' i.e. please do not edit them: they'll be 
# updated automatically.
# Extra fields must be entered by you, manually.
# After you edit these, DO NOT forget to edit the actual template accordingly.
TEMPLATE_FIELDS = {
    'title': "",        # reserved
    'description': "",  # reserved
    'canonical' : "",   # reserved
    'content': "",      # reserved
    'footer_notice': "",
}

# Set any additional fields' values here, for example:
raw_foot = "Copyright 2021 - the author"
TEMPLATE_FIELDS["footer_notice"] = markdown(raw_foot)

