# PYUI NSIS installer script.
# 
# Copyright (c) 2016 Riverbank Computing Limited <info@riverbankcomputing.com>
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


# These will change with different releases.
!define PYUI_VERSION        "1.0.0"
!define PYUI_INSTALLER      ""
#!define PYUI_INSTALLER      "-1"
!define PYUI_LICENSE        "GPL"
!define PYUI_LICENSE_LC     "gpl"
!define PYUI_PYTHON_MAJOR   "3"
!define PYUI_PYTHON_MINOR   "6"
!define PYUI_ARCH           "64"
!define PYUI_QT_VERS        "5.10.1"
!define PYUI_QT_DOC_VERS    "5"

# These are all derived from the above.
!define PYUI_PYTHON_DIR     "C:\Python${PYUI_PYTHON_MAJOR}${PYUI_PYTHON_MINOR}"
!define PYUI_PYTHON_VERS    "${PYUI_PYTHON_MAJOR}.${PYUI_PYTHON_MINOR}"
!define PYUI_PYTHON_HK      "Software\Python\PythonCore\${PYUI_PYTHON_VERS}\InstallPath"
!define PYUI_PYTHON_HK_ARCH "Software\Python\PythonCore\${PYUI_PYTHON_VERS}-${PYUI_ARCH}\InstallPath"
!define PYUI_NAME           "PYUI ${PYUI_LICENSE} v${PYUI_VERSION} for Python v${PYUI_PYTHON_VERS} (x${PYUI_ARCH})"
!define PYUI_HK_ROOT        "Software\PYUI\Py${PYUI_PYTHON_VERS}"
!define PYUI_HK             "${PYUI_HK_ROOT}\InstallPath"
!define PYQT5_HK            "Software\PyQt5\Py${PYUI_PYTHON_VERS}\InstallPath"
!define QT_SRC_DIR          "C:\Qt\${PYUI_QT_VERS}"
!define ICU_SRC_DIR         "C:\icu"
!define OPENSSL_SRC_DIR     "C:\OpenSSL"
!define MYSQL_SRC_DIR       "C:\MySQL"
!define REDIST_DIR          "C:\Redist"


# Include the tools we use.
!include MUI2.nsh
!include LogicLib.nsh
!include AddToPath.nsh
!include StrSlash.nsh


# Tweak some of the standard pages.
!define MUI_WELCOMEPAGE_TEXT \
"This wizard will guide you through the installation of ${PYUI_NAME}.$\r$\n\
$\r$\n\
This copy of PYUI includes a subset of Qt v${PYUI_QT_VERS} Open Source \
Edition needed by PYUI. It also includes MySQL, ODBC, PostgreSQL and SQLite \
drivers and the required OpenSSL DLLs.$\r$\n\
$\r$\n\
Any code you write must be released under a license that is compatible with \
the GPL.$\r$\n\
$\r$\n\
Click Next to continue."

!define MUI_FINISHPAGE_LINK "Get the latest news of PYUI here"
!define MUI_FINISHPAGE_LINK_LOCATION "https://github.com/PYUI/PYUI"


# Define the product name and installer executable.
Name "PYUI"
Caption "${PYUI_NAME} Setup"
OutFile "PYUI-${PYUI_VERSION}-${PYUI_LICENSE_LC}-Py${PYUI_PYTHON_MAJOR}.${PYUI_PYTHON_MINOR}-Qt${PYUI_QT_VERS}-x${PYUI_ARCH}${PYUI_INSTALLER}.exe"


# This is done (along with the use of SetShellVarContext) so that we can remove
# the shortcuts when uninstalling under Vista and Windows 7.  Note that we
# don't actually check if it is successful.
RequestExecutionLevel admin


# The different installation types.  "Full" is everything.  "Minimal" is the
# runtime environment.
InstType "Full"
InstType "Minimal"


# Maximum compression.
SetCompressor /SOLID lzma


# We want the user to confirm they want to cancel.
!define MUI_ABORTWARNING

Function .onInit
    ${If} ${PYUI_ARCH} == "64"
        SetRegView 64
    ${Endif}

    # Check if there is already a version of PyQt5 installed for this version
    # of Python.
    ReadRegStr $0 HKCU "${PYQT5_HK}" ""

    ${If} $0 == ""
        ReadRegStr $0 HKLM "${PYQT5_HK}" ""
    ${Endif}

    ${If} $0 != ""
        MessageBox MB_YESNO|MB_DEFBUTTON2|MB_ICONQUESTION \
