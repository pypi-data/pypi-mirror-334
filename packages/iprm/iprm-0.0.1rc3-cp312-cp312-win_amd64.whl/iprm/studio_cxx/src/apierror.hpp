// apierror.hpp
#pragma once
#include <QString>

namespace iprm {

class APIError {
 public:
  explicit APIError(const QString& msg) : message(msg) {}
  QString message;
};

}

// Register APIError with Qt's meta-type system
Q_DECLARE_METATYPE(iprm::APIError)
