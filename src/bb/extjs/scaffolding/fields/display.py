import json
from zope import schema
from zope.i18n import translate
from zope.schema.vocabulary import getVocabularyRegistry

from bb.extjs.core import ext
from bb.extjs.scaffolding import loader
from bb.extjs.scaffolding.fields import BuilderBase
from bb.extjs.scaffolding.interfaces import IScaffoldingRecipeDisplay

from genshi.template import NewTextTemplate

class BuilderDefaultForm(BuilderBase):
    ext.adapts(IScaffoldingRecipeDisplay, schema.interfaces.IField)

    def __call__(self):
        di = dict(xtype='displayfield',
                  name=self.field.getName(),
                  fieldLabel=translate(self.field.title,
                                       context=self.recipe.request)
                  )
        return json.dumps(di, indent=' ' * 4)


class ChoiceField(BuilderDefaultForm):
    ext.adapts(IScaffoldingRecipeDisplay, schema.interfaces.IChoice)

    def __call__(self):
        di = json.loads(super(ChoiceField, self).__call__())
        di['renderer'] = '%renderer%'
        di = json.dumps(di, indent=' ' * 4)

        # Render the template
        tmpl = loader.load('combobox_renderer.json.tpl', cls=NewTextTemplate)
        stream = tmpl.generate(view=self)
        di = di.replace('"%renderer%"', stream.render())
        return di

    @property
    def terms(self):
        vr = getVocabularyRegistry()
        vocabular = vr.get(None, self.field.vocabularyName)
        terms = list()
        for voc in vocabular:
            terms.append(voc)
        return terms
