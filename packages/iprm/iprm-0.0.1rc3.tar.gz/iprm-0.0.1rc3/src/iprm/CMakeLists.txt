cmake_minimum_required(VERSION 3.23)

# TODO: Become self-hosted and use IPRM itself to build
#  IPRM, instead of being hardcoded to use CMake
project(iprm
    VERSION
        0.0.1
    LANGUAGES
        C CXX
)
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED True)

if(MSVC)
    add_compile_options(/Zc:__cplusplus /permissive-)
endif()

add_subdirectory(third_party)
add_subdirectory(core)

add_subdirectory(studio_cxx)
if(IPRM_INCLUDE_STUDIO_RUST_IMPL)
    # TODO: Remove the rust impl as it isn't helpful long term,
    #   only once the C++ version gets to par with it's dependency
    #   graph rendering
    add_subdirectory(studio_rust)
endif()
if(IPRM_INCLUDE_STUDIO_WEB_IMPL)
    add_subdirectory(studio_web)
endif()
