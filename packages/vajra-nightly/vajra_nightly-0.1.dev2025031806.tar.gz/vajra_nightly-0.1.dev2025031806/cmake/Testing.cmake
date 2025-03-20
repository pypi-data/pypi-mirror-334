# Define common interface library for tests
add_library(vajra_test_common INTERFACE)
target_include_directories(vajra_test_common INTERFACE
  ${CMAKE_CURRENT_SOURCE_DIR}/csrc
  ${CMAKE_CURRENT_SOURCE_DIR}/csrc/include/vajra
)
target_link_libraries(vajra_test_common INTERFACE
  ${TORCH_LIBRARIES}
  gtest
  gtest_main
  glog::glog
  tokenizers_cpp
  fmt::fmt
  nlohmann_json::nlohmann_json
  Flashinfer::Flashinfer
  vajra_python
)

# Function to configure common test target properties
function(vajra_test_config TARGET_NAME)
  target_link_libraries(${TARGET_NAME} PRIVATE vajra_test_common)
  target_compile_definitions(${TARGET_NAME} PRIVATE _GLIBCXX_USE_CXX11_ABI=0)
  set_property(TARGET ${TARGET_NAME} PROPERTY CXX_STANDARD 17)
  set_property(TARGET ${TARGET_NAME} PROPERTY CXX_STANDARD_REQUIRED ON)
  if(CMAKE_CXX_COMPILER_ID MATCHES "GNU|Clang")
    target_compile_options(${TARGET_NAME} PRIVATE -fPIC -Wall -Wextra)
  endif()
  if(VAJRA_GPU_ARCHES)
    set_target_properties(${TARGET_NAME} PROPERTIES ${VAJRA_GPU_LANG}_ARCHITECTURES "${VAJRA_GPU_ARCHES}")
  endif()
endfunction()

# Function to add test suites
function(add_vajra_test_suite NAME SOURCE_DIR LIBS)
  file(GLOB_RECURSE CPP_TEST_SRC "${SOURCE_DIR}/*.cpp")
  file(GLOB_RECURSE CUDA_TEST_SRC "${SOURCE_DIR}/*.cu")
  set(ALL_TEST_SRC ${CPP_TEST_SRC} ${CUDA_TEST_SRC})
  if(ALL_TEST_SRC)
    add_executable(${NAME}_tests ${ALL_TEST_SRC})
    target_link_libraries(${NAME}_tests PRIVATE ${LIBS})
    vajra_test_config(${NAME}_tests)
    if(CUDA_TEST_SRC)
      set_source_files_properties(${CUDA_TEST_SRC} PROPERTIES LANGUAGE CUDA)
      if(VAJRA_GPU_FLAGS)
        set_source_files_properties(${CUDA_TEST_SRC} PROPERTIES COMPILE_FLAGS "${VAJRA_GPU_FLAGS}")
      endif()
    endif()
    add_test(NAME ${NAME}_tests COMMAND ${NAME}_tests --gtest_output=xml:test_reports/${NAME}_tests_results.xml)
  endif()
endfunction()

# Add test suites
add_vajra_test_suite(kernel "csrc/test/kernels" "_kernels_static")
add_vajra_test_suite(native "csrc/test/native" "_native_static" "_kernels_static")

set(TESTDATA_DIR ${CMAKE_CURRENT_SOURCE_DIR}/csrc/test/testdata)
add_custom_target(
  copy_testdata
  COMMAND ${CMAKE_COMMAND} -E copy_directory
  ${TESTDATA_DIR}
  ${CMAKE_CURRENT_BINARY_DIR}/testdata
)

# Define all_tests target
add_custom_target(all_tests DEPENDS default kernel_tests native_tests copy_testdata)


