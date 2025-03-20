/*
 * Copyright (c) 2025 ayeteadoe <ayeteadoe@gmail.com>
 *
 * SPDX-License-Identifier: MIT
 */
#include "graphview.hpp"

#include <QApplication>
#include <QPainter>
#include <QStyleHints>

static QPainterPath create_ellipse(qreal width, qreal height);

static QColor hex_to_colour(const QString& hex);

static QColor system_colour();

LayoutNode::LayoutNode(const NodeItem& node, QGraphicsItem* parent)
    : QGraphicsItem(parent),
      m_id(node.id),
      name_(node.name),
      shape_type_(node.shape_type),
      num_shape_sides_(node.shape_sides),
      hex_colour_(node.hex_colour),
      x_(node.x),
      y_(node.y),
      width_(node.width),
      height_(node.height) {
  setPos(x_, y_);

  setAcceptHoverEvents(true);
}

QPainterPath LayoutNode::node_path() const {
  QPainterPath path;

  if (shape_type_ == "circle") {
    qreal radius = qMin(width_, height_) / 2.0;
    path.addEllipse(-radius, -radius, radius * 2, radius * 2);
  } else if (shape_type_ == "ellipse") {
    path = create_ellipse(width_, height_);
  } else if (shape_type_ == "diamond") {
    path.moveTo(-width_ / 2.0, 0);
    path.lineTo(0, -height_ / 2.0);
    path.lineTo(width_ / 2.0, 0);
    path.lineTo(0, height_ / 2.0);
    path.closeSubpath();
  } else if (shape_type_ == "box" || shape_type_ == "rect" ||
             shape_type_ == "rectangle") {
    path.addRect(-width_ / 2.0, -height_ / 2.0, width_, height_);
  } else if (shape_type_ == "polygon" && num_shape_sides_ == 6) {
    qreal halfWidth = width_ / 2.0;
    qreal thirdHeight = height_ / 3.0;

    path.moveTo(-halfWidth, 0);
    path.lineTo(-halfWidth / 2.0, -thirdHeight);
    path.lineTo(halfWidth / 2.0, -thirdHeight);
    path.lineTo(halfWidth, 0);
    path.lineTo(halfWidth / 2.0, thirdHeight);
    path.lineTo(-halfWidth / 2.0, thirdHeight);
    path.closeSubpath();
  } else if (shape_type_ == "polygon" && num_shape_sides_ > 0) {
    qreal radius = qMin(width_, height_) / 2.0;

    for (int i = 0; i < num_shape_sides_; ++i) {
      qreal angle = 2.0 * M_PI * i / num_shape_sides_ - M_PI / 2.0;
      qreal pointX = radius * qCos(angle);
      qreal pointY = radius * qSin(angle);

      if (i == 0) {
        path.moveTo(pointX, pointY);
      } else {
        path.lineTo(pointX, pointY);
      }
    }
    path.closeSubpath();
  } else if (shape_type_ == "house") {
    qreal roofHeight = height_ * 0.4;

    path.moveTo(-width_ / 2.0, height_ / 2.0);                // Bottom left
    path.lineTo(-width_ / 2.0, -height_ / 2.0 + roofHeight);  // Left wall
    path.lineTo(0, -height_ / 2.0);                           // Left roof slope
    path.lineTo(width_ / 2.0,
                -height_ / 2.0 + roofHeight);  // Right roof slope
    path.lineTo(width_ / 2.0, height_ / 2.0);  // Right wall
    path.closeSubpath();
  } else {
    // Default to circle for unknown shapes
    qreal radius = qMin(width_, height_) / 2.0;
    path.addEllipse(-radius, -radius, radius * 2, radius * 2);
  }

  return path;
}

