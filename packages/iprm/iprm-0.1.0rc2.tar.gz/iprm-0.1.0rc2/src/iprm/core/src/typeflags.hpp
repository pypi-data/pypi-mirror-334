/*
 * Copyright (c) 2025 ayeteadoe <ayeteadoe@gmail.com>
 *
 * SPDX-License-Identifier: MIT
 */
#pragma once

#include <type_traits>
#include <cstdint>

namespace iprm {
enum class TypeFlags : std::uint64_t {
  NONE = 0,
  PROJECT = 1 << 0,
  SUBDIRS = 1 << 1,
  TARGET = 1 << 2,
  TEST = 1 << 3,
  EXECUTABLE = 1 << 4,
  LIBRARY = 1 << 5,
  HEADER = 1 << 6,
  STATIC = 1 << 7,
  SHARED = 1 << 8,
  // TODO: remove this type, and just expose ability for users to specify their
  //  own custom link lines, which on platforms like Linux if you have a system
  //  package installed (and its not supported by pkg-config), it will just
  //  work if you have your paths setup correctly
  NATIVEPKG = 1 << 9,
  PKGCONFIG = 1 << 10,
  PRECOMPILED = 1 << 11,
  SOURCE = 1 << 12,
  ARCHIVE = 1 << 13,
  FRAMEWORK = 1 << 14,
  CONTAINER = 1 << 15,
  CRTSTATIC = 1 << 16,
  CRTDYNAMIC = 1 << 17,
  CRTDUAL = 1 << 18,
  CXX = 1 << 19,
  RUST = 1 << 20,
  QT = 1 << 21,
  PYBIND11 = 1 << 22,
  MSVC = 1 << 23,
  MSVC_CLANG = 1 << 24,
  CLANG = 1 << 25,
  GCC = 1 << 26,
  RUSTC  = 1 << 27,
};

inline TypeFlags operator|(TypeFlags a, TypeFlags b) {
  return static_cast<TypeFlags>(
      static_cast<std::underlying_type_t<TypeFlags>>(a) |
      static_cast<std::underlying_type_t<TypeFlags>>(b));
}

inline TypeFlags operator&(TypeFlags a, TypeFlags b) {
  return static_cast<TypeFlags>(
      static_cast<std::underlying_type_t<TypeFlags>>(a) &
      static_cast<std::underlying_type_t<TypeFlags>>(b));
}

inline TypeFlags operator~(TypeFlags a) {
  return static_cast<TypeFlags>(
      ~static_cast<std::underlying_type_t<TypeFlags>>(a));
}
}  // namespace iprm
