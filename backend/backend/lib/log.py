"""Request/Response Logging
===========================
"""

import logzero
import falcon


class LogComponent(object):
    """Middleware class to log request and response info."""

    def process_request(self, req, res):
        """Log method and path as well as query parameters and body, if
        supplied."""

        logzero.logger.info(f"{req.method:6} Path: {req.path}")
        if req.params:
            logzero.logger.info(f"      Query: {req.params}")
        try:
            logzero.logger.info(f"       Body: {req.media}")
        except falcon.errors.HTTPBadRequest:
            pass

    def process_response(self, req, res, resource, success):
        """Log response status and body."""

        logzero.logger.info(f"     Status: {res.status}")
        logzero.logger.info(f"   Response: {res.media}")
