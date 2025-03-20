import logging
from typing import Optional

from twisted.internet.defer import inlineCallbacks
from vortex.DeferUtil import deferToThreadWrapWithLogger
from vortex.Payload import Payload
from vortex.TupleSelector import TupleSelector
from vortex.handler.TupleDataObservableHandler import TuplesProviderABC

from peek_plugin_base.storage.DbConnection import DbSessionCreator
from peek_plugin_diagram._private.lookup_type_maps import (
    lookupTypeTableEnumToTable,
)
from peek_plugin_diagram._private.lookup_type_maps import (
    lookupTypeTableToImportTuple,
)
from peek_plugin_diagram._private.storage.Lookups import DispLevelTable
from peek_plugin_diagram._private.storage.ModelSet import getOrCreateCoordSet
from peek_plugin_diagram._private.storage.ModelSet import getOrCreateModelSet
from peek_plugin_diagram._private.tuples.admin.private_diagram_lookup_list_tuple import (
    PrivateDiagramLookupListTuple,
)
from peek_plugin_diagram.tuples.lookups.ImportDispColorTuple import (
    ImportDispColorTuple,
)
from peek_plugin_diagram.tuples.lookups.ImportDispLayerTuple import (
    ImportDispLayerTuple,
)
from peek_plugin_diagram.tuples.lookups.ImportDispLevelTuple import (
    ImportDispLevelTuple,
)
from peek_plugin_diagram.tuples.lookups.ImportDispLineStyleTuple import (
    ImportDispLineStyleTuple,
)
from peek_plugin_diagram.tuples.lookups.ImportDispTextStyleTuple import (
    ImportDispTextStyleTuple,
)


logger = logging.getLogger(__name__)


class PrivateDiagramLookupListTupleProvider(TuplesProviderABC):
    def __init__(self, dbSessionCreator: DbSessionCreator):
        self._dbSessionCreator = dbSessionCreator

    @inlineCallbacks
    def makeVortexMsg(self, filt: dict, tupleSelector: TupleSelector) -> bytes:
        modelSetKey = tupleSelector.selector["modelSetKey"]
        coordSetKey = tupleSelector.selector.get("coordSetKey")
        lookupType = tupleSelector.selector["lookupType"]

        assert lookupType in lookupTypeTableToImportTuple, (
            "DiagramLookupListTupleProvider, "
            "lookupType '%s' not in typeMap" % lookupType
        )

        lookupTuples = yield self._getLookups(
            modelSetKey=modelSetKey,
            coordSetKey=coordSetKey,
            lookupType=lookupType,
        )

        tuples = [
            PrivateDiagramLookupListTuple(
                id=t.id, key=t.importHash, name=self._makeName(t)
            )
            for t in lookupTuples
        ]

        payloadEnvelope = yield Payload(
            filt, tuples=tuples
        ).makePayloadEnvelopeDefer()
        vortexMsg = yield payloadEnvelope.toVortexMsgDefer()
        return vortexMsg

    def _makeName(self, lookup) -> str:
        if isinstance(lookup, ImportDispColorTuple):
            return f"{lookup.name} ({lookup.darkColor}/{lookup.lightColor})"
        elif isinstance(lookup, ImportDispLayerTuple):
            return (
                f"{lookup.name} ({lookup.order},"
                f" {'' if lookup.visible else 'not '}visible)"
            )
        elif isinstance(lookup, ImportDispLevelTuple):
            return (
                f"{lookup.name} ({lookup.order},"
                f" {lookup.minZoom} to {lookup.maxZoom})"
            )
        elif isinstance(lookup, ImportDispLineStyleTuple):
            return (
                f"{lookup.name} ({lookup.capStyle}, "
                f" {lookup.joinStyle}, {lookup.dashPattern})"
            )
        elif isinstance(lookup, ImportDispTextStyleTuple):
            return f"{lookup.name} ({lookup.fontName}, {lookup.fontSize})"

        return lookup.name

    @deferToThreadWrapWithLogger(logger)
    def _getLookups(
        self, modelSetKey: str, coordSetKey: Optional[str], lookupType: str
    ):
        LookupType = lookupTypeTableEnumToTable[lookupType]

        ormSession = self._dbSessionCreator()
        try:
            modelSet = getOrCreateModelSet(ormSession, modelSetKey)

            if lookupType == DispLevelTable.LookupTypeE:
                assert coordSetKey, "coordSetKey is required for disp levels"
                coordSet = getOrCreateCoordSet(
                    ormSession, modelSetKey, coordSetKey
                )

                tuples = (
                    ormSession.query(LookupType)
                    .filter(LookupType.coordSetId == coordSet.id)
                    .all()
                )

            else:
                tuples = (
                    ormSession.query(LookupType)
                    .filter(LookupType.modelSetId == modelSet.id)
                    .all()
                )

            ormSession.expunge_all()

            return tuples

        finally:
            ormSession.close()
