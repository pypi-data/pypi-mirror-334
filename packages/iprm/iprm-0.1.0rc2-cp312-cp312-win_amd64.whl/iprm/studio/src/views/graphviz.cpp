/*
 * Copyright (c) 2025 ayeteadoe <ayeteadoe@gmail.com>
 *
 * SPDX-License-Identifier: MIT
 */
#include "graphviz.hpp"
#include <graphviz/cgraph.h>
#include <graphviz/gvc.h>
#include <chrono>
#include <cmath>
#include <random>
#include <string>
#include <unordered_map>

/*
GVC_t* init_graphviz() {
  return gvContext();
}

void cleanup_graphviz(void* context) {
  if (context) {
    gvFreeContext(static_cast<GVC_t*>(context));
  }
}
*/

Agraph_t* create_graph(const char* name) {
  Agdesc_t dir = {1, 0, 0, 1};
  Agraph_t* g = agopen(strdup(name), dir, nullptr);

  char* rankdir_key = strdup("rankdir");
  char* rankdir_val = strdup("RL");
  agattr(g, AGRAPH, rankdir_key, rankdir_val);

  auto g_name = agnameof(g);

  return g;
}

void free_graph(GVC_t* ctx, Agraph_t* g) {
  gvFreeLayout(ctx, g);
  agclose(g);
}

Agnode_t* add_node(Agraph_t* g,
                   int node_id,
                   const char* name,
                   const char* shape_type,
                   int shape_sides,
                   const char* hex_colour) {
  if (!g)
    return nullptr;

  auto g_name = agnameof(g);

  Agnode_t* node = agnode(g, const_cast<char*>(name), 1);

  agsafeset(node, const_cast<char*>("shape"), shape_type,
            const_cast<char*>(""));

  if (shape_sides > 0) {
    char sides[8];
    snprintf(sides, sizeof(sides), "%d", shape_sides);
    agsafeset(node, const_cast<char*>("sides"), sides, const_cast<char*>(""));
  }

  agsafeset(node, const_cast<char*>("fillcolor"), const_cast<char*>(hex_colour),
            const_cast<char*>(""));
  agsafeset(node, const_cast<char*>("style"), const_cast<char*>("filled"),
            const_cast<char*>(""));

  char id_str[16];
  snprintf(id_str, sizeof(id_str), "%d", node_id);
  agsafeset(node, const_cast<char*>("id"), id_str, const_cast<char*>(""));

  return node;
}

Agedge_t* add_edge(Agraph_t* g, Agnode_t* src, Agnode_t* tgt) {
  return agedge(g, src, tgt, nullptr, 1);
}

int apply_layout(GVC_t* ctx, Agraph_t* g, const char* layout_engine) {
  return gvLayout(ctx, g, const_cast<char*>(layout_engine));
}

int get_node_id(Agnode_t* node) {
  char* id_str = agget(node, const_cast<char*>("id"));
  if (id_str) {
    return std::stoi(id_str);
  }
  return -1;
}

LayoutResult get_layout_result(Agraph_t* g) {
  int node_count = 0;
  for (Agnode_t* n = agfstnode(g); n; n = agnxtnode(g, n)) {
    node_count++;
  }

  int edge_count = 0;
  for (Agnode_t* n = agfstnode(g); n; n = agnxtnode(g, n)) {
    for (Agedge_t* e = agfstout(g, n); e; e = agnxtout(g, e)) {
      edge_count++;
    }
  }

  std::vector<NodeItem> nodes;
  nodes.reserve(node_count);
  std::vector<EdgeItem> edges;
  edges.reserve(edge_count);

  std::unordered_map<Agnode_t*, int> node_indices;

  int node_index = 0;
  for (Agnode_t* n = agfstnode(g); n; n = agnxtnode(g, n)) {
#ifdef _WIN64
#define STRDUP _strdup
#else
#define STRDUP strdup
#endif
    NodeItem item;
    item.id = get_node_id(n);
    item.name = STRDUP(agnameof(n));
    item.shape_type = STRDUP(agget(n, const_cast<char*>("shape")));

    char* sides_str = agget(n, const_cast<char*>("sides"));
    item.shape_sides = sides_str ? std::stoi(sides_str) : 0;

    item.hex_colour = STRDUP(agget(n, const_cast<char*>("fillcolor")));

    item.x = ND_coord(n).x;
    item.y = ND_coord(n).y;
    // Convert from inches to points
    item.width = ND_width(n) * 72;
    item.height = ND_height(n) * 72;

    node_indices[n] = node_index;

    node_index++;
    nodes.push_back(item);
  }

  int edge_index = 0;
  for (Agnode_t* n = agfstnode(g); n; n = agnxtnode(g, n)) {
    for (Agedge_t* e = agfstout(g, n); e; e = agnxtout(g, e)) {
      EdgeItem item;
      item.source_id = node_indices[agtail(e)];
      item.target_id = node_indices[aghead(e)];

      if (ED_spl(e) && ED_spl(e)->list) {
        const bezier* bez = &(ED_spl(e)->list[0]);
        for (int i = 0; i < bez->size; i++) {
          pointf pt = bez->list[i];
          item.splines.emplace_back(pt.x, pt.y);
        }
      } else {
        item.splines.reserve(2);
        Agnode_t* src = agtail(e);
        Agnode_t* tgt = aghead(e);
        item.splines.emplace_back(ND_coord(src).x, -ND_coord(src).y);
        item.splines.emplace_back(ND_coord(tgt).x, -ND_coord(tgt).y);
      }

      edge_index++;
      edges.push_back(item);
    }
  }

  return LayoutResult{nodes, edges};
}
