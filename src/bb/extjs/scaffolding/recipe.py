from bb.extjs.core import ext
from bb.extjs.scaffolding import interfaces
from bb.extjs.wsgi.interfaces import IRequest
from bb.extjs.core.interfaces import IApplicationContext



@ext.implementer(interfaces.IScaffoldingRecipe)
class BaseRecipe(ext.MultiAdapter):
    ext.baseclass()
    ext.adapts()

    def __init__(self, context, description):
        self.context = context
        self.description = description


class Model(BaseRecipe):
    ext.name('model')
    ext.adapts(IApplicationContext, interfaces.IRecipeDescriptionModel)

    def __call__(self):
        return 'to do :-)'


class Storage(BaseRecipe):
    ext.name('storage')
    ext.adapts(IApplicationContext, interfaces.IRecipeDescriptionStorage)


class Form(BaseRecipe):
    ext.name('form')
    ext.adapts(IApplicationContext, interfaces.IRecipeDescriptionForm)


class Display(BaseRecipe):
    ext.name('display')
    ext.adapts(IApplicationContext, interfaces.IRecipeDescriptionDisplay)


class Listing(BaseRecipe):
    ext.name('listing')
    ext.adapts(IApplicationContext, interfaces.IRecipeDescriptionListing)