"A copy of PyQt5 for Python v${PYUI_PYTHON_VERS} is already installed in $0 \
and should be uninstalled first.$\r$\n \
$\r$\n\
Do you wish to uninstall it?" IDYES Uninstall
            Abort
Uninstall:
        ExecWait '"$0\Lib\site-packages\PyQt5\Uninstall.exe" /S'
    ${Endif}

    # Check if there is already a version of PYUI installed for this version
    # of Python.
    ReadRegStr $0 HKCU "${PYUI_HK}" ""

    ${If} $0 == ""
        ReadRegStr $0 HKLM "${PYUI_HK}" ""
    ${Endif}

    ${If} $0 != ""
        MessageBox MB_YESNO|MB_DEFBUTTON2|MB_ICONQUESTION \
"A copy of PYUI for Python v${PYUI_PYTHON_VERS} is already installed in $0 \
and should be uninstalled first.$\r$\n \
$\r$\n\
Do you wish to uninstall it?" IDYES UninstallPYUI
            Abort
UninstallPYUI:
        ExecWait '"$0\Lib\site-packages\PYUI\Uninstall.exe" /S'
    ${Endif}

    # Check the right version of Python has been installed.  Different versions
    # of Python use different formats for the version number.
    ReadRegStr $INSTDIR HKCU "${PYUI_PYTHON_HK}" ""

    ${If} $INSTDIR == ""
        ReadRegStr $INSTDIR HKCU "${PYUI_PYTHON_HK_ARCH}" ""

        ${If} $INSTDIR == ""
            ReadRegStr $INSTDIR HKLM "${PYUI_PYTHON_HK}" ""

            ${If} $INSTDIR == ""
                ReadRegStr $INSTDIR HKLM "${PYUI_PYTHON_HK_ARCH}" ""
            ${Endif}
        ${Endif}
    ${Endif}

    ${If} $INSTDIR == ""
        MessageBox MB_YESNO|MB_ICONQUESTION \
"This copy of PYUI has been built against Python v${PYUI_PYTHON_VERS} \
(x${PYUI_ARCH}) which doesn't seem to be installed.$\r$\n\
$\r$\n\
Do you wish to continue with the installation?" IDYES GotPython
            Abort
GotPython:
        StrCpy $INSTDIR "${PYUI_PYTHON_DIR}"
    ${Endif}
FunctionEnd


# Define the different pages.
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_LICENSE ".\LICENSE"
!insertmacro MUI_PAGE_COMPONENTS

!define MUI_DIRECTORYPAGE_TEXT_DESTINATION "Python installation folder"
!define MUI_DIRECTORYPAGE_TEXT_TOP \
"PYUI will be installed in the site-packages folder of your Python \
installation."
!insertmacro MUI_PAGE_DIRECTORY

!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES

 
# Other settings.
!insertmacro MUI_LANGUAGE "English"


# Installer sections.

