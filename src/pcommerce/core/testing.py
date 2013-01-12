from plone.testing.z2 import ZSERVER_FIXTURE

import transaction
from Testing import ZopeTestCase as ztc
from OFS.Folder import Folder

from plone.testing import z2

from plone.app.testing import PloneSandboxLayer
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting
from plone.app.testing import applyProfile
from plone.app.testing import quickInstallProduct
from plone.app.testing import ploneSite

class pcommerceCoreTddLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    #We create our own Session
    class Session(dict):
        def set(self, key, value):
            self[key] = value

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import pcommerce.core
        import Products.SingleKeywordWidget
        import pcommerce.shipment.parcel
        import pcommerce.payment.invoice
        import collective.MockMailHost        
        self.loadZCML(package=pcommerce.core)
        self.loadZCML(package=pcommerce.shipment.parcel)
        self.loadZCML(package=pcommerce.payment.invoice)
        self.loadZCML(package=Products.SingleKeywordWidget)
        self.loadZCML(package=collective.MockMailHost)

        # Install product and call its initialize() function
        z2.installProduct(app, 'pcommerce.core')
        z2.installProduct(app, 'pcommerce.shipment.parcel')
        z2.installProduct(app, 'pcommerce.shipment.invoice')
        z2.installProduct(app, 'collective.MockMailHost')

        # Note: you can skip this if my.product is not a Zope 2-style
        # product, i.e. it is not in the Products.* namespace and it
        # does not have a <five:registerPackage /> directive in its
        # configure.zcml.

        # -------------------------------------------------------------------------
        # support for sessions without invalidreferences if using zeo temp storage
        # -------------------------------------------------------------------------
        app.REQUEST['SESSION'] = self.Session()
        if not hasattr(app, 'temp_folder'):
            tf = Folder('temp_folder')
            app._setObject('temp_folder', tf)
            transaction.commit()
        ztc.utils.setupCoreSessions(app)

    def setUpPloneSite(self, portal):
        # Install into Plone site using portal_setup
        quickInstallProduct(portal, 'pcommerce.core')
        quickInstallProduct(portal, 'pcommerce.shipment.parcel')
        quickInstallProduct(portal, 'pcommerce.shipment.invoice')
        quickInstallProduct(portal, 'collective.MockMailHost')

    def tearDownZope(self, app):
        # Uninstall product
        z2.uninstallProduct(app, 'pcommerce.core')
        z2.uninstallProduct(app, 'pcommerce.shipment.parcel')
        z2.uninstallProduct(app, 'pcommerce.shipment.invoice')
        z2.uninstallProduct(app, 'collective.MockMailHost')

PCOMMERCE_TDD_FIXTURE = pcommerceCoreTddLayer()

PCOMMERCE_TDD_INTEGRATION_TESTING = IntegrationTesting(
    bases=(PCOMMERCE_TDD_FIXTURE,),
    name="pcommerceTddLayer:Integration")

PCOMMERCE_TDD_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(PCOMMERCE_TDD_FIXTURE, ZSERVER_FIXTURE),
    name="pcommerceTddLayer:Acceptance")
