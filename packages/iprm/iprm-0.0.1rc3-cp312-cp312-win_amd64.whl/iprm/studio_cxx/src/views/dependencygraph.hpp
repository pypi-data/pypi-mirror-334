#pragma once

#include <lemon/list_graph.h>
#include <QGraphicsItem>
#include <QGraphicsView>
#include <QPainterPath>
#include <QPointF>
#include <QScrollArea>
#include <QStackedWidget>
#include <QString>
#include <QWheelEvent>
#include <QTabWidget>
#include <queue>
#include <set>
#include <unordered_map>
#include <vector>
#include "../apibridge.hpp"
#include <graphviz/gvc.h>


namespace iprm::views {

class LoadingWidget;

class Legend;
class DependencyScene;
class NodeItem;
class EdgeItem;

class DependencyGraphicsView : public QGraphicsView {
  Q_OBJECT
 public:
  explicit DependencyGraphicsView(QWidget* parent = nullptr);

 protected:
  void wheelEvent(QWheelEvent* event) override;
  void mousePressEvent(QMouseEvent* event) override;
  void mouseReleaseEvent(QMouseEvent* event) override;
  void mouseMoveEvent(QMouseEvent* event) override;

 private:
  bool panning_{false};
  QPoint last_mouse_pos_;
  const qreal zoom_factor_{1.15};
};

class DependencyView : public QScrollArea {
  Q_OBJECT
 public:
  explicit DependencyView(QWidget* parent = nullptr);

  void build_graph(const lemon::ListDigraph& graph,
                   const lemon::ListDigraph::NodeMap<ObjectNode>& node_data);

 protected:
  bool eventFilter(QObject* watched, QEvent* event) override;

 private:
  void updateLegendPosition();

  QStackedWidget* stack_{nullptr};
  LoadingWidget* loading_page_{nullptr};
  DependencyGraphicsView* graph_view_{nullptr};
  DependencyScene* scene_{nullptr};
  Legend* legend_{nullptr};
  // TODO: Actually support all platforms, will need a legend for each graphics view
  QTabWidget* platform_tabs_{nullptr};;
};

class DependencyScene : public QGraphicsScene {
  Q_OBJECT
 public:
  explicit DependencyScene(QObject* parent = nullptr);
  ~DependencyScene();

  void build_graph(const lemon::ListDigraph& graph,
                   const lemon::ListDigraph::NodeMap<ObjectNode>& node_data);

 private:
  std::unordered_map<int, NodeItem*> nodes_;  // node_id -> item
  std::vector<EdgeItem*> edges_;

  GVC_t* gvc_{nullptr};
};

class NodeItem : public QGraphicsItem {
 public:
  NodeItem(const QString& name,
           const QString& shape_type,
           int shape_sides,
           const QString& hex_color);

  QRectF boundingRect() const override;
  void paint(QPainter* painter,
             const QStyleOptionGraphicsItem* option,
             QWidget* widget = nullptr) override;

  QString name() const { return name_; }

 private:
  QColor get_system_color() const;

  void create_shape_path();

  QString name_;
  QString shape_type_;
  int shape_sides_;
  QColor color_;
  QPainterPath shape_path_;
  QGraphicsTextItem* label_;
};

class EdgeItem : public QGraphicsItem {
 public:
  EdgeItem(NodeItem* from, NodeItem* to, const QVector<QPointF>& spline_points);

  QRectF boundingRect() const override;
  void paint(QPainter* painter,
             const QStyleOptionGraphicsItem* option,
             QWidget* widget = nullptr) override;

  NodeItem* from() const { return from_; }
  NodeItem* to() const { return to_; }

 private:
  NodeItem* from_;
  NodeItem* to_;
  QVector<QPointF> spline_points_;
  QPainterPath path_;
  QPainterPath arrow_path_;

  // Arrow dimensions - adjust if needed
  static constexpr qreal ARROW_LENGTH = 10.0;
  static constexpr qreal ARROW_WIDTH = 6.0;

  void update_path();
  QPainterPath create_arrow_head(const QPointF& tip, const QPointF& direction) const;
  QColor get_system_color() const;
};

class Legend : public QWidget {
  Q_OBJECT
 public:
  struct LegendEntry {
    QString hex_color;
    QString shape_type;
    int shape_sides;
  };

  explicit Legend(const std::vector<LegendEntry>& entries, QWidget* parent = nullptr);

  QSize sizeHint() const override;

 protected:
  void paintEvent(QPaintEvent* event) override;

 private:
  QPainterPath node_label_icon(const QString& hex_color,
                               const QString& shape_type,
                               int shape_sides) const;
  QString node_label_text(const QString& shape_type) const;

  std::vector<LegendEntry> entries_;
  const qreal ICON_SIZE = 20;
  const qreal PADDING = 10;
  const qreal TEXT_HEIGHT = 20;
};

}  // namespace iprm::views
