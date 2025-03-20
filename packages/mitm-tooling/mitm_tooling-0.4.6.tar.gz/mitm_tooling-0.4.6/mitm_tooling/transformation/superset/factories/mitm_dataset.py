from uuid import UUID

from mitm_tooling.definition import MITM
from ..common import name_plus_uuid
from ..definitions import SupersetMitMDatasetDef
from ..factories.utils import mk_uuid


def mk_mitm_dataset(name: str, mitm: MITM, database_uuid: UUID, uuid: UUID | None = None, uniquify_name: bool = False) -> SupersetMitMDatasetDef:
    uuid = uuid or mk_uuid()
    if uniquify_name:
        name = name_plus_uuid(name, uuid)
    return SupersetMitMDatasetDef(
        dataset_name=name,
        mitm=mitm,
        database_uuid=database_uuid,
        uuid=uuid or mk_uuid()
    )
