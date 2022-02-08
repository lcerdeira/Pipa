# Install script for directory: /root/bio/Modules/SPAdes-3.15.2/src/projects

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/root/bio/Modules/SPAdes-3.15.2")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "RelWithDebInfo")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Install shared libraries without execute permission?
if(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)
  set(CMAKE_INSTALL_SO_NO_EXE "1")
endif()

# Is this installation the result of a crosscompile?
if(NOT DEFINED CMAKE_CROSSCOMPILING)
  set(CMAKE_CROSSCOMPILING "FALSE")
endif()

# Set default install directory permissions.
if(NOT DEFINED CMAKE_OBJDUMP)
  set(CMAKE_OBJDUMP "/usr/bin/objdump")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for each subdirectory.
  include("/root/bio/Modules/SPAdes-3.15.2/build_spades/projects/spades/cmake_install.cmake")
  include("/root/bio/Modules/SPAdes-3.15.2/build_spades/projects/hammer/cmake_install.cmake")
  include("/root/bio/Modules/SPAdes-3.15.2/build_spades/projects/ionhammer/cmake_install.cmake")
  include("/root/bio/Modules/SPAdes-3.15.2/build_spades/projects/corrector/cmake_install.cmake")
  include("/root/bio/Modules/SPAdes-3.15.2/build_spades/projects/scaffold_correction/cmake_install.cmake")
  include("/root/bio/Modules/SPAdes-3.15.2/build_spades/projects/kmercount/cmake_install.cmake")
  include("/root/bio/Modules/SPAdes-3.15.2/build_spades/projects/bin_converter/cmake_install.cmake")
  include("/root/bio/Modules/SPAdes-3.15.2/build_spades/projects/gbuilder/cmake_install.cmake")
  include("/root/bio/Modules/SPAdes-3.15.2/build_spades/projects/gmapper/cmake_install.cmake")
  include("/root/bio/Modules/SPAdes-3.15.2/build_spades/projects/unitig_coverage/cmake_install.cmake")
  include("/root/bio/Modules/SPAdes-3.15.2/build_spades/projects/spaligner/cmake_install.cmake")
  include("/root/bio/Modules/SPAdes-3.15.2/build_spades/projects/gsimplifier/cmake_install.cmake")
  include("/root/bio/Modules/SPAdes-3.15.2/build_spades/projects/cds_subgraphs/cmake_install.cmake")
  include("/root/bio/Modules/SPAdes-3.15.2/build_spades/projects/bin_analysis/cmake_install.cmake")

endif()

