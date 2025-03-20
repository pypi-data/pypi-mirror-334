/*
 * Copyright (c) 2025 ayeteadoe <ayeteadoe@gmail.com>
 *
 * SPDX-License-Identifier: MIT
 */
#include "dependencygraph.hpp"
#include <QGraphicsProxyWidget>
#include <QGuiApplication>
#include <QPainter>
#include <QScrollBar>
#include <QStyleHints>
#include <QSvgRenderer>
#include <QTabWidget>
#include <QTimer>
#include <cmath>
#include "loadingwidget.hpp"

#include <functional>

#include <graphviz/gvc.h>
#include "graphviz.hpp"

// TODO: Create a C++ API wrapper around the graphviz API instead of the C API
//  that was required for the rust implementation via FFI. That is gone now so
//  we can be fully C++
class scope_guard {
 public:
  scope_guard(const scope_guard&) = delete;
  scope_guard& operator=(const scope_guard&) = delete;
  scope_guard(scope_guard&&) = default;
  scope_guard& operator=(scope_guard&&) = default;
  ~scope_guard() { scope_exit_callback_(); }

  template <typename Func>
  static auto make(Func&& f) {
    scope_guard guard;
    guard.scope_exit_callback_ = f;
    return guard;
  }

 private:
  scope_guard() = default;

  std::function<void()> scope_exit_callback_;
};

