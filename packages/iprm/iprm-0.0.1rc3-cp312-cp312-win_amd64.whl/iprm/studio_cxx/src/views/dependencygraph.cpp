#include "dependencygraph.hpp"
#include <graphviz/gvplugin.h>
#include <QFontMetrics>
#include <QGraphicsProxyWidget>
#include <QGuiApplication>
#include <QPainter>
#include <QScrollBar>
#include <QStyleHints>
#include <QSvgRenderer>
#include <cmath>
#include "loadingwidget.hpp"

#include <functional>

#ifdef _WIN64
// Get access to the dot layout symbol, otherwise we'd have to manually
// it up the plugin ourselves, or add to a plugin search path or something
extern "C" {
__declspec(dllimport) gvplugin_library_t gvplugin_dot_layout_LTX_library;
}
#endif

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

// NodeItem Implementation
NodeItem::NodeItem(const QString& name,
                   const QString& shape_type,
                   int shape_sides,
                   const QString& hex_color)
    : name_(name),
      shape_type_(shape_type),
      shape_sides_(shape_sides),
      color_(hex_color) {
  setFlag(QGraphicsItem::ItemIsSelectable);

  // Create text label with Consolas font
  label_ = new QGraphicsTextItem(this);
  label_->setPlainText(name_);
  label_->setDefaultTextColor(get_system_color());

  QFont font("Consolas");
  font.setBold(true);
  label_->setFont(font);

  // Center the label
  QRectF text_rect = label_->boundingRect();
  label_->setPos(-text_rect.width() / 2, -text_rect.height() / 2);

  // Create shape path based on text size
  create_shape_path();
}

void NodeItem::create_shape_path() {
  shape_path_ = QPainterPath();
  QRectF text_rect = label_->boundingRect();

  // Add padding around text
  const qreal padding = 20;
  QRectF bounds(
      -text_rect.width() / 2 - padding, -text_rect.height() / 2 - padding,
      text_rect.width() + 2 * padding, text_rect.height() + 2 * padding);

  if (shape_type_ == "house") {
    // House shape - rectangle with a triangular roof
    qreal width = bounds.width();
    qreal height = bounds.height();
    qreal roof_height = height * 0.4;  // 40% of height for roof

    shape_path_.moveTo(bounds.left(), bounds.bottom());  // Start bottom left
    shape_path_.lineTo(bounds.left(), bounds.top() + roof_height);  // Left wall
    shape_path_.lineTo(bounds.center().x(), bounds.top());  // Left roof slope
    shape_path_.lineTo(bounds.right(),
                       bounds.top() + roof_height);       // Right roof slope
    shape_path_.lineTo(bounds.right(), bounds.bottom());  // Right wall
    shape_path_.lineTo(bounds.left(), bounds.bottom());   // Bottom
  } else if (shape_type_ == "box") {
    shape_path_.addRect(bounds);
  } else if (shape_type_ == "ellipse" || shape_type_ == "oval") {
    shape_path_.addEllipse(bounds);
  } else if (shape_type_ == "diamond") {
    QPointF points[4] = {QPointF(bounds.left(), bounds.center().y()),
                         QPointF(bounds.center().x(), bounds.top()),
                         QPointF(bounds.right(), bounds.center().y()),
                         QPointF(bounds.center().x(), bounds.bottom())};
    shape_path_.moveTo(points[0]);
    for (int i = 1; i < 4; ++i) {
      shape_path_.lineTo(points[i]);
    }
    shape_path_.closeSubpath();
  } else if (shape_type_ == "polygon" && shape_sides_ > 0) {
    if (shape_sides_ == 6) {  // Special case for hexagon - match Graphviz style
      qreal width = bounds.width() / 2;
      qreal height = bounds.height() / 3;
      QPointF points[6] = {
          QPointF(bounds.center().x() - width, bounds.center().y()),
          QPointF(bounds.center().x() - width / 2,
                  bounds.center().y() - height),
          QPointF(bounds.center().x() + width / 2,
                  bounds.center().y() - height),
          QPointF(bounds.center().x() + width, bounds.center().y()),
          QPointF(bounds.center().x() + width / 2,
                  bounds.center().y() + height),
          QPointF(bounds.center().x() - width / 2,
                  bounds.center().y() + height)};
      shape_path_.moveTo(points[0]);
      for (int i = 1; i < 6; ++i) {
        shape_path_.lineTo(points[i]);
      }
      shape_path_.closeSubpath();
    } else {  // Regular polygon
      QPointF center = bounds.center();
      qreal radius = std::min(bounds.width(), bounds.height()) / 2;

      for (int i = 0; i < shape_sides_; ++i) {
        qreal angle = 2 * M_PI * i / shape_sides_ - M_PI / 2;
        QPointF point(center.x() + radius * std::cos(angle),
                      center.y() + radius * std::sin(angle));

        if (i == 0) {
          shape_path_.moveTo(point);
        } else {
          shape_path_.lineTo(point);
        }
      }
      shape_path_.closeSubpath();
    }
  }
}