QPointF LayoutNode::calculate_shape_intersection(qreal nx, qreal ny) const {
  QPointF center(0, 0);  // In local coordinates, center is at 0,0

  if (shape_type_ == "circle") {
    qreal radius = qMin(width_, height_) / 2.0;
    return center - QPointF(nx * radius, ny * radius);
  } else if (shape_type_ == "ellipse") {
    qreal a = width_ / 2.0;   // semi-major axis (horizontal)
    qreal b = height_ / 2.0;  // semi-minor axis (vertical)

    qreal denominator = (nx * nx) / (a * a) + (ny * ny) / (b * b);
    if (qAbs(denominator) < 0.00001) {
      return center;
    }

    qreal t = 1.0 / qSqrt(denominator);
    return center - QPointF(nx * t, ny * t);
  } else if (shape_type_ == "diamond") {
    qreal halfWidth = width_ / 2.0;
    qreal halfHeight = height_ / 2.0;

    qreal absNx = qAbs(nx);
    qreal absNy = qAbs(ny);

    qreal t = 0.0;
    if (absNx > 0.0 || absNy > 0.0) {
      t = (halfWidth * halfHeight) / (halfHeight * absNx + halfWidth * absNy);
    }

    return center - QPointF(nx * t, ny * t);
  } else if (shape_type_ == "box" || shape_type_ == "rect" ||
             shape_type_ == "rectangle") {
    qreal halfWidth = width_ / 2.0;
    qreal halfHeight = height_ / 2.0;

    qreal tHorizontal = qAbs(nx) > 0.001 ? halfWidth / qAbs(nx)
                                         : std::numeric_limits<qreal>::max();
    qreal tVertical = qAbs(ny) > 0.001 ? halfHeight / qAbs(ny)
                                       : std::numeric_limits<qreal>::max();

    qreal t = qMin(tHorizontal, tVertical);
    return center - QPointF(nx * t, ny * t);
  } else if (shape_type_ == "polygon" && num_shape_sides_ == 6) {
    qreal halfWidth = width_ / 2.0;
    qreal thirdHeight = height_ / 3.0;

    qreal angle = qAtan2(ny, nx);
    qreal angleAbs = qAbs(angle);

    qreal radius;
    if (angleAbs < M_PI / 6.0 || angleAbs > M_PI * 5.0 / 6.0) {
      radius = halfWidth;
    } else {
      qreal t;
      if (angleAbs < M_PI / 2.0) {
        t = (thirdHeight + halfWidth * 0.5) / qSin(M_PI / 3.0);
      } else {
        t = (thirdHeight + halfWidth * 0.5) / qSin(M_PI / 3.0);
      }
      radius = t * 0.8;
    }

    return center - QPointF(nx * radius, ny * radius);
  } else if (shape_type_ == "polygon" && num_shape_sides_ > 0) {
    qreal radius = qMin(width_, height_) / 2.0;
    qreal sides = static_cast<qreal>(num_shape_sides_);

    qreal angle = qAtan2(ny, nx);
    qreal sectorAngle = 2.0 * M_PI / sides;
    qreal normalizedAngle =
        fmod(angle + M_PI + sectorAngle / 2.0, sectorAngle) - sectorAngle / 2.0;

    qreal effectiveRadius = radius * qAbs(1.0 / qCos(normalizedAngle)) * 0.9;

    return center - QPointF(nx * effectiveRadius, ny * effectiveRadius);
  } else if (shape_type_ == "house") {
    qreal halfWidth = width_ / 2.0;
    qreal halfHeight = height_ / 2.0;
    qreal roofHeight = height_ * 0.4;

    qreal t;
    if (ny < 0.0 && qAbs(ny) > qAbs(nx)) {
      qreal roofAngle = halfWidth / roofHeight;
      if (qAbs(nx) < roofAngle * qAbs(ny)) {
        t = halfHeight / qAbs(ny);
      } else {
        t = halfWidth / qAbs(nx);
      }
    } else {
      qreal tHorizontal = qAbs(nx) > 0.001 ? halfWidth / qAbs(nx)
                                           : std::numeric_limits<qreal>::max();
      qreal tVertical = qAbs(ny) > 0.001 ? halfHeight / qAbs(ny)
                                         : std::numeric_limits<qreal>::max();
      t = qMin(tHorizontal, tVertical);
    }

    return center - QPointF(nx * t, ny * t);
  } else {
    // Default to circle
    qreal radius = qMin(width_, height_) / 2.0;
    return center - QPointF(nx * radius, ny * radius);
  }
}

QRectF LayoutNode::boundingRect() const {
  return QRectF(-width_ / 2 - 2, -height_ / 2 - 2, width_ + 4, height_ + 4);
}

void LayoutNode::paint(QPainter* painter,
                       const QStyleOptionGraphicsItem* option,
                       QWidget* widget) {
  Q_UNUSED(option);
  Q_UNUSED(widget);

  QPainterPath path = node_path();

  const QColor nodeColor =
      hex_to_colour(QString::fromUtf8(hex_colour_.c_str()));
  painter->fillPath(path, nodeColor);

  const QString label = QString::fromUtf8(name_.c_str());

  painter->setPen(system_colour());
  painter->setFont(QFont("Arial", 10));

  QRectF textRect = boundingRect();
  painter->drawText(textRect, Qt::AlignCenter, label);
}

