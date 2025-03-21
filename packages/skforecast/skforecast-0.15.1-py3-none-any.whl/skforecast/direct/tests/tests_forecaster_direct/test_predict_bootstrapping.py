# Unit test predict_bootstrapping ForecasterDirect
# ==============================================================================
import re
import pytest
import numpy as np
import pandas as pd
from sklearn.exceptions import NotFittedError
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from lightgbm import LGBMRegressor

from skforecast.preprocessing import RollingFeatures
from skforecast.preprocessing import TimeSeriesDifferentiator
from skforecast.direct import ForecasterDirect

# Fixtures
from .fixtures_forecaster_direct import y
from .fixtures_forecaster_direct import exog
from .fixtures_forecaster_direct import exog_predict
from .fixtures_forecaster_direct import data  # to test results when using differentiation


def test_predict_NotFittedError_when_fitted_is_False():
    """
    Test NotFittedError is raised when fitted is False.
    """
    forecaster = ForecasterDirect(LinearRegression(), lags=3, steps=5)

    err_msg = re.escape(
        "This Forecaster instance is not fitted yet. Call `fit` with "
        "appropriate arguments before using predict."
    )
    with pytest.raises(NotFittedError, match = err_msg):
        forecaster.predict_bootstrapping(steps=5)


def test_predict_bootstrapping_ValueError_when_not_in_sample_residuals_for_some_step():
    """
    Test ValueError is raised when use_in_sample_residuals=True but there is no
    residuals for some step.
    """
    forecaster = ForecasterDirect(LinearRegression(), lags=3, steps=2)
    forecaster.fit(y=pd.Series(np.arange(10)), store_in_sample_residuals=True)
    forecaster.in_sample_residuals_ = {2: np.array([1, 2, 3])}

    err_msg = re.escape(
        f"`forecaster.in_sample_residuals_` doesn't contain residuals for steps: "
        f"{set([1, 2]) - set(forecaster.in_sample_residuals_.keys())}."
    )
    with pytest.raises(ValueError, match = err_msg):
        forecaster.predict_bootstrapping(
            steps=None, use_in_sample_residuals=True, use_binned_residuals=False
        )


@pytest.mark.parametrize("use_binned_residuals", [True, False], 
                         ids=lambda binned: f'use_binned_residuals: {binned}')
def test_predict_bootstrapping_ValueError_when_out_sample_residuals_is_None(use_binned_residuals):
    """
    Test ValueError is raised when use_in_sample_residuals=False and
    out sample residuals is None.
    """
    forecaster = ForecasterDirect(LinearRegression(), lags=3, steps=2)
    forecaster.fit(y=pd.Series(np.arange(10)), store_in_sample_residuals=True)

    if use_binned_residuals:
        literal = "out_sample_residuals_by_bin_"
    else:
        literal = "out_sample_residuals_"

    err_msg = re.escape(
        f"`forecaster.{literal}` is either None or empty. Use "
        f"`use_in_sample_residuals = True` or the `set_out_sample_residuals()` "
        f"method before predicting."
    )
    with pytest.raises(ValueError, match = err_msg):
        forecaster.predict_bootstrapping(
            steps=1, use_in_sample_residuals=False, use_binned_residuals=use_binned_residuals
        )


def test_predict_bootstrapping_ValueError_when_not_out_sample_residuals_for_all_steps_predicted():
    """
    Test ValueError is raised when use_in_sample_residuals=False and
    forecaster.out_sample_residuals_ is not available for all steps predicted.
    """
    forecaster = ForecasterDirect(LinearRegression(), lags=3, steps=3)
    forecaster.fit(y=pd.Series(np.arange(15)), store_in_sample_residuals=True)
    residuals = {
        2: np.array([1, 2, 3, 4, 5]), 
        3: np.array([1, 2, 3, 4, 5])
    }
    forecaster.out_sample_residuals_ = residuals

    err_msg = re.escape(
        f"`forecaster.out_sample_residuals_` doesn't contain residuals for steps: "
        f"{set([1, 2]) - set(forecaster.out_sample_residuals_.keys())}. "
        f"Use method `set_out_sample_residuals()`."
    )
    with pytest.raises(ValueError, match = err_msg):
        forecaster.predict_bootstrapping(
            steps=[1, 2], use_in_sample_residuals=False, use_binned_residuals=False
        )


