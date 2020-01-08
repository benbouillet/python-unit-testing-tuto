from src.functions import maxinlist
from pytest import mark

@mark.feature_engineering
def test_maxinlist_returns_max():
    input_list = [1, 4, 125, 94, 843, 42]
    list_max = 843
    assert maxinlist(input_list) == list_max
