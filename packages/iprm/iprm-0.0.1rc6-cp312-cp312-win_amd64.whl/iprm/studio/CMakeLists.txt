
if (NOT WIN32)
    set(CMAKE_AUTOMOC ON)
    set(CMAKE_AUTORCC ON)
endif()


add_executable(studio)
target_sources(studio
      PRIVATE
      "${CMAKE_CURRENT_SOURCE_DIR}/src/apibridge.hpp"
      "${CMAKE_CURRENT_SOURCE_DIR}/src/apierror.hpp"
      "${CMAKE_CURRENT_SOURCE_DIR}/src/mainwindow.hpp"
      "${CMAKE_CURRENT_SOURCE_DIR}/src/splashscreen.hpp"
      "${CMAKE_CURRENT_SOURCE_DIR}/src/models/filesystem.hpp"
      "${CMAKE_CURRENT_SOURCE_DIR}/src/models/objects.hpp"
      "${CMAKE_CURRENT_SOURCE_DIR}/src/views/dependencygraph.hpp"
      "${CMAKE_CURRENT_SOURCE_DIR}/src/views/project.hpp"
      "${CMAKE_CURRENT_SOURCE_DIR}/src/views/file.hpp"
      "${CMAKE_CURRENT_SOURCE_DIR}/src/views/filesystem.hpp"
      "${CMAKE_CURRENT_SOURCE_DIR}/src/views/graphview.hpp"
      "${CMAKE_CURRENT_SOURCE_DIR}/src/views/graphviz.hpp"
      "${CMAKE_CURRENT_SOURCE_DIR}/src/views/loadingwidget.hpp"
      "${CMAKE_CURRENT_SOURCE_DIR}/src/views/log.hpp"
      "${CMAKE_CURRENT_SOURCE_DIR}/src/views/nativetext.hpp"
      "${CMAKE_CURRENT_SOURCE_DIR}/src/views/cmaketext.hpp"
      "${CMAKE_CURRENT_SOURCE_DIR}/src/views/mesontext.hpp"
      "${CMAKE_CURRENT_SOURCE_DIR}/src/views/textstyle.hpp"
      "${CMAKE_CURRENT_SOURCE_DIR}/src/views/objects.hpp"
      "${CMAKE_CURRENT_SOURCE_DIR}/src/apibridge.cpp"
      "${CMAKE_CURRENT_SOURCE_DIR}/src/main.cpp"
      "${CMAKE_CURRENT_SOURCE_DIR}/src/mainwindow.cpp"
      "${CMAKE_CURRENT_SOURCE_DIR}/src/splashscreen.cpp"
      "${CMAKE_CURRENT_SOURCE_DIR}/src/models/filesystem.cpp"
      "${CMAKE_CURRENT_SOURCE_DIR}/src/models/objects.cpp"
      "${CMAKE_CURRENT_SOURCE_DIR}/src/views/dependencygraph.cpp"
      "${CMAKE_CURRENT_SOURCE_DIR}/src/views/project.cpp"
      "${CMAKE_CURRENT_SOURCE_DIR}/src/views/file.cpp"
      "${CMAKE_CURRENT_SOURCE_DIR}/src/views/filesystem.cpp"
      "${CMAKE_CURRENT_SOURCE_DIR}/src/views/graphview.cpp"
      "${CMAKE_CURRENT_SOURCE_DIR}/src/views/graphviz.cpp"
      "${CMAKE_CURRENT_SOURCE_DIR}/src/views/loadingwidget.cpp"
      "${CMAKE_CURRENT_SOURCE_DIR}/src/views/log.cpp"
      "${CMAKE_CURRENT_SOURCE_DIR}/src/views/nativetext.cpp"
      "${CMAKE_CURRENT_SOURCE_DIR}/src/views/cmaketext.cpp"
      "${CMAKE_CURRENT_SOURCE_DIR}/src/views/mesontext.cpp"
      "${CMAKE_CURRENT_SOURCE_DIR}/src/views/textstyle.cpp"
      "${CMAKE_CURRENT_SOURCE_DIR}/src/views/objects.cpp"
)
target_sources(studio
      PRIVATE
      "${CMAKE_CURRENT_SOURCE_DIR}/res/res.qrc"
)

set_target_properties(studio
        PROPERTIES
        RUNTIME_OUTPUT_DIRECTORY
        "${CMAKE_CURRENT_SOURCE_DIR}/bin"
        LIBRARY_OUTPUT_DIRECTORY
        "${CMAKE_CURRENT_SOURCE_DIR}/bin"
        ARCHIVE_OUTPUT_DIRECTORY
        "${CMAKE_CURRENT_SOURCE_DIR}/bin"
)

