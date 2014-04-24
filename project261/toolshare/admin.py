"""
File:       toolshare/admin.py
Language:   Python 3 with Django Web Framework

Author:     Val Booth <vxb4825@rit.edu>
Author:     Corban Mailloux <cdm3806@rit.edu>
Author:     Adam McCarthy <aem1269@rit.edu>
Author:     Michael Washburn <mdw7326@rit.edu>
Author:     Bryon Wilkins <brw4824@rit.edu>

Determines which parts of the toolshare module show up in the administrative
panel. Can also determine how these are formatted.
"""

from django.contrib import admin
from toolshare.models import *

admin.site.register(Address)
admin.site.register(Sharezone)
admin.site.register(UserProfile)
admin.site.register(Tool)
admin.site.register(ToolGroup)
admin.site.register(Reservation)