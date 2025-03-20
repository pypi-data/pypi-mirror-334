# -*- coding: UTF-8 -*-
# Copyright 2022 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from lino.modlib.users.ui import *

UserDetail.box1 = UserDetail.box1.strip() + " sales_journal"