Section "Extension modules" SecModules
    SectionIn 1 2 RO

    SetOverwrite on

    # We have to take the SIP files from where they should have been installed.
    SetOutPath $INSTDIR\Lib\site-packages
    File "${PYUI_PYTHON_DIR}\Lib\site-packages\sip.pyd"

    SetOutPath $INSTDIR\Lib\site-packages\PYUI
    File .\LICENSE
    File .\__init__.py
    File /r .\pyuic\uic

    File .\build\Qt\Qt.pyd
    File .\build\QtCore\QtCore.pyd
    File .\build\QtDesigner\QtDesigner.pyd
    File .\build\QtGui\QtGui.pyd
    File .\build\QtHelp\QtHelp.pyd
    File .\build\QtLocation\QtLocation.pyd
    File .\build\QtMultimedia\QtMultimedia.pyd
    File .\build\QtMultimediaWidgets\QtMultimediaWidgets.pyd
    File .\build\QtNetwork\QtNetwork.pyd
    File .\build\QtOpenGL\QtOpenGL.pyd
    File .\build\QtPositioning\QtPositioning.pyd
    File .\build\QtPrintSupport\QtPrintSupport.pyd
    File .\build\QtQml\QtQml.pyd
    File .\build\QtQuick\QtQuick.pyd
    File .\build\QtQuickWidgets\QtQuickWidgets.pyd
    File .\build\QtSensors\QtSensors.pyd
    File .\build\QtSerialPort\QtSerialPort.pyd
    File .\build\QtSql\QtSql.pyd
    File .\build\QtSvg\QtSvg.pyd
    File .\build\QtTest\QtTest.pyd
    File .\build\QtWebChannel\QtWebChannel.pyd
    File .\build\QtWebEngineCore\QtWebEngineCore.pyd
    File .\build\QtWebEngineWidgets\QtWebEngineWidgets.pyd
    File .\build\QtWebSockets\QtWebSockets.pyd
    File .\build\QtWinExtras\QtWinExtras.pyd
    File .\build\QtWidgets\QtWidgets.pyd
    File .\build\QtXml\QtXml.pyd
    File .\build\QtXmlPatterns\QtXmlPatterns.pyd
    File .\build\QAxContainer\QAxContainer.pyd
    File .\build\_QOpenGLFunctions_2_0\_QOpenGLFunctions_2_0.pyd
    File .\build\_QOpenGLFunctions_2_1\_QOpenGLFunctions_2_1.pyd
    File .\build\_QOpenGLFunctions_4_1_Core\_QOpenGLFunctions_4_1_Core.pyd
SectionEnd

Section "QScintilla" SecQScintilla
    SectionIn 1

    SetOverwrite on

    SetOutPath $INSTDIR\Lib\site-packages\PYUI
    File "${PYUI_PYTHON_DIR}\Lib\site-packages\PyQt5\Qsci.pyd"
    File /r "${QT_SRC_DIR}\qsci"

    SetOutPath $INSTDIR\Lib\site-packages\PYUI
    File "${QT_SRC_DIR}\lib\qscintilla2.dll"

    SetOutPath $INSTDIR\Lib\site-packages\PYUI\translations
    File "${QT_SRC_DIR}\translations\qscintilla*.qm"
SectionEnd

