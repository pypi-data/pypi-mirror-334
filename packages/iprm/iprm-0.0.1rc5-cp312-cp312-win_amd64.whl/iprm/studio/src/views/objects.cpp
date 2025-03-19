#include "objects.hpp"
#include <QHeaderView>
#include <QMouseEvent>
#include <QPainter>
#include <QSvgRenderer>

namespace iprm::views {

QIcon create_svg_icon(const QString& svg_file) {
  QSvgRenderer renderer(svg_file);
  QPixmap pixmap(QSize(16, 16));
  pixmap.fill(Qt::transparent);
  QPainter painter(&pixmap);
  painter.setRenderHint(QPainter::Antialiasing);
  renderer.render(&painter);
  painter.end();
  QIcon icon;
  icon.addPixmap(pixmap);
  return icon;
}

PlatformObjects::PlatformObjects(QWidget* parent)
    : QTreeView(parent), objects_model_(new models::Objects(this)) {
  setHeaderHidden(false);
  setAlternatingRowColors(true);
  setSelectionMode(QTreeView::SingleSelection);
  setAnimated(false);
  setIndentation(0);
  setItemsExpandable(false);
  setRootIsDecorated(false);
}

void PlatformObjects::showEvent(QShowEvent* event) {
  header()->setStretchLastSection(false);
  header()->setSectionResizeMode(0, QHeaderView::ResizeMode::Stretch);
  header()->setSectionResizeMode(1, QHeaderView::ResizeMode::Stretch);
}

void PlatformObjects::load_objects(const std::vector<ObjectNode>& objects) {
  setModel(objects_model_);
  objects_model_->load_objects(objects);
  connect(this, &QTreeView::doubleClicked, this,
          &PlatformObjects::object_selection_changed);
}

Objects::Objects(QWidget* parent)
    : QTabWidget(parent),
      windows_icon_(create_svg_icon(":/logos/windows.svg")) {}

void Objects::load_windows_objects(const std::vector<ObjectNode>& objects) {
  static const QString s_windows_tab = tr("Windows");
  auto windows_objects_itr = platform_objects_.find(s_windows_tab);
  if (windows_objects_itr != platform_objects_.end()) {
    windows_objects_itr.value()->load_objects(objects);
    setCurrentWidget(windows_objects_itr.value());
  } else {
    auto windows_objects = new PlatformObjects(this);
    connect(windows_objects, &PlatformObjects::object_selection_changed, this,
            &Objects::object_selection_changed);
    windows_objects->load_objects(objects);
    addTab(windows_objects, windows_icon_, s_windows_tab);
  }
}

}  // namespace iprm::views
