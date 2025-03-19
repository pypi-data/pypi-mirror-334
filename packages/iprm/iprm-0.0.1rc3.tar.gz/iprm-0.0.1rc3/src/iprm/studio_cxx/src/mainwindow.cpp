#include "mainwindow.hpp"
#include <QApplication>
#include <QFileDialog>
#include <QMenuBar>
#include <QMessageBox>
#include <QProcess>
#include <QSettings>
#include <QToolButton>
#include <QVBoxLayout>
#include "apibridge.hpp"
#include "models/filesystem.hpp"
#include "views/dependencygraph.hpp"
#include "views/filesystem.hpp"
#include "views/loadingwidget.hpp"
#include "views/log.hpp"
#include "views/project.hpp"

namespace iprm {

MainWindow::MainWindow()
    : QMainWindow(nullptr),
      file_filter_(tr("IPRM Files (*.iprm);;All Files (*.*)")) {
  setup_api_bridge();
  setup_ui();
  create_actions();
  create_menu_bar();
  create_tool_bar();
  setWindowTitle(tr("IPRM Studio"));
  setWindowIcon(QIcon(":/logos/iprm_icon.svg"));
  resize(1280, 720);
  showMaximized();
}

void MainWindow::show_splash() {
  splash_.show();
  qApp->processEvents();
}


void MainWindow::set_project_dir(const QDir& project_dir) {
  project_dir_ = project_dir;
  load_project();
}

void MainWindow::closeEvent(QCloseEvent* event) {
  QMainWindow::closeEvent(event);
  if (api_bridge_.isRunning()) {
    api_bridge_.destroy_sess();
    api_bridge_.quit();
    api_bridge_.wait();
  }
}

void MainWindow::setup_api_bridge() {
  auto bridge = &api_bridge_;
  // TODO: Fix up error handling to not assume all returned errors are project
  //  load failures
  connect(bridge, &APIBridgeThread::error, this,
          &MainWindow::on_project_load_failed);
  connect(bridge, &APIBridgeThread::print_stdout, this,
          &MainWindow::on_print_stdout);
  connect(bridge, &APIBridgeThread::project_load_success, this,
          &MainWindow::on_project_loaded);
  connect(bridge, &APIBridgeThread::cmake_generate_success, this,
          &MainWindow::on_cmake_generated);
  connect(bridge, &APIBridgeThread::meson_generate_success, this,
          &MainWindow::on_meson_generated);
  api_bridge_.start();
  QMetaObject::invokeMethod(bridge, &APIBridgeThread::capture_io,
                            Qt::QueuedConnection);
}

void MainWindow::setup_ui() {
  // Status Bar Setup
  status_bar_ = statusBar();
  auto progress_widget = new QWidget(this);
  auto progress_layout = new QHBoxLayout(progress_widget);
  progress_layout->setContentsMargins(0, 0, 0, 0);
  progress_layout->setSpacing(10);

  status_label_ = new QLabel(this);
  progress_bar_ = new QProgressBar(this);
  progress_bar_->setMaximumWidth(200);
  progress_bar_->setMaximumHeight(15);
  progress_bar_->setTextVisible(false);
  progress_bar_->hide();

  progress_layout->addWidget(status_label_);
  progress_layout->addWidget(progress_bar_);
  status_bar_->addWidget(progress_widget);

  // Log View
  log_view_ = new views::Log(project_dir_, this);
  log_dock_ = new QDockWidget(tr("Log"));
  log_dock_->setObjectName("log_dock");
  log_dock_->setWidget(log_view_);
  addDockWidget(Qt::BottomDockWidgetArea, log_dock_);
  connect(log_view_, &views::Log::process_started, this,
          &MainWindow::handle_process_started);
  connect(log_view_, &views::Log::process_finished, this,
          &MainWindow::handle_process_finished);
  connect(log_view_, &views::Log::process_error, this,
          &MainWindow::handle_process_error);
  log_view_->log("Welcome to IPRM Studio!");

  // File System View
  fs_model_ = new iprm::models::FileSystem(this);
  fs_view_ = new iprm::views::FileSystem(this);
  fs_view_->setModel(fs_model_);
  connect(fs_view_, &iprm::views::FileSystem::file_activated, this,
          &MainWindow::on_file_activated);
  fs_dock_ = new QDockWidget(tr("Project Files"));
  fs_dock_->setObjectName("fs_dock");
  fs_dock_->setWidget(fs_view_);

  // Dependency Graph View
#ifndef __APPLE__
  dep_view_ = new views::DependencyView(this);
  dep_dock_ = new QDockWidget(tr("Dependency Graph"));
  dep_dock_->setObjectName("dep_dock");
  dep_dock_->setWidget(dep_view_);
#endif

  // Project File View
  proj_file_view_ = new QStackedWidget(this);
  proj_view_ = new views::Project(this);
  proj_file_view_->addWidget(proj_view_);
  auto no_file_layout = new QVBoxLayout;
  no_file_layout->setAlignment(Qt::AlignCenter);
  auto no_file_label = new QLabel(tr("Select a File"), this);
  no_file_layout->addWidget(no_file_label);
  no_file_view_ = new QWidget(this);
  no_file_view_->setLayout(no_file_layout);
  connect(proj_view_, &views::Project::file_closed, this,
          [this](const int num_files_opened) {
            if (num_files_opened <= 0) {
              proj_file_view_->setCurrentWidget(no_file_view_);
            }
          });
  proj_file_view_->addWidget(no_file_view_);
  proj_file_view_->setCurrentWidget(no_file_view_);

  // Main View
  auto no_proj_layout = new QVBoxLayout;
  no_proj_layout->setAlignment(Qt::AlignCenter);
  auto no_proj_label = new QLabel(tr("Open a Project"), this);
  no_proj_layout->addWidget(no_proj_label);
  no_proj_view_ = new QWidget(this);
  no_proj_view_->setLayout(no_proj_layout);

  auto loading_proj_failed_layout = new QHBoxLayout;
  loading_proj_failed_layout->setAlignment(Qt::AlignCenter);
  auto err_label_icon = new QLabel();
  err_label_icon->setPixmap(
      style()->standardIcon(QStyle::SP_MessageBoxCritical).pixmap(16, 16));
  auto err_label_msg =
      new QLabel(tr("Failed to load project. See Log window for more details"));
  loading_proj_failed_layout->addWidget(err_label_icon);
  loading_proj_failed_layout->addWidget(err_label_msg);
  loading_proj_failed_view_ = new QWidget(this);
  loading_proj_failed_view_->setLayout(loading_proj_failed_layout);

  loading_proj_view_ = new views::LoadingWidget(this);
  loading_proj_view_->set_text(tr("Loading Project..."));

  stack_ = new QStackedWidget(this);
  stack_->addWidget(no_proj_view_);
  stack_->addWidget(proj_file_view_);
  stack_->addWidget(loading_proj_failed_view_);
  stack_->addWidget(loading_proj_view_);
  stack_->setCurrentWidget(no_proj_view_);
  setCentralWidget(stack_);
}

void MainWindow::create_actions() {
  new_action_ = new QAction(QIcon::fromTheme("document-new"), tr("&New"), this);
  new_action_->setShortcut(QKeySequence::New);
  new_action_->setToolTip(tr("Create a new project"));
  connect(new_action_, &QAction::triggered, this, &MainWindow::new_project);

  open_action_ =
      new QAction(QIcon::fromTheme("document-open"), tr("&Open..."), this);
  open_action_->setShortcut(QKeySequence::Open);
  open_action_->setToolTip(tr("Open an existing project"));
  connect(open_action_, &QAction::triggered, this, &MainWindow::open_project);

  save_action_ =
      new QAction(QIcon::fromTheme("document-save"), tr("&Save"), this);
  save_action_->setShortcut(QKeySequence::Save);
  save_action_->setToolTip(tr("Save the current file"));
  connect(save_action_, &QAction::triggered, this,
          &MainWindow::save_current_file);

  save_as_action_ = new QAction(QIcon::fromTheme("document-save-as"),
                                tr("Save &As..."), this);
  save_as_action_->setShortcut(QKeySequence::SaveAs);
  save_as_action_->setToolTip(tr("Save the current file under a new name"));
  connect(save_as_action_, &QAction::triggered, this,
          &MainWindow::save_file_as);

  // TODO: Generalize this code, use a QHash<QString, GeneratorActions> where
  //  the value is the collection of all the actions the generator supports,
  //  and the key is the generator name, which we will map to the main
  //  entrypoint action

  // TODO: Get icons that work with generate, configure, build ,test, and
  //  install
  cmake_generate_action_ =
      new QAction(QIcon::fromTheme("generate"), tr("Generate"), this);
  cmake_generate_action_->setToolTip(tr("Generate CMakeLists.txt Project"));
  connect(cmake_generate_action_, &QAction::triggered, this,
          &MainWindow::run_cmake_generate);
  meson_generate_action_ =
      new QAction(QIcon::fromTheme("generate"), tr("Generate"), this);
  meson_generate_action_->setToolTip(tr("Generate meson.build Project"));
  connect(meson_generate_action_, &QAction::triggered, this,
          &MainWindow::run_meson_generate);

  cmake_configure_action_ =
      new QAction(QIcon::fromTheme("configure"), tr("Configure"), this);
  cmake_configure_action_->setToolTip(tr("Run CMake Configure"));
  connect(cmake_configure_action_, &QAction::triggered, this,
  &MainWindow::run_cmake_configure);

  meson_configure_action_ =
      new QAction(QIcon::fromTheme("configure"), tr("Configure"), this);
  meson_configure_action_->setToolTip(tr("Run Meson Configure"));
  connect(meson_configure_action_, &QAction::triggered, this,
          &MainWindow::run_meson_configure);

  cmake_build_action_ =
      new QAction(QIcon::fromTheme("build"), tr("Build"), this);
  cmake_build_action_->setToolTip(tr("Run CMake Build"));
  connect(cmake_build_action_, &QAction::triggered, this,
  &MainWindow::run_cmake_build);

  meson_build_action_ =
      new QAction(QIcon::fromTheme("build"), tr("Build"), this);
  meson_build_action_->setToolTip(tr("Run Meson Build"));
  connect(meson_build_action_, &QAction::triggered, this,
          &MainWindow::run_meson_build);

  cmake_test_action_ = new QAction(QIcon::fromTheme("test"), tr("Test"), this);
  cmake_test_action_->setToolTip(tr("Run CMake Test"));
  connect(cmake_test_action_, &QAction::triggered, this,
          &MainWindow::run_cmake_test);

  meson_test_action_ = new QAction(QIcon::fromTheme("test"), tr("Test"), this);
  meson_test_action_->setToolTip(tr("Run Meson Test"));
  connect(meson_test_action_, &QAction::triggered, this,
          &MainWindow::run_meson_test);

  // TODO: these will be generators too, not loaders
  /*
  scons_generate_action_ =
      new QAction(QIcon::fromTheme("import"), tr("Import"), this);
  scons_generate_action_->setToolTip(tr("Import SCons Project"));
  connect(scons_generate_action_, &QAction::triggered, this,
          &MainWindow::on_scons_import);

  msbuild_generate_action_ =
      new QAction(QIcon::fromTheme("import"), tr("Import"), this);
  msbuild_generate_action_->setToolTip(tr("Import MSBuild Project"));
  connect(msbuild_generate_action_, &QAction::triggered, this,
          &MainWindow::on_msbuild_import);
          */
}

void MainWindow::create_menu_bar() {
  auto menu_bar = this->menuBar();

  auto file_menu = menu_bar->addMenu(tr("&File"));
  file_menu->addAction(new_action_);
  file_menu->addAction(open_action_);
  file_menu->addAction(save_action_);
  file_menu->addAction(save_as_action_);
  file_menu->addSeparator();
}

void MainWindow::create_tool_bar() {
  auto toolbar = new QToolBar(this);
  toolbar->setObjectName("toolbar");
  toolbar->setIconSize(QSize(16, 16));
  addToolBar(toolbar);

  toolbar->addAction(new_action_);
  toolbar->addAction(open_action_);
  toolbar->addAction(save_action_);
  toolbar->addAction(save_as_action_);
  toolbar->addSeparator();

  auto cmake_menu = new QMenu(this);
  cmake_menu->addAction(cmake_generate_action_);
  cmake_menu->addAction(cmake_configure_action_);
  cmake_menu->addAction(cmake_build_action_);
  cmake_menu->addAction(cmake_test_action_);
  auto cmake_button = new QToolButton(this);
  cmake_button->setMenu(cmake_menu);
  cmake_button->setPopupMode(QToolButton::MenuButtonPopup);
  cmake_button->setText(tr("CMake"));
  cmake_button->setIcon(QIcon(":/logos/cmake.svg"));
  cmake_button->setToolButtonStyle(Qt::ToolButtonTextBesideIcon);
  toolbar->addWidget(cmake_button);

  auto meson_menu = new QMenu(this);
  meson_menu->addAction(meson_generate_action_);
  meson_menu->addAction(meson_configure_action_);
  meson_menu->addAction(meson_build_action_);
  meson_menu->addAction(meson_test_action_);
  auto meson_button = new QToolButton(this);
  meson_button->setMenu(meson_menu);
  meson_button->setPopupMode(QToolButton::MenuButtonPopup);
  meson_button->setText(tr("Meson"));
  meson_button->setIcon(QIcon(":/logos/meson.png"));
  meson_button->setToolButtonStyle(Qt::ToolButtonTextBesideIcon);
  toolbar->addWidget(meson_button);

  auto scons_menu = new QMenu(this);
  scons_menu->addAction(scons_generate_action_);
  auto scons_button = new QToolButton(this);
  scons_button->setMenu(scons_menu);
  scons_button->setPopupMode(QToolButton::MenuButtonPopup);
  scons_button->setText(tr("SCons"));
  scons_button->setIcon(QIcon(":/logos/scons.png"));
  scons_button->setToolButtonStyle(Qt::ToolButtonTextBesideIcon);
  toolbar->addWidget(scons_button);

  auto msbuild_menu = new QMenu(this);
  msbuild_menu->addAction(msbuild_generate_action_);
  auto msbuild_button = new QToolButton(this);
  msbuild_button->setMenu(msbuild_menu);
  msbuild_button->setPopupMode(QToolButton::MenuButtonPopup);
  msbuild_button->setText(tr("MSBuild"));
  msbuild_button->setIcon(QIcon(":/logos/msbuild.svg"));
  msbuild_button->setToolButtonStyle(Qt::ToolButtonTextBesideIcon);
  toolbar->addWidget(msbuild_button);
}

void MainWindow::disable_actions() {
  new_action_->setEnabled(false);
  open_action_->setEnabled(false);
  save_action_->setEnabled(false);
  save_as_action_->setEnabled(false);
  cmake_generate_action_->setEnabled(false);
  cmake_configure_action_->setEnabled(false);
  cmake_build_action_->setEnabled(false);
  cmake_test_action_->setEnabled(false);
  meson_generate_action_->setEnabled(false);
  /*
  meson_configure_action_->setEnabled(false);
  meson_build_action_->setEnabled(false);
  meson_test_action_->setEnabled(false);
  scons_generate_action_->setEnabled(false);
  msbuild_generate_action_->setEnabled(false);
  */
}

void MainWindow::enable_actions() {
  new_action_->setEnabled(true);
  open_action_->setEnabled(true);
  save_action_->setEnabled(true);
  save_as_action_->setEnabled(true);
  cmake_generate_action_->setEnabled(true);
  cmake_configure_action_->setEnabled(true);
  cmake_build_action_->setEnabled(true);
  cmake_test_action_->setEnabled(true);
  meson_generate_action_->setEnabled(true);
  /*
  meson_configure_action_->setEnabled(true);
  meson_build_action_->setEnabled(true);
  meson_test_action_->setEnabled(true);
  scons_generate_action_->setEnabled(true);
  msbuild_generate_action_->setEnabled(true);
  */
}

void MainWindow::load_project() {
  project_loaded_ = false;
  disable_actions();
  stack_->setCurrentWidget(loading_proj_view_);
  removeDockWidget(fs_dock_);
  removeDockWidget(dep_dock_);
  log_view_->start_logging_section("[Opening Project]");
  log_view_->log(QString("Loading project directory '%0'...")
                     .arg(project_dir_.absolutePath()));
  api_bridge_.set_root_dir(project_dir_);
  QMetaObject::invokeMethod(&api_bridge_, &APIBridgeThread::load_project,
                            Qt::QueuedConnection);
}

void MainWindow::on_project_loaded() {
  const auto& objects = api_bridge_.objects();
  std::vector<std::filesystem::path> file_paths;
  for (const auto& [path, _] : objects) {
    file_paths.push_back(std::filesystem::path(path));
  }
  fs_model_->load_tree(file_paths,
                       project_dir_.absolutePath().toLatin1().data());

  addDockWidget(Qt::LeftDockWidgetArea, fs_dock_);
  fs_dock_->show();

#ifndef __APPLE__
  addDockWidget(Qt::RightDockWidgetArea, dep_dock_);

  resizeDocks({fs_dock_, dep_dock_}, {width() / 6, width() / 2},
              Qt::Orientation::Horizontal);

  dep_dock_->show();
  dep_view_->build_graph(api_bridge_.dependency_graph(),
                         api_bridge_.dependency_node_data());
#endif

  proj_view_->update(project_dir_, objects);
  enable_actions();
  stack_->setCurrentWidget(proj_file_view_);
  // We're ready, let it rip!
  log_view_->log(QString("\nProject directory '%0' loaded!")
                     .arg(project_dir_.absolutePath()),
                 views::Log::Type::Success);
  project_loaded_ = true;
  splash_.finish(this);
  show();
  Q_EMIT ready();
}

void MainWindow::on_project_load_failed(const APIError& error) {
  // TODO: Setup error state, prompt user to re-try opening their folder, or
  //  opening a different one. Also ensure the log window is shown so they can
  //  see the errors that occurred during load
  enable_actions();
  log_view_->log_api_error(error);
  stack_->setCurrentWidget(loading_proj_failed_view_);
  Q_EMIT ready();
}

void MainWindow::on_cmake_generated() {
  log_view_->log(QString("CMake project generated for '%0'!")
                     .arg(project_dir_.absolutePath()),
                 views::Log::Type::Success);
}

void MainWindow::on_meson_generated() {
  log_view_->log(QString("Meson project generated for '%0'!")
                     .arg(project_dir_.absolutePath()),
                 views::Log::Type::Success);
}

void MainWindow::on_print_stdout(const QString& message) {
  log_view_->log(message);
}

void MainWindow::on_file_activated(const models::FileNode& file_node) {
  proj_view_->add_file(file_node);
  proj_file_view_->setCurrentWidget(proj_view_);
}

void MainWindow::on_file_modified(bool modified) {
  save_action_->setEnabled(modified);
}

void MainWindow::save_current_file() {
  // TODO: Implement
}

void MainWindow::save_file_as() {
  // TODO: Implement
}

void MainWindow::new_project() {
  // TODO: Implement
}

void MainWindow::open_project() {
  QString dir = QFileDialog::getExistingDirectory(
      this, tr("Open IPRM Project"), QDir::homePath(),
      QFileDialog::ShowDirsOnly | QFileDialog::DontResolveSymlinks);

  if (!dir.isEmpty()) {
    project_dir_ = QDir(dir);
    load_project();
  }
}

void MainWindow::run_cmake_generate() {
  log_view_->start_logging_section("[CMake Generate]");
  QMetaObject::invokeMethod(&api_bridge_, &APIBridgeThread::cmake_generate,
                            Qt::QueuedConnection);
}

void MainWindow::run_cmake_configure() {
  log_view_->start_logging_section("[CMake Configure]");
  // TODO: Expose a UI to allow for user to specify the configuration options
  //  (e.g. Ninja, binary dir, source dir, etc), as well as a clean
  //  configuration (i.e. delete the binary dir)
  const QString src_dir = project_dir_.absolutePath();
  const QString bin_dir = project_dir_.absoluteFilePath("build");
  log_view_->run_command("iprm-cmake",
                         {
                           "configure",
                           "--generator",
                           "Ninja",
                           "--srcdir",
                           src_dir,
                           "--bindir",
                           bin_dir,
                           "--buildtype",
                           "Release"
                         },
                         src_dir);
}

void MainWindow::run_cmake_build() {
  log_view_->start_logging_section("[CMake Build]");
  // TODO: Add ability in the run settings for IPRM to connect to a remote
  //  worker, using a custom gRPC+protobuf protocol (see iprm_web) that allows
  //  us to build projects on platforms besides our own to validate our changes
  //  locally
  const QString src_dir = project_dir_.absolutePath();
  const QString bin_dir = project_dir_.absoluteFilePath("build");
  log_view_->run_command("iprm-cmake",
                         {
                           "build",
                           "--bindir",
                           bin_dir,
                           "--buildtype",
                           "Release"
                         },
                         src_dir);
}

void MainWindow::run_cmake_test() {
  log_view_->start_logging_section("[CMake Test]");
  const QString src_dir = project_dir_.absolutePath();
  const QString bin_dir = project_dir_.absoluteFilePath("build");
  log_view_->run_command("iprm-cmake",
                         {
                           "test",
                           "--bindir",
                           bin_dir,
                           "--buildtype",
                           "Release"
                         },
                         src_dir);
}

void MainWindow::run_meson_generate() {
  log_view_->start_logging_section("[Meson Generate]");
  QMetaObject::invokeMethod(&api_bridge_, &APIBridgeThread::meson_generate,
                            Qt::QueuedConnection);
}

void MainWindow::run_meson_configure() {
  log_view_->start_logging_section("[Meson Configure]");
  const QString src_dir = project_dir_.absolutePath();
  const QString bin_dir = project_dir_.absoluteFilePath("build");
  log_view_->run_command("iprm-meson",
                         {
                           "configure",
                           "--generator",
                           "ninja",
                           "--srcdir",
                           src_dir,
                           "--bindir",
                           bin_dir,
                           "--buildtype",
                           "release"
                         },
                         src_dir);
}

void MainWindow::run_meson_build() {
  log_view_->start_logging_section("[Meson Build]");
  const QString src_dir = project_dir_.absolutePath();
  const QString bin_dir = project_dir_.absoluteFilePath("build");
  log_view_->run_command("iprm-meson",
                         {
                           "build",
                           "--bindir",
                           bin_dir,
                         },
                         src_dir);
}

void MainWindow::run_meson_test() {
  log_view_->start_logging_section("[Meson Test]");
  const QString src_dir = project_dir_.absolutePath();
  const QString bin_dir = project_dir_.absoluteFilePath("build");
  log_view_->run_command("iprm-meson",
                         {
                           "test",
                           "--bindir",
                           bin_dir,
                         },
                         src_dir);
}

void MainWindow::handle_process_started(const QString& command) {
  if (!project_loaded_)
    return;

  progress_bar_->setRange(0, 0);  // Indeterminate progress
  progress_bar_->show();
  status_label_->setText(tr("Running: %1").arg(command));
}

void MainWindow::handle_process_finished(int exit_code,
                                         QProcess::ExitStatus exit_status) {
  if (!project_loaded_)
    return;

  progress_bar_->hide();
  if (exit_code == 0 && exit_status == QProcess::NormalExit) {
    log_view_->log(tr("Command completed successfully!"),
               views::Log::Type::Success);
  } else {
    log_view_->log(tr("Command failed with exit code %1").arg(exit_code),
               views::Log::Type::Error);
  }
}

void MainWindow::handle_process_error(QProcess::ProcessError error) {
  if (!project_loaded_)
    return;

  progress_bar_->hide();
  status_label_->setText(tr("Error: %1").arg(static_cast<int>(error)));
  QTimer::singleShot(2500, status_label_, &QLabel::clear);
}

void MainWindow::on_scons_import() {
  // TODO: Import scons impl
}

void MainWindow::on_msbuild_import() {
  // TODO: Import msbuild impl
}

}  // namespace iprm
