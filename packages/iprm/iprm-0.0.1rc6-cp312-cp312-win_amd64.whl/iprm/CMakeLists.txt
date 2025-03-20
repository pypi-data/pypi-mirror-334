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

option(IPRM_BUILD_STUDIO "Build IPRM Studio" ON)

add_subdirectory(third_party)
add_subdirectory(core)

if(IPRM_BUILD_STUDIO)
    add_subdirectory(studio)
endif()

# TODO: Infrastructure for the remote worker/builds, eventually move this into studio itself
#add_subdirectory(studio_web)
