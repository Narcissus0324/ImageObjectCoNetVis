import json
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
import os


def draw_graph(g: nx.Graph, title="Graph", draw_node_label=True, circular=False, filename=None):
    # 获取边的权重
    weights = nx.get_edge_attributes(g, 'weight').values()
    max_weight = max(weights)
    min_weight = min(weights)

    # 计算边颜色，使用一个标准化的色谱（比如从黄色到红色）
    cmap = plt.get_cmap('YlOrRd')  # 黄色到红色的色谱
    norm = mcolors.Normalize(vmin=min_weight, vmax=max_weight)
    edge_colors = [cmap(norm(weight)) for weight in weights]

    # 获取节点的位置
    if not circular:
        pos = nx.kamada_kawai_layout(g)
    else:
        pos = nx.circular_layout(g)

    # 创建绘图
    fig, ax = plt.subplots(figsize=(12, 8))

    # 绘制节点
    nx.draw_networkx_nodes(g, pos, node_size=50, node_color='skyblue', ax=ax)

    # 绘制带有颜色的边
    nx.draw_networkx_edges(g, pos, edge_color=edge_colors, width=1, ax=ax)

    # 绘制节点标签
    if draw_node_label:
        nx.draw_networkx_labels(g, pos, font_size=12, font_color='black', ax=ax)

    # 绘制边的权重标签
    # edge_labels = nx.get_edge_attributes(G, 'weight')
    # nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=ax)

    # 添加图例和标题
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])  # 只需要颜色条，因此传递一个空数组
    cbar = plt.colorbar(sm, ax=ax)
    cbar.set_label('Edge Weight')

    plt.title(title)

    # 根据是否提供filename来决定是保存图像还是显示
    if filename:
        plt.savefig(filename, format='png')  # 保存为PNG格式
        plt.close(fig)  # 关闭图形以节省内存
    else:
        plt.show()  # 显示图形

def draw_graphs_combined(g, thresholds, titles, filename):
    fig, axes = plt.subplots(1, len(thresholds), figsize=(len(thresholds)*6, 6))
    for ax, graph, title in zip(axes, g, titles):
        weights = nx.get_edge_attributes(graph, 'weight').values()
        cmap = plt.get_cmap('YlOrRd')
        norm = plt.Normalize(vmin=min(weights), vmax=max(weights))
        edge_colors = [cmap(norm(weight)) for weight in weights]

        pos = nx.kamada_kawai_layout(graph)
        nx.draw_networkx_nodes(graph, pos, node_size=50, node_color='skyblue', ax=ax)
        nx.draw_networkx_edges(graph, pos, edge_color=edge_colors, width=1, ax=ax)
        ax.set_title(title)

    plt.tight_layout()
    os.makedirs(os.path.dirname(filename), exist_ok=True)  # 确保目录存在
    plt.savefig(filename, format='png')
    plt.close(fig)

def draw_node_graphs_combined(g, maxns, titles, filename):
    fig, axes = plt.subplots(1, len(maxns), figsize=(len(maxns)*6, 6))
    for ax, graph, title in zip(axes, g, titles):
        weights = nx.get_edge_attributes(graph, 'weight').values()
        cmap = plt.get_cmap('YlOrRd')
        norm = plt.Normalize(vmin=min(weights), vmax=max(weights))
        edge_colors = [cmap(norm(weight)) for weight in weights]

        pos = nx.kamada_kawai_layout(graph)
        nx.draw_networkx_nodes(graph, pos, node_size=50, node_color='skyblue', ax=ax)
        nx.draw_networkx_edges(graph, pos, edge_color=edge_colors, width=1, ax=ax)
        ax.set_title(title)

    plt.tight_layout()
    os.makedirs(os.path.dirname(filename), exist_ok=True)  # 确保目录存在
    plt.savefig(filename, format='png')
    plt.close(fig)


