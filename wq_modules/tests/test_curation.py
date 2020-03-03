from wq_modules import utils


def test_file1_method1():
    dataset = [
        10, 12, 12, 13, 12, 11, 14, 13, 15, 10, 10, 10, 100,
        12, 14, 130, 12, 10, 10, 11, 12, 15, 12, 13, 12, 11,
        14, 13, 15, 10, 15, 12, 10, 14, 13, 15, 10]
    result_assert = [
        10, 12, 12, 13, 12, 11, 14, 13, 15, 10, 10, 10, None,
        12, 14, None, 12, 10, 10, 11, 12, 15, 12, 13, 12, 11,
        14, 13, 15, 10, 15, 12, 10, 14, 13, 15, 10]
    outlier_datapoints = utils.detect_outlier(dataset)
    new_dataset = []
    for e in dataset:
        if e in outlier_datapoints:
            new_dataset.append(None)
        else:
            new_dataset.append(e)
    assert new_dataset == result_assert
