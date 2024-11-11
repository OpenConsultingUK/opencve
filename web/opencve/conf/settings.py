"""
This file is used to override the `opencve/conf/base.py` settings.
"""

import os
from opencve.conf.base import *  # noqa # pylint: disable=unused-import


# Check if the "OPENCVE_DOMAIN" environment variable is set.
# If so, assign its value to the variable `domain`.
domain = os.environ.get("OPENCVE_DOMAIN")
if domain is not None and domain != "_":
    # Get the value of the "EXTERNAL_WEBSERVER_PORT" environment variable,
    # if it exists, and assign it to the variable `port`.
    port = os.environ.get("OPENCVE_PORT")

    # Configure trusted domains for CSRF (Cross-Site Request Forgery) protection.
    # `CSRF_TRUSTED_ORIGINS` defines a list of origins allowed to make secure requests.
    # Here, we add the external domain with and without a specified port.
    CSRF_TRUSTED_ORIGINS = [
        f'https://{domain}',        # Main domain (e.g., https://example.com)
        f'https://{domain}:{port}'  # Domain with port
    ]

    # Set `CSRF_COOKIE_SECURE` to `True` to ensure the CSRF cookie is only sent
    # over HTTPS. This adds an extra layer of security in production.
    CSRF_COOKIE_SECURE = True
