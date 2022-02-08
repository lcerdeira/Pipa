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
include common/io/binary/CMakeFiles/binary_io.dir/depend.make
# Include any dependencies generated by the compiler for this target.
include common/io/binary/CMakeFiles/binary_io.dir/compiler_depend.make

# Include the progress variables for this target.
include common/io/binary/CMakeFiles/binary_io.dir/progress.make

# Include the compile flags for this target's objects.
include common/io/binary/CMakeFiles/binary_io.dir/flags.make

common/io/binary/CMakeFiles/binary_io.dir/graph_pack.cpp.o: common/io/binary/CMakeFiles/binary_io.dir/flags.make
common/io/binary/CMakeFiles/binary_io.dir/graph_pack.cpp.o: /root/bio/Modules/SPAdes-3.15.2/src/common/io/binary/graph_pack.cpp
common/io/binary/CMakeFiles/binary_io.dir/graph_pack.cpp.o: common/io/binary/CMakeFiles/binary_io.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/root/bio/Modules/SPAdes-3.15.2/build_spades/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object common/io/binary/CMakeFiles/binary_io.dir/graph_pack.cpp.o"
	cd /root/bio/Modules/SPAdes-3.15.2/build_spades/common/io/binary && /usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT common/io/binary/CMakeFiles/binary_io.dir/graph_pack.cpp.o -MF CMakeFiles/binary_io.dir/graph_pack.cpp.o.d -o CMakeFiles/binary_io.dir/graph_pack.cpp.o -c /root/bio/Modules/SPAdes-3.15.2/src/common/io/binary/graph_pack.cpp

common/io/binary/CMakeFiles/binary_io.dir/graph_pack.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/binary_io.dir/graph_pack.cpp.i"
	cd /root/bio/Modules/SPAdes-3.15.2/build_spades/common/io/binary && /usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /root/bio/Modules/SPAdes-3.15.2/src/common/io/binary/graph_pack.cpp > CMakeFiles/binary_io.dir/graph_pack.cpp.i

common/io/binary/CMakeFiles/binary_io.dir/graph_pack.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/binary_io.dir/graph_pack.cpp.s"
	cd /root/bio/Modules/SPAdes-3.15.2/build_spades/common/io/binary && /usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /root/bio/Modules/SPAdes-3.15.2/src/common/io/binary/graph_pack.cpp -o CMakeFiles/binary_io.dir/graph_pack.cpp.s

common/io/binary/CMakeFiles/binary_io.dir/genomic_info.cpp.o: common/io/binary/CMakeFiles/binary_io.dir/flags.make
common/io/binary/CMakeFiles/binary_io.dir/genomic_info.cpp.o: /root/bio/Modules/SPAdes-3.15.2/src/common/io/binary/genomic_info.cpp
common/io/binary/CMakeFiles/binary_io.dir/genomic_info.cpp.o: common/io/binary/CMakeFiles/binary_io.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/root/bio/Modules/SPAdes-3.15.2/build_spades/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Building CXX object common/io/binary/CMakeFiles/binary_io.dir/genomic_info.cpp.o"
	cd /root/bio/Modules/SPAdes-3.15.2/build_spades/common/io/binary && /usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT common/io/binary/CMakeFiles/binary_io.dir/genomic_info.cpp.o -MF CMakeFiles/binary_io.dir/genomic_info.cpp.o.d -o CMakeFiles/binary_io.dir/genomic_info.cpp.o -c /root/bio/Modules/SPAdes-3.15.2/src/common/io/binary/genomic_info.cpp

common/io/binary/CMakeFiles/binary_io.dir/genomic_info.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/binary_io.dir/genomic_info.cpp.i"
	cd /root/bio/Modules/SPAdes-3.15.2/build_spades/common/io/binary && /usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /root/bio/Modules/SPAdes-3.15.2/src/common/io/binary/genomic_info.cpp > CMakeFiles/binary_io.dir/genomic_info.cpp.i

common/io/binary/CMakeFiles/binary_io.dir/genomic_info.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/binary_io.dir/genomic_info.cpp.s"
	cd /root/bio/Modules/SPAdes-3.15.2/build_spades/common/io/binary && /usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /root/bio/Modules/SPAdes-3.15.2/src/common/io/binary/genomic_info.cpp -o CMakeFiles/binary_io.dir/genomic_info.cpp.s

# Object files for target binary_io
binary_io_OBJECTS = \
"CMakeFiles/binary_io.dir/graph_pack.cpp.o" \
"CMakeFiles/binary_io.dir/genomic_info.cpp.o"

# External object files for target binary_io
binary_io_EXTERNAL_OBJECTS =

common/io/binary/libbinary_io.a: common/io/binary/CMakeFiles/binary_io.dir/graph_pack.cpp.o
common/io/binary/libbinary_io.a: common/io/binary/CMakeFiles/binary_io.dir/genomic_info.cpp.o
common/io/binary/libbinary_io.a: common/io/binary/CMakeFiles/binary_io.dir/build.make
common/io/binary/libbinary_io.a: common/io/binary/CMakeFiles/binary_io.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/root/bio/Modules/SPAdes-3.15.2/build_spades/CMakeFiles --progress-num=$(CMAKE_PROGRESS_3) "Linking CXX static library libbinary_io.a"
	cd /root/bio/Modules/SPAdes-3.15.2/build_spades/common/io/binary && $(CMAKE_COMMAND) -P CMakeFiles/binary_io.dir/cmake_clean_target.cmake
	cd /root/bio/Modules/SPAdes-3.15.2/build_spades/common/io/binary && $(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/binary_io.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
common/io/binary/CMakeFiles/binary_io.dir/build: common/io/binary/libbinary_io.a
.PHONY : common/io/binary/CMakeFiles/binary_io.dir/build

common/io/binary/CMakeFiles/binary_io.dir/clean:
	cd /root/bio/Modules/SPAdes-3.15.2/build_spades/common/io/binary && $(CMAKE_COMMAND) -P CMakeFiles/binary_io.dir/cmake_clean.cmake
.PHONY : common/io/binary/CMakeFiles/binary_io.dir/clean

common/io/binary/CMakeFiles/binary_io.dir/depend:
	cd /root/bio/Modules/SPAdes-3.15.2/build_spades && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /root/bio/Modules/SPAdes-3.15.2/src /root/bio/Modules/SPAdes-3.15.2/src/common/io/binary /root/bio/Modules/SPAdes-3.15.2/build_spades /root/bio/Modules/SPAdes-3.15.2/build_spades/common/io/binary /root/bio/Modules/SPAdes-3.15.2/build_spades/common/io/binary/CMakeFiles/binary_io.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : common/io/binary/CMakeFiles/binary_io.dir/depend

