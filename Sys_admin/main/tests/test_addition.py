from Sys_admin.main.src.addition import Addition


def test_calculate_result():
    test_calculate1 = Addition(10,20)
    test_calculate2 = Addition(100,2)
    test_calculate3 = Addition(-15,2)

    assert test_calculate1.calculate_result() == 30 ,"加法的计算结果函数错误"
    assert test_calculate2.calculate_result() == 102 ,"加法的计算结果函数错误"
    assert test_calculate3.calculate_result() == -13 ,"加法的计算结果函数错误"