import pytest
from time import sleep
import sys
import os

userinfo = [
    ('zhang san', 123),
    ('li si', 'password')
]

user = ['zhang wu', 'li liu']
password = [13579, 24680]

@pytest.fixture()
def login_user(request):
    user = request.param
    print(f"User Name is: {user}")
    return user

@pytest.fixture()
def login_pwd(request):
    pwd = request.param
    print(f"Password is: {pwd}")
    return pwd

@pytest.fixture(params="password", ids=[f"{i+1}-{x}" for i,x in enumerate("password")])
def pwds(request):
    print(f"\nparams of field is: {request.param}")
    return request.param

def test_testfixture_params(pwds):
    print(f"\ntest case: {pwds}")
    assert pwds == 'a'


@pytest.mark.parametrize("login_user,login_pwd", userinfo, indirect=['login_user', 'login_pwd'])
def test_1_param(login_user, login_pwd):
    print(f"User Name in Testing: [{login_user}], password is: [{login_pwd}]")

@pytest.mark.parametrize("login_user,login_pwd", userinfo, indirect=['login_user'])
def test_2_param(login_user, login_pwd):
    print(f"User Name in Testing: [{login_user}], password is: [{login_pwd}]")

@pytest.mark.parametrize("login_user,login_pwd", userinfo, indirect=True)
def test_one_param(login_user, login_pwd):
    print(f"User Name in Testing: [{login_user}], password is: [{login_pwd}]")


@pytest.mark.parametrize("login_pwd", password, indirect=True)
@pytest.mark.parametrize("login_user", user, indirect=True)
def test_two_param(login_user, login_pwd):
    print(f"User Name in Testing: [{login_user}], password is: [{login_pwd}]")

@pytest.mark.parametrize("login_user,login_pwd", userinfo, indirect=False)
def test_three_param(login_user, login_pwd):
    print(f"User Name in Testing: [{login_user}], password is: [{login_pwd}]")

@pytest.mark.parametrize("login_U,login_P", userinfo, indirect=False)
def test_four_param(login_U, login_P):
    print(f"User Name in Testing: [{login_U}], password is: [{login_P}]")

# Pytest.Fixture need parameters

@pytest.fixture
def my_fixture():

    def _method(a, b):
        return a*b

    return _method

def test_me(my_fixture):
    result1 = my_fixture(2, 3)
    assert result1 == 6

    result2 = my_fixture(4, 5)
    assert result2 == 20


@pytest.fixture
def my_fixture2(request):
    print("fixture in")
    print(request.fspath)
    print(request.path)
    print(request.module)
    print(request.cls)
    print(request.fixturename)
    print(request.fixturenames)
    request.applymarker(pytest.mark.slow)
    print(request.param_index)
    print(request.keywords)

    def finalizer_func():
        print("added finalizer func")

    request.addfinalizer(finalizer=finalizer_func)


    # config = request.config
    # print(f"Command line arguments: {config.option}")
    # print(f"INI file options: {config.getini('markers')}")
    yield request.param+1 # difference here !
    print("fixture out")
    

@pytest.fixture(name="ffffff")
def my_fixture3(request):
    print("fixture in")
    yield request.param+3 # difference here !
    print("fixture out")

# Indirect=True, will retrieve value from function/method named as in parameter.
@pytest.mark.parametrize("ffffff",[28], indirect=True)
def test_myfixture_f(ffffff):
    print(ffffff)

@pytest.mark.parametrize("my_fixture2", [28, 99], indirect=True)
def test_myfixture(request, my_fixture2):
    print(my_fixture2)
    print(request.getfixturevalue("my_fixture2"))

# Indirect=False, then will retrieve value from parameter itself, default as indirect=False
@pytest.mark.parametrize("my_fixture2",[28], indirect=False)
def test_myfixture_2(my_fixture2):
    print(my_fixture2)

@pytest.mark.parametrize("my_fixture2",[28])
def test_myfixture_3(my_fixture2):
    print(my_fixture2)

data = [{"url":"http://www.baidu.com","http":"get"}, {"url":"https://www.google.com","http":"post"}]

ids = ['get_baidu', 'post_google']

@pytest.fixture(params=data, ids=ids)
def f_function(request):
    print("fixture部分-url:{}".format(request.param['url']))
    print("fixture部分-http:{}".format(request.param['http']))
    return request.param

def test_add_by_func_2(f_function):
    print("测试用例:-url: {}".format(f_function['url']))
    print("测试用例:-http: {}".format(f_function['http']))


class User():
    def __init__(self, first_name: str, last_name: str):
        self.first_name = first_name
        self.last_name = last_name

    def create_full_name(self):
        return f'{self.first_name} {self.last_name}'


@pytest.fixture
def user(request):
    if request.param == 'normal_user':
        # Returns a normal user
        yield User(first_name='katherine', last_name='rose')
    if request.param == 'missing_details':
        # Returns a user without a last name
        yield User(first_name=' ', last_name='rose')

@pytest.fixture
def expected():
    return "xxxxx"

@pytest.mark.parametrize('user, expected', [('normal_user', 'katherine rose'),
                                            ('missing_details', TypeError)],
                         indirect=['user'])
def test_parametrize_user_full_name(user, expected):
    assert user.create_full_name() == expected


@pytest.mark.usefixtures("setup")
class TestTemp():
    
    @pytest.mark.parametrize("x", ["https://www.google.com", "https://www.csdn.com"], ids=["1", "2"])
    def test_portno(self, x):
        """
        Execute multiple cases with parallel mode: python -m pytest ./test_temp.py::TestTemp::test_portno -v -s -n=4
        """
        case_name = sys._getframe().f_code.co_name
        module_name = str(os.path.basename(__file__)).split('.')[0]

        driver = self.driver
        print(x)
        driver.get(x)
        sleep(5)
        assert True

if __name__ == '__main__':
    pytest.main(['-s', '-v', 'test_temp.py'])