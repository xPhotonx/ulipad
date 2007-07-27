from distutils.core import setup
import glob
import py2exe

includes = ["encodings",
	"encodings.*",]
options = {
	"py2exe":
	{
		"compressed": 1,
		"optimize": 2,
		"includes": includes,
	}
}

setup(
	# The first three parameters are not required, if at least a
	# 'version' is given, then a versioninfo resource is built from
	# them and added to the executables.
	version = "2.6",
	description = "NewEdit",
	name = "NewEdit",
	author = "limodou",
	author_email="chatme@263.net",
	url="http://newedit.tigris.org",
	# targets to build
	options = options,
	windows = [
		{
			"script":"NewEdit.pyw",
			"icon_resources": [(1, "newedit.ico")]
		}
	],
	data_files = [
		('images', glob.glob('images/*gif')),
		('resources', glob.glob('resources/*.xrc')),
		('lang', glob.glob('lang/*.*')),
		('', ['newedit.ico', 'COPYLEFT.txt', 'INFO.txt']),
		('tools', glob.glob('tools/*.*')),
		('doc', glob.glob('doc/*.htm')+glob.glob('doc/*.jpg')+glob.glob('doc/*.css')),
	],
	)