
class Centroid:
    def __init__(self, position: int, radius: int):
        self.position = position
        self.radius = radius
        self.dots = [position]

    def calculate_position(self) -> None:
        mean = sum(self.dots) / len(self.dots)
        self.position = int(mean + 0.5)

    def add_new_dots(self, dot: int) -> None:
        if self.position - self.radius <= dot <= self.position + self.radius:
            self.dots.append(dot)

    def delete_dots(self) -> None:
        self.dots = [
            dot for dot in self.dots
            if self.position - self.radius <= dot <= self.position + self.radius
        ]
