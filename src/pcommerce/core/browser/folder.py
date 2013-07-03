import pkg_resources

from Acquisition import aq_inner, aq_parent

from zope.interface import implements

from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from Products.ATContentTypes.interface.image import IImageContent

from plone.memoize.instance import memoize
try:
    pkg_resources.get_distribution('plone.batching')
    from plone.batching import Batch
    from plone import batching
    batching_path = "/".join(batching.__path__)
    batchingfile = '%s/batchnavigation.pt' % batching_path
    HAS_PLONE43 = True
except:
    # Plone <= 4.2
    from plone.app.content import browser
    from plone.app.content.batching import Batch
    batching_path = '/'.join(browser.__path__)
    batchingfile = '%s/batching.pt' % batching_path
    HAS_PLONE43 = False

from pcommerce.core.interfaces import IPricing, IShopFolder, IShop, IProduct
from pcommerce.core.currency import CurrencyAware


class ShopHome(BrowserView):
    """ shop home view
    """
    implements(IShop)
    
    template = ViewPageTemplateFile('folder.pt')

    def __call__(self):
        return self.template()

class ShopFolderListing(BrowserView):
    """ shop folder listing
    """
    implements(IShopFolder)

    template = ViewPageTemplateFile('folder.pt')
    batching = ViewPageTemplateFile(batchingfile)

    def __call__(self):
        self.page = int(self.request.get('pagenumber', 1))
        self.url = self.context.absolute_url()
        return self.template()

    @property
    @memoize
    def batch(self):
        catalog = getToolByName(self.context, 'portal_catalog')
        portal_properties = getToolByName(self.context, 'portal_properties')
        use_view_action = portal_properties.site_properties.getProperty('typesUseViewActionInListings', ())
        props = portal_properties.pcommerce_properties
        columns = int(props.getProperty('columns', 3))
        width = int(props.getProperty('thumb_width', 0))
        width = width and 'image/thumb?width=%s' % width or 'image_thumb'
        results = catalog(object_provides=IProduct.__identifier__, path={'query': '/'.join(self.context.getPhysicalPath()), 'depth': 1}, sort_on='getObjPositionInParent')
        items = []
        i = 0
        start = (self.page-1) * (columns * 5)
        end = start + columns * 5
        for item in results:
            url = item.getURL()
            if item.portal_type in use_view_action:
                url += '/view'

            if start <= i < end:
                object = item.getObject()
                col = i % columns + 1
                adapter = IPricing(object)
                image = None
                if object.getImage():
                    image = {'caption': object.getImageCaption(),
                             'thumb': '%s/%s' % (item.getURL(), width)}

                item = {'uid': item.UID,
                        'class': 'col%s' % col,
                        'title': item.Title,
                        'description': item.Description,
                        'price': CurrencyAware(adapter.getPrice()),
                        'base_price': CurrencyAware(adapter.getBasePrice()),
                        'offer': adapter.getPrice() < adapter.getBasePrice(),
                        'image': image,
                        'url': url}
            else:
                item = {'uid': item.UID,
                        'title': item.Title,
                        'description': item.Description,
                        'url': url}
            i += 1
            items.append(item)
        #different API - plone.batching
        #http://stackoverflow.com/questions/16165446/from-plone-app-content-batching-import-batch-fails-with-importerror-no-module-n 
        if HAS_PLONE43:
            return Batch(items, size=columns * 5, start=0, end=0, orphan=0, overlap=0, pagerange=7)
        else:
            return Batch(items, pagesize=columns * 5, pagenumber=self.page, navlistsize=5)

    @property
    @memoize
    def multiple_pages(self):
        return self.batch.size > self.batch.pagesize
