from behave import when


@when("I evaluate the template")
def step_impl(context):
    context.evaluator.generate_effective_template()
