
AC_PREREQ([2.64])
AC_INIT([Micro-Manager], [1.4], [info@micro-manager.org])
AC_CONFIG_MACRO_DIR([m4])
AC_CONFIG_SRCDIR([MMCore/MMCore.cpp])
AC_CANONICAL_BUILD
AC_CANONICAL_HOST
AM_INIT_AUTOMAKE([foreign 1.11])
LT_PREREQ([2.2.6])
LT_INIT([disable-static])
AC_PROG_MKDIR_P

AC_PROG_CXX([clang++ llvm-g++ g++ c++])
AC_PROG_CC([clang llvm-gcc gcc cc])


# Boost
# TODO Reflect results in configuration
AX_BOOST_BASE([1.46.0])
AX_BOOST_DATE_TIME
AX_BOOST_SYSTEM


# zlib
# TODO Make optional (MMDevice and device adapters do not need zlib)
MM_ARG_WITH_REQUIRED_LIB([zlib], [zlib], [ZLIB])
MM_LIB_Z([$ZLIB_PREFIX], [], [MM_MSG_REQUIRED_LIB_FAILURE([zlib], [zlib])])


# AppleHost dependencies
case $host in
   *apple-darwin*) MMCORE_APPLEHOST_LDFLAGS="-framework CoreFoundation -framework IOKit" ;;
   *) MMCORE_APPLEHOST_LDFLAGS="" ;;
esac
AC_SUBST([MMCORE_APPLEHOST_LDFLAGS])


# TODO Make conditional
can_build_mmcore=yes


##
## MMCoreJ and MMCorePy
##

# SWIG
AC_ARG_VAR([SWIG], [Simple Wrapper and Interface Generator])
AC_CHECK_PROGS([SWIG], [swig])
# TODO Provide SWIGFLAGS as precious variable


# Java

if test -n "$with_javaincl"; then
   AC_MSG_ERROR([--with-javaincl has been removed. You can use one of the following:
  ./configure --with-java=/path/to/java/home
  ./configure JNI_CPPFLAGS="-I/path/to/jni/include"
If you set the Java home, bin/javac and include/jni.h in that directory will be
used. If you set JNI_CPPFLAGS, it will override any automatic detection.
See ./configure --help for more options.])
fi

AC_ARG_VAR([JAVA_HOME], [JDK home directory])
AC_ARG_VAR([JAVACFLAGS], [Java compiler flags])
MM_ARG_WITH_JAVA
AS_IF([test "x$want_java" != xno],
[
   AS_IF([test -n "$JAVA_PREFIX"],
   [
      AS_IF([test -n "$JAVA_HOME"],
      [
         AC_MSG_ERROR([--with-java argument and JAVA_HOME both given. Try removing argument from --with-java])
      ],
      [
         JAVA_HOME="$JAVA_PREFIX"
      ])
   ],
   [
      AS_IF([test -z "$JAVA_HOME"],
      [
         case "$build_os" in
            darwin*) JAVA_HOME=`/usr/libexec/java_home`;;
         esac
      ])
   ])
   have_java=no
   MM_PROGS_JAVA(
   [
      MM_HEADERS_JNI(
      [
         have_java=yes
      ])
   ])

   AS_IF([test "x$want_java" = xyes],
   [
      AS_IF([test "x$have_java" = xno],
      [
         AC_MSG_FAILURE([--with-java was given, but test for Java and JNI failed])
      ])
   ])
   use_java=$have_java
],
[
   use_java=no
])

MM_JNI_LIBRARY_PREFIX_SUFFIX
AM_CONDITIONAL([NONSTD_JNI_PREFIX], [test "x$JNI_PREFIX" != xlib])


build_mmcorej=yes
test "x$can_build_mmcore" = xno && build_mmcorej=no
test "x$use_java" = xno && build_mmcorej=no
test -z "$SWIG" && build_mmcorej=no
AM_CONDITIONAL([BUILD_MMCOREJ], [test "x$build_mmcorej" = xyes])


enable_hardcoded_mmcorej_library_path_default=yes
test "x$enable_imagej_plugin" != xno && enable_hardcoded_mmcorej_library_path_default=no
AC_ARG_ENABLE([hardcoded-mmcorej-library-path],
   [AS_HELP_STRING([--disable-hardcoded-mmcorej-library-path],
                   [Do not use a fallback absolute path to locate the
                    MMCoreJ_wrap native library (default: disable if building
                    as ImageJ plugin; otherwise enable)])],
   [],
   [enable_hardcoded_mmcorej_library_path=yes])
if test "x$enable_hardcoded_mmcorej_library_path" = xyes; then
   # The path to be hard-coded into MMCoreJ's Java class loading code. This
   # should be the value of pkglibdir at build time (not configuration time),
   # so we use an escaped make variable substitution (recall that normal make
   # variables are recursively expanded).
   MMCOREJ_LIBRARY_PATH="\$(pkglibdir)"
else
   MMCOREJ_LIBRARY_PATH=
fi
AC_SUBST([MMCOREJ_LIBRARY_PATH])


