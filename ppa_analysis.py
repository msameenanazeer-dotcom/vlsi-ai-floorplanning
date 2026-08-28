def calculate_ppa(area, wirelength):

    power = (
        0.01 * area +
        0.005 * wirelength
    )

    performance = (
        1000 /
        (wirelength + 1)
    )

    return {
        "Area": area,
        "Wirelength": wirelength,
        "Power": power,
        "Performance": performance
    }
