class TestCase:
    def __init__(self, name):
        self.name = name

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def run(self, result):
        result.test_started()

        self.setUp()
        method = getattr(self, self.name)
        try:
            method()
        except:
            result.test_failed()
        self.tearDown()

        return result


class TestResult:
    def __init__(self):
        self.run_count = 0
        self.error_count = 0

    def test_started(self):
        self.run_count += 1

    def test_failed(self):
        self.error_count += 1

    def summary(self):
        return "{} run, {} failed".format(self.run_count, self.error_count)


class TestSuite:
    def __init__(self):
        self.tests = []

    def add(self, test):
        self.tests.append(test)

    def run(self, result):
        for test in self.tests:
            test.run(result)

        return result


class WasRun(TestCase):
    def __init__(self, name):
        TestCase.__init__(self, name)

    def setUp(self):
        self.wasRun = False
        self.log = "setUp "

    def tearDown(self):
        self.log += "tearDown "

    def testMethod(self):
        self.log += "testMethod "
        self.wasRun = True

    def testBrokenMethod(self):
        raise Exception


class TestCaseTest(TestCase):
    def setUp(self):
        self.result = TestResult()

    def testTemplateMethod(self):
        self.test = WasRun("testMethod")
        self.test.run(self.result)
        assert("setUp testMethod tearDown " == self.test.log)

    def testInvokingTearDownEvenWhenFailure(self):
        test = WasRun("testBrokenMethod")
        test.run(self.result)
        log = test.log
        assert(log.endswith("tearDown "))

    def testResult(self):
        self.test = WasRun("testMethod")
        result = self.test.run(self.result)
        assert("1 run, 0 failed" == result.summary())

    def testFailedResult(self):
        self.test = WasRun("testBrokenMethod")
        result = self.test.run(self.result)
        assert("1 run, 1 failed" == result.summary())

    def testFailedResultFormatting(self):
        result = TestResult()
        result.test_started()
        result.test_failed()
        assert("1 run, 1 failed" == result.summary())

    def testSuite(self):
        test_suite = TestSuite()
        test_suite.add(WasRun("testMethod"))
        test_suite.add(WasRun("testBrokenMethod"))
        result = test_suite.run(self.result)
        assert("2 run, 1 failed" == result.summary())


suite = TestSuite()
suite.add(TestCaseTest('testTemplateMethod'))
suite.add(TestCaseTest('testResult'))
suite.add(TestCaseTest('testFailedResult'))
suite.add(TestCaseTest('testFailedResultFormatting'))
suite.add(TestCaseTest('testSuite'))
suite.add(TestCaseTest('testInvokingTearDownWhenFailure'))
result = TestResult()
suite.run(result)
print result.summary()
