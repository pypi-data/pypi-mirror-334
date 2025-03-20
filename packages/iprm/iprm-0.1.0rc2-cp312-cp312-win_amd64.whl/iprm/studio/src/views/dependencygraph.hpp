/*
 * Copyright (c) 2025 ayeteadoe <ayeteadoe@gmail.com>
 *
 * SPDX-License-Identifier: MIT
 */
#pragma once

#include <graphviz/gvc.h>
#include <lemon/list_graph.h>
#include <QGestureEvent>
#include <QGraphicsView>
#include <QPinchGesture>
#include <QPointF>
#include <QScrollArea>
#include <QStackedWidget>
#include <QString>
#include <optional>
#include <queue>
#include <set>
#include "../apibridge.hpp"
#include "graphview.hpp"

class QTabWidget;

namespace iprm::views {

class LoadingWidget;
class DependencyGraphicsScene;
class DependencyGraphicsView;

class DependencyView : public QScrollArea {
  Q_OBJECT
 public:
  explicit DependencyView(QWidget* parent = nullptr);

  void build_graph(const lemon::ListDigraph& graph,
                   const lemon::ListDigraph::NodeMap<ObjectNode>& node_data);

 private:
  QStackedWidget* stack_{nullptr};
  LoadingWidget* loading_page_{nullptr};
  DependencyGraphicsView* graph_view_{nullptr};
  DependencyGraphicsScene* scene_{nullptr};

  // TODO: Display the ALL dependency graphs for each platform in the tab widget
  QTabWidget* platform_tabs_{nullptr};
};

class DependencyGraphicsView : public QGraphicsView {
  Q_OBJECT
 public:
  explicit DependencyGraphicsView(QWidget* parent = nullptr);

 protected:
  bool event(QEvent* event) override;
  void showEvent(QShowEvent* event) override;
  void wheelEvent(QWheelEvent* event) override;
  void mousePressEvent(QMouseEvent* event) override;
  void mouseReleaseEvent(QMouseEvent* event) override;
  void mouseMoveEvent(QMouseEvent* event) override;
  bool gestureEvent(QGestureEvent* event);
  void pinchTriggered(QPinchGesture* gesture);

 private:
  bool panning_{false};
  qreal current_scale_ = 1.0;
  QPoint last_mouse_pos_;
  const qreal zoom_factor_{1.15};
};

class DependencyGraphicsScene : public QGraphicsScene {
  Q_OBJECT
 public:
  explicit DependencyGraphicsScene(QObject* parent = nullptr);
  ~DependencyGraphicsScene();

  void build_graph(const lemon::ListDigraph& graph,
                   const lemon::ListDigraph::NodeMap<ObjectNode>& node_data);

 private:
  GVC_t* gvc_{nullptr};
  std::optional<GraphView> view_;
};

}  // namespace iprm::views