QRectF NodeItem::boundingRect() const {
  return shape_path_.boundingRect();
}

QColor NodeItem::get_system_color() const {
  QStyleHints* styleHints = QGuiApplication::styleHints();
  switch (styleHints->colorScheme()) {
    case Qt::ColorScheme::Dark:
      return Qt::white;
    case Qt::ColorScheme::Light:
    case Qt::ColorScheme::Unknown:
    default:
      return Qt::black;
  }
}

void NodeItem::paint(QPainter* painter,
                     const QStyleOptionGraphicsItem* option,
                     QWidget* widget) {
  painter->setRenderHint(QPainter::Antialiasing);

  label_->setDefaultTextColor(get_system_color());

  // Draw shape
  painter->setPen(QPen(get_system_color(), 1));
  painter->setBrush(color_);
  painter->drawPath(shape_path_);
}

// EdgeItem Implementation
EdgeItem::EdgeItem(NodeItem* from,
                   NodeItem* to,
                   const QVector<QPointF>& spline_points)
    : from_(from), to_(to), spline_points_(spline_points) {
  setZValue(-1);
  update_path();
}

QColor EdgeItem::get_system_color() const {
  QStyleHints* styleHints = QGuiApplication::styleHints();
  switch (styleHints->colorScheme()) {
    case Qt::ColorScheme::Dark:
      return Qt::white;
    case Qt::ColorScheme::Light:
    case Qt::ColorScheme::Unknown:
    default:
      return Qt::black;
  }
}

void EdgeItem::update_path() {
  if (spline_points_.size() < 4)
    return;

  path_ = QPainterPath();
  path_.moveTo(spline_points_[0]);

  // Draw all Bézier segments except the last point
  for (int i = 1; i < spline_points_.size() - 3; i += 3) {
    path_.cubicTo(spline_points_[i], spline_points_[i + 1],
                  spline_points_[i + 2]);
  }

  // For the last segment, draw to where the arrow will start
  int last_seg = spline_points_.size() - 3;
  if (last_seg >= 1) {
    QPointF end_point = spline_points_.last();
    QPointF ctrl1 = spline_points_[last_seg];
    QPointF ctrl2 = spline_points_[last_seg + 1];

    // Calculate the direction of approach
    QPointF direction = end_point - ctrl2;
    qreal length = std::sqrt(QPointF::dotProduct(direction, direction));
    if (length > 0.1) {
      direction /= length;
      // Draw the curve to where the arrow will start
      QPointF arrow_base = end_point - direction * ARROW_LENGTH;
      path_.cubicTo(ctrl1, ctrl2, arrow_base);

      // Create and store arrow path
      arrow_path_ = create_arrow_head(end_point, direction);
    }
  }
}

