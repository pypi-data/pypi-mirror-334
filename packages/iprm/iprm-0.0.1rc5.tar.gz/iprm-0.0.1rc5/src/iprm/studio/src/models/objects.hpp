#pragma once

#include "../apibridge.hpp"

#include <QAbstractItemModel>
#include <QIcon>
#include <QList>

#include <vector>

namespace iprm::models {

class Objects : public QAbstractItemModel {
  Q_OBJECT
 public:
  Objects(QObject* parent = nullptr);

  void load_objects(const std::vector<ObjectNode>& objects);

 protected:
  [[nodiscard]] int columnCount(const QModelIndex& parent) const override;

  [[nodiscard]] QVariant data(const QModelIndex& index,
                              int role) const override;

  [[nodiscard]] QVariant headerData(int section,
                                    Qt::Orientation orientation,
                                    int role) const override;
  [[nodiscard]] QModelIndex index(int row,
                                  int column,
                                  const QModelIndex& parent) const override;

  [[nodiscard]] QModelIndex parent(const QModelIndex& index) const override;

  [[nodiscard]] int rowCount(const QModelIndex& parent) const override;

 private:
  QIcon get_colour_icon(const QString& hex_colour) const;

  QIcon vs_icon_;
  QIcon qt_icon_;
  std::vector<ObjectNode> objects_;
  inline static QHash<QString, QIcon> object_colour_icons_;
};

}  // namespace iprm::models
