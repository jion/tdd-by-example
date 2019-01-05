class TestCase:
    def __init__(self, name):
        self.name = name

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def run(self):
        result = TestResult()
        result.test_started()

        self.setUp()
        method = getattr(self, self.name)
        method()
        self.tearDown()

        return result


class TestResult:
    def __init__(self):
        self.run_count = 0

    def test_started(self):
        self.run_count += 1

    def summary(self):
        return "{} run, 0 failed".format(self.run_count)


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
    def testTemplateMethod(self):
        self.test = WasRun("testMethod")
        self.test.run()
        assert("setUp testMethod tearDown " == self.test.log)

    def testResult(self):
        self.test = WasRun("testMethod")
        result = self.test.run()
        assert("1 run, 0 failed" == result.summary())

    def testFailedResult(self):
        self.test = WasRun("testBrokenMethod")
        result = self.test.run()
        assert("1 run, 1 failed" == result.summary())


TestCaseTest('testTemplateMethod').run()
TestCaseTest('testResult').run()
# TestCaseTest('testFailedResult').run()