find_package(Python 3.12 COMPONENTS Interpreter Development REQUIRED)
target_link_libraries(studio
    PUBLIC
        tp_lemon
        tp_graphviz
        tp_qt
        tp_pybind11
        tp_K-Editor_md
        Python::Python
)
add_dependencies(studio core)
target_compile_definitions(studio
    PRIVATE
        QT_NO_KEYWORDS
)

if (WIN32)
    set_target_properties(studio
        PROPERTIES
            WIN32_EXECUTABLE TRUE
    )
    target_link_options(studio PRIVATE
        "/SUBSYSTEM:WINDOWS"
        "/ENTRY:mainCRTStartup"
    )

    add_custom_command(TARGET studio
          POST_BUILD
          COMMAND ${CMAKE_COMMAND} -E copy_directory
          ${CMAKE_BINARY_DIR}/third_party/qt/Archive/plugins
          $<TARGET_FILE_DIR:studio>/plugins
    )

    # TODO: Get this method of including Qt working in regular API tests before using in IPRM, so all the kinks have been
    #	worked out, as our manual solution is fine enough for now
    #[===[
    add_executable(studio)
    target_sources(studio
            PRIVATE
            "${CMAKE_CURRENT_SOURCE_DIR}/src/apibridge.hpp"
            "${CMAKE_CURRENT_SOURCE_DIR}/src/apierror.hpp"
            "${CMAKE_CURRENT_SOURCE_DIR}/src/mainwindow.hpp"
            "${CMAKE_CURRENT_SOURCE_DIR}/src/splashscreen.hpp"
            "${CMAKE_CURRENT_SOURCE_DIR}/src/models/filesystem.hpp"
            "${CMAKE_CURRENT_SOURCE_DIR}/src/models/objects.hpp"
            "${CMAKE_CURRENT_SOURCE_DIR}/src/views/dependencygraph.hpp"
            "${CMAKE_CURRENT_SOURCE_DIR}/src/views/files.hpp"
            "${CMAKE_CURRENT_SOURCE_DIR}/src/views/filesystem.hpp"
            "${CMAKE_CURRENT_SOURCE_DIR}/src/views/loadingwidget.hpp"
            "${CMAKE_CURRENT_SOURCE_DIR}/src/views/log.hpp"
            "${CMAKE_CURRENT_SOURCE_DIR}/src/views/nativetext.hpp"
            "${CMAKE_CURRENT_SOURCE_DIR}/src/views/cmaketext.hpp"
            "${CMAKE_CURRENT_SOURCE_DIR}/src/views/textstyle.hpp"
            "${CMAKE_CURRENT_SOURCE_DIR}/src/views/objects.hpp"
            "${CMAKE_CURRENT_SOURCE_DIR}/src/apibridge.cpp"
            "${CMAKE_CURRENT_SOURCE_DIR}/src/main.cpp"
            "${CMAKE_CURRENT_SOURCE_DIR}/src/mainwindow.cpp"
            "${CMAKE_CURRENT_SOURCE_DIR}/src/splashscreen.cpp"
            "${CMAKE_CURRENT_SOURCE_DIR}/src/models/filesystem.cpp"
            "${CMAKE_CURRENT_SOURCE_DIR}/src/models/objects.cpp"
            "${CMAKE_CURRENT_SOURCE_DIR}/src/views/dependencygraph.cpp"
            "${CMAKE_CURRENT_SOURCE_DIR}/src/views/files.cpp"
            "${CMAKE_CURRENT_SOURCE_DIR}/src/views/filesystem.cpp"
            "${CMAKE_CURRENT_SOURCE_DIR}/src/views/loadingwidget.cpp"
            "${CMAKE_CURRENT_SOURCE_DIR}/src/views/log.cpp"
            "${CMAKE_CURRENT_SOURCE_DIR}/src/views/nativetext.cpp"
            "${CMAKE_CURRENT_SOURCE_DIR}/src/views/cmaketext.cpp"
            "${CMAKE_CURRENT_SOURCE_DIR}/src/views/textstyle.cpp"
            "${CMAKE_CURRENT_SOURCE_DIR}/src/views/objects.cpp"
    )

    set_target_properties(studio PROPERTIES
            MSVC_RUNTIME_LIBRARY "MultiThreaded$<$<CONFIG:Debug>:Debug>DLL"
    )

    target_link_libraries(studio
            PUBLIC
            tp_lemon
            tp_graphviz
            tp_qt
            tp_pybind11
            tp_K-Editor_md
    )

    target_compile_definitions(studio
            PRIVATE
            QT_NO_KEYWORDS
    )

    add_custom_command(TARGET studio
            POST_BUILD
            COMMAND ${CMAKE_COMMAND} -E copy_if_different
            $<TARGET_RUNTIME_DLLS:studio>
            $<TARGET_FILE_DIR:studio>
            COMMAND_EXPAND_LISTS
    )

    find_program(WINDEPLOYQT_EXECUTABLE
            NAMES windeployqt6 windeployqt
            HINTS ${QT_BIN_DIR}
            REQUIRED
    )

    target_compile_definitions(studio
            PUBLIC
            QT_NO_KEYWORDS
    )

    set_target_properties(studio
            PROPERTIES
            OUTPUT_NAME
            studio
            RUNTIME_OUTPUT_DIRECTORY
            "${CMAKE_CURRENT_SOURCE_DIR}/."
            LIBRARY_OUTPUT_DIRECTORY
            "${CMAKE_CURRENT_SOURCE_DIR}/."
            ARCHIVE_OUTPUT_DIRECTORY
            "${CMAKE_CURRENT_SOURCE_DIR}/."
    )

    add_custom_command(TARGET studio
            POST_BUILD
            COMMAND ${WINDEPLOYQT_EXECUTABLE}
            --verbose 0
            --no-translations
            --no-compiler-runtime
            --plugindir=$<TARGET_FILE_DIR:studio>/plugins
            --dir $<TARGET_FILE_DIR:studio>
            $<TARGET_FILE:studio>
            COMMENT "Running windeployqt for studio"
            COMMAND_EXPAND_LISTS
    )
    ]===]

    get_target_property(target_sources studio SOURCES)
    foreach (source ${target_sources})
        if (source MATCHES "\.(h|hpp)$")
            get_filename_component(directory ${source} DIRECTORY)
            get_filename_component(filename ${source} NAME_WE)
            get_filename_component(ext ${source} EXT)
            file(RELATIVE_PATH rel_directory ${CMAKE_CURRENT_SOURCE_DIR} ${directory})
            set(moc_output "${CMAKE_CURRENT_BINARY_DIR}/${rel_directory}/moc_${filename}.cpp")
            set(moc_includes "$<LIST:TRANSFORM,$<TARGET_PROPERTY:studio,INTERFACE_INCLUDE_DIRECTORIES>,PREPEND,-I>")
            add_custom_command(
                    OUTPUT ${moc_output}
                    COMMAND ${CMAKE_BINARY_DIR}/third_party/qt/Archive/bin/moc.exe
                    ${moc_includes}
                    "${directory}/${filename}${ext}"
                    -o ${moc_output}
                    DEPENDS
                    ${source} tp_qt_unpack_qt_archive
                    COMMAND_EXPAND_LISTS
            )
            target_sources(studio PRIVATE ${moc_output})
        endif ()
    endforeach ()

    get_target_property(target_sources studio SOURCES)
    foreach (source ${target_sources})
        if (source MATCHES "\.qrc$")
            get_filename_component(directory ${source} DIRECTORY)
            get_filename_component(filename ${source} NAME_WE)
            get_filename_component(ext ${source} EXT)
            file(RELATIVE_PATH rel_directory ${CMAKE_CURRENT_SOURCE_DIR} ${directory})
            set(rcc_output "${CMAKE_CURRENT_BINARY_DIR}/${rel_directory}/qrc_${filename}.cpp")
            add_custom_command(
                    OUTPUT ${rcc_output}
                    COMMAND ${CMAKE_BINARY_DIR}/third_party/qt/Archive/bin/rcc.exe
                    --name ${filename}
                    "${directory}/${filename}${ext}"
                    -o ${rcc_output}
                    DEPENDS
                    ${source} tp_qt_unpack_qt_archive
            )
            target_sources(studio PRIVATE ${rcc_output})
        endif ()
    endforeach ()


    add_custom_command(TARGET studio
    POST_BUILD
          COMMAND ${CMAKE_COMMAND} -E copy_directory
        ${CMAKE_BINARY_DIR}/third_party/qt/Archive/plugins
        $<TARGET_FILE_DIR:studio>/plugins
          COMMAND ${CMAKE_COMMAND} -E copy_if_different
          $<TARGET_RUNTIME_DLLS:studio>
          $<TARGET_FILE_DIR:studio>

          COMMAND_EXPAND_LISTS
    )

    set_target_properties(studio PROPERTIES
            MSVC_RUNTIME_LIBRARY "MultiThreaded$<$<CONFIG:Debug>:Debug>DLL"
    )
    set(graphviz_config6_file "${CMAKE_BINARY_DIR}/third_party/graphviz/Archive/bin/config6")
    add_custom_command(TARGET studio
            POST_BUILD
            COMMAND ${CMAKE_COMMAND} -E copy
            ${graphviz_config6_file}
            $<TARGET_FILE_DIR:studio>
    )
endif()