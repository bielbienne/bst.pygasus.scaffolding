from bb.extjs.core import ext
from bb.extjs.scaffolding.interfaces import IFieldBuilder


@ext.implementer(IFieldBuilder)
class BuilderBase(ext.MultiAdapter):
    ext.baseclass()

    def __init__(self, recipe, field):
        self.recipe = recipe
        self.field = field