def test_predict_bootstrapping_ValueError_when_step_out_sample_residuals_value_is_None():
    """
    Test ValueError is raised when use_in_sample_residuals=False and
    forecaster.out_sample_residuals_ has a step with a None.
    """
    forecaster = ForecasterDirect(LinearRegression(), lags=3, steps=3)
    forecaster.fit(y=pd.Series(np.arange(15)), store_in_sample_residuals=True)
    forecaster.out_sample_residuals_ = {
        1: np.array([1, 2, 3, 4, 5]),
        2: np.array([1, 2, 3, 4, 5]),
        3: None
    }
    err_msg = re.escape(
        "Residuals for step 3 are None. Check `forecaster.out_sample_residuals_`."
    )
    with pytest.raises(ValueError, match = err_msg):
        forecaster.predict_bootstrapping(
            steps=3, use_in_sample_residuals=False, use_binned_residuals=False
        )


@pytest.mark.parametrize("steps", [2, [1, 2], None], 
                         ids=lambda steps: f'steps: {steps}')
def test_predict_bootstrapping_output_when_forecaster_is_LinearRegression_steps_is_2_in_sample_residuals_True_exog_and_transformer(steps):
    """
    Test output of predict_bootstrapping when regressor is LinearRegression,
    2 steps are predicted, using in-sample residuals, exog is included and both
    inputs are transformed.
    """
    forecaster = ForecasterDirect(
                     regressor        = LinearRegression(),
                     steps            = 2,
                     lags             = 3,
                     transformer_y    = StandardScaler(),
                     transformer_exog = StandardScaler(),
                 )
    forecaster.fit(y=y, exog=exog, store_in_sample_residuals=True)
    results = forecaster.predict_bootstrapping(
        steps=steps, exog=exog_predict, n_boot=4, 
        use_in_sample_residuals=True, use_binned_residuals=False
    )

    expected = pd.DataFrame(
                   data = np.array([
                              [0.7319542342426019, 0.6896870991312363, 0.2024868918354829, 0.5468555312708429],
                              [0.13621073709672699, 0.29541488852202646, 0.5160668468937661, 0.33416280223011985]
                          ]),
                   columns = [f"pred_boot_{i}" for i in range(4)],
                   index   = pd.RangeIndex(start=50, stop=52)
               )
    
    pd.testing.assert_frame_equal(expected, results)


def test_predict_bootstrapping_output_when_forecaster_is_LinearRegression_steps_is_2_in_sample_residuals_False_exog_and_transformer():
    """
    Test output of predict_bootstrapping when regressor is LinearRegression,
    2 steps are predicted, using in-sample residuals, exog is included and both
    inputs are transformed.
    """
    forecaster = ForecasterDirect(
                     regressor        = LinearRegression(),
                     steps            = 2,
                     lags             = 3,
                     transformer_y    = StandardScaler(),
                     transformer_exog = StandardScaler(),
                 )
    forecaster.fit(y=y, exog=exog, store_in_sample_residuals=True)
    forecaster.out_sample_residuals_ = forecaster.in_sample_residuals_
    results = forecaster.predict_bootstrapping(
        steps=2, exog=exog_predict, n_boot=4, 
        use_in_sample_residuals=False, use_binned_residuals=False
    )
    
    expected = pd.DataFrame(
                   data = np.array([
                              [0.7319542342426019, 0.6896870991312363, 0.2024868918354829, 0.5468555312708429],
                              [0.13621073709672699, 0.29541488852202646, 0.5160668468937661, 0.33416280223011985]
                          ]),
                   columns = [f"pred_boot_{i}" for i in range(4)],
                   index   = pd.RangeIndex(start=50, stop=52)
               )
    
    pd.testing.assert_frame_equal(expected, results)


def test_predict_bootstrapping_output_when_forecaster_is_LinearRegression_steps_is_2_in_sample_residuals_fixed():
    """
    Test output of predict_bootstrapping when regressor is LinearRegression,
    2 steps are predicted, using in-sample residuals that are fixed.
    """
    forecaster = ForecasterDirect(
                     regressor = LinearRegression(),
                     steps     = 2,
                     lags      = 3
                 )
    forecaster.fit(y=y, exog=exog, store_in_sample_residuals=True)
    forecaster.in_sample_residuals_ = {
        1: pd.Series([1, 1, 1, 1, 1, 1, 1]),
        2: pd.Series([5, 5, 5, 5, 5, 5, 5])
    }
    results = forecaster.predict_bootstrapping(
        steps=2, exog=exog_predict, n_boot=4, 
        use_in_sample_residuals=True, use_binned_residuals=False
    )
    
    expected = pd.DataFrame(
                   data = np.array([[1.67523588, 1.67523588, 1.67523588, 1.67523588],
                                    [5.38024988, 5.38024988, 5.38024988, 5.38024988]]),
                   columns = [f"pred_boot_{i}" for i in range(4)],
                   index   = pd.RangeIndex(start=50, stop=52)
               )
    
    pd.testing.assert_frame_equal(expected, results)


