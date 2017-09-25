# Statement for enabling the development environment
DEBUG = True

# Define the application directory
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))  

BABEL_DEFAULT_LOCALE = 'en'
BABEL_DEFAULT_TIMEZONE = 'UTC'

LANGUAGES = {
    'en': 'English',
    'it': 'Italiano'
    #    'de': 'Deutsch'
}

# Application threads. A common general assumption is
# using 2 per available processor cores - to handle
# incoming requests using one and performing background
# operations using the other.
THREADS_PER_PAGE = 2

# Enable protection agains *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED     = True

# Use a secure, unique and absolutely secret key for
# signing the data. 
CSRF_SESSION_KEY = "ab28b4465f359ef90a91b8215325c9e8"

# Secret key for signing cookies
SECRET_KEY = "a05cd9a6dbde281ddc5840adde39500a"