Section "Qt runtime" SecQt
    SectionIn 1 2

    SetOverwrite on

    SetOutPath $INSTDIR\Lib\site-packages\PYUI\plugins\PYUI
    File .\build\qmlscene\release\pyqt5qmlplugin.dll

    SetOutPath $INSTDIR\Lib\site-packages\PYUI
    File "${QT_SRC_DIR}\bin\qmlscene.exe"
    File "${QT_SRC_DIR}\bin\Qt5CLucene.dll"
    File "${QT_SRC_DIR}\bin\Qt5Core.dll"
    File "${QT_SRC_DIR}\bin\Qt5Designer.dll"
    File "${QT_SRC_DIR}\bin\Qt5DesignerComponents.dll"
    File "${QT_SRC_DIR}\bin\Qt5Gui.dll"
    File "${QT_SRC_DIR}\bin\Qt5Help.dll"
    File "${QT_SRC_DIR}\bin\Qt5Location.dll"
    File "${QT_SRC_DIR}\bin\Qt5Multimedia.dll"
    File "${QT_SRC_DIR}\bin\Qt5MultimediaQuick_p.dll"
    File "${QT_SRC_DIR}\bin\Qt5MultimediaWidgets.dll"
    File "${QT_SRC_DIR}\bin\Qt5Network.dll"
    File "${QT_SRC_DIR}\bin\Qt5OpenGL.dll"
    File "${QT_SRC_DIR}\bin\Qt5Positioning.dll"
    File "${QT_SRC_DIR}\bin\Qt5PrintSupport.dll"
    File "${QT_SRC_DIR}\bin\Qt5Qml.dll"
    File "${QT_SRC_DIR}\bin\Qt5Quick.dll"
    File "${QT_SRC_DIR}\bin\Qt5QuickParticles.dll"
    File "${QT_SRC_DIR}\bin\Qt5QuickWidgets.dll"
    File "${QT_SRC_DIR}\bin\Qt5Sensors.dll"
    File "${QT_SRC_DIR}\bin\Qt5SerialPort.dll"
    File "${QT_SRC_DIR}\bin\Qt5Sql.dll"
    File "${QT_SRC_DIR}\bin\Qt5Svg.dll"
    File "${QT_SRC_DIR}\bin\Qt5Test.dll"
    File "${QT_SRC_DIR}\bin\Qt5WebChannel.dll"
    File "${QT_SRC_DIR}\bin\Qt5WebEngineCore.dll"
    File "${QT_SRC_DIR}\bin\Qt5WebEngineWidgets.dll"
    File "${QT_SRC_DIR}\bin\Qt5WebSockets.dll"
    File "${QT_SRC_DIR}\bin\Qt5Widgets.dll"
    File "${QT_SRC_DIR}\bin\Qt5WinExtras.dll"
    File "${QT_SRC_DIR}\bin\Qt5Xml.dll"
    File "${QT_SRC_DIR}\bin\Qt5XmlPatterns.dll"
    File "${QT_SRC_DIR}\bin\QtWebEngineProcess.exe"

    File "${QT_SRC_DIR}\bin\libEGL.dll"
    File "${QT_SRC_DIR}\bin\libGLESv2.dll"

    File "${ICU_SRC_DIR}\bin\icudt55.dll"
    File "${ICU_SRC_DIR}\bin\icuin55.dll"
    File "${ICU_SRC_DIR}\bin\icuuc55.dll"

    File "${OPENSSL_SRC_DIR}\bin\libeay32.dll"
    File "${OPENSSL_SRC_DIR}\bin\ssleay32.dll"

    File "${MYSQL_SRC_DIR}\lib\libmysql.dll"

    File "${REDIST_DIR}\msvcp140.dll"

    SetOutPath $INSTDIR\Lib\site-packages\PYUI
    File /r "${QT_SRC_DIR}\qml"

    SetOutPath $INSTDIR\Lib\site-packages\PYUI\plugins\audio
    File "${QT_SRC_DIR}\plugins\audio\qtaudio_windows.dll"

    SetOutPath $INSTDIR\Lib\site-packages\PYUI\plugins\bearer
    File "${QT_SRC_DIR}\plugins\bearer\qgenericbearer.dll"
    File "${QT_SRC_DIR}\plugins\bearer\qnativewifibearer.dll"

    SetOutPath $INSTDIR\Lib\site-packages\PYUI\plugins\geoservices
    File "${QT_SRC_DIR}\plugins\geoservices\qtgeoservices_mapbox.dll"
    File "${QT_SRC_DIR}\plugins\geoservices\qtgeoservices_nokia.dll"
    File "${QT_SRC_DIR}\plugins\geoservices\qtgeoservices_osm.dll"

    SetOutPath $INSTDIR\Lib\site-packages\PYUI\plugins\iconengines
    File "${QT_SRC_DIR}\plugins\iconengines\qsvgicon.dll"

    SetOutPath $INSTDIR\Lib\site-packages\PYUI\plugins\imageformats
    File "${QT_SRC_DIR}\plugins\imageformats\qdds.dll"
    File "${QT_SRC_DIR}\plugins\imageformats\qgif.dll"
    File "${QT_SRC_DIR}\plugins\imageformats\qicns.dll"
    File "${QT_SRC_DIR}\plugins\imageformats\qico.dll"
    File "${QT_SRC_DIR}\plugins\imageformats\qjpeg.dll"
    File "${QT_SRC_DIR}\plugins\imageformats\qsvg.dll"
    File "${QT_SRC_DIR}\plugins\imageformats\qtga.dll"
    File "${QT_SRC_DIR}\plugins\imageformats\qtiff.dll"
    File "${QT_SRC_DIR}\plugins\imageformats\qwbmp.dll"
    File "${QT_SRC_DIR}\plugins\imageformats\qwebp.dll"

    SetOutPath $INSTDIR\Lib\site-packages\PYUI\plugins\mediaservice
    File "${QT_SRC_DIR}\plugins\mediaservice\dsengine.dll"
    File "${QT_SRC_DIR}\plugins\mediaservice\qtmedia_audioengine.dll"

    SetOutPath $INSTDIR\Lib\site-packages\PYUI\plugins\platforms
    File "${QT_SRC_DIR}\plugins\platforms\qminimal.dll"
    File "${QT_SRC_DIR}\plugins\platforms\qoffscreen.dll"
    File "${QT_SRC_DIR}\plugins\platforms\qwindows.dll"

    SetOutPath $INSTDIR\Lib\site-packages\PYUI\plugins\playlistformats
    File "${QT_SRC_DIR}\plugins\playlistformats\qtmultimedia_m3u.dll"

    SetOutPath $INSTDIR\Lib\site-packages\PYUI\plugins\position
    File "${QT_SRC_DIR}\plugins\position\qtposition_geoclue.dll"
    File "${QT_SRC_DIR}\plugins\position\qtposition_positionpoll.dll"
    File "${QT_SRC_DIR}\plugins\position\qtposition_serialnmea.dll"

    SetOutPath $INSTDIR\Lib\site-packages\PYUI\plugins\printsupport
    File "${QT_SRC_DIR}\plugins\printsupport\windowsprintersupport.dll"

    SetOutPath $INSTDIR\Lib\site-packages\PYUI\plugins\sensorgestures
    File "${QT_SRC_DIR}\plugins\sensorgestures\qtsensorgestures_plugin.dll"
    File "${QT_SRC_DIR}\plugins\sensorgestures\qtsensorgestures_shakeplugin.dll"

    SetOutPath $INSTDIR\Lib\site-packages\PYUI\plugins\sensors
    File "${QT_SRC_DIR}\plugins\sensors\qtsensors_generic.dll"

    SetOutPath $INSTDIR\Lib\site-packages\PYUI\plugins\sqldrivers
    File "${QT_SRC_DIR}\plugins\sqldrivers\qsqlite.dll"
    File "${QT_SRC_DIR}\plugins\sqldrivers\qsqlmysql.dll"
    File "${QT_SRC_DIR}\plugins\sqldrivers\qsqlodbc.dll"
    File "${QT_SRC_DIR}\plugins\sqldrivers\qsqlpsql.dll"

    SetOutPath $INSTDIR\Lib\site-packages\PYUI\resources
    File /r "${QT_SRC_DIR}\resources"

    SetOutPath $INSTDIR\Lib\site-packages\PYUI\translations
    File "${QT_SRC_DIR}\translations\qt_*.qm"
    File "${QT_SRC_DIR}\translations\qtbase_*.qm"

    SetOutPath $INSTDIR\Lib\site-packages\PYUI\translations\qtwebengine_locales
    File /r "${QT_SRC_DIR}\translations\qtwebengine_locales"

    # Tell Python and the Qt tools where to find Qt.
    FileOpen $0 $INSTDIR\qt.conf w
    FileWrite $0 "[Paths]$\r$\n"
    FileWrite $0 "Prefix = Lib/site-packages/PYUI$\r$\n"
    FileWrite $0 "Binaries = Lib/site-packages/PYUI$\r$\n"
    FileClose $0

    FileOpen $0 $INSTDIR\Lib\site-packages\PYUI\qt.conf w
    FileWrite $0 "[Paths]$\r$\n"
    FileWrite $0 "Prefix = .$\r$\n"
    FileWrite $0 "Binaries = .$\r$\n"
    FileClose $0
