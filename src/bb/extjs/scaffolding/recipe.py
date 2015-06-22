import json
from urllib.parse import urljoin

from zope.component import getMultiAdapter
from zope.schema import getFieldsInOrder

from bb.extjs.core import ext
from bb.extjs.scaffolding import interfaces
from bb.extjs.wsgi.interfaces import IRequest
from bb.extjs.core.interfaces import IBaseUrl
from bb.extjs.core.interfaces import IApplicationContext
from bb.extjs.scaffolding import loader
from builtins import super

from genshi.template import NewTextTemplate

# !!! for this module we use OrderedDict as dict !!!
from collections import OrderedDict as dict

CLASS_NAMESPACE = 'scaffolding'
EXT_DEFINE_CLASS = 'Ext.define("%s", %s);'


class BaseRecipe(ext.MultiAdapter):
    ext.baseclass()
    ext.adapts()

    def __init__(self, context, descriptive, request):
        self.context = context
        self.descriptive = descriptive
        self.request = request

    def buildclass(self, name, extclass):
        return EXT_DEFINE_CLASS % (name, json.dumps(extclass, indent=' ' * 4),)

    def classname(self, namespace, type, name):
        return '%s.%s.%s' % (namespace, type, name)

    def render_template(self, tpl_name):
        tmpl = loader.load(tpl_name, cls=NewTextTemplate)
        stream = tmpl.generate(view=self)
        return stream.render()


@ext.implementer(interfaces.IScaffoldingRecipeModel)
class Model(BaseRecipe):
    ext.name('model')
    ext.adapts(IApplicationContext, interfaces.IRecipeDescriptive, IRequest)

    def __call__(self):
        fields = list()
        for name, zfield in getFieldsInOrder(self.descriptive.interface):
            fields.append(getMultiAdapter((self, zfield,), interfaces.IFieldBuilder)())
        model = dict(extend='Ext.data.Model',
                     fields=fields)
        classname = self.classname(CLASS_NAMESPACE, 'model', self.descriptive.classname)
        return self.buildclass(classname, model)


class BaseStore(BaseRecipe):
    ext.baseclass()
    ext.adapts(IApplicationContext, interfaces.IRecipeDescriptive, IRequest)

    def __init__(self, context, descriptive, request):
        super(BaseStore, self).__init__(context, descriptive, request)
        self.model = self.descriptive.classname
        self.storeattrs = dict(extend='Ext.data.Store',
                               alias=self.descriptive.classname,
                               requires='',
                               autoLoad=True,
                               autoSync=True,
                               storeId=self.descriptive.classname,
                               model='',
                               batchMode=False,
                               pageSize=100,
                               remoteSort=True,
                               # seems to be very buggy
                               # http://www.sencha.com/forum/showthread.php?267654-Buffered-store-findRecord-does-not-work-in-4.2.1
                               buffered=False,
                               proxy=dict(type='rest',
                                          pageParam=None,
                                          batchActions=True,
                                          url=self.url(),
                                          reader=dict(type='json',
                                                      root='data'
                                                      ),
                                          writer=dict(type='json',
                                                      root='data'
                                                      )
                                          ),
                               )

    def __call__(self):
        modelclass = self.classname(CLASS_NAMESPACE, 'model', self.model)
        self.storeattrs['requires'] = modelclass
        self.storeattrs['model'] = modelclass
        classname = self.classname(CLASS_NAMESPACE, 'store', self.descriptive.classname)
        return self.buildclass(classname, self.storeattrs)

    def url(self):
        return IBaseUrl(self.request).url('data/%s' % self.model)


@ext.implementer(interfaces.IScaffoldingRecipeStore)
class Store(BaseStore):
    ext.name('store')
    ext.adapts(IApplicationContext, interfaces.IRecipeDescriptive, IRequest)


