/*
 * Copyright (c) 2025 ayeteadoe <ayeteadoe@gmail.com>
 *
 * SPDX-License-Identifier: MIT
 */
#include "apibridge.hpp"
#include "mainwindow.hpp"
#include "splashscreen.hpp"

#include <QApplication>
#include <QDir>
#include <QStyleHints>

#include <optional>

int main(int argc, char** argv) {
  QApplication app(argc, argv);
  QApplication::setApplicationName("IPRM Studio");
  QApplication::setApplicationVersion("0.0.1");

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

  iprm::SplashScreen splash;
  splash.show();
  QApplication::processEvents();

  std::optional<iprm::MainWindow> window;
  iprm::APIBridgeThread api_bridge;
  const QStringList args = QApplication::arguments();
  if (args.length() == 2) {
    const auto project_dir = QDir(QDir::toNativeSeparators(
        QDir::current().absoluteFilePath(QDir(args[1]).absolutePath())));
    api_bridge.set_root_dir(project_dir);

    QApplication::connect(&api_bridge, &iprm::APIBridgeThread::print_stdout,
                          &app, [](const QString&) {
                            // TODO: Log this somewhere? Main Window doesn't
                            // existing
                            //  yet and we may fail, so best place to put it is
                            //  to disk to help debug if project load fails on
                            //  startup
                          });
    QApplication::connect(
        &api_bridge, &iprm::APIBridgeThread::error, &app,
        [&app, &splash, &window, &api_bridge](const iprm::APIError& error) {
          QApplication::disconnect(&api_bridge, nullptr, &app, nullptr);
          splash.finish(nullptr);
          window.emplace(api_bridge);
          window.value().on_project_load_failed(error);
          window.value().show();
        });
    QApplication::connect(
        &api_bridge, &iprm::APIBridgeThread::project_load_success, &app,
        [project_dir, &app, &window, &splash, &api_bridge]() {
          QApplication::disconnect(&api_bridge, nullptr, &app, nullptr);
          splash.finish(nullptr);
          window.emplace(api_bridge);
          window.value().set_project(project_dir);
          window.value().on_project_loaded();
          window.value().show();
        });

    QMetaObject::invokeMethod(&api_bridge, &iprm::APIBridgeThread::load_project,
                              Qt::QueuedConnection);
  } else {
    splash.finish(nullptr);
    window.emplace(api_bridge);
    window.value().show();
  }
  return QApplication::exec();
}
