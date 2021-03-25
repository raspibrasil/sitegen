# Core settings of sitegen

import os

# Should debug messages be printed to stdout?
DEBUG = True

# -- Site structure -- #

# Path to where the site should be published (put in production):
PUBDIR = os.environ['HOME'] + '/Programs/web/sitegen/testsite/'

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
# It might be necessary to turn it completely into a Python object later.
#

# Path to the template file
TEMPLATE = os.environ['HOME'] + '/Programs/web/sitegen/template.html'

# The fields (holes) for our page's template. 
# Some are fields are 'reserved' i.e. please do not edit them.
# After you edit these, DO NOT forget to edit the actual template accordingly.
TEMPLATE_FIELDS = [
    'title',        # reserved
    'description',  # reserved
    'content',      # reserved
]

# FIXME: this whole section needs it...
