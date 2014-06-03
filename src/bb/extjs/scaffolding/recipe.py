import json

from zope.component import getMultiAdapter

from bb.extjs.core import ext
from bb.extjs.scaffolding import interfaces
from bb.extjs.wsgi.interfaces import IRequest
from bb.extjs.core.interfaces import IApplicationContext


EXT_DEFINE_CLASS = 'Ext.define("%s", %s);'


@ext.implementer(interfaces.IScaffoldingRecipe)
class BaseRecipe(ext.MultiAdapter):
    ext.baseclass()
    ext.adapts()

    def buildclass(self, name, extclass):
        return EXT_DEFINE_CLASS % (name, json.dumps(extclass, indent=' '*4),)

    def classname(self, namespace, type, name):
        return '%s.%s.%s' % (namespace, type, name)

    def __init__(self, context, descriptive):
        self.context = context
        self.descriptive = descriptive


class Model(BaseRecipe):
    ext.name('model')
    ext.adapts(IApplicationContext, interfaces.IRecipeDescriptive)

    def __call__(self):
        fields = list()
        for name in self.descriptive.fields:
            zfield = self.descriptive.fields.get(name)
            fields.append(getMultiAdapter((self, zfield,), interfaces.IFieldBuilder)())
        model = dict(extend='Ext.data.Model',
                     fields=fields)
        '%s.model.%s' % (self.context, self.descriptive)
        classname = self.classname(self.context.namespace, 'model', self.descriptive.classname)
        return self.buildclass(classname, model)


class Storage(BaseRecipe):
    ext.name('storage')
    ext.adapts(IApplicationContext, interfaces.IRecipeDescriptive)


class Form(BaseRecipe):
    ext.name('form')
    ext.adapts(IApplicationContext, interfaces.IRecipeDescriptive)


class Display(BaseRecipe):
    ext.name('display')
    ext.adapts(IApplicationContext, interfaces.IRecipeDescriptive)


class Listing(BaseRecipe):
    ext.name('listing')
    ext.adapts(IApplicationContext, interfaces.IRecipeDescriptive)