namespace iprm::views {

DependencyView::DependencyView(QWidget* parent) : QScrollArea(parent) {
  setWidgetResizable(true);
  setHorizontalScrollBarPolicy(Qt::ScrollBarAsNeeded);
  setVerticalScrollBarPolicy(Qt::ScrollBarAsNeeded);

  stack_ = new QStackedWidget(this);
  setWidget(stack_);

  loading_page_ = new LoadingWidget(this);
  loading_page_->set_text(tr("Generating graph..."));

  platform_tabs_ = new QTabWidget(this);
  platform_tabs_->setMovable(true);

  graph_view_ = new DependencyGraphicsView(this);
  scene_ = new DependencyGraphicsScene(this);
  graph_view_->setScene(scene_);

  // TODO: don't hardcode to windows, DependencyView should have a function that
  //  passes object of ALL platforms, then setup each tab
  QSvgRenderer renderer(QString(":/logos/windows.svg"));
  QPixmap pixmap(QSize(16, 16));
  pixmap.fill(Qt::transparent);
  QPainter painter(&pixmap);
  painter.setRenderHint(QPainter::Antialiasing);
  renderer.render(&painter);
  painter.end();
  QIcon icon;
  icon.addPixmap(pixmap);

  // TODO: Follow Objects model of being able to dynamically object the
  //  platform-specific views
  platform_tabs_->addTab(graph_view_, icon, tr("Windows"));

  stack_->addWidget(loading_page_);
  stack_->addWidget(platform_tabs_);
  stack_->setCurrentWidget(loading_page_);
}

void DependencyView::build_graph(
    const lemon::ListDigraph& graph,
    const lemon::ListDigraph::NodeMap<ObjectNode>& node_data) {
  stack_->setCurrentWidget(loading_page_);

  scene_->build_graph(graph, node_data);
  stack_->setCurrentWidget(platform_tabs_);
}

DependencyGraphicsView::DependencyGraphicsView(QWidget* parent)
    : QGraphicsView(parent) {
  setRenderHint(QPainter::Antialiasing);
  setViewportUpdateMode(FullViewportUpdate);
  setHorizontalScrollBarPolicy(Qt::ScrollBarAsNeeded);
  setVerticalScrollBarPolicy(Qt::ScrollBarAsNeeded);
  setDragMode(RubberBandDrag);

  setAttribute(Qt::WA_AcceptTouchEvents);
  grabGesture(Qt::PinchGesture);
  viewport()->setAttribute(Qt::WA_AcceptTouchEvents);
}

bool DependencyGraphicsView::event(QEvent* event) {
  if (event->type() == QEvent::Gesture) {
    return gestureEvent(dynamic_cast<QGestureEvent*>(event));
  }
  return QGraphicsView::event(event);
}

void DependencyGraphicsView::showEvent(QShowEvent* event) {
  QGraphicsView::showEvent(event);
  QTimer::singleShot(100, this, [this]() {
    QGraphicsScene* dep_scene = scene();
    if (dep_scene == nullptr) {
      return;
    }

    QRectF itemsRect = dep_scene->itemsBoundingRect();
    if (itemsRect.isEmpty()) {
      return;
    }

    static constexpr qreal margin = 0.2;
    QRectF expandedRect = itemsRect.adjusted(
        -itemsRect.width() * margin, -itemsRect.height() * margin,
        itemsRect.width() * margin, itemsRect.height() * margin);

    dep_scene->setSceneRect(expandedRect);
    fitInView(expandedRect, Qt::KeepAspectRatio);
    viewport()->update();
  });
}

void DependencyGraphicsView::wheelEvent(QWheelEvent* event) {
  bool from_trackpad = (event->source() == Qt::MouseEventSynthesizedBySystem);
  if (!from_trackpad) {
    QPointF scene_pos = mapToScene(event->position().toPoint());
    qreal factor =
        event->angleDelta().y() > 0 ? zoom_factor_ : 1.0 / zoom_factor_;
    scale(factor, factor);
    QPointF delta = mapToScene(event->position().toPoint()) - scene_pos;
    translate(delta.x(), delta.y());
  } else {
    QPoint pixels = event->pixelDelta();
    QPoint degrees = event->angleDelta() / 8;

    // Use pixel delta for smoother scrolling if available
    if (!pixels.isNull()) {
      horizontalScrollBar()->setValue(horizontalScrollBar()->value() -
                                      pixels.x());
      verticalScrollBar()->setValue(verticalScrollBar()->value() - pixels.y());
    } else if (!degrees.isNull()) {
      QPoint steps = degrees / 15;
      horizontalScrollBar()->setValue(horizontalScrollBar()->value() -
                                      steps.x() * 20);
      verticalScrollBar()->setValue(verticalScrollBar()->value() -
                                    steps.y() * 20);
    }
  }
  event->accept();
}

bool DependencyGraphicsView::gestureEvent(QGestureEvent* event) {
  if (QGesture* pinch = event->gesture(Qt::PinchGesture)) {
    pinchTriggered(dynamic_cast<QPinchGesture*>(pinch));
    return true;
  }
  return false;
}

void DependencyGraphicsView::pinchTriggered(QPinchGesture* gesture) {
  QPinchGesture::ChangeFlags changeFlags = gesture->changeFlags();

  if (changeFlags & QPinchGesture::ScaleFactorChanged) {
    QPointF center = gesture->centerPoint();

    QPointF scene_pos = mapToScene(center.toPoint());

    qreal scale_factor = gesture->scaleFactor();

    // Avoid excessive scaling from single gestures
    if (scale_factor > 2.0)
      scale_factor = 2.0;
    if (scale_factor < 0.5)
      scale_factor = 0.5;

    scale(scale_factor, scale_factor);
    current_scale_ *= scale_factor;

    QPointF delta = mapToScene(center.toPoint()) - scene_pos;
    translate(delta.x(), delta.y());
  }
}

void DependencyGraphicsView::mousePressEvent(QMouseEvent* event) {
  if (event->button() == Qt::LeftButton) {
    panning_ = true;
    last_mouse_pos_ = event->pos();
    setCursor(Qt::ClosedHandCursor);
    event->accept();
  } else {
    QGraphicsView::mousePressEvent(event);
  }
}

void DependencyGraphicsView::mouseReleaseEvent(QMouseEvent* event) {
  if (event->button() == Qt::LeftButton) {
    panning_ = false;
    setCursor(Qt::ArrowCursor);
    event->accept();
  } else {
    QGraphicsView::mouseReleaseEvent(event);
  }
}

void DependencyGraphicsView::mouseMoveEvent(QMouseEvent* event) {
  if (panning_) {
    QPoint delta = event->pos() - last_mouse_pos_;
    last_mouse_pos_ = event->pos();
    horizontalScrollBar()->setValue(horizontalScrollBar()->value() - delta.x());
    verticalScrollBar()->setValue(verticalScrollBar()->value() - delta.y());
    event->accept();
  } else {
    QGraphicsView::mouseMoveEvent(event);
  }
}

DependencyGraphicsScene::DependencyGraphicsScene(QObject* parent)
    : QGraphicsScene(parent), gvc_(gvContext()) {
  setItemIndexMethod(QGraphicsScene::NoIndex);
  assert(gvc_ != nullptr);
}

DependencyGraphicsScene::~DependencyGraphicsScene() {
  view_.reset();
  if (gvc_ != nullptr) {
    gvFreeContext(gvc_);
  }
}

void DependencyGraphicsScene::build_graph(
    const lemon::ListDigraph& graph,
    const lemon::ListDigraph::NodeMap<ObjectNode>& node_data) {
  if (view_.has_value()) {
    view_.value().clear();
  }
  clear();

  auto g = create_graph("depenency_graph");
  // TODO: don't leak here
  // auto graph_guard = scope_guard::make([this, g]() { free_graph(gvc_, g); });

  std::unordered_map<int, Agnode_t*> gv_nodes;

  for (lemon::ListDigraph::NodeIt n(graph); n != lemon::INVALID; ++n) {
    const auto& data = node_data[n];
    const int node_id = graph.id(n);

    const auto name = data.name.toStdString();
    const int num_shape_sides = data.shape_sides;
    const auto shape_type = data.shape_type.toStdString();
    const auto hex_colour = data.hex_colour.toStdString();
    gv_nodes[node_id] = add_node(g, node_id, name.c_str(), shape_type.c_str(),
                                 num_shape_sides, hex_colour.c_str());
  }

  for (lemon::ListDigraph::ArcIt a(graph); a != lemon::INVALID; ++a) {
    auto source_id = graph.id(graph.source(a));
    auto target_id = graph.id(graph.target(a));

    add_edge(g, gv_nodes[source_id], gv_nodes[target_id]);
  }

  apply_layout(gvc_, g, "dot");
  LayoutResult gl = get_layout_result(g);
  if (!view_.has_value()) {
    view_.emplace(this);
  }
  view_.value().create(gl);
}

}  // namespace iprm::views
