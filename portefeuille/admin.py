from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from portefeuille.models import Portefeuille, Stock, BaseOF, BaseOperation, BaseNomenclature, StockGobal


@admin.register(Stock)
class StockAdmin(ImportExportModelAdmin):
    pass


@admin.register(Portefeuille)
class PortefeuilleAdmin(ImportExportModelAdmin):
    pass


@admin.register(BaseOF)
class BaseOFAdmin(ImportExportModelAdmin):
    pass


@admin.register(BaseOperation)
class BaseOperationAdmin(ImportExportModelAdmin):
    pass


@admin.register(BaseNomenclature)
class BaseNomenclatureAdmin(ImportExportModelAdmin):
    pass


@admin.register(StockGobal)
class StockGobalAdmin(ImportExportModelAdmin):
    pass
