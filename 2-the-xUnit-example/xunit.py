class TestCase:
    def __init__(self, name):
        self.name = name

    def setUp(self):
        pass

    def run(self):
        self.setUp()
        method = getattr(self, self.name)
        method()


class WasRun(TestCase):
    def __init__(self, name):
        TestCase.__init__(self, name)

    def setUp(self):
        self.wasRun = False
        self.wasSetup = True

    def testMethod(self):
        self.wasRun = True


class TestCaseTest(TestCase):
    def setUp(self):
        self.test = WasRun("testMethod")

    def testSetup(self):
        self.test.run()
        assert(self.test.wasSetup)

    def testRunning(self):
        self.test.run()
        assert(self.test.wasRun)

TestCaseTest('testSetup').run()
TestCaseTest('testRunning').run()
