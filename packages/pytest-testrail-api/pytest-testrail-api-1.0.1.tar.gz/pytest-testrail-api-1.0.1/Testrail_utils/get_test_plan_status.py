import os
from datetime import datetime

import pandas as pd
import plotly.graph_objects as go

from Admin_utils.custom_logger import logger
from Rest.api.custom_dict import CustomDict
from Testrail_utils.tools.testrail_tool import TRTool

TEST_PLAN_ID = os.environ.get("TEST_PLAN_ID", 1880)

# Statuses for test cases
PASSED = "Passed"
FAILED = "Failed"
BLOCKED = "Blocked"
NOT_APPLICABLE = "N/A"
NOT_RELEVANT = "Not relevant"
UNTESTED = "Untested"
# Colors for test case statuses
STATUS_COLORS = {
    PASSED: "#B2E2A4",
    FAILED: "#F5A6A6",
    NOT_APPLICABLE: "#BFA2DB",
    NOT_RELEVANT: "#FFD580",
    BLOCKED: "#FF9980",
    UNTESTED: "#E6F7FA",
}


def get_run_status(test_run):
    return {
        PASSED: test_run.passed_count,
        FAILED: test_run.failed_count,
        BLOCKED: test_run.blocked_count,
        NOT_APPLICABLE: test_run.custom_status1_count,
        NOT_RELEVANT: test_run.custom_status2_count,
        UNTESTED: test_run.untested_count,
    }


def test_plan_status(plan_id=TEST_PLAN_ID, test_rail_client=None):
    logger.info("Running test_plan_status function")
    test_rail_client = test_rail_client or TRTool()
    test_plan = test_rail_client.plans.get_plan(plan_id)
    test_plan_name = test_plan.name
    test_plan_status = CustomDict()

    for test_suite in test_plan.entries:
        for test_run in test_suite.runs:
            test_run_name = f"{test_run.name} {test_run.config}" if test_run.config else test_run.name
            if plan_id == "1543":
                if "Regression testing of CA" in test_run_name:
                    test_plan_status[test_run_name] = get_run_status(test_run)
            else:
                test_plan_status[test_run_name] = get_run_status(test_run)

    test_plan_status.Total = get_run_status(test_plan)
    logger.info("Finished running test_plan_status function")
    return test_plan_name, test_plan_status


def visualize_test_plan_status(testplan_data, test_plan_name):
    logger.info("Running visualize_test_plan_status function")
    df = pd.DataFrame(testplan_data).T
    df_percent = round(df.div(df.sum(axis=1), axis=0) * 100, 2)

    fig = go.Figure()

    for status, color in STATUS_COLORS.items():
        fig.add_trace(
            go.Bar(
                y=df_percent.index,
                x=df_percent[status],
                name=status,
                orientation="h",
                marker=dict(color=color),
                hovertemplate=f"<b>Status</b>: {status}<br><b>Percentage</b>: %{{x}}%<extra></extra>",
            )
        )

    fig.update_layout(
        barmode="stack",
        title=test_plan_name,
        xaxis=dict(title="Percentage of Tests"),
        yaxis=dict(title="Test Suites"),
        plot_bgcolor="white",
        paper_bgcolor="white",
        font_color="black",
        legend=dict(title="Test Outcome", x=1.05, y=1),
        margin=dict(l=40, r=40, t=40, b=40),
    )

    for i, row in df_percent.iterrows():
        previous_percentage = 0
        for status in df_percent.columns:
            percentage = row[status]
            if status == PASSED or percentage > 5:
                fig.add_annotation(
                    x=previous_percentage + percentage / 2,
                    y=i,
                    text=f"{percentage:.1f}%",
                    showarrow=False,
                    font=dict(color="black"),
                )
            previous_percentage += percentage

    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    fig.add_annotation(
        x=1.25,
        y=-0.05,
        text=f"Generated on: {current_datetime}",
        showarrow=False,
        xref="paper",
        yref="paper",
        xanchor="right",
        yanchor="top",
        font=dict(size=10, color="black"),
    )

    fig.show()
    logger.info("Finished running visualize_test_plan_status function")


def main():
    logger.info("Starting main function")
    test_plan_ids = TEST_PLAN_ID.split(",") if "," in TEST_PLAN_ID else [TEST_PLAN_ID]
    for test_plan_id in test_plan_ids:
        test_plan_name, test_plan_data = test_plan_status(test_plan_id)
        visualize_test_plan_status(test_plan_data, test_plan_name)
    logger.info("Finished main function")


if __name__ == "__main__":
    main()
