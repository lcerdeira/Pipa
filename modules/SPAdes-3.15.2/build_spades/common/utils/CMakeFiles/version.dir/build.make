# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.20

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:

#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:

# Disable VCS-based implicit rules.
% : %,v

# Disable VCS-based implicit rules.
% : RCS/%

# Disable VCS-based implicit rules.
% : RCS/%,v

# Disable VCS-based implicit rules.
% : SCCS/s.%

# Disable VCS-based implicit rules.
% : s.%

.SUFFIXES: .hpux_make_needs_suffix_list

# Command-line flag to silence nested $(MAKE).
$(VERBOSE)MAKESILENT = -s

#Suppress display of executed commands.
$(VERBOSE).SILENT:

# A target that is always out of date.
cmake_force:
.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/local/bin/cmake

# The command to remove a file.
RM = /usr/local/bin/cmake -E rm -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /root/bio/Modules/SPAdes-3.15.2/src

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /root/bio/Modules/SPAdes-3.15.2/build_spades

# Include any dependencies generated for this target.
include common/utils/CMakeFiles/version.dir/depend.make
# Include any dependencies generated by the compiler for this target.
include common/utils/CMakeFiles/version.dir/compiler_depend.make

# Include the progress variables for this target.
include common/utils/CMakeFiles/version.dir/progress.make

# Include the compile flags for this target's objects.
include common/utils/CMakeFiles/version.dir/flags.make

common/utils/CMakeFiles/version.dir/version.cpp.o: common/utils/CMakeFiles/version.dir/flags.make
common/utils/CMakeFiles/version.dir/version.cpp.o: /root/bio/Modules/SPAdes-3.15.2/src/common/utils/version.cpp
common/utils/CMakeFiles/version.dir/version.cpp.o: common/utils/CMakeFiles/version.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/root/bio/Modules/SPAdes-3.15.2/build_spades/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object common/utils/CMakeFiles/version.dir/version.cpp.o"
	cd /root/bio/Modules/SPAdes-3.15.2/build_spades/common/utils && /usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT common/utils/CMakeFiles/version.dir/version.cpp.o -MF CMakeFiles/version.dir/version.cpp.o.d -o CMakeFiles/version.dir/version.cpp.o -c /root/bio/Modules/SPAdes-3.15.2/src/common/utils/version.cpp

common/utils/CMakeFiles/version.dir/version.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/version.dir/version.cpp.i"
	cd /root/bio/Modules/SPAdes-3.15.2/build_spades/common/utils && /usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /root/bio/Modules/SPAdes-3.15.2/src/common/utils/version.cpp > CMakeFiles/version.dir/version.cpp.i

common/utils/CMakeFiles/version.dir/version.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/version.dir/version.cpp.s"
	cd /root/bio/Modules/SPAdes-3.15.2/build_spades/common/utils && /usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /root/bio/Modules/SPAdes-3.15.2/src/common/utils/version.cpp -o CMakeFiles/version.dir/version.cpp.s

# Object files for target version
version_OBJECTS = \
"CMakeFiles/version.dir/version.cpp.o"

# External object files for target version
version_EXTERNAL_OBJECTS =

common/utils/libversion.a: common/utils/CMakeFiles/version.dir/version.cpp.o
common/utils/libversion.a: common/utils/CMakeFiles/version.dir/build.make
common/utils/libversion.a: common/utils/CMakeFiles/version.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/root/bio/Modules/SPAdes-3.15.2/build_spades/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX static library libversion.a"
	cd /root/bio/Modules/SPAdes-3.15.2/build_spades/common/utils && $(CMAKE_COMMAND) -P CMakeFiles/version.dir/cmake_clean_target.cmake
	cd /root/bio/Modules/SPAdes-3.15.2/build_spades/common/utils && $(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/version.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
common/utils/CMakeFiles/version.dir/build: common/utils/libversion.a
.PHONY : common/utils/CMakeFiles/version.dir/build

common/utils/CMakeFiles/version.dir/clean:
	cd /root/bio/Modules/SPAdes-3.15.2/build_spades/common/utils && $(CMAKE_COMMAND) -P CMakeFiles/version.dir/cmake_clean.cmake
.PHONY : common/utils/CMakeFiles/version.dir/clean

common/utils/CMakeFiles/version.dir/depend:
	cd /root/bio/Modules/SPAdes-3.15.2/build_spades && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /root/bio/Modules/SPAdes-3.15.2/src /root/bio/Modules/SPAdes-3.15.2/src/common/utils /root/bio/Modules/SPAdes-3.15.2/build_spades /root/bio/Modules/SPAdes-3.15.2/build_spades/common/utils /root/bio/Modules/SPAdes-3.15.2/build_spades/common/utils/CMakeFiles/version.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : common/utils/CMakeFiles/version.dir/depend

