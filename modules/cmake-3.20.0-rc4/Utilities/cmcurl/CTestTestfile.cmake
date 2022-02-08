# CMake generated Testfile for 
# Source directory: /root/bio/Modules/cmake-3.20.0-rc4/Utilities/cmcurl
# Build directory: /root/bio/Modules/cmake-3.20.0-rc4/Utilities/cmcurl
# 
# This file includes the relevant testing commands required for 
# testing this directory and lists subdirectories to be tested as well.
add_test(curl "curltest" "http://open.cdash.org/user.php")
set_tests_properties(curl PROPERTIES  _BACKTRACE_TRIPLES "/root/bio/Modules/cmake-3.20.0-rc4/Utilities/cmcurl/CMakeLists.txt;1468;add_test;/root/bio/Modules/cmake-3.20.0-rc4/Utilities/cmcurl/CMakeLists.txt;0;")
subdirs("lib")
