from five import grok
from collective.pdfexport.interfaces import IPDFConverter, IPDFHTMLProvider
import os
from StringIO import StringIO
import pdfkit

class PDFKitPDFConverter(grok.GlobalUtility):
    grok.implements(IPDFConverter)

    def __init__(self):
        path = os.environ.get('WKHTMLTOPDF_PATH', None)
        if path:
            config = pdfkit.configuration(wkhtmltopdf=path)
        else:
            config = pdfkit.configuration()
        self.config = config


    def _options(self):
        opts = {
            '--print-media-type': None,
            '--disable-javascript': None,
            '--quiet': None,
        }

        auth = os.environ.get('WKHTMLTOPDF_HTTPAUTH', None)
        if auth:
            username, password = auth.split(':', 1)
            opts['--username'] = username
            opts['--password'] = password
        return opts

    def convert(self, content, view=None):
        item = IPDFHTMLProvider(content)
        html = item.pdf_html(view=view)
        out = pdfkit.from_string(html, 
            False, 
            options=self._options(), 
            configuration=self.config
        )
        return StringIO(out)


