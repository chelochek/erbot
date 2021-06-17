from aiogram.utils.helper import Helper, HelperMode, ListItem


class Test(Helper):
    mode = HelperMode.snake_case
    TEST_0 = ListItem()
    TEST_1 = ListItem()
    TEST_2 = ListItem()
    TEST_3 = ListItem()


class ChangeLink(Helper):
    mode = HelperMode.snake_case
    CHANGE_0 = ListItem()
