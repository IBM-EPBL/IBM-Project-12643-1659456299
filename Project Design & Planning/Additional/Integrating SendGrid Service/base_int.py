import python_http_client


class BaseInterface(object):
    def __init__(self, auth, host, impersonate_subuser):
        """
        Construct the Twilio SendGrid v3 API object.
        Note that the underlying client is being set up during initialization,
        therefore changing attributes in runtime will not affect HTTP client
        behaviour.

        :param auth: the authorization header
        :type auth: string
        :param impersonate_subuser: the subuser to impersonate. Will be passed
                                    by "On-Behalf-Of" header by underlying
                                    client. See
                                    https://sendgrid.com/docs/User_Guide/Settings/subusers.html
                                    for more details
        :type impersonate_subuser: string
        :param host: base URL for API calls
        :type host: string
        """
        from . import __version__
        self.auth = auth
        self.host = host
        self.impersonate_subuser = impersonate_subuser
        self.version = __version__
        self.useragent = 'sendgrid/{};python'.format(self.version)

        self.client = python_http_client.Client(
            host=self.host,
            request_headers=self._default_headers,
            version=3)

    @property
    def _default_headers(self):
        """Set the default header for a Twilio SendGrid v3 API call"""
        headers = {
            "Authorization": self.auth,
            "User-Agent": self.useragent,
            "Accept": 'application/json'
        }
        if self.impersonate_subuser:
            headers['On-Behalf-Of'] = self.impersonate_subuser

        return headers

    def reset_request_headers(self):
        self.client.request_headers = self._default_headers

    def send(self, message):
        """Make a Twilio SendGrid v3 API request with the request body generated by
           the Mail object

        :param message: The Twilio SendGrid v3 API request body generated by the Mail
                        object
        :type message: Mail
        """
        if not isinstance(message, dict):
            message = message.get()

        return self.client.mail.send.post(request_body=message)