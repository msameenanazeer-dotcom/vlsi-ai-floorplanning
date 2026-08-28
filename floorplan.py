import random
import pandas as pd


class Floorplanner:

    def __init__(self, blocks_file, nets_file):

        self.blocks = pd.read_csv(blocks_file)
        self.nets = pd.read_csv(nets_file)

        self.block_data = {}

        for _, row in self.blocks.iterrows():

            self.block_data[row["block"]] = {
                "width": float(row["width"]),
                "height": float(row["height"])
            }

    def random_floorplan(self):

        placement = {}

        x = 0
        y = 0
        row_height = 0

        for block in self.block_data:

            width = self.block_data[block]["width"]
            height = self.block_data[block]["height"]

            if x + width > 50:

                x = 0
                y += row_height
                row_height = 0

            placement[block] = (x, y)

            x += width

            row_height = max(
                row_height,
                height
            )

        return placement

    def calculate_area(self, placement):

        max_x = 0
        max_y = 0

        for block, (x, y) in placement.items():

            width = self.block_data[block]["width"]
            height = self.block_data[block]["height"]

            max_x = max(
                max_x,
                x + width
            )

            max_y = max(
                max_y,
                y + height
            )

        return max_x * max_y

    def calculate_wirelength(self, placement):

        total = 0

        for _, row in self.nets.iterrows():

            names = row["blocks"].split("-")

            xs = []
            ys = []

            for block in names:

                x, y = placement[block]

                width = self.block_data[block]["width"]
                height = self.block_data[block]["height"]

                xs.append(x + width / 2)
                ys.append(y + height / 2)

            if xs:

                hpwl = (
                    max(xs) - min(xs)
                    + max(ys) - min(ys)
                )

                total += hpwl

        return total

    def objective(self, placement):

        area = self.calculate_area(placement)

        wirelength = self.calculate_wirelength(
            placement
        )

        return (
            0.5 * area +
            0.5 * wirelength
        )

    def optimize(self, iterations=2000):

        best = self.random_floorplan()

        best_score = self.objective(best)

        blocks = list(
            self.block_data.keys()
        )

        for _ in range(iterations):

            candidate = best.copy()

            b1, b2 = random.sample(
                blocks,
                2
            )

            candidate[b1], candidate[b2] = (
                candidate[b2],
                candidate[b1]
            )

            score = self.objective(
                candidate
            )

            if score < best_score:

                best = candidate
                best_score = score

        return best, best_score
