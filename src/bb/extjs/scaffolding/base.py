from grokcore.component import Adapter
from grokcore.component import baseclass
from grokcore.component import context
from zope.interface import implementer

from bb.extjs.core.interfaces import IApplicationContext
from bb.extjs.scaffolding.interfaces import IRecipeDescriptive



@implementer(IRecipeDescriptive)
class Scaffolding(Adapter):
    """ base class for all recipe Description that
        will build the scaffolding for ExtJs.
    """
    baseclass()
    context(IApplicationContext)
