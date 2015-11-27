INCLUDE(FindPkgConfig)
PKG_CHECK_MODULES(PC_AUTOTUNE autotune)

FIND_PATH(
    AUTOTUNE_INCLUDE_DIRS
    NAMES autotune/api.h
    HINTS $ENV{AUTOTUNE_DIR}/include
        ${PC_AUTOTUNE_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    AUTOTUNE_LIBRARIES
    NAMES gnuradio-autotune
    HINTS $ENV{AUTOTUNE_DIR}/lib
        ${PC_AUTOTUNE_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
)

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(AUTOTUNE DEFAULT_MSG AUTOTUNE_LIBRARIES AUTOTUNE_INCLUDE_DIRS)
MARK_AS_ADVANCED(AUTOTUNE_LIBRARIES AUTOTUNE_INCLUDE_DIRS)

