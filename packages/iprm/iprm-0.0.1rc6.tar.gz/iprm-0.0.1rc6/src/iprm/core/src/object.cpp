/*
 * Copyright (c) 2025 ayeteadoe <ayeteadoe@gmail.com>
 *
 * SPDX-License-Identifier: MIT
 */
#include "object.hpp"
#include "session.hpp"

#include <pybind11/pybind11.h>

#include <filesystem>

namespace iprm {
void Object::rename(const std::string& new_name) {
  Session::register_rename(new_name, shared_from_this());
}

bool Object::is_type(TypeFlags type_flags) const {
  return static_cast<bool>(this->type_flags() & type_flags);
}

bool Object::is_project() const {
  return is_type(TypeFlags::PROJECT);
}
bool Object::is_subdirectories() const {
  return is_type(TypeFlags::SUBDIRS);
}

bool Object::is_target() const {
  return is_type(TypeFlags::TARGET);
}

bool Object::is_test() const {
  return is_type(TypeFlags::TEST);
}

bool Object::is_executable() const {
  return is_type(TypeFlags::EXECUTABLE);
}

bool Object::is_library() const {
  return is_type(TypeFlags::LIBRARY);
}

bool Object::is_header() const {
  return is_type(TypeFlags::HEADER);
}

bool Object::is_static_library() const {
  return is_type(TypeFlags::STATIC);
}

bool Object::is_shared_library() const {
  return is_type(TypeFlags::SHARED);
}

bool Object::is_system_native_pkg() const {
  return is_type(TypeFlags::NATIVEPKG);
}

bool Object::is_system_pkg_config() const {
  return is_type(TypeFlags::PKGCONFIG);
}

bool Object::is_precompiled() const {
  return is_type(TypeFlags::PRECOMPILED);
}

bool Object::is_source() const {
  return is_type(TypeFlags::SOURCE);
}

bool Object::is_archive() const {
  return is_type(TypeFlags::ARCHIVE);
}

bool Object::is_framework() const {
  return is_type(TypeFlags::FRAMEWORK);
}

bool Object::is_container() const {
  return is_type(TypeFlags::CONTAINER);
}

bool Object::is_static_crt() const {
  return is_type(TypeFlags::CRTSTATIC);
}

bool Object::is_dynamic_crt() const {
  return is_type(TypeFlags::CRTDYNAMIC);
}

bool Object::is_dual_crt() const {
  return is_type(TypeFlags::CRTDUAL);
}

bool Object::is_cxx() const {
  return is_type(TypeFlags::CXX);
}

bool Object::is_rust() const {
  return is_type(TypeFlags::RUST);
}

bool Object::is_qt() const {
  return is_type(TypeFlags::QT);
}

bool Object::is_pybind11() const {
  return is_type(TypeFlags::PYBIND11);
}

}  // namespace iprm
