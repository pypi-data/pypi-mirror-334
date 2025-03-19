add_subdirectory(lemon)
add_subdirectory(pybind11)
add_subdirectory(graphviz)
add_subdirectory(K-Editor)
add_subdirectory(qt)

if(IPRM_INCLUDE_STUDIO_RUST_IMPL)
    add_subdirectory(corrosion-rs)
endif()
