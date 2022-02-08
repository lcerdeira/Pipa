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
include projects/spaligner/CMakeFiles/spaligner.dir/depend.make
# Include any dependencies generated by the compiler for this target.
include projects/spaligner/CMakeFiles/spaligner.dir/compiler_depend.make

# Include the progress variables for this target.
include projects/spaligner/CMakeFiles/spaligner.dir/progress.make

# Include the compile flags for this target's objects.
include projects/spaligner/CMakeFiles/spaligner.dir/flags.make

projects/spaligner/CMakeFiles/spaligner.dir/align_longreads.cpp.o: projects/spaligner/CMakeFiles/spaligner.dir/flags.make
projects/spaligner/CMakeFiles/spaligner.dir/align_longreads.cpp.o: /root/bio/Modules/SPAdes-3.15.2/src/projects/spaligner/align_longreads.cpp
projects/spaligner/CMakeFiles/spaligner.dir/align_longreads.cpp.o: projects/spaligner/CMakeFiles/spaligner.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/root/bio/Modules/SPAdes-3.15.2/build_spades/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object projects/spaligner/CMakeFiles/spaligner.dir/align_longreads.cpp.o"
	cd /root/bio/Modules/SPAdes-3.15.2/build_spades/projects/spaligner && /usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT projects/spaligner/CMakeFiles/spaligner.dir/align_longreads.cpp.o -MF CMakeFiles/spaligner.dir/align_longreads.cpp.o.d -o CMakeFiles/spaligner.dir/align_longreads.cpp.o -c /root/bio/Modules/SPAdes-3.15.2/src/projects/spaligner/align_longreads.cpp

projects/spaligner/CMakeFiles/spaligner.dir/align_longreads.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/spaligner.dir/align_longreads.cpp.i"
	cd /root/bio/Modules/SPAdes-3.15.2/build_spades/projects/spaligner && /usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /root/bio/Modules/SPAdes-3.15.2/src/projects/spaligner/align_longreads.cpp > CMakeFiles/spaligner.dir/align_longreads.cpp.i

projects/spaligner/CMakeFiles/spaligner.dir/align_longreads.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/spaligner.dir/align_longreads.cpp.s"
	cd /root/bio/Modules/SPAdes-3.15.2/build_spades/projects/spaligner && /usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /root/bio/Modules/SPAdes-3.15.2/src/projects/spaligner/align_longreads.cpp -o CMakeFiles/spaligner.dir/align_longreads.cpp.s

# Object files for target spaligner
spaligner_OBJECTS = \
"CMakeFiles/spaligner.dir/align_longreads.cpp.o"

# External object files for target spaligner
spaligner_EXTERNAL_OBJECTS = \
"/root/bio/Modules/SPAdes-3.15.2/build_spades/ext/mimalloc/CMakeFiles/mimalloc-obj.dir/src/static.c.o"

bin/spaligner: projects/spaligner/CMakeFiles/spaligner.dir/align_longreads.cpp.o
bin/spaligner: ext/mimalloc/CMakeFiles/mimalloc-obj.dir/src/static.c.o
bin/spaligner: projects/spaligner/CMakeFiles/spaligner.dir/build.make
bin/spaligner: projects/spaligner/libmapping_printer.a
bin/spaligner: common/libcommon_modules.a
bin/spaligner: ext/bwa/libbwa.a
bin/spaligner: ext/edlib/libedlib.a
bin/spaligner: common/io/graph/libgraphio.a
bin/spaligner: common/utils/libversion.a
bin/spaligner: ext/cppformat/libformat.a
bin/spaligner: common/paired_info/libpaired_info.a
bin/spaligner: common/stages/libstages.a
bin/spaligner: common/pipeline/libpipeline.a
bin/spaligner: common/io/libinput.a
bin/spaligner: ext/samtools/libsamtools.a
bin/spaligner: ext/bamtools/api/libBamTools.a
bin/spaligner: common/modules/path_extend/libpath_extend.a
bin/spaligner: ext/ssw/libssw.a
bin/spaligner: common/io/binary/libbinary_io.a
bin/spaligner: common/modules/coverage_model/libcoverage_model.a
bin/spaligner: ext/nlopt/libnlopt.a
bin/spaligner: ext/gqf/libgqf.a
bin/spaligner: common/modules/libmodules.a
bin/spaligner: ext/bwa/libbwa.a
bin/spaligner: common/assembly_graph/libassembly_graph.a
bin/spaligner: common/utils/libutils.a
bin/spaligner: common/utils/libversion.a
bin/spaligner: ext/cppformat/libformat.a
bin/spaligner: ext/llvm/libllvm-support.a
bin/spaligner: /usr/lib/x86_64-linux-gnu/libdl.so
bin/spaligner: common/sequence/libsequence.a
bin/spaligner: ext/edlib/libedlib.a
bin/spaligner: ext/gfa1/libgfa1.a
bin/spaligner: /usr/lib/x86_64-linux-gnu/libz.so
bin/spaligner: projects/spaligner/CMakeFiles/spaligner.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/root/bio/Modules/SPAdes-3.15.2/build_spades/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX executable ../../bin/spaligner"
	cd /root/bio/Modules/SPAdes-3.15.2/build_spades/projects/spaligner && $(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/spaligner.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
projects/spaligner/CMakeFiles/spaligner.dir/build: bin/spaligner
.PHONY : projects/spaligner/CMakeFiles/spaligner.dir/build

projects/spaligner/CMakeFiles/spaligner.dir/clean:
	cd /root/bio/Modules/SPAdes-3.15.2/build_spades/projects/spaligner && $(CMAKE_COMMAND) -P CMakeFiles/spaligner.dir/cmake_clean.cmake
.PHONY : projects/spaligner/CMakeFiles/spaligner.dir/clean

projects/spaligner/CMakeFiles/spaligner.dir/depend:
	cd /root/bio/Modules/SPAdes-3.15.2/build_spades && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /root/bio/Modules/SPAdes-3.15.2/src /root/bio/Modules/SPAdes-3.15.2/src/projects/spaligner /root/bio/Modules/SPAdes-3.15.2/build_spades /root/bio/Modules/SPAdes-3.15.2/build_spades/projects/spaligner /root/bio/Modules/SPAdes-3.15.2/build_spades/projects/spaligner/CMakeFiles/spaligner.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : projects/spaligner/CMakeFiles/spaligner.dir/depend

