import json
from zope import schema
from zope.i18n import translate

from bb.extjs.core import ext
from bb.extjs.scaffolding.fields import BuilderBase
from bb.extjs.scaffolding.interfaces import IScaffoldingRecipeDisplay


class BuilderDefaultForm(BuilderBase):
    ext.adapts(IScaffoldingRecipeDisplay, schema.interfaces.IField)

    def __call__(self):
        di = dict(xtype='displayfield',
                  name=self.field.getName(),
                  fieldLabel=translate(self.field.title,
                                       context=self.recipe.request)
                  )
        return json.dumps(di, indent=' ' * 4)