def test_predict_bootstrapping_output_when_forecaster_is_LinearRegression_and_differentiation_is_1_steps_1():
    """
    Test output of predict_bootstrapping when regressor is LinearRegression and
    differentiation=1 and steps=1.
    """
    # Data differentiated
    differentiator = TimeSeriesDifferentiator(order=1)
    data_diff = differentiator.fit_transform(data.to_numpy())
    data_diff = pd.Series(data_diff, index=data.index).dropna()

    # Simulated exogenous variable
    rng = np.random.default_rng(9876)
    exog = pd.Series(
        rng.normal(loc=0, scale=1, size=len(data)), index=data.index, name='exog'
    )
    exog_diff = exog.iloc[1:]
    end_train = '2003-03-01 23:59:00'

    forecaster_1 = ForecasterDirect(regressor=LinearRegression(), steps=1, lags=15)
    forecaster_1.fit(
        y=data_diff.loc[:end_train], exog=exog_diff.loc[:end_train], store_in_sample_residuals=True
    )
    boot_predictions_diff = forecaster_1.predict_bootstrapping(
        exog=exog_diff.loc[end_train:], n_boot=10, use_in_sample_residuals=True, use_binned_residuals=False
    )

    # Revert the differentiation
    last_value_train = data.loc[:end_train].iloc[[-1]]
    boot_predictions_1 = boot_predictions_diff.copy()
    boot_predictions_1.loc[last_value_train.index[0]] = last_value_train.values[0]
    boot_predictions_1 = boot_predictions_1.sort_index()
    boot_predictions_1 = boot_predictions_1.cumsum(axis=0).iloc[1:,]
    boot_predictions_1 = boot_predictions_1.asfreq('MS')
    
    forecaster_2 = ForecasterDirect(regressor=LinearRegression(), steps=1, lags=15, differentiation=1)
    forecaster_2.fit(
        y=data.loc[:end_train], exog=exog.loc[:end_train], store_in_sample_residuals=True
    )
    boot_predictions_2 = forecaster_2.predict_bootstrapping(
        exog=exog_diff.loc[end_train:], n_boot=10, use_in_sample_residuals=True, use_binned_residuals=False
    )
    
    pd.testing.assert_frame_equal(boot_predictions_1, boot_predictions_2)


def test_predict_bootstrapping_output_when_forecaster_is_LinearRegression_and_differentiation_is_1_steps_10():
    """
    Test output of predict_bootstrapping when regressor is LinearRegression and
    differentiation=1 and steps=10.
    """
    # Data differentiated
    differentiator = TimeSeriesDifferentiator(order=1)
    data_diff = differentiator.fit_transform(data.to_numpy())
    data_diff = pd.Series(data_diff, index=data.index).dropna()

    # Simulated exogenous variable
    rng = np.random.default_rng(9876)
    exog = pd.Series(
        rng.normal(loc=0, scale=1, size=len(data)), index=data.index, name='exog'
    )
    exog_diff = exog.iloc[1:]
    end_train = '2003-03-01 23:59:00'

    forecaster_1 = ForecasterDirect(regressor=LinearRegression(), steps=10, lags=15)
    forecaster_1.fit(
        y=data_diff.loc[:end_train], exog=exog_diff.loc[:end_train], store_in_sample_residuals=True
    )
    boot_predictions_diff = forecaster_1.predict_bootstrapping(
        exog=exog_diff.loc[end_train:], n_boot=10, use_in_sample_residuals=True, use_binned_residuals=False
    )
    last_value_train = data.loc[:end_train].iloc[[-1]]
    boot_predictions_1 = boot_predictions_diff.copy()
    boot_predictions_1.loc[last_value_train.index[0]] = last_value_train.values[0]
    boot_predictions_1 = boot_predictions_1.sort_index()
    boot_predictions_1 = boot_predictions_1.cumsum(axis=0).iloc[1:,]
    boot_predictions_1 = boot_predictions_1.asfreq('MS')
    
    forecaster_2 = ForecasterDirect(regressor=LinearRegression(), steps=10, lags=15, differentiation=1)
    forecaster_2.fit(
        y=data.loc[:end_train], exog=exog.loc[:end_train], store_in_sample_residuals=True
    )
    boot_predictions_2 = forecaster_2.predict_bootstrapping(
        exog=exog_diff.loc[end_train:], n_boot=10, use_in_sample_residuals=True, use_binned_residuals=False
    )
    
    pd.testing.assert_frame_equal(boot_predictions_1, boot_predictions_2)


