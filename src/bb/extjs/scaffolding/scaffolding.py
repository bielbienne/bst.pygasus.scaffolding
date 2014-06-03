import re
import fanstatic
from webob.exc import HTTPNotFound

from zope.component import queryAdapter
from zope.component import queryMultiAdapter

from bb.extjs.core import ext
from bb.extjs.core.interfaces import IApplicationContext

from bb.extjs.wsgi.interfaces import IRequest
from bb.extjs.wsgi.interfaces import IRootDispatcher

from bb.extjs.scaffolding.interfaces import IRecipeDescriptive
from bb.extjs.scaffolding.interfaces import IScaffoldingRecipe



REGEX_URL = re.compile(r'^\/scaffolding\/([A-z_]*)\/([A-z_]*)\..*')


@ext.implementer(IRootDispatcher)
class ScaffoldinglEntryPoint(ext.MultiAdapter):
    """ generate a index html. This html site will than
        load extjs framework with css and run the
        application.
    """
    ext.name('scaffolding')
    ext.adapts(IApplicationContext, IRequest)
    
    
    def __init__(self, context, request):
        self.context = context
        self.request = request
    
    def __call__(self):
        match = REGEX_URL.match(self.request.path_info)
        if match is None:
            raise HTTPNotFound()
        recipename, descname = match.groups()
        recipename, descname = recipename.lower(), descname.lower()
        
        description = queryAdapter(self.context, IRecipeDescriptive, descname)
        if description is None:
            raise HTTPNotFound('No scaffolding for %s' % descname)
        recipe = queryMultiAdapter((self.context, description), IScaffoldingRecipe, recipename)
        if recipe is None:
            raise Exception('Missing Recipe to generate Exjs %s' % recipename)
        
        self.request.response.content_type='application/javascript'
        self.request.response.write(recipe())
