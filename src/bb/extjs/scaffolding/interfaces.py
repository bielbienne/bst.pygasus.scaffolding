from zope.interface import Interface


class IScaffoldingRecipe(Interface):
    """ Take the logic to build scaffolding
        elements, like extjs store, model..
    """
    
    def __init__(self, context, description):
        pass
    
    def __call__(self):
        pass


class IScaffoldingRecipeModel(IScaffoldingRecipe):
    pass


class IScaffoldingRecipeStore(IScaffoldingRecipe):
    pass


class IScaffoldingRecipeForm(IScaffoldingRecipe):
    pass


class IScaffoldingRecipeDisplay(IScaffoldingRecipe):
    pass


class IScaffoldingRecipeGrid(IScaffoldingRecipe):
    pass


class IRecipeDescriptive(Interface):
    """ Define a description for each recipe.
    """


class IFieldBuilder(Interface):
    """
    """

    def __init__(self, recipe, field):
        pass
    
    def __call__(self):
        pass