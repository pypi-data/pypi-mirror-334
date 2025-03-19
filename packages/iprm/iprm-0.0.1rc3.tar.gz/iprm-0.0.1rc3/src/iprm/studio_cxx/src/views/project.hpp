#pragma once

#include "../apibridge.hpp"
#include "../models/filesystem.hpp"
#include "../models/objects.hpp"

#include <QFileInfo>
#include <QHash>
#include <QItemSelection>
#include <QTabWidget>

class QTabWidget;

namespace iprm::views {

class NativeText;
class CMakeText;
class MesonText;
class Objects;

class FileNode : public QWidget {
  Q_OBJECT
 public:
  FileNode(
const QString& file_name,
  const QString& proj_relative_dir_path,
           const QString& file_contents,
           const std::vector<ObjectNode>& objects,
           QWidget* parent = nullptr);

  void show_cmake(QString contents);
  void show_meson(QString contents);

  QString file_path() const;

 private Q_SLOTS:
  void on_object_selection_changed(const QModelIndex& index);

 private:
  QString file_name_;
  QString proj_relative_dir_path_;
  Objects* objects_view_{nullptr};
  NativeText* native_text_view_{nullptr};
  QTabWidget* cmake_text_{nullptr};
  QTabWidget* meson_text_{nullptr};
  // TODO: This should be a QHash of platform to GeneratedText file instances
  // that are
  //  in the tab widget, given Windows +WSL means we can have one scenario
  //  where there is more than 1 platform we can generate to on a single host
  CMakeText* cmake_text_view_{nullptr};
  MesonText* meson_text_view_{nullptr};
};

class Project : public QTabWidget {
  Q_OBJECT

 public:
  Project(QWidget* parent = nullptr);

  void update(
      const QDir& root_dir,
      const std::unordered_map<std::string, std::vector<ObjectNode>>& objects);

  void add_file(const models::FileNode& file_node);

 Q_SIGNALS:
  void file_closed(const int num_files_opened);

 private Q_SLOTS:
  void on_file_tab_closed(const int tab_index);

 private:
  QDir project_dir_;

  FileNode* add_native(const std::filesystem::path& file_path);
  void add_cmake(const models::CMakeFile& file_node);
  void add_meson(const models::MesonFile& file_node);

  QHash<std::filesystem::path, FileNode*> open_files_;
  std::unordered_map<std::string, std::vector<ObjectNode>> project_objects_;
};

}  // namespace iprm::views
