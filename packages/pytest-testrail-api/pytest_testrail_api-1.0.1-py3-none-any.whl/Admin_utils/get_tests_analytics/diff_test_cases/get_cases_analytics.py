import pandas as pd

from Admin_utils.custom_logger import logger
from Admin_utils.get_tests_analytics.diff_test_cases.get_all_ids_cases_from_features import get_all_cases
from Testrail_utils.config import PROJECT_DIRECTORY

PRIORITY_LVLS = ("@critical", "@smoke", "@regression", "@rare", "@archive")
AUTOMATION_TYPES = ("@automated", "@broken", "@to_automate", "@manual")

automation_percentage_name = "Automation %"
broken_percentage_name = "Broken %"
scenario_id_name = "Scenario ID"
priority_name = "Priority"
automation_status_name = "Automation Status"
tags_name = "Tags"
path_to_case_name = "Path to Case"

# Setup Pandas to display all columns
pd.options.display.max_columns = 100
pd.options.display.width = 200


def convert_scenarios_data_to_data_frame(scenarios_data):
    data = []
    for case_id, case_info in scenarios_data.items():
        automation_status = priority = "unknown"
        case_tags = case_info["tags"]
        path_to_case = case_info["path_to_case"]

        for tag in case_tags:
            if "@broken_" in tag:
                # It might be one of the following:
                # "@broken_android_phone", "@broken_android_tablet", "@broken_iPhone", "@broken_iPad",
                # "@broken_android", "@broken_iOS",
                automation_status = "@broken"
            elif tag in AUTOMATION_TYPES:
                automation_status = tag
            if tag in PRIORITY_LVLS:
                priority = tag

        data.append(
            {
                scenario_id_name: case_id,
                priority_name: priority,
                automation_status_name: automation_status,
                tags_name: case_tags,
                path_to_case_name: path_to_case,
            }
        )

    # Create DataFrame
    df = pd.DataFrame(data)

    return df


def gather_scenarios_data(scenarios_data):
    """
    The gather_scenarios_data function processes scenario data to generate a summary DataFrame that includes counts
    and percentages of different automation statuses and priorities.
    """
    # The function convert_scenarios_data_to_data_frame is called to convert the input scenarios_data dictionary
    # into a Pandas DataFrame. Each row in the DataFrame represents a scenario with columns
    # for Scenario ID, Priority, Automation Status, Tags, and Path to Case.
    data_frame = convert_scenarios_data_to_data_frame(scenarios_data)

    # A pivot table is created from the DataFrame to count the occurrences of each combination of
    # Priority and Automation Status. The aggfunc="size" parameter is used to count the number of occurrences,
    # and fill_value=0 ensures that missing values are filled with 0.
    pivot_table = pd.pivot_table(
        data_frame, index=priority_name, columns=automation_status_name, aggfunc="size", fill_value=0
    )

    # The function ensures that the columns for each automation status (@automated, @to_automate, @manual, @broken)
    # exist in the pivot table. If any of these columns are missing, they are added with a value of 0.
    for status in AUTOMATION_TYPES:
        if status not in pivot_table.columns:
            pivot_table[status] = 0

    # The function calculates the total number of scenarios for each priority and the overall total.
    pivot_table["Total"] = pivot_table.sum(axis=1)
    total_row = pivot_table.sum(axis=0)
    pivot_table.loc["Total"] = total_row
    # It also calculates the percentage of automated and broken scenarios for each priority.
    pivot_table[automation_percentage_name] = round(pivot_table["@automated"] / pivot_table["Total"] * 100, 2)
    pivot_table[broken_percentage_name] = round(pivot_table["@broken"] / pivot_table["Total"] * 100, 2)

    # The pivot table is finalized by selecting the relevant columns and filling any NaN values with 0.
    pivot_table = pivot_table[[*AUTOMATION_TYPES, "Total", automation_percentage_name, broken_percentage_name]]
    pivot_table = pivot_table.fillna(0)  # Replace NaN values with 0

    # The priority index is converted to a categorical type with a specified order,
    # and the DataFrame is sorted by priority.
    priority_order = [*PRIORITY_LVLS, "Total"]
    pivot_table.index = pd.CategoricalIndex(pivot_table.index, categories=priority_order, ordered=True)
    pivot_table = pivot_table.sort_index()

    return pivot_table


def main():
    get_all_cases()
    for proj in PROJECT_DIRECTORY:
        summary_scenarios = get_all_cases(proj)
        df = gather_scenarios_data(summary_scenarios)
        logger.info(f"\n{df}")


if __name__ == "__main__":
    main()
