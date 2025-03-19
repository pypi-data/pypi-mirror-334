#include "objects.hpp"

#include <QGuiApplication>
#include <QPainter>
#include <QStyleHints>
#include <QSvgRenderer>

namespace iprm::models {

// TODO: moved this into a shared location to prevent duplication,
//  as Objects and Dependency Graph use this too
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

QIcon create_colour_icon(const QString& hex_colour) {
  QSize icon_size(16, 16);
  QPixmap pixmap(icon_size);
  pixmap.fill(Qt::transparent);
  QPainter painter(&pixmap);
  painter.setRenderHint(QPainter::Antialiasing);
  painter.setPen(Qt::NoPen);
  painter.setBrush(QColor::fromString(hex_colour));
  painter.drawRect(1, 1, icon_size.width() - 2, icon_size.height() - 2);
  painter.end();
  return pixmap;
}

Objects::Objects(QObject* parent)
    : QAbstractItemModel(parent),
      vs_icon_(create_svg_icon(":/logos/visualstudio.svg")),
      qt_icon_(create_svg_icon(":/logos/qt.svg")) {}

void Objects::load_objects(const std::vector<ObjectNode>& objects) {
  // TODO: Implicit objects shouldn't be shown here, but they SHOULD be
  //  shown in a specific objects properties view
  beginResetModel();
  objects_ = objects;
  object_colour_icons_.clear();
  endResetModel();
}

QIcon Objects::get_colour_icon(const QString& hex_colour) const {
  auto it = object_colour_icons_.find(hex_colour);
  if (it != object_colour_icons_.end()) {
    return it.value();
  }
  QIcon icon = create_colour_icon(hex_colour);
  object_colour_icons_.insert(hex_colour, icon);
  return icon;
}

QVariant Objects::data(const QModelIndex& index, int role) const {
  if (!index.isValid()) {
    return QModelIndex();
  }

  const int row = index.row();
  const int column = index.column();

  const ObjectNode& obj = objects_[row];

  switch (role) {
    case Qt::DisplayRole: {
      if (column == 0) {
        return obj.name;
      } else if (column == 1) {
        return obj.type_name;
      }
    }
    case Qt::DecorationRole: {
      if (column == 0) {
        return get_colour_icon(obj.hex_colour);
      } else if (column == 1) {
        if (static_cast<bool>(obj.type & TypeFlags::QT)) {
          return qt_icon_;
        } else if (static_cast<bool>(obj.type & TypeFlags::CRTDUAL) ||
                   static_cast<bool>(obj.type & TypeFlags::CRTSTATIC) ||
                   static_cast<bool>(obj.type & TypeFlags::CRTDYNAMIC)) {
          return vs_icon_;
        }
      }
    }
    default:
      break;
  }

  return QVariant{};
}

QVariant Objects::headerData(int section,
                             Qt::Orientation orientation,
                             int role) const {
  if (orientation == Qt::Horizontal && role == Qt::DisplayRole) {
    static const QStringList headers{tr("Name"), tr("Type")};
    return headers[section];
  }
  return QVariant{};
}

int Objects::columnCount(const QModelIndex&) const {
  // Name and Type
  return 2;
}

QModelIndex Objects::index(int row,
                           int column,
                           const QModelIndex& parent) const {
  if (row < 0 || column < 0 || row >= rowCount(parent) ||
      column >= columnCount(parent)) {
    return QModelIndex{};
  }
  return createIndex(row, column, &objects_.at(row));
}

QModelIndex Objects::parent(const QModelIndex&) const {
  // We tabular
  return QModelIndex{};
}

int Objects::rowCount(const QModelIndex&) const {
  return static_cast<int>(objects_.size());
}

}  // namespace iprm::models
