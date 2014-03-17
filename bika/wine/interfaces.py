from zope.interface import Interface


class ICountry(Interface):
    """Country, used for wine-region selection"""


class IRegions(Interface):
    """Regions configuration folder"""


class IRegion(Interface):
    """Region, used for wine-region selection"""


class ICultivars(Interface):
    """Cultivars configuration folder"""


class ICultivar(Interface):
    """Cultivar"""


class IWineTypes(Interface):
    """Wine types configuration folder"""


class IWineType(Interface):
    """Wine type"""


class ITransportConditions(Interface):
    """Transprt Conditions configuration folder"""


class ITransportCondition(Interface):
    """Transport condition"""


class IStorageConditions(Interface):
    """Storage conditions configuration folder"""


class IStorageCondition(Interface):
    """Storage condition"""
