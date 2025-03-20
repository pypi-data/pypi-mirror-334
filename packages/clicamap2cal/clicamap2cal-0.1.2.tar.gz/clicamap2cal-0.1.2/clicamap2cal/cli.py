#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (c) Rémi Ferrand
#
# Contributor(s): Rémi Ferrand <riton.github@gmail.com>, 2025
#
# This software is governed by the CeCILL  license under French law and
# abiding by the rules of distribution of free software.  You can  use,
# modify and/ or redistribute the software under the terms of the CeCILL
# license as circulated by CEA, CNRS and INRIA at the following URL
# "http://www.cecill.info".
#
# As a counterpart to the access to the source code and  rights to copy,
# modify and redistribute granted by the license, users are provided only
# with a limited warranty  and the software's author,  the holder of the
# economic rights,  and the successive licensors  have only  limited
# liability.
#
# In this respect, the user's attention is drawn to the risks associated
# with loading,  using,  modifying and/or developing or reproducing the
# software by the user in light of its specific status of free software,
# that may mean  that it is complicated to manipulate,  and  that  also
# therefore means  that it is reserved for developers  and  experienced
# professionals having in-depth computer knowledge. Users are therefore
# encouraged to load and test the software's suitability as regards their
# requirements in conditions enabling the security of their systems and/or
# data to be ensured and,  more generally, to use and operate it in the
# same conditions as regards security.
#
# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license and that you accept its terms.
#
from __future__ import annotations

import sys
from datetime import datetime, timedelta

from ics import Calendar, Event
from pydantic_settings import CliApp

from . import __version__
from .clicamap.client import Client, LivraisonDetails
from .logging import setup_logging
from .settings import Settings


def main() -> int:
    return real_main(sys.argv[1:])


def _summarize_livraison_details(details: list[LivraisonDetails]) -> str:
    s = ""
    for detail in details:
        s += f"* {detail.title}\n"
        for item in detail.items:
            s += f"  - {item}\n"
        s += "\n"

    return s


# pylint: disable=unused-argument
def real_main(argv) -> int:
    args: Settings = CliApp.run(
        Settings,
        cli_args=argv,
    )

    logger = setup_logging(sys.stderr, level="DEBUG" if args.debug else "INFO")

    Client.LOGGER = logger.bind(logger="clicamap.client")

    cal = Calendar(creator="clicamap2cal@riton.fr")

    with Client(
        username=args.username,
        password=args.password,
    ) as amap:
        for livraison_dt, livraison_details in amap.get_livraisons():
            livraison_locations = {x.location for x in livraison_details}
            assert len(livraison_locations) == 1

            evt = Event(name=f"Livraison AMAP du {str(livraison_dt)}")
            evt.begin = livraison_dt
            evt.end = livraison_dt + timedelta(hours=1)
            evt.location = livraison_locations.pop()
            evt.description = _summarize_livraison_details(livraison_details)

            cal.events.add(evt)

    print(cal.serialize())

    return 0


if __name__ == "__main__":
    raise SystemExit(real_main(sys.argv))
