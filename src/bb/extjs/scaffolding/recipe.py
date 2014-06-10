import json
from urllib.parse import urlencode

from zope.component import getMultiAdapter

from bb.extjs.core import ext
from bb.extjs.scaffolding import interfaces
from bb.extjs.wsgi.interfaces import IRequest
from bb.extjs.core.interfaces import IApplicationContext
from builtins import super


EXT_DEFINE_CLASS = 'Ext.define("%s", %s);'


class BaseRecipe(ext.MultiAdapter):
    ext.baseclass()
    ext.adapts()

    def __init__(self, context, descriptive):
        self.context = context
        self.descriptive = descriptive

    def buildclass(self, name, extclass):
        return EXT_DEFINE_CLASS % (name, json.dumps(extclass, indent=' '*4),)

    def classname(self, namespace, type, name):
        return '%s.%s.%s' % (namespace, type, name)


@ext.implementer(interfaces.IScaffoldingRecipeModel)
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


@ext.implementer(interfaces.IScaffoldingRecipeStore)
class Storage(BaseRecipe):
    ext.name('store')
    ext.adapts(IApplicationContext, interfaces.IRecipeDescriptive)
    
    def __init__(self, context, descriptive):
        super(Storage, self).__init__(context, descriptive)
        self.model = self.descriptive.classname

    def __call__(self):
        modelclass = self.classname(self.context.namespace, 'model', self.model)
        store = dict(extend='Ext.data.Store',
                     requires=modelclass,
                     autoLoad=False,
                     autoSync=True,
                     storeId=self.descriptive.classname,
                     model=modelclass,
                     proxy=dict(type='ajax',
                                pageParam=None,
                                startParam=None,
                                limitParam=None,
                                api=dict(read=self.url('read'),
                                         update=self.url('update'),
                                         destroy=self.url('destroy')
                                         )
                                ),
                                reader=dict(type='json',
                                            root='data'
                                            ),
                                writer=dict(type='json',
                                            root='data'
                                            )
                     )
        '%s.store.%s' % (self.context, self.descriptive)
        classname = self.classname(self.context.namespace, 'store', self.descriptive.classname)
        return self.buildclass(classname, store)

    def url(self, crud):
        return 'data/%s' % urlencode(dict(entity=self.model, crud=crud))


@ext.implementer(interfaces.IScaffoldingRecipeForm)
class Form(BaseRecipe):
    ext.name('form')
    ext.adapts(IApplicationContext, interfaces.IRecipeDescriptive)

    def __call__(self):
        items = list()
        for name in self.descriptive.fields:
            zfield = self.descriptive.fields.get(name)
            items.append(getMultiAdapter((self, zfield,), interfaces.IFieldBuilder)())
        model = dict(extend='Ext.form.Panel',
                     alias='widget.Form%s' % self.descriptive.classname,
                     items=items,
                     title=self.descriptive.title)
        '%s.form.%s' % (self.context, self.descriptive)
        classname = self.classname(self.context.namespace, 'form', self.descriptive.classname)
        return self.buildclass(classname, model)


@ext.implementer(interfaces.IScaffoldingRecipeDisplay)
class Display(BaseRecipe):
    ext.name('display')
    ext.adapts(IApplicationContext, interfaces.IRecipeDescriptive)


@ext.implementer(interfaces.IScaffoldingRecipeGrid)
class Grid(BaseRecipe):
    ext.name('grid')
    ext.adapts(IApplicationContext, interfaces.IRecipeDescriptive)

    def __call__(self):
        columns = list()
        for name in self.descriptive.fields:
            zfield = self.descriptive.fields.get(name)
            columns.append(getMultiAdapter((self, zfield,), interfaces.IFieldBuilder)())
        model = dict(extend='Ext.grid.Panel',
                     storeId=self.descriptive.classname,
                     alias='widget.Grid%s' % self.descriptive.classname,
                     columns=columns,
                     title=self.descriptive.title)
        '%s.grid.%s' % (self.context, self.descriptive)
        classname = self.classname(self.context.namespace, 'grid', self.descriptive.classname)
        return self.buildclass(classname, model)