QPainterPath EdgeItem::create_arrow_head(const QPointF& tip,
                                         const QPointF& direction) const {
  QPainterPath arrow_path;

  // Calculate perpendicular vector for arrow width
  QPointF perp(-direction.y(), direction.x());

  // Create arrow triangle
  QPointF arrow_base = tip - direction * ARROW_LENGTH;
  QPointF left = arrow_base + perp * ARROW_WIDTH;
  QPointF right = arrow_base - perp * ARROW_WIDTH;

  arrow_path.moveTo(tip);
  arrow_path.lineTo(left);
  arrow_path.lineTo(right);
  arrow_path.closeSubpath();

  return arrow_path;
}

QRectF EdgeItem::boundingRect() const {
  // Combine both curve and arrow bounds
  QRectF bounds = path_.boundingRect().united(arrow_path_.boundingRect());

  // Add small margin for debug visualization
  return bounds.adjusted(-5, -5, 5, 5);
}

void EdgeItem::paint(QPainter* painter,
                     const QStyleOptionGraphicsItem* option,
                     QWidget* widget) {
  painter->setRenderHint(QPainter::Antialiasing);

  // Get system-appropriate color for edges
  QColor edge_color = get_system_color();

  // Draw main curve
  painter->setPen(QPen(edge_color, 2));
  painter->setBrush(Qt::NoBrush);
  painter->drawPath(path_);

  // Draw arrow head with same color
  painter->setPen(Qt::NoPen);
  painter->setBrush(edge_color);
  painter->drawPath(arrow_path_);

  // Debug visualization
  if (false) {
    painter->setPen(Qt::NoPen);
    for (int i = 0; i < spline_points_.size(); ++i) {
      switch (i % 3) {
        case 0:  // End points
          painter->setBrush(Qt::red);
          painter->drawEllipse(spline_points_[i], 4, 4);
          break;
        case 1:  // First control point
          painter->setBrush(Qt::blue);
          painter->drawEllipse(spline_points_[i], 3, 3);
          break;
        case 2:  // Second control point
          painter->setBrush(Qt::green);
          painter->drawEllipse(spline_points_[i], 3, 3);
          break;
      }
    }

    // Draw node bounding boxes
    painter->setPen(QPen(Qt::red, 1, Qt::DashLine));
    painter->setBrush(Qt::NoBrush);
    QRectF fromRect = from_->boundingRect().translated(from_->pos());
    QRectF toRect = to_->boundingRect().translated(to_->pos());
    painter->drawRect(fromRect);
    painter->drawRect(toRect);
  }
}

Legend::Legend(const std::vector<LegendEntry>& entries, QWidget* parent)
    : QWidget(parent), entries_(entries) {
  setAttribute(Qt::WA_NoSystemBackground);
  setAttribute(Qt::WA_TranslucentBackground);
}

QSize Legend::sizeHint() const {
  qreal width = 0;
  qreal height = PADDING * 2;

  QFont font;
  QFontMetrics fm(font);

  for (const auto& entry : entries_) {
    QString text = node_label_text(entry.shape_type);
    width =
        std::max(width, PADDING * 3 + ICON_SIZE + fm.horizontalAdvance(text));
    height += TEXT_HEIGHT + PADDING;
  }

  return QSize(width, height);
}

QString Legend::node_label_text(const QString& shape_type) const {
  // TODO: APIBridge should supply us with a shape-type map
  return QString("Placeholder for %1").arg(shape_type);
}