LayoutEdge::LayoutEdge(const EdgeItem& edge,
                       const std::vector<LayoutNode*>& nodes,
                       QGraphicsItem* parent)
    : QGraphicsItem(parent),
      source_id_(edge.source_id),
      target_id_(edge.target_id) {
  source_node_ = nullptr;
  target_node_ = nullptr;

  for (LayoutNode* node : nodes) {
    if (node->id() == source_id_) {
      source_node_ = node;
    }
    if (node->id() == target_id_) {
      target_node_ = node;
    }
  }

  if (!source_node_ || !target_node_) {
    qWarning() << "Edge created with invalid source or target node IDs";
    return;
  }

  for (const auto& spline : edge.splines) {
    original_points_.push_back(QPointF(spline.x, spline.y));
  }

  // Set item position to (0,0) since we're working in scene coordinates
  setPos(0, 0);
}

QRectF LayoutEdge::boundingRect() const {
  if (original_points_.empty()) {
    return QRectF();
  }

  qreal minX = original_points_[0].x();
  qreal minY = original_points_[0].y();
  qreal maxX = original_points_[0].x();
  qreal maxY = original_points_[0].y();

  for (const QPointF& p : original_points_) {
    minX = qMin(minX, p.x());
    minY = qMin(minY, p.y());
    maxX = qMax(maxX, p.x());
    maxY = qMax(maxY, p.y());
  }

  // Add margin for arrow head and stroke width
  return QRectF(minX - 15, minY - 15, maxX - minX + 30, maxY - minY + 30);
}
void LayoutEdge::paint(QPainter* painter,
                       const QStyleOptionGraphicsItem* option,
                       QWidget* widget) {
  Q_UNUSED(option);
  Q_UNUSED(widget);

  if (original_points_.size() < 2 || !source_node_ || !target_node_) {
    return;
  }

  QVector<QPointF> adjustedPoints;
  for (const QPointF& p : original_points_) {
    adjustedPoints.append(p);
  }

  QPointF sourcePos = source_node_->pos();
  QPointF targetPos = target_node_->pos();

  // Direction vector from source to target (for the edge)
  QPointF sourceToTarget = targetPos - sourcePos;
  qreal distanceBetweenNodes =
      qSqrt(QPointF::dotProduct(sourceToTarget, sourceToTarget));

  if (distanceBetweenNodes > 0.001) {
    QPointF dirNormalized = sourceToTarget / distanceBetweenNodes;

    // For source node, we need direction pointing OUT from source towards
    // target
    QPointF sourceIntersection =
        calculate_shape_intersection(source_node_, dirNormalized);

    // For target node, we need direction pointing IN from source towards
    // target
    QPointF targetIntersection =
        calculate_shape_intersection(target_node_, -dirNormalized);

    // Now adjust the first and last points to these intersections
    adjustedPoints[0] = sourceIntersection;
    adjustedPoints[adjustedPoints.size() - 1] = targetIntersection;
  }

  // Draw the arrow head first so we can calculate where to end the line
  QPointF tip = adjustedPoints.back();
  QPointF preTip = adjustedPoints[adjustedPoints.size() - 2];

  // Calculate the base point of the arrow (where the line should end)
  qreal dx = tip.x() - preTip.x();
  qreal dy = tip.y() - preTip.y();
  qreal length = qSqrt(dx * dx + dy * dy);

  QPointF arrowBasePoint;

  if (length > 0.001) {
    qreal nx = dx / length;
    qreal ny = dy / length;

    // Set the new end point for the line to be at the base of the arrow head
    // Arrow length is 10.0 as defined in drawArrowHead
    qreal arrowLength = 10.0;
    arrowBasePoint = tip - QPointF(nx * arrowLength, ny * arrowLength);

    // Replace the last point with this base point
    adjustedPoints[adjustedPoints.size() - 1] = arrowBasePoint;
  }

  // Draw the edge with a slightly thinner stroke to avoid visual artifacts
  QPen edgePen(system_colour(), 1.5, Qt::SolidLine, Qt::RoundCap);
  painter->setPen(edgePen);

  QPainterPath path;
  path.moveTo(adjustedPoints[0]);

  for (int i = 1; i < adjustedPoints.size(); ++i) {
    path.lineTo(adjustedPoints[i]);
  }

  painter->drawPath(path);
  draw_arrow_head(painter, tip, preTip);
}

