from zope.interface import Interface


class IScaffoldingRecipe(Interface):
    """ Take the logic to build scaffolding
        elements, like extjs store, model..
    """
    
    def __init__(self, context, description):
        pass
    
    def __call__(self):
        pass


class IRecipeDescription(Interface):
    """ Define a description for each recipe.
    """


class IRecipeDescriptionModel(IRecipeDescription):
    pass
    

class IRecipeDescriptionStorage(IRecipeDescription):
    pass


class IRecipeDescriptionForm(IRecipeDescription):
    pass


class IRecipeDescriptionDisplay(IRecipeDescription):
    pass


class IRecipeDescriptionListing(IRecipeDescription):
    pass


class IRecipeDescriptionGeneric(IRecipeDescriptionModel,
                                IRecipeDescriptionStorage,
                                IRecipeDescriptionForm,
                                IRecipeDescriptionDisplay,
                                IRecipeDescriptionListing):
    pass