# chunk_manager.py
import threading
from map_chunk import MapChunk  # Updated import to reflect the new class name
from side import Side

class ChunkManager:
    def __init__(self, noise_generator, texture_manager):
        self.loaded_chunks = {} 
        self.noise_generator = noise_generator
        self.texture_manager = texture_manager
        self.chunk_lock = threading.Lock()

    def load_chunk(self, position):
        """Load a chunk at the specified position if not already loaded."""
        if position not in self.loaded_chunks:
            print('generating chunk ' + str(position[0]) +  ', ' + str(position[1]))
            threading.Thread(target=self._load_chunk_thread, args=(position,)).start()

    def regen_neighbours(self, position):
        for x in [-1, 0, 1]:
            for y in [-1, 0, 1]:
                if x == y == 0:
                    continue
                neighbour_pos = (position[0] + x, position[1] + y)
                if neighbour_pos in self.loaded_chunks:
                    self.loaded_chunks[neighbour_pos].regenerate_edges()

    def _load_chunk_thread(self, position):
        chunk = MapChunk(position, self.noise_generator, self.texture_manager, self)

        with self.chunk_lock:
            self.loaded_chunks[position] = chunk
        
        self.regen_neighbours(position)
    
    def get_chunk(self, position):
        return self.loaded_chunks.get(position)
    
    def unload_chunk(self, position):
        """Unload a chunk at the specified position."""
        if position in self.loaded_chunks:
            del self.loaded_chunks[position]

    def get_loaded_chunk_positions(self):
        """Return a list of currently loaded chunk positions."""
        return list(self.loaded_chunks.keys())

    def get_edge_chunks(self):
        """Identify and return the chunks on the perimeter (edge) of the currently loaded grid."""
        edge_chunks = set()
        loaded_positions = self.get_loaded_chunk_positions()
        if not loaded_positions:
            return edge_chunks

        min_x = min(pos[0] for pos in loaded_positions)
        max_x = max(pos[0] for pos in loaded_positions)
        min_y = min(pos[1] for pos in loaded_positions)
        max_y = max(pos[1] for pos in loaded_positions)

        # Chunks on the left and right edges
        for y in range(min_y, max_y + 1):
            edge_chunks.add((min_x, y))
            edge_chunks.add((max_x, y))

        # Chunks on the top and bottom edges
        for x in range(min_x, max_x + 1):
            edge_chunks.add((x, min_y))
            edge_chunks.add((x, max_y))

        return edge_chunks

    def update_chunks_around_camera(self, camera_chunk_pos):
        """
        Ensure a 3x3 grid of chunks is loaded around the camera's current chunk position.
        Dynamically load and unload chunks as needed.
        """
        cx, cy = camera_chunk_pos
        # Load new chunks in a 3x3 grid around the camera's current chunk position
        for x in range(cx - 1, cx + 2):
            for y in range(cy - 1, cy + 2):
                self.load_chunk((x, y))

        # Unload chunks that are not in the 3x3 grid around the camera
        for pos in self.get_loaded_chunk_positions():
            if abs(pos[0] - cx) > 1 or abs(pos[1] - cy) > 1:
                self.unload_chunk(pos)

    def render(self, surface, camera_position, screen_center):
        """Render all loaded chunks with the camera position at the center of the screen."""
        with self.chunk_lock:
            for chunk in self.loaded_chunks.values():
                # Render each MapChunk with adjusted camera centering
                chunk.render(surface, camera_position, screen_center)
