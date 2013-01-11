from plone.testing import z2

from plone.app.testing import PloneSandboxLayer
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting
from plone.app.testing import applyProfile
from plone.app.testing import quickInstallProduct
from plone.app.testing import ploneSite

class pcommerceCoreTddLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import pcommerce.core
        import Products.SingleKeywordWidget
        import pcommerce.shipment.parcel
        import pcommerce.payment.invoice
        self.loadZCML(package=pcommerce.core)
        self.loadZCML(package=Products.SingleKeywordWidget)

        # Install product and call its initialize() function
        z2.installProduct(app, 'pcommerce.core')
        z2.installProduct(app, 'pcommerce.shipment.parcel')
        z2.installProduct(app, 'pcommerce.shipment.invoice')

        # Note: you can skip this if my.product is not a Zope 2-style
        # product, i.e. it is not in the Products.* namespace and it
        # does not have a <five:registerPackage /> directive in its
        # configure.zcml.

    def setUpPloneSite(self, portal):
        # Install into Plone site using portal_setup
        quickInstallProduct(portal, 'pcommerce.core')
        quickInstallProduct(portal, 'pcommerce.shipment.parcel')
        quickInstallProduct(portal, 'pcommerce.shipment.invoice')

    def tearDownZope(self, app):
        # Uninstall product
        z2.uninstallProduct(app, 'pcommerce.core')
        z2.uninstallProduct(app, 'pcommerce.shipment.parcel')
        z2.uninstallProduct(app, 'pcommerce.shipment.invoice')

PCOMMERCE_TDD_FIXTURE = pcommerceCoreTddLayer()
PCOMMERCE_TDD_INTEGRATION_TESTING = IntegrationTesting(
    bases=(PCOMMERCE_TDD_FIXTURE,),
    name="pcommerceTddLayer:Integration")
