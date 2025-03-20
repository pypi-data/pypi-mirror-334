from abc import ABC, abstractmethod
from typing import Any

import pydantic

from .definitions import SupersetDatabaseDef, SupersetMitMDatasetDef, \
    SupersetChartDef, SupersetDashboardDef, SupersetAssetsImport, SupersetDatasetDef, \
    SupersetMitMDatasetImport, SupersetDefFolder, DatasourceIdentifier
from .factories.importable import mk_assets_import, mk_mitm_dataset_import
from ...representation import TableName


class SupersetAssetBundle(SupersetDefFolder, ABC):
    @abstractmethod
    def to_import(self) -> SupersetAssetsImport | SupersetMitMDatasetImport:
        pass

    @property
    def folder_dict(self) -> dict[str, Any]:
        return self.to_import().folder_dict


class SupersetDatasourceBundle(SupersetAssetBundle):
    database: SupersetDatabaseDef
    datasets: list[SupersetDatasetDef] = pydantic.Field(default_factory=list)

    @property
    def placeholder_dataset_identifiers(self) -> dict[TableName, DatasourceIdentifier]:
        return {ds.table_name: DatasourceIdentifier(uuid=ds.uuid) for ds in self.datasets}

    def to_import(self) -> SupersetAssetsImport:
        return mk_assets_import(databases=[self.database], datasets=self.datasets)


class SupersetVisualizationBundle(SupersetAssetBundle):
    charts: list[SupersetChartDef] = pydantic.Field(default_factory=list)
    dashboards: list[SupersetDashboardDef] = pydantic.Field(default_factory=list)

    def to_import(self) -> SupersetAssetsImport:
        return mk_assets_import(charts=self.charts, dashboards=self.dashboards)


class SupersetMitMDatasetBundle(SupersetAssetBundle):
    mitm_dataset: SupersetMitMDatasetDef
    datasource_bundle: SupersetDatasourceBundle
    visualization_bundle: SupersetVisualizationBundle = pydantic.Field(default_factory=SupersetVisualizationBundle)

    def to_import(self) -> SupersetMitMDatasetImport:
        base_assets = mk_assets_import(databases=[self.datasource_bundle.database],
                                       datasets=self.datasource_bundle.datasets,
                                       charts=self.visualization_bundle.charts,
                                       dashboards=self.visualization_bundle.dashboards)
        return mk_mitm_dataset_import(mitm_datasets=[self.mitm_dataset], base_assets=base_assets)
