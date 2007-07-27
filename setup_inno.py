# A setup script showing how to extend py2exe.
#
# In this case, the py2exe command is subclassed to create an installation
# script for InnoSetup, which can be compiled with the InnoSetup compiler
# to a single file windows installer.
#
# By default, the installer will be created as dist\Output\setup.exe.

from distutils.core import setup
import py2exe
import sys, os

################################################################
# A program using wxPython

# The manifest will be inserted as resource into test_wx.exe.  This
# gives the controls the Windows XP appearance (if run on XP ;-)
#
# Another option would be to store if in a file named
# test_wx.exe.manifest, and probably copy it with the data_files
# option.
#
manifest_template = '''
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<assembly xmlns="urn:schemas-microsoft-com:asm.v1" manifestVersion="1.0">
<assemblyIdentity
    version="5.0.0.0"
    processorArchitecture="x86"
    name="%(prog)s"
    type="win32"
/>
<description>%(prog)s Program</description>
<dependency>
    <dependentAssembly>
        <assemblyIdentity
            type="win32"
            name="Microsoft.Windows.Common-Controls"
            version="6.0.0.0"
            processorArchitecture="X86"
            publicKeyToken="6595b64144ccf1df"
            language="*"
        />
    </dependentAssembly>
</dependency>
</assembly>
'''

RT_MANIFEST = 24

################################################################
# arguments for the setup() call

newedit_wx = dict(
    script = "NewEdit.pyw",
    other_resources = [(RT_MANIFEST, 1, manifest_template % dict(prog="NewEdit"))],
    dest_base = r"prog\newedit_wx")

zipfile = r"lib\sharedlib.zip"

includes = ["modules.EasyGuider.*", "modules.meteor.*"]
options = {
	"py2exe":
	{
		"compressed": 1,
		"optimize": 2,
		"includes": includes,
	}
}

################################################################
import os

class InnoScript:
    def __init__(self,
                 name,
                 lib_dir,
                 dist_dir,
                 windows_exe_files = [],
                 lib_files = [],
                 version = "1.0"):
        self.lib_dir = lib_dir
        self.dist_dir = dist_dir
        if not self.dist_dir[-1] in "\\/":
            self.dist_dir += "\\"
        self.name = name
        self.version = version
        self.windows_exe_files = [self.chop(p) for p in windows_exe_files]
        self.lib_files = [self.chop(p) for p in lib_files]

    def chop(self, pathname):
        assert pathname.startswith(self.dist_dir)
        return pathname[len(self.dist_dir):]

    def create(self, pathname="dist\\newedit.iss"):
        self.pathname = pathname
        ofi = self.file = open(pathname, "w")
        print >> ofi, "[Setup]"
        print >> ofi, "AppName=%s" % self.name
        print >> ofi, "AppVerName=%s" % self.name + ' ' + self.version
        print >> ofi, "AppPublisher=Limodou"
        print >> ofi, "AppPublisherURL=http://wiki.woodpecker.org.cn/moin/NewEdit"
        print >> ofi, "AppSupportURL=http://www.donews.net/limodou"
        print >> ofi, "AppUpdatesURL=http://wiki.woodpecker.org.cn/moin/NewEdit"
        print >> ofi, "DefaultDirName={pf}\%s" % self.name
        print >> ofi, "DefaultGroupName=%s" % self.name
        print >> ofi, "AllowNoIcons=yes"
        print >> ofi, "LicenseFile=%s\dist\COPYLEFT.txt" % os.getcwd()
        print >> ofi, "InfoBeforeFile=%s\dist\INFO.txt" % os.getcwd()
        print >> ofi, "Compression=lzma/max"
        print >> ofi, "SolidCompression=yes"
        print >> ofi
        print >> ofi, "[Tasks]"
        print >> ofi, 'Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked'
        print >> ofi, 'Name: "quicklaunchicon"; Description: "{cm:CreateQuickLaunchIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked'
        print >> ofi
        print >> ofi, "[Files]"
        print >> ofi, 'Source: "%s.exe"; DestDir: "{app}"; Flags: ignoreversion' % self.name
        print >> ofi, '; NOTE: Don\'t use "Flags: ignoreversion" on any shared system files'
        print >> ofi
        print >> ofi, "[Icons]"
        print >> ofi, 'Name: "{group}\%s"; Filename: "{app}\%s.exe"' % (self.name, self.name)
        print >> ofi, 'Name: "{group}\{cm:UninstallProgram,%s}"; Filename: "{uninstallexe}"' % self.name
        print >> ofi, 'Name: "{userdesktop}\%s"; Filename: "{app}\%s.exe"; Tasks: desktopicon' % (self.name, self.name)
        print >> ofi, 'Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\%s"; Filename: "{app}\%s.exe"; Tasks: quicklaunchicon' % (self.name, self.name)
        print >> ofi
        print >> ofi, "[Registry]"
        print >> ofi, 'Root: HKCR; Subkey: "*\shell\NewEdit"; Flags: uninsdeletekey deletekey;'
        print >> ofi, 'Root: HKCR; Subkey: "*\\shell\\NewEdit\\command"; Flags: uninsdeletekey deletekey; ValueType: string; ValueData: "{app}\\%s.exe %%L"' % self.name
        print >> ofi
        print >> ofi, "[Run]"
        print >> ofi, 'Filename: "{app}\%s.exe"; Description: "{cm:LaunchProgram,%s}"; Flags: nowait postinstall skipifsilent' % (self.name, self.name)
        print >> ofi
        print >> ofi, r"[Files]"
        for path in self.windows_exe_files + self.lib_files:
            print >> ofi, r'Source: "%s"; DestDir: "{app}\%s"; Flags: ignoreversion' % (path, os.path.dirname(path))
        print >> ofi

        print >> ofi, r"[Icons]"
        for path in self.windows_exe_files:
            print >> ofi, r'Name: "{group}\%s"; Filename: "{app}\%s"' % \
                  (self.name, path)
        print >> ofi, 'Name: "{group}\Uninstall %s"; Filename: "{uninstallexe}"' % self.name

    def compile(self):
        try:
            import ctypes
        except ImportError:
            try:
                import win32api
            except ImportError:
                import os
                os.startfile(self.pathname)
            else:
                print "Ok, using win32api."
                win32api.ShellExecute(0, "compile",
                                    self.pathname,
                                    None,
                                    None,
                                    0)
        else:
            print "Cool, you have ctypes installed."
            res = ctypes.windll.shell32.ShellExecuteA(0, "compile",
                                  self.pathname,
                                  None,
                                  None,
                                  0)
            if res < 32:
                raise RuntimeError, "ShellExecute failed, error %d" % res


