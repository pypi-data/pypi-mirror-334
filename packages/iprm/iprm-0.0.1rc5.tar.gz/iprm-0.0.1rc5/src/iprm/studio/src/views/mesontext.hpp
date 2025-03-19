#pragma once

#include <QCodeEditor>

namespace iprm::views {


class MesonText : public QCodeEditor {
  Q_OBJECT

 public:
  explicit MesonText(QWidget* parent = nullptr);
};

}  // namespace iprm::views
