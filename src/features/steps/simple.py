from behave import *
from bs4 import BeautifulSoup

@given('Datahub is installed')
def step_impl(context):
    pass

@when('I open "{url}"')
def step_impl(context, url):
    context.response = context.client.get(url, follow=True)

@then('I should be redirected to "{url}"')
def step_impl(context, url):
    u = context.response.redirect_chain[-1][0][17:]
    assert u == url

@then('I should see "{t}"')
def step_impl(context, t):
    s = BeautifulSoup(context.response.content)
    assert s.find(text=t)
