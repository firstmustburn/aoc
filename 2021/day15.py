import heapq
import sys

def debug(*args):
    pass
    # print(*args)

class Node:

    def __init__(self, x, y, cost):
        """X,Y - the location in the grid
        cost - the cost to move onto this node
        
        Additional state:  (for the search alg):
        neighbors - a list of the adjacent nodes, to be populated by the parent NodeGrid
        
        Node is reset at creation"""
        self.x = x
        self.y = y
        self.cost = cost

        self.neighbors = []
        self.reset()

    def reset(self):
        """set search algorithm state to initial conditions"""
        self.visited = False
        self.tcost = float("inf")  #tentative cost
        self.hcost = 0 #heuristic cost
        self.parent = None

    def path_cost(self):
        return self.tcost + self.hcost

    def __str__(self):
        #parent string avoids recursion in the string printing
        if self.parent is None:
            parentstr = "None"
        else:
            parentstr = f"[{self.parent.x},{self.parent.y}]"
        return f"Node({self.x}, {self.y}, cost={self.cost}, tcost={self.tcost}, visited={self.visited}, parent={parentstr})"

    def __repr__(self):
        return self.__str__()

    def __lt__(self, other):
        return self.path_cost() < other.path_cost()
    

class NodeGrid:

    @classmethod
    def load(cls, filename):
        with open(filename) as infile:
            lines = infile.readlines()
        
        rows = []
        rowlen = None
        for y, line in enumerate(lines):
            row = []
            for x, cost in enumerate(line.strip()):
                row.append(Node(x,y,int(cost)))
            #make sure the rows are all the same length
            if rowlen is None:
                rowlen = len(row)
            else:
                assert rowlen == len(row)
            
            rows.append(row)

        return NodeGrid(rows)

    @classmethod
    def make_expanded_grid(cls, template_grid, iterations, cost_iterator):
        #expand each row of the template grid rightward over the iterations
        rightward_expanded_rows = []
        for row in template_grid.grid:
            expanded_row = []
            #start the expanded row with a copy of the original grid row
            previous_iteration = [ Node(n.x, n.y, n.cost) for n in row ]
            expanded_row.extend(previous_iteration)
            for iteration in range(1,iterations): #skip the first iteration because it is our copy
                #iterate the row by incrementing the X direction
                #apply the cost function
                current_iteration = [ Node(n.x+template_grid.xdim, n.y, cost_iterator(n.cost)) for n in previous_iteration ]
                expanded_row.extend(current_iteration)
                previous_iteration = current_iteration
            #done expanding the row
            rightward_expanded_rows.append(expanded_row)

        #now repeat the expansion downward, iterating the whole set of rightward expanded rows
        def copygrid(ingrid):
            """Straight copy the ingrid"""
            outgrid = []
            for row in ingrid:
                outrow = [ Node(n.x, n.y, n.cost) for n in row ]
                outgrid.append(outrow)
            return outgrid

        def iterategrid(ingrid):
            """Copy the ingrid "downward" by incrementing the y direction
            Apply the cost iterator"""
            outgrid = []
            for row in ingrid:
                outrow = [ Node(n.x, n.y+template_grid.ydim, cost_iterator(n.cost)) for n in row ]
                outgrid.append(outrow)
            return outgrid

        expanded_rows = []
        #first iteration is just a copy of the rer
        previous_iteration = copygrid(rightward_expanded_rows)
        expanded_rows.extend(previous_iteration)
        for i in range(1,iterations):
            current_iteration = iterategrid(previous_iteration)
            expanded_rows.extend(current_iteration)
            previous_iteration = current_iteration

        assert len(expanded_rows) == template_grid.ydim*5
        assert len(expanded_rows[0]) == template_grid.xdim*5


        return NodeGrid(expanded_rows)





    def __init__(self, grid):
        self.grid = grid
        self.xdim = len(grid[0])
        self.ydim = len(grid)
        self._set_neighbors()

    def get_node(self, x, y):
        return self.grid[y][x]

    def get_node_from_point(self, pt):
        return self.grid[pt[1]][pt[0]]

    def iterate(self):
        for row in self.grid:
            for cell in row:
                yield cell

    def reset(self):
        self.visit_count = 0
        self.next_node_pq = [] # a heap sorted list of the next neighbor nodes
        for node in self.iterate():
            node.reset()

    def draw_path(self, end_node, file=sys.stdout):
        """Call this when the search state is already set up to print the grid with the path from the end_node highlighted"""
        #collect the path nodes
        path_nodes = [end_node]
        next_node = end_node.parent
        while next_node is not None:
            path_nodes.append(next_node)
            next_node = next_node.parent
        #print the grid
        print("*"*self.xdim*2, file=file)
        for row in self.grid:
            rowstr = ""
            for cell in row:
                if cell in path_nodes:
                    rowstr += f"*{cell.cost}"
                else:
                    rowstr += f" {cell.cost}"
            print(rowstr, file=file)
        print("*"*self.xdim*2, file=file)

    def draw_path_with_pathcosts(self, end_node, file=sys.stdout):
        """Call this when the search state is already set up to print the grid with the path from the end_node highlighted"""
        #collect the path nodes
        path_nodes = [end_node]
        next_node = end_node.parent
        while next_node is not None:
            path_nodes.append(next_node)
            next_node = next_node.parent
        #print the grid
        print("*"*self.xdim*2, file=file)
        for row in self.grid:
            rowstr = ""
            for cell in row:
                if cell in path_nodes:
                    rowstr += f"{cell.path_cost():4d}* "
                else:
                    if cell.visited:
                        rowstr += f"{cell.path_cost():4d}v "
                    else:
                        if isinstance(cell.path_cost(), float):
                            rowstr += f"{cell.path_cost():4f} "
                        else:
                            rowstr += f"{cell.path_cost():4d} "
            print(rowstr, file=file)
        print("*"*self.xdim*2, file=file)

    def draw_grid(self):
        """Call this when the search state is already set up to print the grid with the path from the end_node highlighted"""
        #print the grid
        print("*"*self.xdim)
        for row in self.grid:
            for cell in row:
                print(f"{cell.cost}", end="")
            print("")
        print("*"*self.xdim)

    def _set_neighbors(self):
        for x in range(self.xdim):
            for y in range(self.ydim):
                #set the neighbors for x,y
                neighbors = []
                if (x-1) >= 0:
                    neighbors.append(self.get_node(x-1, y))
                if (x+1) < self.xdim:
                    neighbors.append(self.get_node(x+1, y))
                if (y-1) >= 0:
                    neighbors.append(self.get_node(x, y-1))
                if (y+1) < self.ydim:
                    neighbors.append(self.get_node(x, y+1))
                self.get_node(x,y).neighbors = neighbors

    def find_path(self, start, end):
        """Start and end are x,y tuples in the grid
        
        return the list of nodes from start to end with the smallest cost
        Uses Dijkstra's algorithm for search
        Add the A* optimization by add the heuristic cost to the nodes and
        using hcost + tcost for the node sort criteria"""
        start_node = self.get_node_from_point(start)
        end_node = self.get_node_from_point(end)
        self.reset()
        
        #since the heuristic costs are spatial and fixed, set them one time
        self._set_hcosts(end_node)

        #visit the start node
        start_node.tcost = 0
        self._visit_node(start_node)

        while len(self.next_node_pq) > 0:
            next_node = self._find_next_node()
            #as soon as the end node has the lowest cost, we're done
            if next_node == end_node:
                break
            #otherwise, visit the next node and iterate
            self._visit_node(next_node)

        return start_node, end_node

    def _set_hcosts(self, end_node):
        #all nodes have a cost of at least one, so taking the number of steps needed to reach the
        #end node as a heuristic is admissible and will result in an optimized result
        for node in self.iterate():
            # node.hcost = 0
            node.hcost = abs(end_node.x - node.x) + abs(end_node.y - node.y)

    def _find_next_node(self):
        """Find the unvisited node with the lowest path_cost"""
        return heapq.heappop(self.next_node_pq)

    def _visit_node(self, node):
        self.visit_count += 1
        if self.visit_count % 500 == 0:
            debug("Visited", self.visit_count)
        for neighbor in node.neighbors:
            if neighbor.visited:
                continue
            
            #compute the tenative cost from node to neighbor and set it if lower
            tcost = node.tcost + neighbor.cost
            if tcost < neighbor.tcost:
                neighbor.tcost = tcost
                neighbor.parent = node
                if neighbor not in self.next_node_pq:
                    heapq.heappush(self.next_node_pq, neighbor)
                debug("Setting neighbor tcost", neighbor)
        #mark the node as visited
        node.visited = True