@ext.implementer(interfaces.IScaffoldingRecipeBufferedStore)
class BufferedStore(BaseStore):
    ext.name('bufferedstore')
    ext.adapts(IApplicationContext, interfaces.IRecipeDescriptive, IRequest)

    def __call__(self):
        modelclass = self.classname(CLASS_NAMESPACE, 'model', self.model)
        self.storeattrs['requires'] = modelclass
        self.storeattrs['model'] = modelclass
        self.storeattrs['buffered'] = True
        self.storeattrs['autoSync'] = False
        self.storeattrs['alias'] = 'Buffered%s' % self.descriptive.classname
        self.storeattrs['storeId'] = 'Buffered%s' % self.descriptive.classname
        classname = self.classname(CLASS_NAMESPACE, 'bufferedstore', self.descriptive.classname)
        return self.buildclass(classname, self.storeattrs)


class BaseForm(BaseRecipe):
    ext.baseclass()
    ext.adapts(IApplicationContext, interfaces.IRecipeDescriptive, IRequest)

    aliasprefix = 'Form'

    def __call__(self):
        return self.render_template('form.json.tpl')

    @property
    def title(self):
        return self.descriptive.title

    @property
    def items(self):
        items = list()
        for name, zfield in getFieldsInOrder(self.descriptive.interface):
            items.append(str(getMultiAdapter((self, zfield,), interfaces.IFieldBuilder)()))
        return items

    @property
    def name(self):
        return self.classname(CLASS_NAMESPACE, self.aliasprefix.lower(), self.descriptive.classname)


@ext.implementer(interfaces.IScaffoldingRecipeForm)
class Form(BaseForm):
    ext.name('form')
    ext.adapts(IApplicationContext, interfaces.IRecipeDescriptive, IRequest)


@ext.implementer(interfaces.IScaffoldingRecipeDisplay)
class Display(BaseForm):
    ext.name('display')
    ext.adapts(IApplicationContext, interfaces.IRecipeDescriptive, IRequest)

    aliasprefix = 'Display'


@ext.implementer(interfaces.IScaffoldingRecipeGrid)
class Grid(BaseRecipe):
    ext.name('grid')
    ext.adapts(IApplicationContext, interfaces.IRecipeDescriptive, IRequest)

    def __call__(self):
        classname = self.classname(CLASS_NAMESPACE, 'grid', self.descriptive.classname)
        output = self.buildclass(classname, self.build())
        return self.create_store(output)

    def create_store(self, output):
        name = self.classname(CLASS_NAMESPACE, 'bufferedstore', self.descriptive.classname)
        newstore = 'Ext.create("%s")' % name
        return output.replace('"%store%"', newstore)

    def build(self):
        columns = list()
        for name, zfield in getFieldsInOrder(self.descriptive.interface):
            columns.append(getMultiAdapter((self, zfield,), interfaces.IFieldBuilder)())
        return dict(extend='Ext.grid.Panel',
                    requires=self.classname(CLASS_NAMESPACE, 'bufferedstore', self.descriptive.classname),
                    store='%store%',
                    alias='widget.Grid%s' % self.descriptive.classname,
                    columns=columns,
                    title=self.descriptive.title)


@ext.implementer(interfaces.IScaffoldingRecipeEditGrid)
class EditGrid(Grid):
    ext.name('editgrid')
    ext.provides(interfaces.IScaffoldingRecipeEditGrid)
    ext.adapts(IApplicationContext, interfaces.IRecipeDescriptive, IRequest)

    def __call__(self):
        classname = self.classname(CLASS_NAMESPACE, 'editgrid', self.descriptive.classname)
        grid = self.build()
        grid.update(dict(alias='widget.EditGrid%s' % self.descriptive.classname,
                         plugins=['%plugins%']))
        output = 'var rowEditing = Ext.create("Ext.grid.plugin.RowEditing");\n'
        output += self.buildclass(classname, grid)
        # QD: this may be rewrite with a proper solution
        output = output.replace('"%plugins%"', 'rowEditing')
        return self.create_store(output)
