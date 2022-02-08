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
include projects/scaffold_correction/CMakeFiles/spades-truseq-scfcorrection.dir/depend.make
# Include any dependencies generated by the compiler for this target.
include projects/scaffold_correction/CMakeFiles/spades-truseq-scfcorrection.dir/compiler_depend.make

# Include the progress variables for this target.
include projects/scaffold_correction/CMakeFiles/spades-truseq-scfcorrection.dir/progress.make

# Include the compile flags for this target's objects.
include projects/scaffold_correction/CMakeFiles/spades-truseq-scfcorrection.dir/flags.make

projects/scaffold_correction/CMakeFiles/spades-truseq-scfcorrection.dir/main.cpp.o: projects/scaffold_correction/CMakeFiles/spades-truseq-scfcorrection.dir/flags.make
projects/scaffold_correction/CMakeFiles/spades-truseq-scfcorrection.dir/main.cpp.o: /root/bio/Modules/SPAdes-3.15.2/src/projects/scaffold_correction/main.cpp
projects/scaffold_correction/CMakeFiles/spades-truseq-scfcorrection.dir/main.cpp.o: projects/scaffold_correction/CMakeFiles/spades-truseq-scfcorrection.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/root/bio/Modules/SPAdes-3.15.2/build_spades/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object projects/scaffold_correction/CMakeFiles/spades-truseq-scfcorrection.dir/main.cpp.o"
	cd /root/bio/Modules/SPAdes-3.15.2/build_spades/projects/scaffold_correction && /usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT projects/scaffold_correction/CMakeFiles/spades-truseq-scfcorrection.dir/main.cpp.o -MF CMakeFiles/spades-truseq-scfcorrection.dir/main.cpp.o.d -o CMakeFiles/spades-truseq-scfcorrection.dir/main.cpp.o -c /root/bio/Modules/SPAdes-3.15.2/src/projects/scaffold_correction/main.cpp

projects/scaffold_correction/CMakeFiles/spades-truseq-scfcorrection.dir/main.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/spades-truseq-scfcorrection.dir/main.cpp.i"
	cd /root/bio/Modules/SPAdes-3.15.2/build_spades/projects/scaffold_correction && /usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /root/bio/Modules/SPAdes-3.15.2/src/projects/scaffold_correction/main.cpp > CMakeFiles/spades-truseq-scfcorrection.dir/main.cpp.i

projects/scaffold_correction/CMakeFiles/spades-truseq-scfcorrection.dir/main.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/spades-truseq-scfcorrection.dir/main.cpp.s"
	cd /root/bio/Modules/SPAdes-3.15.2/build_spades/projects/scaffold_correction && /usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /root/bio/Modules/SPAdes-3.15.2/src/projects/scaffold_correction/main.cpp -o CMakeFiles/spades-truseq-scfcorrection.dir/main.cpp.s

# Object files for target spades-truseq-scfcorrection
spades__truseq__scfcorrection_OBJECTS = \
"CMakeFiles/spades-truseq-scfcorrection.dir/main.cpp.o"

# External object files for target spades-truseq-scfcorrection
spades__truseq__scfcorrection_EXTERNAL_OBJECTS = \
"/root/bio/Modules/SPAdes-3.15.2/build_spades/ext/mimalloc/CMakeFiles/mimalloc-obj.dir/src/static.c.o"

bin/spades-truseq-scfcorrection: projects/scaffold_correction/CMakeFiles/spades-truseq-scfcorrection.dir/main.cpp.o
bin/spades-truseq-scfcorrection: ext/mimalloc/CMakeFiles/mimalloc-obj.dir/src/static.c.o
bin/spades-truseq-scfcorrection: projects/scaffold_correction/CMakeFiles/spades-truseq-scfcorrection.dir/build.make
bin/spades-truseq-scfcorrection: common/libcommon_modules.a
bin/spades-truseq-scfcorrection: common/utils/libversion.a
bin/spades-truseq-scfcorrection: ext/cppformat/libformat.a
bin/spades-truseq-scfcorrection: common/paired_info/libpaired_info.a
bin/spades-truseq-scfcorrection: common/stages/libstages.a
bin/spades-truseq-scfcorrection: common/pipeline/libpipeline.a
bin/spades-truseq-scfcorrection: common/io/libinput.a
bin/spades-truseq-scfcorrection: ext/samtools/libsamtools.a
bin/spades-truseq-scfcorrection: ext/bamtools/api/libBamTools.a
bin/spades-truseq-scfcorrection: /usr/lib/x86_64-linux-gnu/libz.so
bin/spades-truseq-scfcorrection: common/modules/path_extend/libpath_extend.a
bin/spades-truseq-scfcorrection: ext/ssw/libssw.a
bin/spades-truseq-scfcorrection: common/io/binary/libbinary_io.a
bin/spades-truseq-scfcorrection: common/modules/coverage_model/libcoverage_model.a
bin/spades-truseq-scfcorrection: ext/nlopt/libnlopt.a
bin/spades-truseq-scfcorrection: ext/gqf/libgqf.a
bin/spades-truseq-scfcorrection: common/modules/libmodules.a
bin/spades-truseq-scfcorrection: common/assembly_graph/libassembly_graph.a
bin/spades-truseq-scfcorrection: common/utils/libutils.a
bin/spades-truseq-scfcorrection: common/utils/libversion.a
bin/spades-truseq-scfcorrection: ext/cppformat/libformat.a
bin/spades-truseq-scfcorrection: ext/llvm/libllvm-support.a
bin/spades-truseq-scfcorrection: /usr/lib/x86_64-linux-gnu/libdl.so
bin/spades-truseq-scfcorrection: common/sequence/libsequence.a
bin/spades-truseq-scfcorrection: ext/edlib/libedlib.a
bin/spades-truseq-scfcorrection: ext/bwa/libbwa.a
bin/spades-truseq-scfcorrection: projects/scaffold_correction/CMakeFiles/spades-truseq-scfcorrection.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/root/bio/Modules/SPAdes-3.15.2/build_spades/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX executable ../../bin/spades-truseq-scfcorrection"
	cd /root/bio/Modules/SPAdes-3.15.2/build_spades/projects/scaffold_correction && $(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/spades-truseq-scfcorrection.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
projects/scaffold_correction/CMakeFiles/spades-truseq-scfcorrection.dir/build: bin/spades-truseq-scfcorrection
.PHONY : projects/scaffold_correction/CMakeFiles/spades-truseq-scfcorrection.dir/build

projects/scaffold_correction/CMakeFiles/spades-truseq-scfcorrection.dir/clean:
	cd /root/bio/Modules/SPAdes-3.15.2/build_spades/projects/scaffold_correction && $(CMAKE_COMMAND) -P CMakeFiles/spades-truseq-scfcorrection.dir/cmake_clean.cmake
.PHONY : projects/scaffold_correction/CMakeFiles/spades-truseq-scfcorrection.dir/clean

projects/scaffold_correction/CMakeFiles/spades-truseq-scfcorrection.dir/depend:
	cd /root/bio/Modules/SPAdes-3.15.2/build_spades && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /root/bio/Modules/SPAdes-3.15.2/src /root/bio/Modules/SPAdes-3.15.2/src/projects/scaffold_correction /root/bio/Modules/SPAdes-3.15.2/build_spades /root/bio/Modules/SPAdes-3.15.2/build_spades/projects/scaffold_correction /root/bio/Modules/SPAdes-3.15.2/build_spades/projects/scaffold_correction/CMakeFiles/spades-truseq-scfcorrection.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : projects/scaffold_correction/CMakeFiles/spades-truseq-scfcorrection.dir/depend