def test_predict_bootstrapping_output_when_window_features_steps_1():
    """
    Test output of predict_bootstrapping when regressor is LGBMRegressor and
    4 steps ahead are predicted with exog and window features using in-sample residuals
    with steps=1.
    """
    y_datetime = y.copy()
    y_datetime.index = pd.date_range(start='2001-01-01', periods=len(y), freq='D')
    exog_datetime = exog.copy()
    exog_datetime.index = pd.date_range(start='2001-01-01', periods=len(exog), freq='D')
    exog_predict_datetime = exog_predict.copy()
    exog_predict_datetime.index = pd.date_range(start='2001-02-20', periods=len(exog_predict), freq='D')
    
    rolling = RollingFeatures(stats=['mean', 'sum'], window_sizes=[3, 5])
    forecaster = ForecasterDirect(
        LGBMRegressor(verbose=-1, random_state=123), steps=1, lags=3, window_features=rolling
    )
    forecaster.fit(y=y_datetime, exog=exog_datetime, store_in_sample_residuals=True)
    results = forecaster.predict_bootstrapping(
        n_boot=10, exog=exog_predict_datetime, 
        use_in_sample_residuals=True, use_binned_residuals=False
    )

    expected = pd.DataFrame(
                   data    = np.array(
                                 [[0.61866004, 0.42315364, 0.54459359, 0.6327955 , 0.29239436,
                                   0.46729748, 0.3783451 , 0.18128852, 0.71765599, 0.58209158]]
                             ),
                   columns = [f"pred_boot_{i}" for i in range(10)],
                   index   = pd.date_range(start='2001-02-20', periods=1, freq='D')
               )

    pd.testing.assert_frame_equal(expected, results)


def test_predict_bootstrapping_output_when_window_features_steps_10():
    """
    Test output of predict_bootstrapping when regressor is LGBMRegressor and
    4 steps ahead are predicted with exog and window features using in-sample residuals
    with steps=10.
    """
    y_datetime = y.copy()
    y_datetime.index = pd.date_range(start='2001-01-01', periods=len(y), freq='D')
    exog_datetime = exog.copy()
    exog_datetime.index = pd.date_range(start='2001-01-01', periods=len(exog), freq='D')
    exog_predict_datetime = exog_predict.copy()
    exog_predict_datetime.index = pd.date_range(start='2001-02-20', periods=len(exog_predict), freq='D')
    
    rolling = RollingFeatures(stats=['mean', 'sum'], window_sizes=[3, 5])
    forecaster = ForecasterDirect(
        LGBMRegressor(verbose=-1, random_state=123), steps=10, lags=3, window_features=rolling
    )
    forecaster.fit(y=y_datetime, exog=exog_datetime, store_in_sample_residuals=True)
    results = forecaster.predict_bootstrapping(
        n_boot=10, exog=exog_predict_datetime, 
        use_in_sample_residuals=True, use_binned_residuals=False
    )

    expected = pd.DataFrame(
                   data    = np.array(
                                 [[0.42310646, 0.63097612, 0.36178866, 0.9807642 , 0.89338916,
                                   0.43857224, 0.39804426, 0.72904971, 0.17545176, 0.72904971],
                                  [0.53155137, 0.31226122, 0.72445532, 0.50183668, 0.72445532,
                                   0.73799541, 0.42583029, 0.31226122, 0.89338916, 0.94416002],
                                  [0.68482974, 0.32295891, 0.18249173, 0.73799541, 0.73799541,
                                   0.42635131, 0.31226122, 0.39804426, 0.84943179, 0.4936851 ],
                                  [0.0596779 , 0.09210494, 0.61102351, 0.1156184 , 0.42583029,
                                   0.18249173, 0.94416002, 0.42635131, 0.73799541, 0.36178866],
                                  [0.89338916, 0.17545176, 0.17545176, 0.39804426, 0.39211752,
                                   0.36178866, 0.39211752, 0.63097612, 0.61102351, 0.73799541],
                                  [0.61102351, 0.34317802, 0.73799541, 0.36178866, 0.43857224,
                                   0.42635131, 0.53182759, 0.41482621, 0.18249173, 0.43086276],
                                  [0.63097612, 0.86630916, 0.4936851 , 0.31728548, 0.22826323,
                                   0.53155137, 0.17545176, 0.31728548, 0.53155137, 0.89338916],
                                  [0.09210494, 0.72445532, 0.36178866, 0.62395295, 0.29371405,
                                   0.41482621, 0.48303426, 0.72445532, 0.09210494, 0.09210494],
                                  [0.43086276, 0.73799541, 0.36178866, 0.4936851 , 0.48303426,
                                   0.84943179, 0.42635131, 0.62395295, 0.48303426, 0.53182759],
                                  [0.94416002, 0.32295891, 0.63097612, 0.39804426, 0.62395295,
                                   0.73799541, 0.22826323, 0.43370117, 0.94416002, 0.09210494]]
                             ),
                   columns = [f"pred_boot_{i}" for i in range(10)],
                   index   = pd.date_range(start='2001-02-20', periods=10, freq='D')
               )

    pd.testing.assert_frame_equal(expected, results)