def check_expanded_grid(test_grid, reference_filename):
    ref_grid = NodeGrid.load(reference_filename)
    if ref_grid.xdim != test_grid.xdim:
        print("X size mismatch: ", ref_grid.xdim, test_grid.xdim)
        return False
    if ref_grid.ydim != test_grid.ydim:
        print("y size mismatch: ", ref_grid.ydim, test_grid.ydim)
        return False
    for x in range(test_grid.xdim):
        for y in range(test_grid.ydim):
            if ref_grid.get_node(x,y).cost != test_grid.get_node(x,y).cost:
                print("Node mismatch: ", x, y, ref_grid.get_node(x,y).cost, test_grid.get_node(x,y).cost)
                return False
    #everything matched
    return True



def part1(grid):
    # part1:

    start = (0,0)
    end = (grid.xdim-1, grid.ydim-1)

    start_node, end_node = grid.find_path(start, end)
    grid.draw_path_with_pathcosts(end_node)
    print("start node", start_node)
    print("end node", end_node)
    print("visit count", grid.visit_count)


    # part1: 

    # start node Node(0, 0, cost=1, tcost=0, visited=True, parent=None)
    # end node Node(99, 99, cost=1, tcost=388, visited=False, parent=[99,98])


def part2(smallgrid):
    def cost_iterator(old_cost):
        new_cost = old_cost + 1
        if new_cost > 9:
            new_cost = 1
        return new_cost

    expanded_grid = NodeGrid.make_expanded_grid(smallgrid, 5, cost_iterator)
    # expanded_grid.draw_grid()

    # assert check_expanded_grid(expanded_grid, "day15_test_expanded_reference.txt")

    start = (0,0)
    end = (expanded_grid.xdim-1, expanded_grid.ydim-1)

    start_node, end_node = expanded_grid.find_path(start, end)

    # with open("expanded_grid_final_path.txt", 'w') as outfile:
    #     expanded_grid.draw_path(end_node, outfile)
    # expanded_grid.draw_path_with_pathcosts(end_node)

    print("start node", start_node)
    print("end node", end_node)
    print("visit count", expanded_grid.visit_count)

    # for node in expanded_grid.iterate():
    #     assert node.hcost == 0
    #     if node.visited:
    #         assert node not in expanded_grid.next_node_pq
    #         continue
    #     if node not in expanded_grid.next_node_pq and node != end_node:
    #         assert node.tcost == float("inf")

    # for node in expanded_grid.next_node_pq:
    #     print("****")
    #     print(node)
    #     print(end_node)
    #     assert node.tcost < float("inf")
    #     assert node.tcost >= end_node.tcost
    #     assert end_node <= node

    # results without heuristic
    # start node Node(0, 0, cost=1, tcost=0, visited=True, parent=None)
    # end node Node(99, 99, cost=1, tcost=388, visited=False, parent=[99,98])
    # visit count 9995
    # start node Node(0, 0, cost=1, tcost=0, visited=True, parent=None)
    # end node Node(499, 499, cost=9, tcost=2819, visited=False, parent=[499,498])
    # visit count 249998

    # results with heuristic
    # start node Node(0, 0, cost=1, tcost=0, visited=True, parent=None)
    # end node Node(99, 99, cost=1, tcost=388, visited=False, parent=[99,98])
    # visit count 9989
    # start node Node(0, 0, cost=1, tcost=0, visited=True, parent=None)
    # end node Node(499, 499, cost=9, tcost=2819, visited=False, parent=[499,498])
    # visit count 249997

if __name__ == "__main__":

    # grid = NodeGrid.load("day15_test.txt")
    grid = NodeGrid.load("day15.txt")

    # print(grid.xdim, grid.ydim)

    # for node in grid.iterate():
    #     print("Neighbors for node", node)
    #     for n in node.neighbors:
    #         print("   ",n)

    part1(grid)
    part2(grid)


