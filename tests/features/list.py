from lettuce import step, world
from gists.actions import list_gists


@step("None user")
def none_user(step):
    world.user = None


@step("None password")
def none_password(step):
    world.password = None


@step("Request list of Gists")
def list_of_gists(step):
    world.result = list_gists(world.user, world.password)


@step("The Result is false")
def result_false(step):
    print world.result.success
    assert world.result.success == True
    print world.result.data
