/*
 * Copyright (c) 2025 ayeteadoe <ayeteadoe@gmail.com>
 *
 * SPDX-License-Identifier: MIT
 */
#pragma once

#include <lemon/list_graph.h>
#include <pybind11/embed.h>
#include <pybind11/pybind11.h>
#include <QDir>
#include <QObject>
#include <QString>
#include <QThread>
#include <optional>
#include "../../core/src/typeflags.hpp"
#include "apierror.hpp"

#include <functional>

namespace iprm {
struct ObjectNode {
  QString name;
  QString type_name;
  TypeFlags type;
  QStringList dependencies;
  QString hex_colour;
  QString shape_type;
  int shape_sides{0};

  ObjectNode() = default;

  ObjectNode(const std::string& obj_name,
             const std::string& obj_type_name,
             const TypeFlags obj_type,
             const std::vector<std::string>& obj_dependencies,
             const std::string& obj_hex_color,
             const std::string& obj_shape_type,
             int obj_shape_sides)
      : name(QString::fromStdString(obj_name)),
        type_name(QString::fromStdString(obj_type_name)),
        type(obj_type),
        hex_colour(QString::fromStdString(obj_hex_color)),
        shape_type(QString::fromStdString(obj_shape_type)),
        shape_sides(obj_shape_sides) {
    dependencies.reserve(obj_dependencies.size());
    for (const auto& dependency : obj_dependencies) {
      dependencies.push_back(QString::fromStdString(dependency));
    }
  }
};

class APIBridge : public QObject {
  Q_OBJECT

  friend class APIBridgeThread;

 public:
  explicit APIBridge(QObject* parent = nullptr);

  APIBridge(const APIBridge&) = delete;
  APIBridge& operator=(const APIBridge&) = delete;

  void set_root_dir(const QDir& root_dir);

 public Q_SLOTS:
  void capture_io();
  void init_sess();
  void destroy_sess();
  void load_project();

  void cmake_generate();
  void meson_generate();

 Q_SIGNALS:
  void error(const APIError& error);

  void print_stdout(const QString& message);
  // TODO: print_stderr

  void project_load_success();

  void cmake_generate_success();
  void meson_generate_success();

 private:
  void process_objects(const pybind11::dict& py_objects);

  void generate(const std::string& generator_module,
                const std::string& generator_class,
                std::function<void()> notify_success);

  QDir root_dir_;

  QString host_platform_;
  QStringList supported_platforms_;

  std::optional<pybind11::object> sess_;
  std::optional<pybind11::object> native_loader_;

  lemon::ListDigraph dep_graph_;
  lemon::ListDigraph::NodeMap<ObjectNode> dep_node_data_;
  std::unordered_map<QString, lemon::ListDigraph::Node> target_map_;

  std::unordered_map<std::string, std::vector<ObjectNode>> objs_;
};

class APIBridgeThread : public QThread {
  Q_OBJECT

 public:
  explicit APIBridgeThread();

  void set_root_dir(const QDir& root_dir);

  // TODO: return the objects for each platform
  const std::unordered_map<std::string, std::vector<ObjectNode>>& objects()
      const {
    return bridge_.objs_;
  }

  const lemon::ListDigraph& dependency_graph() const {
    return bridge_.dep_graph_;
  }

  const lemon::ListDigraph::NodeMap<ObjectNode>& dependency_node_data() const {
    return bridge_.dep_node_data_;
  }

 public Q_SLOTS:
  void capture_io();
  void destroy_sess();
  void load_project();

  void cmake_generate();
  void meson_generate();

 Q_SIGNALS:
  void error(const APIError& error);

  void print_stdout(const QString& message);

  void project_load_success();

  void cmake_generate_success();
  void meson_generate_success();

 private:
  QDir root_dir_;
  APIBridge bridge_;
  pybind11::scoped_interpreter interp_;
};
}  // namespace iprm
