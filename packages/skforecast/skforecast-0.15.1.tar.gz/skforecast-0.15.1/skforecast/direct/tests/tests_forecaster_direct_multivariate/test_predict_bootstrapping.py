# Unit test predict_bootstrapping ForecasterDirectMultiVariate
# ==============================================================================
import re
import pytest
import numpy as np
import pandas as pd
from sklearn.exceptions import NotFittedError
from sklearn.linear_model import LinearRegression
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import OneHotEncoder
from lightgbm import LGBMRegressor

from skforecast.preprocessing import RollingFeatures
from skforecast.preprocessing import TimeSeriesDifferentiator
from skforecast.direct import ForecasterDirectMultiVariate

# Fixtures
from .fixtures_forecaster_direct_multivariate import series
from .fixtures_forecaster_direct_multivariate import exog
from .fixtures_forecaster_direct_multivariate import exog_predict
from .fixtures_forecaster_direct_multivariate import data  # to test results when using differentiation

transformer_exog = ColumnTransformer(
                       [('scale', StandardScaler(), ['exog_1']),
                        ('onehot', OneHotEncoder(), ['exog_2'])],
                       remainder = 'passthrough',
                       verbose_feature_names_out = False
                   )


def test_predict_NotFittedError_when_fitted_is_False():
    """
    Test NotFittedError is raised when fitted is False.
    """
    forecaster = ForecasterDirectMultiVariate(
        LinearRegression(), level='l1', lags=3, steps=3
    )

    err_msg = re.escape(
        "This Forecaster instance is not fitted yet. Call `fit` with "
        "appropriate arguments before using predict."
    )
    with pytest.raises(NotFittedError, match = err_msg):
        forecaster.predict_bootstrapping(steps=5)