QPainterPath Legend::node_label_icon(const QString& hex_color,
                                     const QString& shape_type,
                                     int shape_sides) const {
  QPainterPath path;
  QRectF bounds(0, 0, ICON_SIZE, ICON_SIZE);

  // Simplified version of NodeItem::create_shape_path logic
  if (shape_type == "house") {
    qreal roof_height = ICON_SIZE * 0.4;
    path.moveTo(bounds.left(), bounds.bottom());
    path.lineTo(bounds.left(), bounds.top() + roof_height);
    path.lineTo(bounds.center().x(), bounds.top());
    path.lineTo(bounds.right(), bounds.top() + roof_height);
    path.lineTo(bounds.right(), bounds.bottom());
    path.lineTo(bounds.left(), bounds.bottom());
  } else if (shape_type == "box") {
    path.addRect(bounds);
  } else if (shape_type == "ellipse" || shape_type == "oval") {
    path.addEllipse(bounds);
  } else if (shape_type == "diamond") {
    QPointF points[4] = {QPointF(bounds.left(), bounds.center().y()),
                         QPointF(bounds.center().x(), bounds.top()),
                         QPointF(bounds.right(), bounds.center().y()),
                         QPointF(bounds.center().x(), bounds.bottom())};
    path.moveTo(points[0]);
    for (int i = 1; i < 4; ++i) {
      path.lineTo(points[i]);
    }
    path.closeSubpath();
  } else if (shape_type == "polygon" && shape_sides > 0) {
    // Reuse the same polygon logic as NodeItem
    QPointF center = bounds.center();
    qreal radius = ICON_SIZE / 2;

    for (int i = 0; i < shape_sides; ++i) {
      qreal angle = 2 * M_PI * i / shape_sides - M_PI / 2;
      QPointF point(center.x() + radius * std::cos(angle),
                    center.y() + radius * std::sin(angle));

      if (i == 0) {
        path.moveTo(point);
      } else {
        path.lineTo(point);
      }
    }
    path.closeSubpath();
  }

  return path;
}

void Legend::paintEvent(QPaintEvent* event) {
  QPainter painter(this);
  painter.setRenderHint(QPainter::Antialiasing);

  // Draw background
  painter.setPen(Qt::NoPen);

  auto [brush, pen] = []() {
    QStyleHints* styleHints = QGuiApplication::styleHints();
    switch (styleHints->colorScheme()) {
      case Qt::ColorScheme::Dark: {
        return std::make_tuple(QColor(30, 30, 30, 220), Qt::white);
      }
      case Qt::ColorScheme::Light:
      case Qt::ColorScheme::Unknown:
      default: {
        return std::make_tuple(QColor(255, 255, 255, 200), Qt::black);
      }
    }
  }();
  painter.setBrush(brush);
  painter.drawRect(rect());

  // Draw border
  painter.setPen(QPen(pen, 1));
  painter.setBrush(Qt::NoBrush);
  painter.drawRect(rect());

  qreal y = PADDING;
  for (const auto& entry : entries_) {
    // Draw icon
    QPainterPath icon_path =
        node_label_icon(entry.hex_color, entry.shape_type, entry.shape_sides);

    painter.save();
    painter.translate(PADDING, y);
    painter.setPen(QPen(Qt::black, 1));
    painter.setBrush(QColor(entry.hex_color));
    painter.drawPath(icon_path);
    painter.restore();

    // Draw text
    painter.setPen(pen);
    QString text = node_label_text(entry.shape_type);
    painter.drawText(QPointF(PADDING * 2 + ICON_SIZE, y + TEXT_HEIGHT * 0.75),
                     text);

    y += TEXT_HEIGHT + PADDING;
  }
}
DependencyGraphicsView::DependencyGraphicsView(QWidget* parent)
    : QGraphicsView(parent) {
  setRenderHint(QPainter::Antialiasing);
  setViewportUpdateMode(QGraphicsView::FullViewportUpdate);
  setHorizontalScrollBarPolicy(Qt::ScrollBarAsNeeded);
  setVerticalScrollBarPolicy(Qt::ScrollBarAsNeeded);
  setDragMode(QGraphicsView::RubberBandDrag);
}

