class BuildGraph:
    @staticmethod
    def construct_graph(tensor):

        topo = []
        visited = set()
        queue = [tensor]
        while queue:
            ele = queue.pop(0)
            if ele not in visited:
                visited.add(ele)
                topo.append(ele)

                for child in ele._prev:
                    queue.append(child)
        return topo

    __module__ = "anygrad.autograd"
