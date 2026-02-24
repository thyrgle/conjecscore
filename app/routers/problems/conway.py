from .utils import register_problem, parse_JSON


def conway_score(graph, n):
    bad_count = 0
    for i in range(n):
        for j in range(i+1, n):
            c = len(set(graph[str(i)]) & set(graph[str(j)]))
            e = int(i in graph[str(j)])
            bad_count += (c - (2 - e)) * (c - (2 - e))
    return bad_count


def score(graph):
    return conway_score(graph, 99)


register_problem("conway99", score, "Conway's 99 Problem",
                 "conway99.j2", "lowest", "conway99", parse_JSON, "conway.svg")