def remove_graph(g: nx.Graph, quantile_value=0.5):
    G = g.copy()

    # 获取所有边的权重
    weights = np.array([data['weight'] for u, v, data in G.edges(data=True)])

    # 计算所需的分位数值
    threshold = np.quantile(weights, quantile_value)

    # 找出权重小于该分位数的边
    edges_to_remove = [(u, v) for u, v, data in G.edges(data=True) if data['weight'] < threshold]

    # 从图中删除这些边
    G.remove_edges_from(edges_to_remove)

    nodelist = list(G.nodes)
    for node in nodelist:
        if len(list(G.neighbors(node))) == 0:
            G.remove_node(node)

    return G, threshold


if __name__ == '__main__':
    with open("infer_result.json", 'r', encoding='utf-8') as f:
        recognition = json.load(f)

    N = {}
    all_items = []
    for item in recognition:
        for comment in recognition[item]:
            targets = recognition[item][comment]
            for target in targets:
                if target not in N:
                    N[target] = set()
                N[target].add(item)


    accimg = 0
    for u in N.keys():
        for v in N.keys():
            if u != v:
                accimg = max(accimg, len(N[u].intersection(N[v])) / len(N[u].union(N[v])))
    print(accimg)

    g = nx.Graph()
    for detect_obj in N.keys():
        g.add_node(detect_obj)
    for u in N.keys():
        for v in N.keys():
            if u != v:
                g.add_edge(u, v, weight=len(N[u].intersection(N[v])) / len(N[u].union(N[v])))

    # delete edge
    # for remove_rate in [0.8, 0.9, 0.95, 0.99]:
    #     g_draw, thres = remove_graph(g, remove_rate)
    #     draw_graph(g_draw, title=f"$maxn={thres} (percentile = {remove_rate})$", draw_node_label=False,
    #                circular=False, filename=f'figure/graph_{remove_rate}.png')

    remove_rates = [0.8, 0.9, 0.95, 0.99]
    graphs = []
    thresholds = []
    titles = []
    for remove_rate in remove_rates:
        g_draw, thres = remove_graph(g, remove_rate)
        graphs.append(g_draw)
        thresholds.append(thres)
        titles.append(f"$maxn={thres} (percentile = {remove_rate})$")

    draw_graphs_combined(graphs, thresholds, titles, 'figure/graph_combined.png')

    # delete node
    all_count = [len(i) for i in N.values()]

    # for quantile in [0.7, 0.8, 0.9]:
    #     maxn = np.quantile(all_count, quantile)
    #     g2 = nx.Graph()
    #     for detect_obj in N.keys():
    #         g2.add_node(detect_obj)
    #     for u in N.keys():
    #         for v in N.keys():
    #             if u != v:
    #                 g2.add_edge(u, v, weight=len(N[u].intersection(N[v])) / len(N[u].union(N[v])))
    #     for i in N.keys():
    #         if len(N[i]) < maxn:
    #             g2.remove_node(i)
    #     draw_graph(g2, title=f"maxn={maxn:.2f} (percentile={quantile})", filename=f'figure/graph_node_{quantile}.png')

    quantiles = [0.7, 0.8, 0.9]
    graphs = []
    maxns = []
    titles = []
    for quantile in quantiles:
        maxn = np.quantile(all_count, quantile)
        g2 = nx.Graph()
        for detect_obj in N.keys():
            g2.add_node(detect_obj)
        for u in N.keys():
            for v in N.keys():
                if u != v:
                    g2.add_edge(u, v, weight=len(N[u].intersection(N[v])) / len(N[u].union(N[v])))
        for i in N.keys():
            if len(N[i]) < maxn:
                g2.remove_node(i)
        graphs.append(g2)
        maxns.append(maxn)
        titles.append(f"maxn={maxn:.2f} (percentile={quantile})")

    draw_node_graphs_combined(graphs, maxns, titles, 'figure/graph_node_combined.png')