################################################################

def runother():
    import os

    f = file('run_setup.bat', 'w')
    print >> f, 'cd dist/lib'
#    print >> f, '7z x sharedlib.zip -osharedlib'
#    print >> f, 'del sharedlib.zip'
#    print >> f, 'cd sharedlib'
#    print >> f, '7z a -tzip -mx9 ..\sharedlib.zip -r'
#    print >> f, 'cd ..'
#    print >> f, 'rd sharedlib /s /q'
    print >> f, 'upx --best *.*'
    print >> f, 'cd ../..'
    f.close()
    os.system('run_setup.bat')

from modules.Version import version

from py2exe.build_exe import py2exe

class build_installer(py2exe):
    # This class first builds the exe file(s), then creates a Windows installer.
    # You need InnoSetup for it.
    def run(self):
        # First, let py2exe do it's work.
        py2exe.run(self)

        runother()

        lib_dir = self.lib_dir
        dist_dir = self.dist_dir

        # create the Installer, using the files py2exe has created.
        script = InnoScript("NewEdit",
                            lib_dir,
                            dist_dir,
                            self.windows_exe_files,
                            self.lib_files, version)
        print "*** creating the inno setup script***"
        script.create()
        print "*** compiling the inno setup script***"
        script.compile()
        # Note: By default the final setup.exe will be in an Output subdirectory.

################################################################

import glob

setup(
	version = version,
	description = "NewEdit",
	name = "NewEdit",
	author = "limodou",
	author_email="limodou@gmail.com",
	url="http://wiki.woodpecker.org.cn/moin/NewEdit",

	options = options,
	# The lib directory contains everything except the executables and the python dll.
	zipfile = zipfile,
	windows = [
		{
			"script":"NewEdit.pyw",
			"icon_resources": [(1, "newedit.ico")]
		}
	],
	data_files = [
		('images', glob.glob('images/*gif') + glob.glob('images/*jpg') + + glob.glob('images/*png')),
		('resources', glob.glob('resources/*.xrc')),
		('lang', glob.glob('lang/*.*')),
		('lang/zh_CN', glob.glob('lang/zh_CN/*.*')),
		('', ['newedit.ico', 'COPYLEFT.txt', 'INFO.txt']),
		('tools', glob.glob('tools/*.*')),
		('doc', glob.glob('doc/*.htm')+glob.glob('doc/*.jpg')+glob.glob('doc/*.css')),
        ('conf', glob.glob('conf/*.*')),
	],
    # use out build_installer class as extended py2exe build command
    cmdclass = {"py2exe": build_installer},
    )