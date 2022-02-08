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
include projects/cds_subgraphs/CMakeFiles/cds-mapping-stats.dir/depend.make
# Include any dependencies generated by the compiler for this target.
include projects/cds_subgraphs/CMakeFiles/cds-mapping-stats.dir/compiler_depend.make

# Include the progress variables for this target.
include projects/cds_subgraphs/CMakeFiles/cds-mapping-stats.dir/progress.make

# Include the compile flags for this target's objects.
include projects/cds_subgraphs/CMakeFiles/cds-mapping-stats.dir/flags.make

projects/cds_subgraphs/CMakeFiles/cds-mapping-stats.dir/stats.cpp.o: projects/cds_subgraphs/CMakeFiles/cds-mapping-stats.dir/flags.make
projects/cds_subgraphs/CMakeFiles/cds-mapping-stats.dir/stats.cpp.o: /root/bio/Modules/SPAdes-3.15.2/src/projects/cds_subgraphs/stats.cpp
projects/cds_subgraphs/CMakeFiles/cds-mapping-stats.dir/stats.cpp.o: projects/cds_subgraphs/CMakeFiles/cds-mapping-stats.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/root/bio/Modules/SPAdes-3.15.2/build_spades/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object projects/cds_subgraphs/CMakeFiles/cds-mapping-stats.dir/stats.cpp.o"
	cd /root/bio/Modules/SPAdes-3.15.2/build_spades/projects/cds_subgraphs && /usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT projects/cds_subgraphs/CMakeFiles/cds-mapping-stats.dir/stats.cpp.o -MF CMakeFiles/cds-mapping-stats.dir/stats.cpp.o.d -o CMakeFiles/cds-mapping-stats.dir/stats.cpp.o -c /root/bio/Modules/SPAdes-3.15.2/src/projects/cds_subgraphs/stats.cpp

projects/cds_subgraphs/CMakeFiles/cds-mapping-stats.dir/stats.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/cds-mapping-stats.dir/stats.cpp.i"
	cd /root/bio/Modules/SPAdes-3.15.2/build_spades/projects/cds_subgraphs && /usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /root/bio/Modules/SPAdes-3.15.2/src/projects/cds_subgraphs/stats.cpp > CMakeFiles/cds-mapping-stats.dir/stats.cpp.i

projects/cds_subgraphs/CMakeFiles/cds-mapping-stats.dir/stats.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/cds-mapping-stats.dir/stats.cpp.s"
	cd /root/bio/Modules/SPAdes-3.15.2/build_spades/projects/cds_subgraphs && /usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /root/bio/Modules/SPAdes-3.15.2/src/projects/cds_subgraphs/stats.cpp -o CMakeFiles/cds-mapping-stats.dir/stats.cpp.s

# Object files for target cds-mapping-stats
cds__mapping__stats_OBJECTS = \
"CMakeFiles/cds-mapping-stats.dir/stats.cpp.o"

# External object files for target cds-mapping-stats
cds__mapping__stats_EXTERNAL_OBJECTS = \
"/root/bio/Modules/SPAdes-3.15.2/build_spades/ext/mimalloc/CMakeFiles/mimalloc-obj.dir/src/static.c.o"

bin/cds-mapping-stats: projects/cds_subgraphs/CMakeFiles/cds-mapping-stats.dir/stats.cpp.o
bin/cds-mapping-stats: ext/mimalloc/CMakeFiles/mimalloc-obj.dir/src/static.c.o
bin/cds-mapping-stats: projects/cds_subgraphs/CMakeFiles/cds-mapping-stats.dir/build.make
bin/cds-mapping-stats: common/io/graph/libgraphio.a
bin/cds-mapping-stats: common/libcommon_modules.a
bin/cds-mapping-stats: common/utils/libversion.a
bin/cds-mapping-stats: ext/cppformat/libformat.a
bin/cds-mapping-stats: ext/gfa1/libgfa1.a
bin/cds-mapping-stats: common/paired_info/libpaired_info.a
bin/cds-mapping-stats: common/stages/libstages.a
bin/cds-mapping-stats: common/pipeline/libpipeline.a
bin/cds-mapping-stats: common/io/libinput.a
bin/cds-mapping-stats: ext/samtools/libsamtools.a
bin/cds-mapping-stats: ext/bamtools/api/libBamTools.a
bin/cds-mapping-stats: /usr/lib/x86_64-linux-gnu/libz.so
bin/cds-mapping-stats: common/modules/path_extend/libpath_extend.a
bin/cds-mapping-stats: ext/ssw/libssw.a
bin/cds-mapping-stats: common/io/binary/libbinary_io.a
bin/cds-mapping-stats: common/modules/coverage_model/libcoverage_model.a
bin/cds-mapping-stats: ext/nlopt/libnlopt.a
bin/cds-mapping-stats: ext/gqf/libgqf.a
bin/cds-mapping-stats: common/modules/libmodules.a
bin/cds-mapping-stats: common/assembly_graph/libassembly_graph.a
bin/cds-mapping-stats: common/utils/libutils.a
bin/cds-mapping-stats: common/utils/libversion.a
bin/cds-mapping-stats: ext/cppformat/libformat.a
bin/cds-mapping-stats: ext/llvm/libllvm-support.a
bin/cds-mapping-stats: /usr/lib/x86_64-linux-gnu/libdl.so
bin/cds-mapping-stats: common/sequence/libsequence.a
bin/cds-mapping-stats: ext/edlib/libedlib.a
bin/cds-mapping-stats: ext/bwa/libbwa.a
bin/cds-mapping-stats: projects/cds_subgraphs/CMakeFiles/cds-mapping-stats.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/root/bio/Modules/SPAdes-3.15.2/build_spades/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX executable ../../bin/cds-mapping-stats"
	cd /root/bio/Modules/SPAdes-3.15.2/build_spades/projects/cds_subgraphs && $(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/cds-mapping-stats.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
projects/cds_subgraphs/CMakeFiles/cds-mapping-stats.dir/build: bin/cds-mapping-stats
.PHONY : projects/cds_subgraphs/CMakeFiles/cds-mapping-stats.dir/build

projects/cds_subgraphs/CMakeFiles/cds-mapping-stats.dir/clean:
	cd /root/bio/Modules/SPAdes-3.15.2/build_spades/projects/cds_subgraphs && $(CMAKE_COMMAND) -P CMakeFiles/cds-mapping-stats.dir/cmake_clean.cmake
.PHONY : projects/cds_subgraphs/CMakeFiles/cds-mapping-stats.dir/clean

projects/cds_subgraphs/CMakeFiles/cds-mapping-stats.dir/depend:
	cd /root/bio/Modules/SPAdes-3.15.2/build_spades && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /root/bio/Modules/SPAdes-3.15.2/src /root/bio/Modules/SPAdes-3.15.2/src/projects/cds_subgraphs /root/bio/Modules/SPAdes-3.15.2/build_spades /root/bio/Modules/SPAdes-3.15.2/build_spades/projects/cds_subgraphs /root/bio/Modules/SPAdes-3.15.2/build_spades/projects/cds_subgraphs/CMakeFiles/cds-mapping-stats.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : projects/cds_subgraphs/CMakeFiles/cds-mapping-stats.dir/depend

