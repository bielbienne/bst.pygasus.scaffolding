import json
from urllib.parse import urljoin

from zope.component import getMultiAdapter
from zope.schema import getFieldsInOrder

from bb.extjs.core import ext
from bb.extjs.scaffolding import interfaces
from bb.extjs.wsgi.interfaces import IRequest
from bb.extjs.core.interfaces import IApplicationContext
from builtins import super


# !!! for this module we use OrderedDict as dict !!!
from collections import OrderedDict as dict

CLASS_NAMESPACE = 'scaffolding'
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
        for name, zfield in getFieldsInOrder(self.descriptive.fields):
            fields.append(getMultiAdapter((self, zfield,), interfaces.IFieldBuilder)())
        model = dict(extend='Ext.data.Model',
                     fields=fields)
        '%s.model.%s' % (self.context, self.descriptive)
        classname = self.classname(CLASS_NAMESPACE, 'model', self.descriptive.classname)
        return self.buildclass(classname, model)


@ext.implementer(interfaces.IScaffoldingRecipeStore)
class Store(BaseRecipe):
    ext.name('store')
    ext.adapts(IApplicationContext, interfaces.IRecipeDescriptive)
    
    def __init__(self, context, descriptive):
        super(Store, self).__init__(context, descriptive)
        self.model = self.descriptive.classname

    def __call__(self):
        modelclass = self.classname(CLASS_NAMESPACE, 'model', self.model)
        store = dict(extend='Ext.data.Store',
                     alias=self.descriptive.classname,
                     requires=modelclass,
                     autoLoad=True,
                     autoSync=True,
                     storeId=self.descriptive.classname,
                     model=modelclass,
                     batchMode=False,
                     pageSize=100,
                     remoteSort=True,
                     # seems to be very buggy
                     # http://www.sencha.com/forum/showthread.php?267654-Buffered-store-findRecord-does-not-work-in-4.2.1
                     buffered=False,
                     proxy=dict(type='rest',
                                pageParam=None,
                                url=self.url(),
                                reader=dict(type='json',
                                            root='data'
                                            ),
                                writer=dict(type='json',
                                            root='data'
                                            )
                                ),
                     )
        '%s.store.%s' % (self.context, self.descriptive)
        classname = self.classname(CLASS_NAMESPACE, 'store', self.descriptive.classname)
        return self.buildclass(classname, store)

    def url(self):
        return 'data/%s' % self.model


@ext.implementer(interfaces.IScaffoldingRecipeForm)
class Form(BaseRecipe):
    ext.name('form')
    ext.adapts(IApplicationContext, interfaces.IRecipeDescriptive)

    def __call__(self):
        items = list()
        for name, zfield in getFieldsInOrder(self.descriptive.fields):
            items.append(getMultiAdapter((self, zfield,), interfaces.IFieldBuilder)())
        model = dict(extend='Ext.form.Panel',
                     alias='widget.Form%s' % self.descriptive.classname,
                     items=items,
                     title=self.descriptive.title)
        '%s.form.%s' % (self.context, self.descriptive)
        classname = self.classname(CLASS_NAMESPACE, 'form', self.descriptive.classname)
        return self.buildclass(classname, model)


@ext.implementer(interfaces.IScaffoldingRecipeDisplay)
class Display(BaseRecipe):
    ext.name('display')
    ext.adapts(IApplicationContext, interfaces.IRecipeDescriptive)
    
    def __call__(self):
        raise NotImplementedError('display is not implemented at the moment')


@ext.implementer(interfaces.IScaffoldingRecipeGrid)
class Grid(BaseRecipe):
    ext.name('grid')
    ext.adapts(IApplicationContext, interfaces.IRecipeDescriptive)

    def __call__(self):
        classname = self.classname(CLASS_NAMESPACE, 'grid', self.descriptive.classname)
        return self.buildclass(classname, self.build())
    
    def build(self):
        columns = list()
        for name, zfield in getFieldsInOrder(self.descriptive.fields):
            columns.append(getMultiAdapter((self, zfield,), interfaces.IFieldBuilder)())
        return dict(extend='Ext.grid.Panel',
                     requires=self.classname(CLASS_NAMESPACE, 'store', self.descriptive.classname),
                     store=self.classname(CLASS_NAMESPACE, 'store', self.descriptive.classname),
                     alias='widget.Grid%s' % self.descriptive.classname,
                     columns=columns,
                     title=self.descriptive.title)


@ext.implementer(interfaces.IScaffoldingRecipeEditGrid)
class EditGrid(Grid):
    ext.name('editgrid')
    ext.provides(interfaces.IScaffoldingRecipeEditGrid)
    ext.adapts(IApplicationContext, interfaces.IRecipeDescriptive)
    
    def __call__(self):
        classname = self.classname(CLASS_NAMESPACE, 'editgrid', self.descriptive.classname)
        grid = self.build()
        grid.update(dict(alias='widget.EditGrid%s' % self.descriptive.classname,
                         plugins=['%plugins%']))
        output = 'var rowEditing = Ext.create("Ext.grid.plugin.RowEditing");\n'
        output += self.buildclass(classname, grid)
        # QD: this may be rewrite with a proper solution
        output = output.replace('"%plugins%"', 'rowEditing')
        return output