# Python and NumPy
MM_ARG_WITH_PYTHON
AS_IF([test "x$want_python" != xno],
[
   AS_IF([test -n "$PYTHON_PREFIX"],
   [
      # Be lenient if user gives --with-python=bindir instead of
      # --with-python=prefix.
      MM_PROG_PYTHON([$PYTHON_PREFIX/bin $PYTHON_PREFIX])
   ],
   [
      MM_PROG_PYTHON
   ])

   have_python=no
   AS_IF([test -n "$PYTHON"],
   [
      MM_HEADERS_PYTHON(
      [
         MM_HEADERS_NUMPY([have_python=yes])
      ])
   ])

   AS_IF([test "x$want_python" = xyes],
   [
      AS_IF([test "x$have_python" = xno],
      [
         AC_MSG_FAILURE([--with-python was given, but test for Python and NumPy failed])
      ])
   ])
   use_python=$have_python
],
[
   use_python=no
])


build_mmcorepy=yes
test "x$can_build_mmcore" = xno && build_mmcorepy=no
test "x$use_python" = xno && build_mmcorepy=no
test -z "$SWIG" && build_mmcorepy=no
AM_CONDITIONAL([BUILD_MMCOREPY], [test "x$build_mmcorepy" = xyes])


build_mmcore=no
test "x$build_mmcorej" = xyes && build_mmcore=yes
test "x$build_mmcorepy" = xyes && build_mmcore=yes
AM_CONDITIONAL([BUILD_MMCORE], [test "x$build_mmcore" = xyes])


##
## Java application (MMStudio and plugins)
##

AC_ARG_ENABLE([java-app],
   [AS_HELP_STRING([--disable-java-app], [do not build the Java app])],
   [], [enable_java_app=auto])

build_java_app=yes
test "x$enable_java_app" = xno && build_java_app=no
test "x$build_mmcorej" = xno && build_java_app=no
# TODO Require dependency JARs

AS_IF([test "x$enable_java_app" = xyes],
[
   AS_IF([test "x$build_java_app" = xno],
   [
      AC_MSG_ERROR([--enable-java-app was given, but prerequisites were not satisfied])
   ])
])

AM_CONDITIONAL([BUILD_JAVA_APP], [test "x$build_java_app" = xyes])


if test -n "$with_imagej"; then
   AC_MSG_ERROR([--with-imagej has been removed. Please use --enable-imagej-plugin and (optionally) --with-ij-jar.])
fi


# Set the default install directories used in Makefile.am's.
MM_INSTALL_DIRS


# Allow user to override location of ij.jar (whether or not we are building as
# ImageJ plugin). If we are building as ImageJ plugin, default to the ij.jar in
# the target ImageJ directory. Otherwise do not set imagejjar, and use the copy
# in CLASSEXT.
AC_ARG_WITH([ij-jar],
   [AS_HELP_STRING([--with-ij-jar=FILE],
      [Use specified ImageJ ij.jar for building and running])],
   [], [with_ij_jar=auto])
case $with_ij_jar in
   yes) AC_MSG_ERROR([--with-ij-jar requires argument (ij.jar path)]) ;;
   no)  imagejjar="";;
   *)   imagejjar="$with_ij_jar";;
esac
if test "x$imagejjar" = xauto; then
   if test -n "$imagejdir"; then
      AC_MSG_CHECKING([for ij.jar under $imagejdir])
      # Select the first ij.jar found
      imagejjar=`find "$imagejdir" -name ij.jar | head -n 1`
      if test -z "$imagejjar"; then
         AC_MSG_RESULT([no])
         AC_MSG_ERROR([use --with-ij-jar=FILE to specify where to find ij.jar])
      fi
      # But make sure all copies are equal (this is for cases like the OS X
      # version, where there is one copy each within ImageJ.app and
      # ImageJ64.app)
      for ij_jar in `find "$imagejdir" -name ij.jar`
      do
         if cmp -s "$imagejjar" "$ij_jar"; then :; else
            AC_MSG_RESULT([multiple non-identical copies])
            AC_MSG_ERROR([use --with-ij-jar=FILE to specify which ij.jar to use])
         fi
      done
      AC_MSG_RESULT([$imagejjar])
   else
      imagejjar=
   fi
fi
AC_SUBST([imagejjar])


# Java dependencies. These should be checked for and their location should be
# configurable (CLASSPATH for each library). For now, hard-coded to
# 3rdpartypublic.
if test "x$build_java_app" = xyes; then
   # TODO This path should be configurable. And we should have an automated way
   # to fetch dependencies, but that is a future project.
   CLASSEXT="\$(top_srcdir)/../3rdpartypublic/classext"

   # For now, just use hard-coded locations for dependency JARs. Ideally, we
   # would just use a user-provided classpath and check for classes, not JARs.
   # (In addition to that, there should be a way to fetch dependencies using
   # Ivy.)

   # Note: imagejjar is the location of an installed ij.jar (part of the
   # system). IJJARPATH is the ij.jar to use for the build, which may not be
   # installed.
   if test -n "$imagejjar"; then
      IJJARPATH="$imagejjar"
   else
      IJJARPATH="$CLASSEXT/ij.jar"
   fi
   BSHJARPATH="$CLASSEXT/bsh-2.0b4.jar"
   SWINGXJARPATH="$CLASSEXT/swingx-0.9.5.jar"
   COMMONSMATHJARPATH="$CLASSEXT/commons-math-2.0.jar"
   SWINGLAYOUTJARPATH="$CLASSEXT/swing-layout-1.0.4.jar"
   ABSOLUTEJARPATH="$CLASSEXT/AbsoluteLayout.jar"
   JFREECHARTJARPATH="$CLASSEXT/jfreechart-1.0.13.jar:$CLASSEXT/jcommon-1.0.16.jar"
   # TODO This list is incomplete, and various Makefile.am's are using CLASSEXT
   # with the JAR name.
