/*
 * Copyright (c) 2025 ayeteadoe <ayeteadoe@gmail.com>
 *
 * SPDX-License-Identifier: MIT
 */
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <string>
#include "object.hpp"
#include "session.hpp"
#include "typeflags.hpp"

namespace py = pybind11;

PYBIND11_MODULE(core, m) {
  py::enum_<iprm::TypeFlags>(m, "TypeFlags")
      .value("NONE", iprm::TypeFlags::NONE)
      .value("PROJECT", iprm::TypeFlags::PROJECT)
      .value("SUBDIRS", iprm::TypeFlags::SUBDIRS)
      .value("TARGET", iprm::TypeFlags::TARGET)
      .value("TEST", iprm::TypeFlags::TEST)
      .value("EXECUTABLE", iprm::TypeFlags::EXECUTABLE)
      .value("LIBRARY", iprm::TypeFlags::LIBRARY)
      .value("HEADER", iprm::TypeFlags::HEADER)
      .value("STATIC", iprm::TypeFlags::STATIC)
      .value("SHARED", iprm::TypeFlags::SHARED)
      .value("NATIVEPKG", iprm::TypeFlags::NATIVEPKG)
      .value("PKGCONFIG", iprm::TypeFlags::PKGCONFIG)
      .value("PRECOMPILED", iprm::TypeFlags::PRECOMPILED)
      .value("SOURCE", iprm::TypeFlags::SOURCE)
      .value("ARCHIVE", iprm::TypeFlags::ARCHIVE)
      .value("FRAMEWORK", iprm::TypeFlags::FRAMEWORK)
      .value("CONTAINER", iprm::TypeFlags::CONTAINER)
      .value("CRTSTATIC", iprm::TypeFlags::CRTSTATIC)
      .value("CRTDYNAMIC", iprm::TypeFlags::CRTDYNAMIC)
      .value("CRTDUAL", iprm::TypeFlags::CRTDUAL)
      .value("CXX", iprm::TypeFlags::CXX)
      .value("RUST", iprm::TypeFlags::RUST)
      .value("QT", iprm::TypeFlags::QT)
      .value("PYBIND11", iprm::TypeFlags::PYBIND11)
      .value("MSVC", iprm::TypeFlags::MSVC)
      .value("MSVC_CLANG", iprm::TypeFlags::MSVC_CLANG)
      .value("CLANG", iprm::TypeFlags::CLANG)
      .value("GCC", iprm::TypeFlags::GCC)
      .value("RUSTC", iprm::TypeFlags::RUSTC)
      .export_values()
      .def(
          "__or__",
          [](const iprm::TypeFlags& a, const iprm::TypeFlags& b) {
            return a | b;
          },
          py::is_operator())
      .def(
          "__and__",
          [](const iprm::TypeFlags& a, const iprm::TypeFlags& b) {
            return a & b;
          },
          py::is_operator())
      .def(
          "__invert__", [](const iprm::TypeFlags& a) { return ~a; },
          py::is_operator())
      .def("__int__",
           [](const iprm::TypeFlags& f) { return static_cast<int>(f); });

  py::class_<iprm::Object, std::shared_ptr<iprm::Object> >(m, "Object")
      .def(py::init<const std::string&>())
      .def_property("name", &iprm::Object::name, &iprm::Object::rename)
      /*
      .def_property_readonly("type_name", &iprm::Object::type_name)
       */
      .def_property("type_flags", &iprm::Object::type_flags,
                    &iprm::Object::set_type_flags)
      .def_property("dependencies", &iprm::Object::dependencies,
                    &iprm::Object::set_dependencies)
      .def_property("hex_colour", &iprm::Object::hex_colour,
                    &iprm::Object::set_hex_colour)
      .def_property("shape_type", &iprm::Object::shape_type,
                    &iprm::Object::set_shape_type)
      .def_property("shape_num_sides", &iprm::Object::shape_num_sides,
                    &iprm::Object::set_shape_num_sides)
      .def("rename", &iprm::Object::rename)
      .def_property_readonly("is_project", &iprm::Object::is_project)
      .def_property_readonly("is_subdirs", &iprm::Object::is_subdirectories)
      .def_property_readonly("is_target", &iprm::Object::is_target)
      .def_property_readonly("is_test", &iprm::Object::is_test)
      .def_property_readonly("is_app", &iprm::Object::is_executable)
      .def_property_readonly("is_lib", &iprm::Object::is_library)
      .def_property_readonly("is_header", &iprm::Object::is_header)
      .def_property_readonly("is_static", &iprm::Object::is_static_library)
      .def_property_readonly("is_shared", &iprm::Object::is_shared_library)
      .def_property_readonly("is_native_pkg",
                             &iprm::Object::is_system_native_pkg)
      .def_property_readonly("is_pkg_config",
                             &iprm::Object::is_system_pkg_config)
      .def_property_readonly("is_precompiled", &iprm::Object::is_precompiled)
      .def_property_readonly("is_source", &iprm::Object::is_source)
      .def_property_readonly("is_archive", &iprm::Object::is_archive)
      .def_property_readonly("is_framework", &iprm::Object::is_framework)
      .def_property_readonly("is_container", &iprm::Object::is_container)
      .def_property_readonly("is_static_crt", &iprm::Object::is_static_crt)
      .def_property_readonly("is_dynamic_crt", &iprm::Object::is_dynamic_crt)
      .def_property_readonly("is_dual_crt", &iprm::Object::is_dual_crt)
      .def_property_readonly("is_cxx", &iprm::Object::is_cxx)
      .def_property_readonly("is_rust", &iprm::Object::is_rust)
      .def_property_readonly("is_qt", &iprm::Object::is_qt)
      .def_property_readonly("is_pybind11", &iprm::Object::is_pybind11);

  py::class_<iprm::Session>(m, "Session")
      .def(py::init<const std::string&>())
      .def_static("create", &iprm::Session::create)
      .def_static("destroy", &iprm::Session::destroy)
      .def_static("get_object", &iprm::Session::get_object)
      .def_static("get_objects", &iprm::Session::get_objects,
                  py::return_value_policy::copy)
      .def_static("register_object", &iprm::Session::register_object)
      .def_static("begin_file_context", &iprm::Session::begin_file_context)
      .def_static("end_file_context", &iprm::Session::end_file_context)
      .def_static("retrieve_loadable_files",
                  &iprm::Session::retrieve_loadable_files,
                  py::return_value_policy::copy)
      .def_static("root_relative_source_dir",
                  &iprm::Session::root_relative_source_dir,
                  py::return_value_policy::copy);

  m.attr("__version__") = "0.0.1-rc6";

  m.attr("FILE_NAME") = iprm::FILE_NAME;
}