def test_predict_bootstrapping_output_when_recommended_n_boot():
    """
    Test output of predict_bootstrapping when regressor is LinearRegression,
    5 steps are predicted, using recommended n_boot.
    """
    forecaster = ForecasterDirect(
                     regressor = LinearRegression(),
                     steps     = 5,
                     lags      = 5
                 )
    forecaster.fit(y=y, store_in_sample_residuals=True)

    recommended_n_boot = 5
    for k, v in forecaster.in_sample_residuals_.items():
        forecaster.in_sample_residuals_[k] = v[:recommended_n_boot]
        
    results = forecaster.predict_bootstrapping(
        steps=5, n_boot=recommended_n_boot, 
        use_in_sample_residuals=True, use_binned_residuals=False
    )
    
    expected = pd.DataFrame(
                   data = np.array([
                              [0.48721565, 1.02484437, 0.61905973, 0.56793914, 0.5081311 ],
                              [0.9590885 , 0.61539607, 0.49375752, 0.43661094, 0.37422496],
                              [0.58708183, 0.38215125, 0.35461588, 0.3501964 , 0.77520526],
                              [0.38407239, 0.29983844, 0.29727213, 0.73461524, 0.51531151],
                              [0.29604462, 0.28561801, 0.73504556, 0.52313719, 0.05451923]
                          ]),
                   columns = [f"pred_boot_{i}" for i in range(5)],
                   index   = pd.RangeIndex(start=50, stop=55)
               )
    
    pd.testing.assert_frame_equal(expected, results)


def test_predict_bootstrapping_output_when_recommended_n_boot_binned_residuals():
    """
    Test output of predict_bootstrapping when regressor is LinearRegression,
    5 steps are predicted, using recommended n_boot and binned residuals.
    """
    forecaster = ForecasterDirect(
                     regressor = LinearRegression(),
                     steps     = 5,
                     lags      = 5
                 )
    forecaster.fit(y=y, store_in_sample_residuals=True)

    recommended_n_boot = 5
    for k, v in forecaster.in_sample_residuals_by_bin_.items():
        forecaster.in_sample_residuals_by_bin_[k] = v[:recommended_n_boot]
        
    results = forecaster.predict_bootstrapping(
        steps=5, n_boot=recommended_n_boot, 
        use_in_sample_residuals=True, use_binned_residuals=True
    )
    
    expected = pd.DataFrame(
                   data = np.array([
                              [0.0871959 , 0.42151611, 0.31312881, 0.93930242, 0.50375378],
                              [0.41707327, 0.42057899, 0.17540809, 0.60089178, 0.87562183],
                              [0.40475029, 0.4001072 , 0.17872038, 0.24435799, 0.31957347],
                              [0.42421302, 0.73008654, 0.43387046, 0.38206866, 0.22417746],
                              [0.43065853, 0.73653206, 0.44031597, 0.38851417, 0.23062297]
                          ]),
                   columns = [f"pred_boot_{i}" for i in range(5)],
                   index   = pd.RangeIndex(start=50, stop=55)
               )
    
    pd.testing.assert_frame_equal(expected, results)
