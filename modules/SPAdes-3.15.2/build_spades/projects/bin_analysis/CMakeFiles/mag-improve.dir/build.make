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
include projects/bin_analysis/CMakeFiles/mag-improve.dir/depend.make
# Include any dependencies generated by the compiler for this target.
include projects/bin_analysis/CMakeFiles/mag-improve.dir/compiler_depend.make

# Include the progress variables for this target.
include projects/bin_analysis/CMakeFiles/mag-improve.dir/progress.make

# Include the compile flags for this target's objects.
include projects/bin_analysis/CMakeFiles/mag-improve.dir/flags.make

projects/bin_analysis/CMakeFiles/mag-improve.dir/main.cpp.o: projects/bin_analysis/CMakeFiles/mag-improve.dir/flags.make
projects/bin_analysis/CMakeFiles/mag-improve.dir/main.cpp.o: /root/bio/Modules/SPAdes-3.15.2/src/projects/bin_analysis/main.cpp
projects/bin_analysis/CMakeFiles/mag-improve.dir/main.cpp.o: projects/bin_analysis/CMakeFiles/mag-improve.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/root/bio/Modules/SPAdes-3.15.2/build_spades/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object projects/bin_analysis/CMakeFiles/mag-improve.dir/main.cpp.o"
	cd /root/bio/Modules/SPAdes-3.15.2/build_spades/projects/bin_analysis && /usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT projects/bin_analysis/CMakeFiles/mag-improve.dir/main.cpp.o -MF CMakeFiles/mag-improve.dir/main.cpp.o.d -o CMakeFiles/mag-improve.dir/main.cpp.o -c /root/bio/Modules/SPAdes-3.15.2/src/projects/bin_analysis/main.cpp

projects/bin_analysis/CMakeFiles/mag-improve.dir/main.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/mag-improve.dir/main.cpp.i"
	cd /root/bio/Modules/SPAdes-3.15.2/build_spades/projects/bin_analysis && /usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /root/bio/Modules/SPAdes-3.15.2/src/projects/bin_analysis/main.cpp > CMakeFiles/mag-improve.dir/main.cpp.i

projects/bin_analysis/CMakeFiles/mag-improve.dir/main.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/mag-improve.dir/main.cpp.s"
	cd /root/bio/Modules/SPAdes-3.15.2/build_spades/projects/bin_analysis && /usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /root/bio/Modules/SPAdes-3.15.2/src/projects/bin_analysis/main.cpp -o CMakeFiles/mag-improve.dir/main.cpp.s

# Object files for target mag-improve
mag__improve_OBJECTS = \
"CMakeFiles/mag-improve.dir/main.cpp.o"

# External object files for target mag-improve
mag__improve_EXTERNAL_OBJECTS = \
"/root/bio/Modules/SPAdes-3.15.2/build_spades/ext/mimalloc/CMakeFiles/mimalloc-obj.dir/src/static.c.o"

bin/mag-improve: projects/bin_analysis/CMakeFiles/mag-improve.dir/main.cpp.o
bin/mag-improve: ext/mimalloc/CMakeFiles/mimalloc-obj.dir/src/static.c.o
bin/mag-improve: projects/bin_analysis/CMakeFiles/mag-improve.dir/build.make
bin/mag-improve: common/io/graph/libgraphio.a
bin/mag-improve: common/libcommon_modules.a
bin/mag-improve: common/utils/libversion.a
bin/mag-improve: ext/cppformat/libformat.a
bin/mag-improve: ext/gfa1/libgfa1.a
bin/mag-improve: common/paired_info/libpaired_info.a
bin/mag-improve: common/stages/libstages.a
bin/mag-improve: common/pipeline/libpipeline.a
bin/mag-improve: common/io/libinput.a
bin/mag-improve: ext/samtools/libsamtools.a
bin/mag-improve: ext/bamtools/api/libBamTools.a
bin/mag-improve: /usr/lib/x86_64-linux-gnu/libz.so
bin/mag-improve: common/modules/path_extend/libpath_extend.a
bin/mag-improve: ext/ssw/libssw.a
bin/mag-improve: common/io/binary/libbinary_io.a
bin/mag-improve: common/modules/coverage_model/libcoverage_model.a
bin/mag-improve: ext/nlopt/libnlopt.a
bin/mag-improve: ext/gqf/libgqf.a
bin/mag-improve: common/modules/libmodules.a
bin/mag-improve: common/assembly_graph/libassembly_graph.a
bin/mag-improve: common/utils/libutils.a
bin/mag-improve: common/utils/libversion.a
bin/mag-improve: ext/cppformat/libformat.a
bin/mag-improve: ext/llvm/libllvm-support.a
bin/mag-improve: /usr/lib/x86_64-linux-gnu/libdl.so
bin/mag-improve: common/sequence/libsequence.a
bin/mag-improve: ext/edlib/libedlib.a
bin/mag-improve: ext/bwa/libbwa.a
bin/mag-improve: projects/bin_analysis/CMakeFiles/mag-improve.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/root/bio/Modules/SPAdes-3.15.2/build_spades/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX executable ../../bin/mag-improve"
	cd /root/bio/Modules/SPAdes-3.15.2/build_spades/projects/bin_analysis && $(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/mag-improve.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
projects/bin_analysis/CMakeFiles/mag-improve.dir/build: bin/mag-improve
.PHONY : projects/bin_analysis/CMakeFiles/mag-improve.dir/build

projects/bin_analysis/CMakeFiles/mag-improve.dir/clean:
	cd /root/bio/Modules/SPAdes-3.15.2/build_spades/projects/bin_analysis && $(CMAKE_COMMAND) -P CMakeFiles/mag-improve.dir/cmake_clean.cmake
.PHONY : projects/bin_analysis/CMakeFiles/mag-improve.dir/clean

projects/bin_analysis/CMakeFiles/mag-improve.dir/depend:
	cd /root/bio/Modules/SPAdes-3.15.2/build_spades && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /root/bio/Modules/SPAdes-3.15.2/src /root/bio/Modules/SPAdes-3.15.2/src/projects/bin_analysis /root/bio/Modules/SPAdes-3.15.2/build_spades /root/bio/Modules/SPAdes-3.15.2/build_spades/projects/bin_analysis /root/bio/Modules/SPAdes-3.15.2/build_spades/projects/bin_analysis/CMakeFiles/mag-improve.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : projects/bin_analysis/CMakeFiles/mag-improve.dir/depend

