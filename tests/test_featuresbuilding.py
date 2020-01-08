import pytest
import pandas as pd
from src.features.feat_functions import maxslopeDetection
from pytest import mark

@mark.feature_engineering
class maxslopeDetectionTests:
    def test_returns_macslope(self):
        input_list = pd.DataFrame([2, 5, 16, 8, 3])
        output_list = 11
        assert output_list == maxslopeDetection(input_list)

    def test_returns_asserterror_if_text_in_input(self):
        input_text = "this is a text string"
        with pytest.raises(AssertionError):
           maxslopeDetection(input_text)

@mark.bound_to_fail
class boundToFailTests:
    def test_returns_asserterror_if_int_input(self):
        input_int = 3
        with pytest.raises(AssertionError):
            maxslopeDetection(input_int)

def returnsTranspose(df):
    return df.transpose()

@mark.feature_engineering
class withDatasetTests:
    def test_returns_df_shape(self):
        input_df = pd.read_csv('tests/data/sample_df_10x10.csv', sep=';')
        output_df = input_df.transpose()
        assert output_df.equals(returnsTranspose(input_df))