SectionEnd

Section "Developer tools" SecTools
    SectionIn 1

    SetOverwrite on

    SetOutPath $INSTDIR\Lib\site-packages\PYUI
    File .\build\pylupdate\release\pylupdate5.exe
    File .\build\pyrcc\release\pyrcc5.exe

    FileOpen $0 $INSTDIR\Lib\site-packages\PYUI\pyuic5.bat w
    FileWrite $0 "@$\"$INSTDIR\python$\" -m PYUI.uic.pyuic %1 %2 %3 %4 %5 %6 %7 %8 %9$\r$\n"
    FileClose $0
SectionEnd

Section "Qt developer tools" SecQtTools
    SectionIn 1

    SetOverwrite on

    SetOutPath $INSTDIR\Lib\site-packages\PYUI
    File "${QT_SRC_DIR}\bin\assistant.exe"
    File "${QT_SRC_DIR}\bin\designer.exe"
    File "${QT_SRC_DIR}\bin\linguist.exe"
    File "${QT_SRC_DIR}\bin\lrelease.exe"
    File "${QT_SRC_DIR}\bin\qcollectiongenerator.exe"
    File "${QT_SRC_DIR}\bin\qhelpgenerator.exe"
    File "${QT_SRC_DIR}\bin\qmake.exe"
    File "${QT_SRC_DIR}\bin\xmlpatterns.exe"
    File /r "${QT_SRC_DIR}\mkspecs"

    SetOutPath $INSTDIR\Lib\site-packages\PYUI\plugins\designer
    File "${QT_SRC_DIR}\plugins\designer\qaxwidget.dll"
    File "${QT_SRC_DIR}\plugins\designer\qquickwidget.dll"

    File .\build\designer\release\pyqt5.dll
    File "${QT_SRC_DIR}\plugins\designer\qscintillaplugin.dll"

    SetOutPath $INSTDIR\Lib\site-packages\PYUI\translations
    File "${QT_SRC_DIR}\translations\assistant_*.qm"
    File "${QT_SRC_DIR}\translations\designer_*.qm"
    File "${QT_SRC_DIR}\translations\linguist_*.qm"
