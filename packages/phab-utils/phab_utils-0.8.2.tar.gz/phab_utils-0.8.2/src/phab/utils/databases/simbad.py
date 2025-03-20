"""
Getting data from [SIMBAD](https://simbad.u-strasbg.fr/simbad/)
astronomical database.
"""

from astroquery.simbad import Simbad
from astroquery import __version__ as astroqueryVersion
import re

from typing import Optional, Any

from ..logs.log import logger
from ..databases import tap


def findIdentificatorFromAnotherCatalogue(
    starName: str,
    otherIDname: str,
    otherIDversion: Optional[str] = None,
    withoutIDprefix: bool = True
) -> Optional[str]:
    """
    Finds object identificator from a particular catalogue. SIMBAD returns
    a list of identificators prepended with the catalogue name, and this
    function finds the identificator for the specified catalogue and returns
    just the identificator. In addition to that, some catalogues have versions,
    so it is possible to specify which one if of interest.

    For instance, if you need to find the identificator for `TWA 20` star
    in `Gaia` catalog version `DR3`, then SIMBAD will return
    `Gaia DR3 6132146982868270976` value for it, out of which this function
    will extract `6132146982868270976` as the result.

    Example:

    ``` py
    from phab.utils.databases import simbad

    otherID = simbad.findIdentificatorFromAnotherCatalogue(
        "TWA 20",
        "gaia",
        "dr3"
    )
    print(otherID)
    ```
    """
    otherID = None

    otherIDs = Simbad.query_objectids(starName)
    if otherIDs is None:
        logger.warning(
            " ".join((
                "SIMBAD database doesn't have information",
                f"about [{starName}]"
            ))
        )
    else:
        logger.debug(f"Checking SIMBAD IDs for [{starName}]:")

        # before astroquery version 0.4.8 this table had
        # an upper-cased `ID` column key, but starting
        # with version 0.4.8 it is now lower-cased `id`
        #
        # https://github.com/astropy/astropy/issues/17695
        idColumnKey: str = "ID"
        # or compare `astroquery.__version__` with `0.4.7`
        if idColumnKey not in otherIDs.colnames:
            logger.debug(
                " ".join((
                    "There is no upper-cased [ID] key",
                    "in the resulting table, will try",
                    "with lower-cased [id] key"
                ))
            )
            idColumnKey = idColumnKey.lower()  # "id"
            if idColumnKey not in otherIDs.colnames:
                errorMsg = " ".join((
                    "SIMBAD results table has neither [ID]",
                    "nor [id] column"
                ))
                logger.error(errorMsg)
                if len(otherIDs.colnames) > 0:
                    logger.debug(
                        " ".join((
                            "Here are all the columns/keys",
                            "in this table:",
                            ", ".join(otherIDs.colnames)
                        ))
                    )
                else:
                    logger.debug(
                        " ".join((
                            "There are no columns/keys",
                            "in this table at all"
                        ))
                    )
                raise KeyError(errorMsg)

        for oid in otherIDs:
            idCandidate: str = oid[idColumnKey]
            logger.debug(f"- {idCandidate}")
            if otherIDname.lower() in idCandidate.lower():
                idToLookFor = (
                    f"{otherIDname} {otherIDversion}"
                    if otherIDversion else otherIDname
                )
                if idToLookFor.lower() in idCandidate.lower():
                    if withoutIDprefix:
                        prefixRE = re.compile(
                            rf"{idToLookFor}\s?",
                            re.IGNORECASE
                        )
                        otherID = prefixRE.sub("", idCandidate)
                    else:
                        otherID = idCandidate
                    break
    return otherID