def test_predict_bootstrapping_ValueError_when_not_in_sample_residuals_for_some_step():
    """
    Test ValueError is raised when in_sample_residuals=True but there is no
    residuals for some step.
    """
    forecaster = ForecasterDirectMultiVariate(
        LinearRegression(), level='l1', lags=3, steps=2
    )
    forecaster.fit(series=series, store_in_sample_residuals=True)
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
    forecaster.out_sample_residuals_ is None.
    """
    forecaster = ForecasterDirectMultiVariate(
        LinearRegression(), level='l1', lags=3, steps=2
    )
    forecaster.fit(series=series, store_in_sample_residuals=True)

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
    forecaster = ForecasterDirectMultiVariate(
        LinearRegression(), level='l1', steps=3, lags=3
    )
    forecaster.fit(series=series, store_in_sample_residuals=True)
    residuals = {2: np.array([1, 2, 3, 4, 5]), 
                 3: np.array([1, 2, 3, 4, 5])}
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


@pytest.mark.parametrize("transformer_series", 
                         [None, StandardScaler()],
                         ids = lambda tr: f'transformer_series type: {type(tr)}')
def test_predict_bootstrapping_ValueError_when_step_out_sample_residuals_value_is_None(transformer_series):
    """
    Test ValueError is raised when use_in_sample_residuals=False and
    forecaster.out_sample_residuals_ has a step with a None.
    """
    forecaster = ForecasterDirectMultiVariate(
        LinearRegression(), level='l1', steps=3, lags=3, transformer_series=transformer_series
    )
    forecaster.fit(series=series, store_in_sample_residuals=True)
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
    forecaster = ForecasterDirectMultiVariate(
                     regressor          = LinearRegression(),
                     steps              = 2,
                     level              = 'l1',
                     lags               = 3,
                     transformer_series = StandardScaler(),
                     transformer_exog   = transformer_exog
                 )
    forecaster.fit(series=series, exog=exog, store_in_sample_residuals=True)
    results = forecaster.predict_bootstrapping(
        steps=steps, exog=exog_predict, n_boot=4, 
        use_in_sample_residuals=True, use_binned_residuals=False
    )
    
    expected = pd.DataFrame(
                   data = np.array([[0.68370403, 0.61428329, 0.38628787, 0.46804785],
                                    [0.23010355, 0.19812106, 0.62028743, 0.25357764]]),
                   columns = [f"pred_boot_{i}" for i in range(4)],
                   index   = pd.RangeIndex(start=50, stop=52)
               )
    expected.insert(0, 'level', np.tile(['l1'], 2))
    
    pd.testing.assert_frame_equal(expected, results)


def test_predict_bootstrapping_output_when_forecaster_is_LinearRegression_steps_is_2_in_sample_residuals_False_exog_and_transformer():
    """
    Test output of predict_bootstrapping when regressor is LinearRegression,
    2 steps are predicted, using in-sample residuals, exog is included and both
    inputs are transformed.
    """
    forecaster = ForecasterDirectMultiVariate(
                     regressor          = LinearRegression(),
                     steps              = 2,
                     level              = 'l1',
                     lags               = 3,
                     transformer_series = StandardScaler(),
                     transformer_exog   = transformer_exog
                 )
    forecaster.fit(series=series, exog=exog, store_in_sample_residuals=True)
    forecaster.out_sample_residuals_ = forecaster.in_sample_residuals_
    results = forecaster.predict_bootstrapping(
        steps=2, exog=exog_predict, n_boot=4, 
        use_in_sample_residuals=False, use_binned_residuals=False
    )
    
    expected = pd.DataFrame(
                   data = np.array([[0.68370403, 0.61428329, 0.38628787, 0.46804785],
                                    [0.23010355, 0.19812106, 0.62028743, 0.25357764]]),
                   columns = [f"pred_boot_{i}" for i in range(4)],
                   index   = pd.RangeIndex(start=50, stop=52)
               )
    expected.insert(0, 'level', np.tile(['l1'], 2))
    
    pd.testing.assert_frame_equal(expected, results)


def test_predict_bootstrapping_output_when_forecaster_is_LinearRegression_steps_is_2_in_sample_residuals_fixed():
    """
    Test output of predict_bootstrapping when regressor is LinearRegression,
    2 steps are predicted, using in-sample residuals that are fixed.
    """
    forecaster = ForecasterDirectMultiVariate(
                     regressor          = LinearRegression(),
                     steps              = 2,
                     level              = 'l1',
                     lags               = 3,
                     transformer_series = None
                 )
    forecaster.fit(series=series, exog=exog['exog_1'], store_in_sample_residuals=True)
    forecaster.in_sample_residuals_ = {1: pd.Series([1, 1, 1, 1, 1, 1, 1]),
                                       2: pd.Series([5, 5, 5, 5, 5, 5, 5])}
    results = forecaster.predict_bootstrapping(
        steps=2, exog=exog_predict['exog_1'], n_boot=4, 
        use_in_sample_residuals=True, use_binned_residuals=False
    )
    
    expected = pd.DataFrame(
                   data = np.array([[1.57457831, 1.57457831, 1.57457831, 1.57457831],
                                    [5.3777698 , 5.3777698 , 5.3777698 , 5.3777698 ]]),
                   columns = [f"pred_boot_{i}" for i in range(4)],
                   index   = pd.RangeIndex(start=50, stop=52)
               )
    expected.insert(0, 'level', np.tile(['l1'], 2))
    
    pd.testing.assert_frame_equal(expected, results)


def test_predict_bootstrapping_output_when_regressor_is_LinearRegression_with_exog_and_differentiation_is_1_steps_1():
    """
    Test predict_bootstrapping output when using LinearRegression as regressor 
    and differentiation=1 and steps=1.
    """

    arr = data.to_numpy(copy=True)
    series_2 = pd.DataFrame(
        {'l1': arr,
         'l2': arr * 1.6},
        index=data.index
    )

    # Data differentiated
    differentiator = TimeSeriesDifferentiator(order=1)
    series_diff = pd.DataFrame(
        {'l1': differentiator.fit_transform(arr),
         'l2': differentiator.fit_transform(arr * 1.6)},
        index=data.index
    ).dropna()

    # Simulated exogenous variable
    rng = np.random.default_rng(9876)
    exog = pd.Series(
        rng.normal(loc=0, scale=1, size=len(data)), index=data.index, name='exog'
    )
    exog_diff = exog.iloc[1:]
    end_train = '2003-03-01 23:59:00'

    forecaster_1 = ForecasterDirectMultiVariate(
        regressor=LinearRegression(), level='l1', steps=1, lags=15, transformer_series=None
    )
    forecaster_1.fit(
        series=series_diff.loc[:end_train], exog=exog_diff.loc[:end_train], store_in_sample_residuals=True
    )
    boot_predictions_diff = forecaster_1.predict_bootstrapping(
        exog=exog_diff.loc[end_train:], n_boot=10, use_in_sample_residuals=True, use_binned_residuals=False
    )

    # Revert the differentiation
    last_value_train = series_2[['l1']].loc[:end_train].iloc[[-1]]
    boot_predictions_1 = boot_predictions_diff.drop(columns='level').copy()
    last_value_train = pd.DataFrame(
        np.full(shape=(1, 10), fill_value=last_value_train.values[0]), 
        columns = boot_predictions_1.columns, 
        index   = pd.date_range(last_value_train.index[0], periods=1)
    )
    boot_predictions_1 = pd.concat([last_value_train, boot_predictions_1])    
    boot_predictions_1 = boot_predictions_1.sort_index()
    boot_predictions_1 = boot_predictions_1.cumsum(axis=0).iloc[1:,]
    boot_predictions_1 = boot_predictions_1.asfreq('MS')
    boot_predictions_1.insert(0, 'level', np.tile(['l1'], 1))

    forecaster_2 = ForecasterDirectMultiVariate(
        regressor=LinearRegression(), level='l1', steps=1, lags=15, transformer_series=None, differentiation=1
    )
    forecaster_2.fit(
        series=series_2.loc[:end_train], exog=exog.loc[:end_train], store_in_sample_residuals=True
    )
    boot_predictions_2 = forecaster_2.predict_bootstrapping(
        exog=exog_diff.loc[end_train:], n_boot=10, use_in_sample_residuals=True, use_binned_residuals=False
    )

    pd.testing.assert_frame_equal(boot_predictions_1, boot_predictions_2)


def test_predict_bootstrapping_output_when_regressor_is_LinearRegression_with_exog_and_differentiation_is_1_steps_10():
    """
    Test predict_bootstrapping output when using LinearRegression as regressor 
    and differentiation=1 and steps=10.
    """

    arr = data.to_numpy(copy=True)
    series_2 = pd.DataFrame(
        {'l1': arr,
         'l2': arr * 1.6},
        index=data.index
    )

    # Data differentiated
    differentiator = TimeSeriesDifferentiator(order=1)
    series_diff = pd.DataFrame(
        {'l1': differentiator.fit_transform(arr),
         'l2': differentiator.fit_transform(arr * 1.6)},
        index=data.index
    ).dropna()

    # Simulated exogenous variable
    rng = np.random.default_rng(9876)
    exog = pd.Series(
        rng.normal(loc=0, scale=1, size=len(data)), index=data.index, name='exog'
    )
    exog_diff = exog.iloc[1:]
    end_train = '2003-03-01 23:59:00'

    forecaster_1 = ForecasterDirectMultiVariate(
        regressor=LinearRegression(), level='l1', steps=10, lags=15, transformer_series=None
    )
    forecaster_1.fit(
        series=series_diff.loc[:end_train], exog=exog_diff.loc[:end_train], store_in_sample_residuals=True
    )
    boot_predictions_diff = forecaster_1.predict_bootstrapping(
        exog=exog_diff.loc[end_train:], n_boot=10, use_in_sample_residuals=True, use_binned_residuals=False
    )

    # Revert the differentiation
    last_value_train = series_2[['l1']].loc[:end_train].iloc[[-1]]
    boot_predictions_1 = boot_predictions_diff.drop(columns='level').copy()
    last_value_train = pd.DataFrame(
        np.full(shape=(1, 10), fill_value=last_value_train.values[0]), 
        columns = boot_predictions_1.columns, 
        index   = pd.date_range(last_value_train.index[0], periods=1)
    )
    boot_predictions_1 = pd.concat([last_value_train, boot_predictions_1])    
    boot_predictions_1 = boot_predictions_1.sort_index()
    boot_predictions_1 = boot_predictions_1.cumsum(axis=0).iloc[1:,]
    boot_predictions_1 = boot_predictions_1.asfreq('MS')
    boot_predictions_1.insert(0, 'level', np.tile(['l1'], 10))

    forecaster_2 = ForecasterDirectMultiVariate(
        regressor=LinearRegression(), level='l1', steps=10, lags=15, transformer_series=None, differentiation=1
    )
    forecaster_2.fit(
        series=series_2.loc[:end_train], exog=exog.loc[:end_train], store_in_sample_residuals=True
    )
    boot_predictions_2 = forecaster_2.predict_bootstrapping(
        exog=exog_diff.loc[end_train:], n_boot=10, use_in_sample_residuals=True, use_binned_residuals=False
    )

    pd.testing.assert_frame_equal(boot_predictions_1, boot_predictions_2)


def test_predict_output_when_window_features_steps_1():
    """
    Test output of predict when regressor is LGBMRegressor and window features
    with steps=1.
    """

    rolling = RollingFeatures(stats=['mean', 'sum'], window_sizes=[3, 5])
    forecaster = ForecasterDirectMultiVariate(
        regressor=LGBMRegressor(verbose=-1, random_state=123), level='l1', 
        steps=1, lags=5, window_features=rolling
    )
    forecaster.fit(series=series, exog=exog['exog_1'], store_in_sample_residuals=True)
    predictions = forecaster.predict_bootstrapping(
        n_boot=10, exog=exog_predict['exog_1'], use_in_sample_residuals=True, use_binned_residuals=False
    )

    expected = pd.DataFrame(
                   data    = np.array(
                                 [[0.60290414, 0.4125675 , 0.49927603, 0.64983046, 0.49009973,
                                   0.48971982, 0.40030064, 0.3430941 , 0.82287993, 0.67578235]]
                             ),
                   columns = [f"pred_boot_{i}" for i in range(10)],
                   index   = pd.RangeIndex(start=50, stop=51)
               )
    expected.insert(0, 'level', np.tile(['l1'], 1))
    
    pd.testing.assert_frame_equal(predictions, expected)


def test_predict_output_when_window_features_steps_10():
    """
    Test output of predict when regressor is LGBMRegressor and window features
    with steps=10.
    """

    rolling = RollingFeatures(stats=['mean', 'sum'], window_sizes=[3, 5])
    forecaster = ForecasterDirectMultiVariate(
        regressor=LGBMRegressor(verbose=-1, random_state=123), level='l1', 
        steps=10, lags=5, window_features=rolling
    )
    forecaster.fit(series=series, exog=exog['exog_1'], store_in_sample_residuals=True)
    predictions = forecaster.predict_bootstrapping(
        n_boot=10, exog=exog_predict['exog_1'], use_in_sample_residuals=True, use_binned_residuals=False
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
                   index   = pd.RangeIndex(start=50, stop=60)
               )
    expected.insert(0, 'level', np.tile(['l1'], 10))
    
    pd.testing.assert_frame_equal(predictions, expected)


def test_predict_bootstrapping_output_when_recommended_n_boot():
    """
    Test output of predict_bootstrapping when regressor is LinearRegression,
    5 steps are predicted, using recommended n_boot.
    """
    forecaster = ForecasterDirectMultiVariate(
                     regressor = LinearRegression(),
                     level     = 'l1',
                     steps     = 5,
                     lags      = 5
                 )
    forecaster.fit(series=series, store_in_sample_residuals=True)

    recommended_n_boot = 5
    for k, v in forecaster.in_sample_residuals_.items():
        forecaster.in_sample_residuals_[k] = v[:recommended_n_boot]
        
    results = forecaster.predict_bootstrapping(
        steps=5, n_boot=recommended_n_boot, use_in_sample_residuals=True, use_binned_residuals=False
    )
    
    expected = pd.DataFrame(
                   data = np.array([
                              [0.47205022, 0.98950112, 0.68481511, 0.68584113, 0.59849854],
                              [0.80767016, 0.5800906 , 0.50603608, 0.39370766, 0.27603111],
                              [0.46384638, 0.39252358, 0.27605498, 0.18799982, 0.55115865],
                              [0.49217581, 0.3449488 , 0.30432267, 0.73228185, 0.52068247],
                              [0.23775143, 0.26042536, 0.70757427, 0.51939237, 0.07577542]
                          ]),
                   columns = [f"pred_boot_{i}" for i in range(5)],
                   index   = pd.RangeIndex(start=50, stop=55)
               )
    expected.insert(0, 'level', np.tile(['l1'], 5))
    
    pd.testing.assert_frame_equal(expected, results)


def test_predict_bootstrapping_output_when_recommended_n_boot_binned_residuals():
    """
    Test output of predict_bootstrapping when regressor is LinearRegression,
    5 steps are predicted, using recommended n_boot and binned residuals.
    """
    forecaster = ForecasterDirectMultiVariate(
                     regressor = LinearRegression(),
                     level     = 'l1',
                     steps     = 5,
                     lags      = 5
                 )
    forecaster.fit(series=series, store_in_sample_residuals=True)

    recommended_n_boot = 5
    for k, v in forecaster.in_sample_residuals_by_bin_.items():
        forecaster.in_sample_residuals_by_bin_[k] = v[:recommended_n_boot]
        
    results = forecaster.predict_bootstrapping(
        steps=5, n_boot=recommended_n_boot, use_in_sample_residuals=True, use_binned_residuals=True
    )
    
    expected = pd.DataFrame(
                   data = np.array([
                              [0.98950112, 0.68481511, 0.88114584, 0.7556436 , 0.97899051],
                              [0.75212361, 0.45230689, 0.62572451, 0.41465675, 0.26430958],
                              [0.30609163, 0.40967018, 0.42519328, 0.41910018, 0.38359395],
                              [0.03661046, 0.74549056, 0.28977873, 0.46779981, 0.60740805],
                              [0.48660788, 0.39926529, 0.64537401, 0.3644564 , 0.09744978]
                          ]),
                   columns = [f"pred_boot_{i}" for i in range(5)],
                   index   = pd.RangeIndex(start=50, stop=55)
               )
    expected.insert(0, 'level', np.tile(['l1'], 5))
    
    pd.testing.assert_frame_equal(expected, results)
