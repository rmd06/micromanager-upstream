#!/usr/bin/env python

"""
setup.py file for SWIG example
"""

from distutils.core import setup, Extension
from distutils.command.build_ext import build_ext
import numpy.distutils.misc_util
import os

os.environ['CC'] = 'g++'
#os.environ['CXX'] = 'g++'
#os.environ['CPP'] = 'g++'
#os.environ['LDSHARED'] = 'g++'

class build_ext_subclass( build_ext ):
    def build_extensions(self):
        c = self.compiler.compiler_type
        compiler_so = self.compiler.compiler_so
        linker_so = self.compiler.linker_so

        while 1:
            try:
                index = compiler_so.index('-arch')
                del compiler_so[index:index+2]
                index = linker_so.index('-arch')
                del linker_so[index:index+2]
            except ValueError:
                break

        if compiler_so[0] != 'clang' and '-Wshorten-64-to-32' in compiler_so:
            compiler_so.remove('-Wshorten-64-to-32')
            linker_so[0] = compiler_so[0]

        #if sys.platform == 'darwin':
        #    try:
        #        linker_so.remove("-Wl,-F.")
        #        linker_so.remove("-Wl,-F.")
        #    except: pass

        #if copt.has_key(c):
        #   for e in self.extensions:
        #       e.extra_compile_args = copt[ c ]
        #if lopt.has_key(c):
        #    for e in self.extensions:
        #        e.extra_link_args = lopt[ c ]
        
        build_ext.build_extensions(self)


mmcorepy_module = Extension('_MMCorePy',
                           sources=['MMCorePy_wrap.cxx',
			'../MMDevice/DeviceUtils.cpp',
			'../MMDevice/ImgBuffer.cpp', 
			'../MMDevice/Property.cpp', 
			'../MMCore/CircularBuffer.cpp',
			'../MMCore/Configuration.cpp',
			'../MMCore/CoreCallback.cpp',
			'../MMCore/CoreProperty.cpp',
			'../MMCore/FastLogger.cpp',
			'../MMCore/MMCore.cpp',
			'../MMCore/PluginManager.cpp'],
			language = "c++",
			extra_objects = [],
                        include_dirs = ["/Developer/SDKs/MacOSX10.5.sdk/System/Library/Frameworks/Python.framework/Versions/2.5/Extras/lib/python/numpy/core/include/numpy"]
                           )

setup(name='MMCorePy',
      version='0.1',
      author="Micro-Manager",
      description="Micro-Manager Core Python wrapper",
      ext_modules=[mmcorepy_module],
      py_modules=["MMCorePy"],
      cmdclass         = {'build_ext': build_ext_subclass },
     )