def getObjectID(starName: str) -> Optional[int]:
    """
    Finds object identificator for
    [SIMBAD tables](http://simbad.cds.unistra.fr/simbad/tap/tapsearch.html).
    It is stored in the `oid` field of the `basic` table.

    The discovery process is to compare all the known object identificators
    with the `main_id` field value (*also from the `basic` table*). It is
    not clear, how exactly SIMBAD maintainers choose the main ID for an object,
    so one has to iterate through all the identificators known to SIMBAD.

    Example:

    ``` py
    from phab.utils.databases import simbad
    from typing import Optional

    oid: Optional[int] = None
    try:
        oid = simbad.getObjectID("A2 146")
    except KeyError as ex:
        print(f"Something wrong with querying SIMBAD. {repr(ex)}")
    if oid is not None:
        print(f"Object ID: {oid}")
    else:
        print("No results")
    ```
    """
    oid: Optional[int] = None

    # check if this name is already the main ID
    logger.debug(f"Checking whether [{starName}] is already the main ID")
    rez = tap.queryService(
        tap.getServiceEndpoint("simbad"),
        " ".join((
            "SELECT oid",
            "FROM basic",
            f"WHERE main_id = '{starName}'"
        ))
    )
    if rez:
        oid = rez[0]["oid"]
        logger.debug(
            " ".join((
                f"- yes, that is already the main ID,",
                "no need to iterate all the identificators.",
                f"SIMBAD object ID is: {oid}"
            ))
        )
    else:
        logger.debug(
            " ".join((
                "- no, that is not the main ID, will have to iterate",
                "all the other identificators"
            ))
        )
        ids = Simbad.query_objectids(starName)
        if ids is None:
            logger.warning(
                " ".join((
                    "SIMBAD database doesn't have information",
                    f"about [{starName}]"
                ))
            )
        else:
            logger.debug(f"Checking SIMBAD IDs for [{starName}]:")

            # before astroquery version 0.4.8 this table had
            # an upper-cased `ID` column key, but starting
            # with version 0.4.8 it is now lower-cased `id`
            #
            # https://github.com/astropy/astropy/issues/17695
            idColumnKey: str = "ID"
            # or compare `astroquery.__version__` with `0.4.7`
            if idColumnKey not in ids.colnames:
                logger.debug(
                    " ".join((
                        "There is no upper-cased [ID] key",
                        "in the resulting table, will try",
                        "with lower-cased [id] key"
                    ))
                )
                idColumnKey = idColumnKey.lower()  # "id"
                if idColumnKey not in ids.colnames:
                    errorMsg = " ".join((
                        "SIMBAD results table has neither [ID]",
                        "nor [id] column"
                    ))
                    logger.error(errorMsg)
                    if len(ids.colnames) > 0:
                        logger.debug(
                            " ".join((
                                "Here are all the columns/keys",
                                "in this table:",
                                ", ".join(ids.colnames)
                            ))
                        )
                    else:
                        logger.debug(
                            " ".join((
                                "There are no columns/keys",
                                "in this table at all"
                            ))
                        )
                    raise KeyError(errorMsg)

            for id in ids:
                idValue: str = id[idColumnKey]
                logger.debug(f"- {idValue}")

                if idValue == starName:
                    logger.debug(
                        f"...the [{idValue}] has already been tested, skipping"
                    )
                    continue
                rez = tap.queryService(
                    tap.getServiceEndpoint("simbad"),
                    " ".join((
                        "SELECT oid",
                        "FROM basic",
                        f"WHERE main_id = '{idValue}'"
                    ))
                )
                if rez:
                    oid = rez[0]["oid"]
                    logger.debug(
                        " ".join((
                            f"The [{idValue}] is the main ID for",
                            f"[{starName}], SIMBAD object ID is: {oid}"
                        ))
                    )
                    break
    return oid


def getStellarParameter(
    starName: str,
    table: str,
    param: str
) -> Optional[tuple[Any, str]]:
    """
    A convenience function for querying SIMBAD for a stellar parameter:

    1. Finds SIMBAD's object ID by the star name
    (*with `utils.databases.simbad.getObjectID`*);
    2. Queries for a stellar parameter by that object ID
    (*with `utils.databases.tap.getStellarParameterFromSimbadByObjectID`*).

    Example:

    ``` py
    from phab.utils.databases import simbad

    starName = "PPM 725297"
    param = "period"
    rez = simbad.getStellarParameter(
        starName,
        "mesVar",
        param
    )
    if rez:
        val = rez[0]
        ref = rez[1]
        print(f"Value: {val}, reference: {ref}")
    else:
        print(f"SIMBAD doesn't have data about [{param}] parameter of [{starName}] object")
    ```
    """
    rez: Optional[tuple[Any, str]] = None

    oid = getObjectID(starName)
    if oid:
        # logger.debug(
        #     f"Found the following object ID for [{starName}]: {oid}"
        # )
        rez = tap.getStellarParameterFromSimbadByObjectID(
            oid,
            table,
            param
        )

    return rez
