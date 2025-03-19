#include "mainwindow.hpp"
#include "splashscreen.hpp"

#include <QApplication>
#include <QDir>
#include <QStyleHints>

int main(int argc, char** argv) {
  QApplication app(argc, argv);

  QStyleHints* styleHints = QGuiApplication::styleHints();
  auto set_stylesheet = [&app](const Qt::ColorScheme colour_scheme) {
    switch (colour_scheme) {
      case Qt::ColorScheme::Dark: {
        QFile ss(":/styles/dark_theme_stylesheet.qss");
        ss.open(QFile::ReadOnly);
        app.setStyleSheet(QString::fromUtf8(ss.readAll()));
        break;
      }
      case Qt::ColorScheme::Light:
      case Qt::ColorScheme::Unknown:
      default: {
        QFile ss(":/styles/light_theme_stylesheet.qss");
        ss.open(QFile::ReadOnly);
        app.setStyleSheet(QString::fromUtf8(ss.readAll()));
        break;
      }
    }
  };
  set_stylesheet(styleHints->colorScheme());
  QObject::connect(styleHints, &QStyleHints::colorSchemeChanged, &app,
                   [&set_stylesheet](Qt::ColorScheme colour_scheme) {
                     set_stylesheet(colour_scheme);
                   });

  app.setApplicationName("IPRM Studio");
  app.setApplicationVersion("0.1.0");


  iprm::MainWindow window;
  window.show_splash();
  const QStringList args = QApplication::arguments();
  if (args.length() == 2) {
    const auto project_dir = QDir(QDir::toNativeSeparators(
        QDir::current().absoluteFilePath(QDir(args[1]).absolutePath())));
    window.set_project_dir(project_dir);
  } else {
    window.show();
  }
  return app.exec();
}
