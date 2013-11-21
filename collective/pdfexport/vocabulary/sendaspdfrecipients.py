from five import grok
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.schema.interfaces import IVocabularyFactory
from zope.component import getUtility
from z3c.formwidget.query.interfaces import IQuerySource
from plone import api

class SendAsPDFRecipients(grok.GlobalUtility):
    grok.name('collective.pdfexport.sendaspdfrecipients')
    grok.implements(IVocabularyFactory)

    def __call__(self, context):
        vocab = getUtility(IVocabularyFactory,
                name='plone.principalsource.Users')(context)
        values = set()
        for i in vocab:
            user = api.user.get(i.value)
            if not user:
                continue
            fullname = user.getProperty('fullname')
            email = user.getProperty('email')
            if not email:
                continue
            value = '%s <%s>' % (fullname, email)
            values.add(value)
        terms = [SimpleTerm(value=v, title=v) for v in values]
        return SimpleVocabulary(terms)