QPointF LayoutEdge::calculate_shape_intersection(
    LayoutNode* node,
    const QPointF& direction) const {
  QPointF nodePos = node->pos();

  // The node's intersection calculation expects direction FROM the center
  // So we need to invert the direction for the calculation
  QPointF nodeLocalDir = QPointF(-direction.x(), -direction.y());

  // Calculate in local coordinates
  QPointF localIntersection =
      node->calculate_shape_intersection(nodeLocalDir.x(), nodeLocalDir.y());

  // Transform back to scene coordinates
  return localIntersection + nodePos;
}

void LayoutEdge::draw_arrow_head(QPainter* painter,
                                 const QPointF& tip,
                                 const QPointF& control) {
  qreal dx = tip.x() - control.x();
  qreal dy = tip.y() - control.y();

  qreal length = qSqrt(dx * dx + dy * dy);
  qreal nx, ny;

  if (length > 0.001) {
    nx = dx / length;
    ny = dy / length;
  } else {
    // Default direction if vectors are too close
    nx = 0.0;
    ny = -1.0;
  }

  qreal arrowLength = 10.0;
  qreal arrowWidth = 6.0;

  qreal baseX = tip.x() - nx * arrowLength;
  qreal baseY = tip.y() - ny * arrowLength;

  qreal perpX = -ny;
  qreal perpY = nx;

  qreal leftX = baseX + perpX * arrowWidth / 2.0;
  qreal leftY = baseY + perpY * arrowWidth / 2.0;

  qreal rightX = baseX - perpX * arrowWidth / 2.0;
  qreal rightY = baseY - perpY * arrowWidth / 2.0;

  QPolygonF arrowHead;
  arrowHead << tip << QPointF(leftX, leftY) << QPointF(rightX, rightY);

  painter->setBrush(system_colour());
  painter->setPen(Qt::NoPen);
  painter->drawPolygon(arrowHead);
}

GraphView::GraphView(QGraphicsScene* scene) : scene_(scene) {}

void GraphView::create(const LayoutResult& result) {
  clear();

  for (const auto& layout_node : result.nodes) {
    auto node = new LayoutNode(layout_node);
    nodes_.push_back(node);
    scene_->addItem(node);
  }

  for (const auto& layout_edge : result.edges) {
    auto edge = new LayoutEdge(layout_edge, nodes_);
    edges_.push_back(edge);
    scene_->addItem(edge);

    edge->setZValue(-1);
  }
}

void GraphView::clear() {
  for (auto node : nodes_) {
    scene_->removeItem(node);
    delete node;
  }
  nodes_.clear();

  for (auto edge : edges_) {
    scene_->removeItem(edge);
    delete edge;
  }
  edges_.clear();
}

QPainterPath create_ellipse(qreal width, qreal height) {
  QPainterPath path;

  qreal rx = width / 2.0;
  qreal ry = height / 2.0;

  // Magic constant for a close approximation of an ellipse using Bezier
  // curves
  qreal c = 0.551915024494;

  // Top point
  path.moveTo(0, -ry);

  // Right curve
  path.cubicTo(c * rx, -ry, rx, -c * ry, rx, 0);

  // Bottom curve
  path.cubicTo(rx, c * ry, c * rx, ry, 0, ry);

  // Left curve
  path.cubicTo(-c * rx, ry, -rx, c * ry, -rx, 0);

  // Top curve
  path.cubicTo(-rx, -c * ry, -c * rx, -ry, 0, -ry);

  return path;
}

inline QColor hex_to_colour(const QString& hex) {
  QString cleanHex = hex;
  if (cleanHex.startsWith('#')) {
    cleanHex = cleanHex.mid(1);
  }

  if (cleanHex.length() != 6) {
    return QColor(Qt::gray);  // Default color on error
  }

  bool ok;
  int r = cleanHex.mid(0, 2).toInt(&ok, 16);
  if (!ok)
    return QColor(Qt::gray);

  int g = cleanHex.mid(2, 2).toInt(&ok, 16);
  if (!ok)
    return QColor(Qt::gray);

  int b = cleanHex.mid(4, 2).toInt(&ok, 16);
  if (!ok)
    return QColor(Qt::gray);

  return QColor(r, g, b);
}

QColor system_colour() {
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
