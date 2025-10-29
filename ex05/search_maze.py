import sys
import collections
import subprocess
import tempfile
import os
from typing import List, Tuple, Optional

class MazeSolver:
    """Maze solver using BFS or DFS algorithms"""
    
    # ANSI color codes
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    
    # Maze characters
    WALL = '#'
    PATH = '.'
    START = 'S'
    TARGET = 'T'
    SOLUTION = '*'
    
    def __init__(self, maze: List[str]):
        self.maze = [list(row) for row in maze]
        self.rows = len(maze)
        self.cols = len(maze[0]) if maze else 0
        self.start_pos = None
        self.target_pos = None
        
    def find_positions(self) -> None:
        """Find the start and target positions in the maze"""
        for i in range(self.rows):
            for j in range(self.cols):
                if self.maze[i][j] == self.START:
                    self.start_pos = (i, j)
                elif self.maze[i][j] == self.TARGET:
                    self.target_pos = (i, j)
        
        if self.start_pos is None:
            raise ValueError("Start position 'S' not found in maze")
        if self.target_pos is None:
            raise ValueError("Target position 'T' not found in maze")
    
    def get_neighbors(self, pos: Tuple[int, int]) -> List[Tuple[int, int]]:
        row, col = pos
        neighbors = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # UP, DOWN, LEFT, RIGHT
        
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            
            # Check boundaries
            if 0 <= new_row < self.rows and 0 <= new_col < self.cols:
                # Check if it's not a wall and not the start position
                cell = self.maze[new_row][new_col]
                if cell != self.WALL and (new_row, new_col) != self.start_pos:
                    neighbors.append((new_row, new_col))
        
        return neighbors
    
    def bfs(self) -> Optional[List[Tuple[int, int]]]:
        queue = collections.deque()
        visited = set()
        parent = {}  # To reconstruct the path
        
        queue.append(self.start_pos)
        visited.add(self.start_pos)
        parent[self.start_pos] = None
        
        while queue:
            current = queue.popleft()
            
            if current == self.target_pos:
                # Reconstruct path
                path = []
                while current is not None:
                    path.append(current)
                    current = parent[current]
                return path[::-1]  # Reverse to get start->target
            
            for neighbor in self.get_neighbors(current):
                if neighbor not in visited:
                    visited.add(neighbor)
                    parent[neighbor] = current
                    queue.append(neighbor)
        
        return None
    
    def dfs(self) -> Optional[List[Tuple[int, int]]]:
        stack = []
        visited = set()
        parent = {}  # To reconstruct the path
        
        stack.append(self.start_pos)
        visited.add(self.start_pos)
        parent[self.start_pos] = None
        
        while stack:
            current = stack.pop()
            
            if current == self.target_pos:
                # Reconstruct path
                path = []
                while current is not None:
                    path.append(current)
                    current = parent[current]
                return path[::-1]  # Reverse to get start->target
            
            for neighbor in self.get_neighbors(current):
                if neighbor not in visited:
                    visited.add(neighbor)
                    parent[neighbor] = current
                    stack.append(neighbor)
        
        return None
    
    def solve(self, algorithm: str) -> bool:
        self.find_positions()
        
        if algorithm == 'bfs':
            path = self.bfs()
        elif algorithm == 'dfs':
            path = self.dfs()
        else:
            raise ValueError("Algorithm must be 'bfs' or 'dfs'")
        
        if path:
            # Mark solution path (excluding start and target)
            for pos in path[1:-1]:  # Skip start and target
                row, col = pos
                # Only replace path characters ('.') with solution marker
                if self.maze[row][col] == self.PATH:
                    self.maze[row][col] = self.SOLUTION
            return True
        return False
    
    def display(self) -> None:
        """Display the maze with ANSI colors"""
        for i in range(self.rows):
            for j in range(self.cols):
                cell = self.maze[i][j]
                if (i, j) == self.start_pos:
                    print(f"{self.YELLOW}{cell}{self.RESET}", end='')
                elif (i, j) == self.target_pos:
                    print(f"{self.GREEN}{cell}{self.RESET}", end='')
                elif cell == self.SOLUTION:
                    print(f"{self.RED}{cell}{self.RESET}", end='')
                elif cell == self.WALL:
                    print(f"{self.BLUE}{cell}{self.RESET}", end='')
                else:
                    print(cell, end='')
            print()  # New line after each row
    
    def display_stats(self, path: Optional[List[Tuple[int, int]]]) -> None:
        """Display statistics about the solution"""
        if path:
            print(f"\n{self.GREEN}✓ Path found!{self.RESET}")
            print(f"Path length: {len(path)} steps")
            print(f"Steps from start to target: {len(path) - 1}")
        else:
            print(f"\n{self.RED}✗ No path found!{self.RESET}")

