from five import grok
from Products.CMFCore.interfaces import IContentish
from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory
import json
grok.templatedir('templates')

class SendAsPDF(grok.View):
    grok.context(IContentish)
    grok.name('send_as_pdf')
    grok.template('send_as_pdf')

    def js(self):
        return '''
            $(document).ready(function () {
                $('#sendaspdf-recipients').tokenInput('%s', {
                      theme: "facebook",
                      tokenDelimiter: "\\n",
                      preventDuplicates: true
                });
            })
        ''' % (self.context.absolute_url() + '/sendaspdf-recipients')


class Recipients(grok.View):
    grok.context(IContentish)
    grok.name('sendaspdf-recipients')

    def render(self):
        self.request.response.setHeader("Content-type", "application/json")

        vocab = getUtility(IVocabularyFactory,
            name='collective.pdfexport.sendaspdfrecipients'
        )(self.context)
        if 'q' in self.request.keys():
            query = self.request['q']
            keys = [(k.value, k.title) for k in vocab if (
                        query.lower() in k.title.lower())]
        else:
            keys = []

        # we will return up to 10 tokens only
        tokens = map(self._tokenize, keys[:10])
        return json.dumps(tokens)

    def _tokenize(self, value_title):
        value, title = value_title
        if isinstance(value, str):
            value = value.decode('utf-8')
            title = title.decode('utf-8')

        return {'id': '%s' % value.replace(u"'", u"\\'"),
                'name': '%s' % title.replace(u"'", u"\\'")}

