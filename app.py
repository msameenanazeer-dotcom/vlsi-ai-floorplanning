import streamlit as st
import matplotlib.pyplot as plt

from floorplan import Floorplanner
from ml_model import FloorplanML
from ppa_analysis import calculate_ppa


st.set_page_config(
    page_title="AI/ML VLSI Floorplanner",
    page_icon="🔬",
    layout="wide"
)


st.title(
    "🔬 AI/ML Based VLSI Floorplanning"
)

st.write(
    "VLSI Floorplanning using Artificial "
    "Intelligence and Machine Learning"
)


st.sidebar.header(
    "Floorplanning Parameters"
)


iterations = st.sidebar.slider(
    "Optimization Iterations",
    100,
    5000,
    2000,
    100
)


if st.button(
    "🚀 RUN AI/ML FLOORPLANNER"
):

    with st.spinner(
        "Optimizing VLSI floorplan..."
    ):

        planner = Floorplanner(
            "data/sample_blocks.csv",
            "data/sample_nets.csv"
        )

        initial = (
            planner.random_floorplan()
        )

        initial_area = (
            planner.calculate_area(initial)
        )

        initial_wirelength = (
            planner.calculate_wirelength(initial)
        )

        ml = FloorplanML()

        ml.train(planner)

        optimized, score = (
            planner.optimize(iterations)
        )

        optimized_area = (
            planner.calculate_area(
                optimized
            )
        )

        optimized_wirelength = (
            planner.calculate_wirelength(
                optimized
            )
        )

        prediction = ml.predict(
            optimized_area,
            optimized_wirelength
        )

        ppa = calculate_ppa(
            optimized_area,
            optimized_wirelength
        )


    st.success(
        "Floorplan optimization completed!"
    )


    st.subheader("📊 PPA Results")


    col1, col2, col3, col4 = st.columns(4)


    col1.metric(
        "Area",
        f"{ppa['Area']:.2f}"
    )

    col2.metric(
        "Wirelength",
        f"{ppa['Wirelength']:.2f}"
    )

    col3.metric(
        "Power Estimate",
        f"{ppa['Power']:.2f}"
    )

    col4.metric(
        "Performance",
        f"{ppa['Performance']:.4f}"
    )


    st.subheader(
        "🤖 Machine Learning Prediction"
    )

    st.write(
        f"Predicted objective: "
        f"**{prediction:.2f}**"
    )


    st.subheader(
        "📐 Optimized VLSI Floorplan"
    )


    fig, ax = plt.subplots(
        figsize=(12, 7)
    )


    for block, (x, y) in optimized.items():

        width = planner.block_data[
            block
        ]["width"]

        height = planner.block_data[
            block
        ]["height"]


        rectangle = plt.Rectangle(
            (x, y),
            width,
            height,
            fill=False,
            linewidth=2
        )

        ax.add_patch(rectangle)


        ax.text(
            x + width / 2,
            y + height / 2,
            block,
            ha="center",
            va="center",
            fontsize=12
        )


    max_x = max(
        x + planner.block_data[b]["width"]
        for b, (x, y)
        in optimized.items()
    )


    max_y = max(
        y + planner.block_data[b]["height"]
        for b, (x, y)
        in optimized.items()
    )


    ax.set_xlim(0, max_x + 5)

    ax.set_ylim(0, max_y + 5)

    ax.set_xlabel("X Position")

    ax.set_ylabel("Y Position")

    ax.set_title(
        "Optimized AI/ML VLSI Floorplan"
    )

    ax.grid(True)

    st.pyplot(fig)


    st.subheader(
        "📍 Block Coordinates"
    )


    st.dataframe(
        [
            {
                "Block": block,
                "X": round(x, 2),
                "Y": round(y, 2)
            }
            for block, (x, y)
            in optimized.items()
        ]
    )


    st.subheader(
        "📈 Optimization Comparison"
    )


    area_improvement = (
        (
            initial_area -
            optimized_area
        )
        / initial_area
        * 100
    )


    wirelength_improvement = (
        (
            initial_wirelength -
            optimized_wirelength
        )
        / initial_wirelength
        * 100
    )


    st.write(
        f"Area improvement: "
        f"**{area_improvement:.2f}%**"
    )

    st.write(
        f"Wirelength improvement: "
        f"**{wirelength_improvement:.2f}%**"
    )