void DependencyGraphicsView::wheelEvent(QWheelEvent* event) {
  QPointF scene_pos = mapToScene(event->position().toPoint());
  qreal factor =
      event->angleDelta().y() > 0 ? zoom_factor_ : 1.0 / zoom_factor_;
  scale(factor, factor);
  QPointF delta = mapToScene(event->position().toPoint()) - scene_pos;
  translate(delta.x(), delta.y());
  event->accept();
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
  scene_ = new DependencyScene(this);
  graph_view_->setScene(scene_);
  graph_view_->viewport()->installEventFilter(this);

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

  // TODO: Come up with better way to represent the dep graph legend
  /*
  // Collect unique node types for legend
  std::set<std::tuple<QString, QString, int>> unique_types;
  for (lemon::ListDigraph::NodeIt n(graph); n != lemon::INVALID; ++n) {
    const auto& data = node_data[n];
    unique_types.insert(
        std::make_tuple(data.hex_colour, data.shape_type, data.shape_sides));
  }

  // Create legend entries
  std::vector<Legend::LegendEntry> legend_entries;
  for (const auto& [color, shape, sides] : unique_types) {
    legend_entries.push_back({color, shape, sides});
  }

  // Create and position legend if we have entries
  if (!legend_entries.empty()) {
    delete legend_;  // Delete any existing legend
    legend_ = new Legend(legend_entries, graph_view_->viewport());
    updateLegendPosition();
  }
  */

  scene_->build_graph(graph, node_data);
  graph_view_->fitInView(scene_->itemsBoundingRect(), Qt::KeepAspectRatio);

  stack_->setCurrentWidget(platform_tabs_);
}

void DependencyView::updateLegendPosition() {
  if (legend_ != nullptr) {
    // Position in top-left of viewport with padding
    legend_->move(20, 20);
    legend_->raise();  // Ensure it stays on top
  }
}

DependencyScene::DependencyScene(QObject* parent)
    : QGraphicsScene(parent), gvc_(gvContext()) {
  setItemIndexMethod(QGraphicsScene::NoIndex);
  assert(gvc_ != nullptr);
#ifdef _WIN64
  gvAddLibrary(gvc_, &gvplugin_dot_layout_LTX_library);
#endif
}

DependencyScene::~DependencyScene() {
  if (gvc_ != nullptr) {
    gvFreeContext(gvc_);
  }
}

bool DependencyView::eventFilter(QObject* watched, QEvent* event) {
  if (graph_view_ != nullptr && watched == graph_view_->viewport() &&
      event->type() == QEvent::Resize) {
    updateLegendPosition();
  }
  return QScrollArea::eventFilter(watched, event);
}

