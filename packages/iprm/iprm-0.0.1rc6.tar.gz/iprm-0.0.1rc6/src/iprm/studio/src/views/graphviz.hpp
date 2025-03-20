/*
 * Copyright (c) 2025 ayeteadoe <ayeteadoe@gmail.com>
 *
 * SPDX-License-Identifier: MIT
 */
#pragma once

#include <graphviz/cgraph.h>
#include <graphviz/gvc.h>

#include <string>
#include <vector>

// TODO: Originally made this for Rust FFI Interop so it needed a C API, expose
//  a C++ wrapper around it now and move it into src/graphviz, with the
//  namespacec iprm::graphviz:: ,as this is a wrapper library that in theory
//  could be separated out from IPRM as a standalone thing

// TODO: Use the API at https://www.graphviz.org/pdf/cgraph.3.pdf (or tutorial
//  at https://graphviz.org/pdf/cgraph.pdf) for nodes to provide extra metadata
//  to the user (e.g. number of dependencies) as well as general graph wide
//  stats (e.g. number of nodes, number of total dependencies, longest
//  dependency chain, etc)

struct NodeItem {
  int id;
  std::string name;
  std::string shape_type;
  int shape_sides;
  std::string hex_colour;
  double x;
  double y;
  double width;
  double height;
};

struct Point {
  double x;
  double y;
};

struct EdgeItem {
  int source_id;
  int target_id;
  std::vector<Point> splines;
};

struct LayoutResult {
  std::vector<NodeItem> nodes;
  std::vector<EdgeItem> edges;
};

// TODO: Prevent callers from need to invoke new/delete in the C++ wrapper
/*
GVG_t* init_graphviz();
void cleanup_graphviz(GVG_t* context);
*/

// TODO: Wrap all these types in a C++ abstraction
Agraph_t* create_graph(const char* name);
void free_graph(GVG_t* ctx, Agraph_t* g);
Agnode_t* add_node(Agraph_t* g,
                   int node_id,
                   const char* name,
                   const char* shape_type,
                   int shape_sides,
                   const char* hex_colour);
Agedge_t* add_edge(Agraph_t* g, Agnode_t* src, Agnode_t* tgt);
int apply_layout(GVC_t* ctx, Agraph_t* g, const char* layout_engine);
LayoutResult get_layout_result(Agraph_t* g);
