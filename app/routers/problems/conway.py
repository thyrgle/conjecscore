def conway_score(graph, n):
    bad_count = 0
    for i in range(n):
        for j in range(i+1, n):
            try:
                c = len(set(graph[str(i)]) & set(graph[str(j)]))
                e = int(i in graph[str(j)])
                bad_count += (c - (2 - e)) * (c - (2 - e))
            except IndexError:
                return None
    return bad_count


async def score(graph):
    return conway_score(graph, 99)


async def score6273(graph):
    return conway_score(graph, 6273)


async def score494019(graph):
    return conway_score(graph, 494019)