void DependencyScene::build_graph(
    const lemon::ListDigraph& graph,
    const lemon::ListDigraph::NodeMap<ObjectNode>& node_data) {
  clear();
  nodes_.clear();
  edges_.clear();

  // TODO: make graph name have the platform as a prefix when we support
  //  showing all platforms
  Agdesc_t dir = {1, 0, 0, 1};
  Agraph_t* g = agopen(const_cast<char*>("dependency_graph"), dir, nullptr);
  agattr(g, AGRAPH, const_cast<char*>("rankdir"), const_cast<char*>("RL"));

  auto graph_guard = scope_guard::make([this, g]() {
    gvFreeLayout(gvc_, g);
    agclose(g);
  });

  std::unordered_map<int, Agnode_t*> gv_nodes;

  // First pass: Create nodes
  for (lemon::ListDigraph::NodeIt n(graph); n != lemon::INVALID; ++n) {
    const auto& data = node_data[n];
    const int node_id = graph.id(n);
    Agnode_t* gv_node =
        agnode(g, const_cast<char*>(data.name.toStdString().c_str()), 1);
    gv_nodes[node_id] = gv_node;

    agsafeset(gv_node, const_cast<char*>("shape"),
              data.shape_type.toStdString().c_str(), "");

    if (data.shape_sides > 0) {
      char sides[8];
      snprintf(sides, sizeof(sides), "%d", data.shape_sides);
      agsafeset(gv_node, const_cast<char*>("sides"), sides, "");
    }

    agsafeset(gv_node, const_cast<char*>("fillcolor"),
              data.hex_colour.toStdString().c_str(), "");
    agsafeset(gv_node, const_cast<char*>("style"), "filled", "");
  }

  // Second pass: Create edges in Graphviz
  for (lemon::ListDigraph::ArcIt a(graph); a != lemon::INVALID; ++a) {
    auto source_id = graph.id(graph.source(a));
    auto target_id = graph.id(graph.target(a));

    agedge(g, gv_nodes[source_id], gv_nodes[target_id], nullptr, 1);
  }

  // Apply dot layout
  gvLayout(gvc_, g, "dot");

  // Create nodes based on Graphviz layout
  for (lemon::ListDigraph::NodeIt n(graph); n != lemon::INVALID; ++n) {
    const auto& data = node_data[n];
    const int node_id = graph.id(n);
    Agnode_t* gv_node = gv_nodes[node_id];

    const double x = ND_coord(gv_node).x;
    const double y = ND_coord(gv_node).y;

    auto node = new NodeItem(data.name, data.shape_type, data.shape_sides,
                             data.hex_colour);

    // Convert from Graphviz coordinates to Qt coordinates
    // Note: Graphviz uses points (72 points = 1 inch), and y grows downward
    node->setPos(x * 1.5,
                 -y * 1.5);  // Scale factor of 1.5 to match Graphviz spacing

    addItem(node);
    nodes_[node_id] = node;
  }

  for (lemon::ListDigraph::ArcIt a(graph); a != lemon::INVALID; ++a) {
    auto source_id = graph.id(graph.source(a));
    auto target_id = graph.id(graph.target(a));

    // Get Graphviz edge
    Agedge_t* gv_edge = agfindedge(g, gv_nodes[source_id], gv_nodes[target_id]);
    if (!gv_edge)
      continue;

    // Extract spline points
    QVector<QPointF> spline_points;

    // Inside the edge creation loop
    if (ED_spl(gv_edge) && ED_spl(gv_edge)->list) {
      const bezier* bez = &(ED_spl(gv_edge)->list[0]);

      // Get our actual Qt nodes
      NodeItem* source_node = nodes_[source_id];
      NodeItem* target_node = nodes_[target_id];

      // Get Qt node positions and bounds
      QPointF source_pos = source_node->pos();
      QPointF target_pos = target_node->pos();
      QRectF source_bounds = source_node->boundingRect();
      QRectF target_bounds = target_node->boundingRect();

      spline_points.reserve(bez->size);

      // Convert spline points to Qt space
      for (int i = 0; i < bez->size; i++) {
        pointf pt = bez->list[i];
        QPointF converted_pt(pt.x * 1.5, -pt.y * 1.5);

        // Adjust endpoints to match our actual node boundaries
        if (i == 0) {
          // Start at source node's left edge
          converted_pt.setX(source_pos.x() - source_bounds.width() / 2);
        } else if (i == bez->size - 1) {
          // End at target node's right edge
          converted_pt.setX(target_pos.x() + target_bounds.width() / 2);
        }

        spline_points.append(converted_pt);
      }

      // Create edge with the adjusted points
      auto edge = new EdgeItem(source_node, target_node, spline_points);
      addItem(edge);
      edges_.push_back(edge);
    } else {
      // Fallback case - still use the same scaling as nodes
      Agnode_t* source = gv_nodes[source_id];
      Agnode_t* target = gv_nodes[target_id];
      spline_points.append(
          QPointF(ND_coord(source).x * 1.5, -ND_coord(source).y * 1.5));
      spline_points.append(
          QPointF(ND_coord(target).x * 1.5, -ND_coord(target).y * 1.5));
    }

    // Create edge with the exact graphviz spline points
    auto edge =
        new EdgeItem(nodes_[source_id], nodes_[target_id], spline_points);
    addItem(edge);
    edges_.push_back(edge);
  }
}

}  // namespace iprm::views
