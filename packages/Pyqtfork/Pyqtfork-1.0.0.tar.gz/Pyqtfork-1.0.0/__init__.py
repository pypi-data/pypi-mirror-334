# Copyright (c) 2018 Riverbank Computing Limited <info@riverbankcomputing.com>
# Copyright (c) 2023 PYUI Contributors
#
# This file is part of PYUI.
#
# This file may be used under the terms of the GNU General Public License
# version 3.0 as published by the Free Software Foundation and appearing in
# the file LICENSE included in the packaging of this file.  Please review the
# following information to ensure the GNU General Public License version 3.0
# requirements will be met: http://www.gnu.org/copyleft/gpl.html.
#
# If you do not wish to use this file under the terms of the GPL version 3.0
# then you may purchase a commercial license.  For more information contact
# info@riverbankcomputing.com.
#
# This file is provided AS IS with NO WARRANTY OF ANY KIND, INCLUDING THE
# WARRANTY OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.

# PYUI version
__version__ = '1.0.0'

# Import PyQt5 modules for backward compatibility
# This allows existing PyQt5 code to work with PYUI
try:
    from PyQt5 import *
except ImportError:
    pass

# Add PYUI-specific enhancements and utilities
# These will be implemented in future versions