SectionEnd

Section "SIP developer tools" SecSIPTools
    SectionIn 1

    SetOverwrite on

    SetOutPath $INSTDIR\Lib\site-packages\PYUI
    File "${PYUI_PYTHON_DIR}\Lib\site-packages\sipdistutils.py"
    File "${PYUI_PYTHON_DIR}\Lib\site-packages\sipconfig.py"
    File "${PYUI_PYTHON_DIR}\Lib\site-packages\sipconfig_nd.py"
    File "${PYUI_PYTHON_DIR}\Lib\site-packages\sipdistutils.py"
    File "${PYUI_PYTHON_DIR}\Scripts\sip.exe"
SectionEnd

Section "Documentation" SecDocumentation
    SectionIn 1

    SetOverwrite on

    SetOutPath $INSTDIR\Lib\site-packages\PYUI\doc
    File /r doc\html
SectionEnd

Section "Examples" SecExamples
    SectionIn 1

    SetOverwrite on

    SetOutPath $INSTDIR\Lib\site-packages\PYUI\examples
    File /r examples\*.*
SectionEnd

Section "Start Menu shortcuts" SecShortcuts
    SectionIn 1

    SetShellVarContext all
    CreateDirectory "$SMPROGRAMS\${PYUI_NAME}"

    StrCpy $0 "$SMPROGRAMS\${PYUI_NAME}"
    CreateShortCut "$0\Assistant.lnk" "$INSTDIR\Lib\site-packages\PYUI\assistant.exe"
    CreateShortCut "$0\Designer.lnk" "$INSTDIR\Lib\site-packages\PYUI\designer.exe"
    CreateShortCut "$0\Linguist.lnk" "$INSTDIR\Lib\site-packages\PYUI\linguist.exe"
    CreateShortCut "$0\Command Prompt.lnk" "%COMSPEC%" "/k cd /d $INSTDIR"

    ${If} ${FileExists} "$INSTDIR\Lib\site-packages\PYUI\doc\html\index.html"
        CreateShortCut "$0\Documentation.lnk" "$INSTDIR\Lib\site-packages\PYUI\doc\html\index.html"
    ${Endif}

    ${If} ${FileExists} "$INSTDIR\Lib\site-packages\PYUI\examples"
        CreateShortCut "$0\Examples.lnk" "$INSTDIR\Lib\site-packages\PYUI\examples"
    ${Endif}

    CreateShortCut "$0\Uninstall.lnk" "$INSTDIR\Lib\site-packages\PYUI\Uninstall.exe"
SectionEnd

