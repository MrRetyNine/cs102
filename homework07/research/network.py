import typing as tp
from collections import defaultdict

import community as community_louvain  # type: ignore
import matplotlib.pyplot as plt  # type: ignore
import networkx as nx  # type: ignore
import pandas as pd  # type: ignore
from vkapi.friends import get_friends, get_mutual


def ego_network(
    user_id: tp.Optional[int] = None, friends: tp.Optional[tp.List[int]] = None
) -> tp.List[tp.Tuple[int, int]]:
    """
    Построить эгоцентричный граф друзей.

    :param user_id: Идентификатор пользователя, для которого строится граф друзей.
    :param friends: Идентификаторы друзей, между которыми устанавливаются связи.
    """
    list_of_id_friends = []

    if not friends:
        friends_resp = get_friends(user_id=user_id, fields=["nickname"])  # type: ignore
        friends = [user["id"] for user in friends_resp.items if not user.get("deactivated")]  # type: ignore

    mutual_friends = get_mutual(user_id, target_uids=friends)
    for person in mutual_friends:
        list_of_id_friends.extend([(person["id"], n) for n in person["common_friends"]])  # type: ignore

    return list_of_id_friends


def plot_ego_network(net: tp.List[tp.Tuple[int, int]]) -> None:
    graph = nx.Graph()
    graph.add_edges_from(net)
    layout = nx.spring_layout(graph)
    nx.draw(graph, layout, node_size=10, node_color="black", alpha=0.5)
    plt.title("Ego Network", size=15)
    plt.show()


def plot_communities(net: tp.List[tp.Tuple[int, int]]) -> None:
    graph = nx.Graph()
    graph.add_edges_from(net)
    layout = nx.spring_layout(graph)
    partition = community_louvain.best_partition(graph)
    nx.draw(graph, layout, node_size=25, node_color=list(partition.values()), alpha=0.8)
    plt.title("Ego Network", size=15)
    plt.show()


def get_communities(net: tp.List[tp.Tuple[int, int]]) -> tp.Dict[int, tp.List[int]]:
    communities = defaultdict(list)
    graph = nx.Graph()
    graph.add_edges_from(net)
    partition = community_louvain.best_partition(graph)
    for uid, cluster in partition.items():
        communities[cluster].append(uid)
    return communities


def describe_communities(
    clusters: tp.Dict[int, tp.List[int]],
    friends: tp.List[tp.Dict[str, tp.Any]],
    fields: tp.Optional[tp.List[str]] = None,
) -> pd.DataFrame:
    if fields is None:
        fields = ["first_name", "last_name"]

    data = []
    for cluster_n, cluster_users in clusters.items():
        for uid in cluster_users:
            for friend in friends:
                if uid == friend["id"]:
                    data.append([cluster_n] + [friend.get(field) for field in fields])  # type: ignore
                    break
    return pd.DataFrame(data=data, columns=["cluster"] + fields)


if __name__ == "__main__":
    net = ego_network(user_id=238422411)
    # print(net[:5])
    # plot_ego_network(net)
    #
    # net1 = ego_network(user_id=238422411)
    # plot_communities(net1)
    #
    # communities = get_communities(net)
    # friends_response = get_friends(user_id=238422411)
    # print(describe_communities(communities, friends_response.items, fields=["first_name", "last_name"]))
    friends = get_friends(user_id=238422411, fields=["first_name", "last_name"]).items
    clusters = get_communities(net)
    print(describe_communities(clusters, friends))  # type: ignore