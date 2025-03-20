from delayed_assert.delayed_assert import assert_all, expect
from pytest_bdd import given, parsers, then, when

from Load_tests.base_classes.load_test_runner import LoadTestRunner
from Load_tests.test_classes.load_tests_mapping import TESTS_MAP
from Rest.tests.steps_defs import login_in_the_app


@given(parsers.parse('"{subscription}" user is logged in'))
def load_testing_login(subscription, context):
    login_in_the_app(subscription, context)


@given(parsers.parse("the '{test_name}' is selected for the load testing"))
def set_test_name(context, test_name):
    context["load_test"] = context.get("load_test") if context.get("load_test") else {}
    context["load_test"]["test_suite"] = TESTS_MAP[test_name.lower()]


@given(parsers.parse("The test duration is selected as '{test_duration}' seconds"))
def set_test_duration(context, test_duration):
    context["load_test"]["test_duration"] = int(test_duration)


@given(parsers.parse("The number of users is '{number_of_users}'"))
def set_number_of_users(context, number_of_users):
    context["load_test"]["number_of_users"] = int(number_of_users)


@when(parsers.parse("Load test is started"))
def load_test(context):
    test_duration = context["load_test"]["test_duration"]
    number_of_users = context["load_test"]["number_of_users"]
    selected_test = context["load_test"]["test_suite"]

    load_test_run = LoadTestRunner(selected_test)
    load_test_results = load_test_run.run_test(number_of_users, test_duration)

    context["load_test"]["num_failures"] = load_test_results.stats.total.num_failures
    context["load_test"]["response_time_percentile"] = load_test_results.stats.total.get_response_time_percentile(0.95)
    context["load_test"]["avg_response_time"] = load_test_results.stats.total.avg_response_time

    # print(*load_test_results.failure_report().items(), sep="\n")

    load_test_results.stats.reset_all()


@when("Load test is finished")
def load_test_is_finished():
    # Empty step for better scenarios readability
    ...


@then("The target metrics is correct")
def check_of_metrics(context):
    with assert_all():
        expect(context["load_test"]["num_failures"] == 0, f'{context["load_test"]["num_failures"]} failures observing')
        expect(
            context["load_test"]["response_time_percentile"] < 100,
            f'Response_time_percentile is equal to {context["load_test"]["response_time_percentile"]} is higher than 100 ms!',
        )
        expect(
            context["load_test"]["avg_response_time"] < 60,
            f'avg_response_time is equal to {context["load_test"]["avg_response_time"]} that is higher than 60 ms!',
        )


if __name__ == "__main__":
    ...
