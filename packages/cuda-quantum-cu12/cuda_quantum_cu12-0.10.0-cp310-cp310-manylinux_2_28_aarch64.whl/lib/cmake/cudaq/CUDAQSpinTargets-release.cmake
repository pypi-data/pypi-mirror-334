#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "cudaq::cudaq-spin" for configuration "Release"
set_property(TARGET cudaq::cudaq-spin APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(cudaq::cudaq-spin PROPERTIES
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libcudaq-spin.so"
  IMPORTED_SONAME_RELEASE "libcudaq-spin.so"
  )

list(APPEND _cmake_import_check_targets cudaq::cudaq-spin )
list(APPEND _cmake_import_check_files_for_cudaq::cudaq-spin "${_IMPORT_PREFIX}/lib/libcudaq-spin.so" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