def read_maze(filename: str) -> List[str]:
    try:
        with open(filename, 'r') as f:
            maze = [line.rstrip('\n') for line in f]
        return maze
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)

def validate_maze(maze: List[str]) -> bool:
    if not maze:
        print("Error: Maze is empty.")
        return False
    
    # Check if all rows have same length
    row_lengths = [len(row) for row in maze]
    if len(set(row_lengths)) != 1:
        print("Error: Maze rows have inconsistent lengths.")
        return False
    
    # Check for start and target
    start_count = sum(row.count('S') for row in maze)
    target_count = sum(row.count('T') for row in maze)
    
    if start_count != 1:
        print("Error: Maze must contain exactly one start position 'S'.")
        return False
    
    if target_count != 1:
        print("Error: Maze must contain exactly one target position 'T'.")
        return False
    
    return True

def generate_sample_maze(height: int = 15, width: int = 25) -> List[str]:
    try:
        # Run the maze generator and capture output
        result = subprocess.run(
            ['python', 'maze_generator.py', str(height), str(width)],
            capture_output=True,
            text=True,
            check=True
        )
        
        # Split the output into lines and remove empty ones
        maze_lines = [line for line in result.stdout.split('\n') if line.strip()]
        return maze_lines
        
    except subprocess.CalledProcessError as e:
        print(f"Error generating maze: {e}")
        print("Falling back to simple maze...")
        return generate_fallback_maze()
    except FileNotFoundError:
        print("Error: maze_generator.py not found in current directory")
        print("Falling back to simple maze...")
        return generate_fallback_maze()

def generate_fallback_maze() -> List[str]:
    """Generate a simple fallback maze if the generator is not available"""
    return [
        "#########",
        "#S......#",
        "#.#####.#",
        "#.#...#.#",
        "#.#.#.#.#",
        "#.....#T#",
        "#########"
    ]

def main():
    if len(sys.argv) != 3:
        print("Usage: python search_maze.py <algorithm> <maze_file>")
        print("  algorithm: 'bfs' or 'dfs'")
        print("  maze_file: path to maze file")
        print("\nExample: python search_maze.py bfs maze1.txt")
        print("\nNo maze file provided. Generating a random maze...")
        
        # Generate a random maze
        maze = generate_sample_maze(15, 25)
        algorithm = 'bfs'  # Default algorithm
        
        print(f"\nUsing randomly generated maze with algorithm: {algorithm}")
    else:
        algorithm = sys.argv[1].lower()
        filename = sys.argv[2]
        
        if algorithm not in ['bfs', 'dfs']:
            print("Error: Algorithm must be 'bfs' or 'dfs'")
            sys.exit(1)
        
        maze = read_maze(filename)
    
    # Validate maze
    if not validate_maze(maze):
        sys.exit(1)
    
    # Create solver and solve maze
    solver = MazeSolver(maze)
    
    print(f"\nOriginal Maze ({len(maze)}x{len(maze[0])}):")
    print("=" * 50)
    solver.find_positions()  # Just to set positions for display
    solver.display()
    
    print(f"\nSolving with {algorithm.upper()}...")
    solution_found = solver.solve(algorithm)
    
    print(f"\nSolved Maze:")
    print("=" * 50)
    solver.display()
    
    # Display statistics
    if solution_found:
        path = solver.bfs() if algorithm == 'bfs' else solver.dfs()
        solver.display_stats(path)
    else:
        solver.display_stats(None)
    
    # Legend
    print(f"\nLegend:")
    print(f"{solver.YELLOW}S{solver.RESET} - Start position")
    print(f"{solver.GREEN}T{solver.RESET} - Target position")
    print(f"{solver.RED}*{solver.RESET} - Solution path")
    print(f"{solver.BLUE}#{solver.RESET} - Walls")
    print(f". - Available path")

if __name__ == "__main__":
    main()