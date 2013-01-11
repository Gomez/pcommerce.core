import unittest2 as unittest

from zope.component import getUtility

from plone.app.testing import PloneSandboxLayer
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting
from plone.app.testing import applyProfile
from plone.app.testing import quickInstallProduct
from plone.app.testing import ploneSite
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import SITE_OWNER_NAME, SITE_OWNER_PASSWORD

from plone.testing.z2 import Browser

from Products.CMFCore.utils import getToolByName

from pcommerce.core.testing import PCOMMERCE_TDD_INTEGRATION_TESTING

class PcommerceTest(unittest.TestCase):

    layer = PCOMMERCE_TDD_INTEGRATION_TESTING
    
    def test_pcommerce_content_type_installed(self):
        portal = self.layer['portal']
        typesTool = getToolByName(portal, 'portal_types')
        self.assertNotEqual(typesTool.getTypeInfo('Product'), None)
 
    def test_content_creation(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ['Manager'])
        portal.invokeFactory('Product', 'TestProduct', shipments='pcommerce.shipment.parcel',title='TestProduct')
        product = portal['TestProduct']
        self.assertEqual(product.Title(), u"TestProduct")

