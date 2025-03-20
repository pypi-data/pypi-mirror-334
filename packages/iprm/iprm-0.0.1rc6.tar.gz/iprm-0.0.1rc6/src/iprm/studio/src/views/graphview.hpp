/*
 * Copyright (c) 2025 ayeteadoe <ayeteadoe@gmail.com>
 *
 * SPDX-License-Identifier: MIT
 */
#pragma once

#include <QGraphicsItem>
#include <QGraphicsScene>
#include <QPainterPath>
#include <QStyleOptionGraphicsItem>
#include <QWidget>
#include <memory>
#include <string>
#include <vector>
#include "graphviz.hpp"

class QPainter;

class LayoutNode : public QGraphicsItem {
 public:
  LayoutNode(const NodeItem& node, QGraphicsItem* parent = nullptr);

  QPainterPath node_path() const;

  QPointF calculate_shape_intersection(qreal nx, qreal ny) const;

  QRectF boundingRect() const override;

  void paint(QPainter* painter,
             const QStyleOptionGraphicsItem* option,
             QWidget* widget) override;

  qreal x() const { return x_; }
  qreal y() const { return y_; }
  qreal width() const { return width_; }
  qreal height() const { return height_; }
  int id() const { return m_id; }
  std::string name() const { return name_; }
  std::string shape_type() const { return shape_type_; }

 private:
  int m_id;
  std::string name_;
  std::string shape_type_;
  int num_shape_sides_;
  std::string hex_colour_;
  qreal x_;
  qreal y_;
  qreal width_;
  qreal height_;
};

class LayoutEdge : public QGraphicsItem {
 public:
  LayoutEdge(const EdgeItem& edge,
             const std::vector<LayoutNode*>& nodes,
             QGraphicsItem* parent = nullptr);

  QRectF boundingRect() const override;

  void paint(QPainter* painter,
             const QStyleOptionGraphicsItem* option,
             QWidget* widget) override;

  QPointF calculate_shape_intersection(LayoutNode* node,
                                       const QPointF& direction) const;

 private:
  void draw_arrow_head(QPainter* painter,
                       const QPointF& tip,
                       const QPointF& control);
  int source_id_;
  int target_id_;
  LayoutNode* source_node_;
  LayoutNode* target_node_;
  std::vector<QPointF> original_points_;
};

class GraphView {
 public:
  GraphView(QGraphicsScene* scene);

  void create(const LayoutResult& result);

  void clear();

 private:
  QGraphicsScene* scene_;
  std::vector<LayoutNode*> nodes_;
  std::vector<LayoutEdge*> edges_;
};
