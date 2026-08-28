import numpy as np

from sklearn.ensemble import RandomForestRegressor


class FloorplanML:

    def __init__(self):

        self.model = RandomForestRegressor(
            n_estimators=100,
            random_state=42
        )

    def train(self, floorplanner):

        X = []
        y = []

        for _ in range(200):

            placement = (
                floorplanner.random_floorplan()
            )

            area = (
                floorplanner.calculate_area(
                    placement
                )
            )

            wirelength = (
                floorplanner.calculate_wirelength(
                    placement
                )
            )

            objective = (
                floorplanner.objective(
                    placement
                )
            )

            X.append([
                area,
                wirelength
            ])

            y.append(objective)

        X = np.array(X)
        y = np.array(y)

        self.model.fit(X, y)

    def predict(self, area, wirelength):

        return self.model.predict(
            [[area, wirelength]]
        )[0]
