#include "project.hpp"
#include <QFile>
#include <QFileInfo>
#include <QHBoxLayout>
#include <QIcon>
#include <QLabel>
#include <QPainter>
#include <QSplitter>
#include <QSvgRenderer>
#include <QVBoxLayout>
#include <complex>
#include <filesystem>
#include "cmaketext.hpp"
#include "mesontext.hpp"
#include "nativetext.hpp"
#include "objects.hpp"

namespace iprm::views {

QPixmap create_svg_pixmap(const QString& svg_file) {
  QSvgRenderer renderer(svg_file);
  QPixmap pixmap(QSize(16, 16));
  pixmap.fill(Qt::transparent);
  QPainter painter(&pixmap);
  painter.setRenderHint(QPainter::Antialiasing);
  renderer.render(&painter);
  painter.end();
  return pixmap;
}

FileNode::FileNode(const QString& file_name,
                   const QString& proj_relative_dir_path,
                   const QString& file_contents,
                   const std::vector<ObjectNode>& objects,
                   QWidget* parent)
    : QWidget(parent),
      file_name_(file_name),
      proj_relative_dir_path_(proj_relative_dir_path) {
  // Graphical and Textual representation of a native project file
  auto view = new QSplitter(Qt::Vertical, this);
  auto gui_view = new QSplitter(Qt::Horizontal, this);
  objects_view_ = new Objects(this);
  connect(objects_view_, &Objects::object_selection_changed, this,
          &FileNode::on_object_selection_changed);
  // TODO: don't hardcode to windows, FileNode should have a function that
  //  passes object of ALL platforms, then setup each tab
  objects_view_->load_windows_objects(objects);
  gui_view->addWidget(objects_view_);

  // TODO: add objects properties view
  // gui_view->setSizes({300, 400});

  auto text_view = new QSplitter(Qt::Horizontal, this);
  auto native_text = new QWidget();
  auto native_text_layout = new QVBoxLayout(native_text);
  native_text_layout->setContentsMargins(0, 0, 0, 0);

  auto native_platforms_layout = new QHBoxLayout();
  native_platforms_layout->setContentsMargins(0, 0, 0, 0);
  native_platforms_layout->setSpacing(0);

  auto windows_layout = new QHBoxLayout();
  windows_layout->setContentsMargins(0, 0, 0, 0);
  auto windows_icon = new QLabel(this);
  windows_icon->setPixmap(create_svg_pixmap(":/logos/windows.svg"));
  windows_layout->addWidget(windows_icon);
  auto windows_text = new QLabel(tr("Windows"), this);
  windows_layout->addWidget(windows_text);
  windows_layout->addStretch();
  native_platforms_layout->addLayout(windows_layout);

  auto macos_layout = new QHBoxLayout();
  macos_layout->setContentsMargins(0, 0, 0, 0);
  auto macos_icon = new QLabel(this);
  macos_icon->setPixmap(create_svg_pixmap(":/logos/macos2.svg"));
  macos_layout->addWidget(macos_icon);
  auto macos_text = new QLabel(tr("macOS"), this);
  macos_layout->addWidget(macos_text);
  macos_layout->addStretch();
  native_platforms_layout->addLayout(macos_layout);

  auto linux_layout = new QHBoxLayout();
  linux_layout->setContentsMargins(0, 0, 0, 0);
  auto linux_icon = new QLabel(this);
  linux_icon->setPixmap(create_svg_pixmap(":/logos/linux.svg"));
  linux_layout->addWidget(linux_icon);
  auto linux_text = new QLabel(tr("Linux"), this);
  linux_layout->addWidget(linux_text);
  linux_layout->addStretch();

  native_platforms_layout->addLayout(linux_layout);
  native_platforms_layout->addStretch(1);
  native_text_layout->addLayout(native_platforms_layout);

  native_text_view_ = new NativeText(this);
  native_text_view_->setPlainText(file_contents);
  native_text_layout->addWidget(native_text_view_);
  text_view->addWidget(native_text);

  // TODO: With windows WSL, we should be able to generate the files for windows
  // and Linux,
  //  so making this a TabWidget instead as windows users will be able to view
  //  the CMake for Windows AND their WSL distro

  // TODO: Don't hardcode all the text views to windows
  cmake_text_ = new QTabWidget(this);
  cmake_text_->hide();
  cmake_text_view_ = new CMakeText(this);
  cmake_text_->addTab(cmake_text_view_,
                      QIcon(create_svg_pixmap(":/logos/windows.svg")),
                      tr("Windows"));
  text_view->addWidget(cmake_text_);

  meson_text_ = new QTabWidget(this);
  meson_text_->hide();
  meson_text_view_ = new MesonText(this);
  meson_text_->addTab(meson_text_view_,
                      QIcon(create_svg_pixmap(":/logos/windows.svg")),
                      tr("Windows"));
  text_view->addWidget(meson_text_);

  // TODO: Don't set this as there can be an arbitrary amount of files
  //  being generated
  // text_view->setSizes({400, 300, 300});

  view->addWidget(gui_view);
  view->addWidget(text_view);

  view->setSizes({100, 200});

  auto main_layout = new QVBoxLayout(this);
  main_layout->addWidget(view);
}

QString FileNode::file_path() const {
  return QDir(proj_relative_dir_path_).filePath(file_name_);
}

void FileNode::show_cmake(QString contents) {
  auto cmake_contents = std::move(contents);
  // TODO: handle multiple platforms here in the Windows + WSL scenario
  cmake_text_view_->setText(
      cmake_contents.replace(QChar('\t'), QString(" ").repeated(4)));
  cmake_text_->show();
}

void FileNode::show_meson(QString contents) {
  auto meson_contents = std::move(contents);
  // TODO: handle multiple platforms here in the Windows + WSL scenario
  meson_text_view_->setText(
      meson_contents.replace(QChar('\t'), QString(" ").repeated(4)));
  meson_text_->show();
}

void FileNode::on_object_selection_changed(const QModelIndex& index) {
  Q_UNUSED(index);
}

Project::Project(QWidget* parent) : QTabWidget(parent) {
  setTabPosition(QTabWidget::TabPosition::North);
  setMovable(true);
  setTabsClosable(true);
  connect(this, &Project::tabCloseRequested, this,
          &Project::on_file_tab_closed);
}

void Project::update(
    const QDir& root_dir,
    const std::unordered_map<std::string, std::vector<ObjectNode>>& objects) {
  project_dir_ = root_dir;
  while (count() > 0) {
    auto file_node = qobject_cast<FileNode*>(widget(0));
    removeTab(0);
    file_node->deleteLater();
  }
  open_files_.clear();
  project_objects_ = objects;
}

void Project::add_file(const models::FileNode& file_node) {
  std::visit(overloaded{[](const models::Folder&) {
                          // Ignore Folders
                        },
                        [this](const models::NativeFile& n) {
                          (void)add_native(n.path);
                        },
                        [this](const models::CMakeFile& n) { add_cmake(n); },
                        [this](const models::MesonFile& n) { add_meson(n); }},
             file_node);
}

FileNode* Project::add_native(const std::filesystem::path& file_path) {
  auto file_node_itr = open_files_.find(file_path);
  if (file_node_itr != open_files_.end()) {
    FileNode* file_node = file_node_itr.value();
    setCurrentWidget(file_node);
    return file_node;
  }
  auto path = file_path.generic_string();
  auto file_path_str = QString::fromStdString(path);
  QFile native_file(file_path_str);
  if (!native_file.open(QIODevice::ReadOnly | QIODevice::Text)) {
    return nullptr;
  }

  const auto file_objects_itr = project_objects_.find(file_path.string());
  const auto file_objects = (file_objects_itr != project_objects_.end())
                                ? file_objects_itr->second
                                : std::vector<ObjectNode>{};
  QFileInfo native_info(native_file.fileName());
  const QString native_file_name = native_info.fileName();
  const QString proj_relative_dir_path =
      project_dir_.relativeFilePath(native_info.absoluteDir().path());
  const QString native_file_contents = native_file.readAll();
  auto native_node = new FileNode(native_file_name, proj_relative_dir_path, native_file_contents,
                                  file_objects, this);
  const int tab_index = addTab(native_node, native_file_name);
  tabBar()->setTabData(tab_index, native_info.filePath());
  setCurrentIndex(tab_index);
  setTabToolTip(tab_index, proj_relative_dir_path);
  open_files_[file_path] = native_node;
  return native_node;
}

void Project::add_cmake(const models::CMakeFile& file_node) {
  auto path = file_node.path.generic_string();
  auto file_path_str = QString::fromStdString(path);
  QFile cmake_file(file_path_str);
  if (!cmake_file.open(QIODevice::ReadOnly | QIODevice::Text)) {
    return;
  }
  auto native_node_itr = open_files_.find(file_node.native_path);
  if (native_node_itr != open_files_.end()) {
    FileNode* native_node = native_node_itr.value();
    native_node->show_cmake(cmake_file.readAll());
    setCurrentWidget(native_node);
  } else {
    if (FileNode* native_node = add_native(file_node.native_path)) {
      native_node->show_cmake(cmake_file.readAll());
      setCurrentWidget(native_node);
    }
  }
}

void Project::add_meson(const models::MesonFile& file_node) {
  auto path = file_node.path.generic_string();
  auto file_path_str = QString::fromStdString(path);
  QFile meson_file(file_path_str);
  if (!meson_file.open(QIODevice::ReadOnly | QIODevice::Text)) {
    return;
  }
  auto native_node_itr = open_files_.find(file_node.native_path);
  if (native_node_itr != open_files_.end()) {
    FileNode* native_node = native_node_itr.value();
    native_node->show_meson(meson_file.readAll());
    setCurrentWidget(native_node);
  } else {
    if (FileNode* native_node = add_native(file_node.native_path)) {
      native_node->show_meson(meson_file.readAll());
      setCurrentWidget(native_node);
    }
  }
}

void Project::on_file_tab_closed(const int tab_index) {
  const auto native_file_path = std::filesystem::path(
      tabBar()->tabData(tab_index).toString().toStdString());
  auto file_node = qobject_cast<FileNode*>(widget(tab_index));
  removeTab(tab_index);
  file_node->deleteLater();
  open_files_.remove(native_file_path);
  Q_EMIT file_closed(static_cast<int>(open_files_.size()));
}

}  // namespace iprm::views