Section "Uninstaller" SecUninstaller
    SectionIn 1 2 RO

    # Make sure the uninstaller isn't running.
    ${If} ${FileExists} "$INSTDIR\Lib\site-packages\PYUI\Uninstall.exe"
        ExecWait '"$INSTDIR\Lib\site-packages\PYUI\Uninstall.exe" /S _?=$INSTDIR\Lib\site-packages\PYUI'
        Delete "$INSTDIR\Lib\site-packages\PYUI\Uninstall.exe"
    ${Endif}

    # Write the uninstaller.
    WriteUninstaller "$INSTDIR\Lib\site-packages\PYUI\Uninstall.exe"

    # Write the installation information to the registry.
    WriteRegStr HKLM "${PYUI_HK}" "" $INSTDIR
    WriteRegStr HKLM "${PYUI_HK_ROOT}" "Version" "${PYUI_VERSION}"
    WriteRegStr HKLM "${PYUI_HK_ROOT}" "Python" "${PYUI_PYTHON_VERS}"
    WriteRegStr HKLM "${PYUI_HK_ROOT}" "Arch" "${PYUI_ARCH}"
    WriteRegStr HKLM "${PYUI_HK_ROOT}" "License" "${PYUI_LICENSE}"

    # Write the uninstall information to the registry.
    WriteRegExpandStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${PYUI_NAME}" "UninstallString" '"$INSTDIR\Lib\site-packages\PYUI\Uninstall.exe"'
    WriteRegExpandStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${PYUI_NAME}" "InstallLocation" "$INSTDIR"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${PYUI_NAME}" "DisplayName" "${PYUI_NAME}"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${PYUI_NAME}" "DisplayVersion" "${PYUI_VERSION}"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${PYUI_NAME}" "DisplayIcon" "$INSTDIR\Lib\site-packages\PYUI\designer.exe"
    WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${PYUI_NAME}" "NoModify" "1"
    WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${PYUI_NAME}" "NoRepair" "1"
SectionEnd


# Section description text.
!insertmacro MUI_FUNCTION_DESCRIPTION_BEGIN
!insertmacro MUI_DESCRIPTION_TEXT ${SecModules} \
"The PYUI extension modules"
!insertmacro MUI_DESCRIPTION_TEXT ${SecQScintilla} \
"QScintilla and its extension module"
!insertmacro MUI_DESCRIPTION_TEXT ${SecQt} \
"The Qt DLLs, plugins and translations used by PYUI"
!insertmacro MUI_DESCRIPTION_TEXT ${SecTools} \
"The PYUI developer tools (pyuic5, pyrcc5, pylupdate5)"
!insertmacro MUI_DESCRIPTION_TEXT ${SecQtTools} \
"The Qt developer tools (designer, assistant, linguist etc.)"
!insertmacro MUI_DESCRIPTION_TEXT ${SecSIPTools} \
"The SIP developer tools and .sip files"
!insertmacro MUI_DESCRIPTION_TEXT ${SecDocumentation} \
"The PYUI documentation"
!insertmacro MUI_DESCRIPTION_TEXT ${SecExamples} \
"The PYUI examples"
!insertmacro MUI_DESCRIPTION_TEXT ${SecShortcuts} \
"This adds shortcuts to your Start Menu"
!insertmacro MUI_FUNCTION_DESCRIPTION_END


# Uninstaller code.

Section "Uninstall"
    # Get the install directory.
    ReadRegStr $INSTDIR HKLM "${PYUI_HK}" ""

    # The shortcuts.
    SetShellVarContext all
    ReadRegStr $0 HKLM "${PYUI_HK_ROOT}" "Version"
    ReadRegStr $1 HKLM "${PYUI_HK_ROOT}" "Python"
    ReadRegStr $2 HKLM "${PYUI_HK_ROOT}" "Arch"
    ReadRegStr $3 HKLM "${PYUI_HK_ROOT}" "License"
    Delete "$SMPROGRAMS\PYUI $3 v$0 for Python v$1 (x$2)\Assistant.lnk"
    Delete "$SMPROGRAMS\PYUI $3 v$0 for Python v$1 (x$2)\Designer.lnk"
    Delete "$SMPROGRAMS\PYUI $3 v$0 for Python v$1 (x$2)\Linguist.lnk"
    Delete "$SMPROGRAMS\PYUI $3 v$0 for Python v$1 (x$2)\Command Prompt.lnk"
    Delete "$SMPROGRAMS\PYUI $3 v$0 for Python v$1 (x$2)\Documentation.lnk"
    Delete "$SMPROGRAMS\PYUI $3 v$0 for Python v$1 (x$2)\Examples.lnk"
    Delete "$SMPROGRAMS\PYUI $3 v$0 for Python v$1 (x$2)\Uninstall.lnk"
    RMDir "$SMPROGRAMS\PYUI $3 v$0 for Python v$1 (x$2)"

    # The Python modules.
    RMDir /r "$INSTDIR\Lib\site-packages\PYUI"

    # The Qt configuration file.
    Delete $INSTDIR\qt.conf

    # The registry entries.
    DeleteRegKey HKLM "${PYUI_HK_ROOT}"
    DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\PYUI $3 v$0 for Python v$1 (x$2)"
SectionEnd