fi

AC_SUBST(CLASSEXT)
AC_SUBST(BSHJARPATH)
AC_SUBST(SWINGXJARPATH)
AC_SUBST(COMMONSMATHJARPATH)
AC_SUBST(SWINGLAYOUTJARPATH)
AC_SUBST(ABSOLUTEJARPATH)
AC_SUBST(JFREECHARTJARPATH)
AC_SUBST(IJJARPATH)


AC_ARG_ENABLE([install-dependency-jars],
   [AS_HELP_STRING([--disable-install-dependency-jars],
      [Do not install third-party library JARs])],
   [], [enable_install_dependency_jars=yes])
test "x$build_java_app" = xno && enable_install_dependency_jars=no
AM_CONDITIONAL([INSTALL_DEPENDENCY_JARS],
      [test "x$enable_install_dependency_jars" != xno])


##
## Leftover stuff (needs cleanup)
##

AC_HEADER_STDC
AC_HEADER_STDBOOL
AC_C_CONST
AC_C_INLINE
AC_CHECK_FUNCS([memset])
AC_CHECK_LIB(dl, dlopen)


# Install Device Adapter API library and headers
install_mmdevapi=false
# TODO reinstate this flag in some better form
#AC_ARG_ENABLE(inst-devapi,
#    [  --enable-inst-devapi    Install the Device Adapter API library and headers ],
#    [ install_mmdevapi=true ])
AM_CONDITIONAL([INSTALL_MMDEVAPI], [test x$install_mmdevapi = xtrue])


##
## Subdirectory configuration
##

AC_MSG_CHECKING([for proprietary device adapter source])
AS_IF([test -f "$srcdir/SecretDeviceAdapters/configure"],
   [build_secretdeviceadapters=yes], [build_secretdeviceadapters=no])
AM_CONDITIONAL([BUILD_SECRETDEVICEADAPTERS],
   [test "x$build_secretdeviceadapters" = xyes])

AC_CONFIG_SUBDIRS([DeviceAdapters])
AS_IF([test "x$build_secretdeviceadapters" = xyes], [
   AC_CONFIG_SUBDIRS([SecretDeviceAdapters])
])
AC_CONFIG_SUBDIRS([DeviceKit])


##
## Output generation
##

AC_CONFIG_FILES(m4_strip([
   Makefile
   MMDevice/Makefile
   MMCore/Makefile
   MMCoreJ_wrap/Makefile
   MMCorePy_wrap/Makefile
   mmstudio/Makefile
   acqEngine/Makefile
   plugins/Makefile
   autofocus/Makefile
   scripts/Makefile
   bindist/Makefile
]))

AC_OUTPUT

echo ""
echo "m4_text_box([Micro-Manager configuration])"
echo ""

if test "x$use_java" = xyes; then
echo "   JAVA_HOME    = $JAVA_HOME"
echo "   JNI_CPPFLAGS = $JNI_CPPFLAGS"
echo "   JAVAC        = $JAVAC"
echo ""
fi

if test "x$use_python" = xyes; then
echo "   PYTHON          = $PYTHON"
echo "   PYTHON_CPPFLAGS = $PYTHON_CPPFLAGS"
echo "   NUMPY_CPPFLAGS  = $NUMPY_CPPFLAGS"
echo ""
fi

echo "   Build MMCoreJ (MMCore Java wrapper):    $build_mmcorej"
echo "   Build MMCorePy (MMCore Python wrapper): $build_mmcorepy"
echo "   Build Java application (MMStudio):      $build_java_app"
echo "   Build device adapters:                  yes"
echo "   Build closed-source device adapters:    $build_secretdeviceadapters"
echo ""

if test "x$build_java_app" = xyes; then
AM_COND_IF([INSTALL_AS_IMAGEJ_PLUGIN],
[
echo "   Install MMStudio as ImageJ plugin:      yes"
echo "   Target ImageJ directory:                $imagejdir"
],
[
echo "   Install MMStudio as ImageJ plugin:      no"
echo "   Installation prefix:                    $prefix"
])
if test -n "$imagejjar"; then
echo "   ij.jar:                                 $imagejjar"
else
echo "   ij.jar:                                 from build classpath"
fi
AM_COND_IF([INSTALL_DEPENDENCY_JARS],
[
echo "   Install dependency JARs:                yes"
],
[
echo "   Install dependency JARs:                no"
])
echo ""
fi # build_java_app

echo "Now type 'make' to build."
echo "Then type 'make install' to install."
