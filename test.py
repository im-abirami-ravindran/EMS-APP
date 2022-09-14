try:
    from app import app
    import unittest
except Exception as e:
    print("something is missing")

class FlaskTest(unittest.TestCase):
    def test_login(self):
        tester = app.test_client(self)
        res = tester.get("/login")
        statuscode = res.status_code
        self.assertEqual(statuscode,200)

    def test_signup(self):
        tester = app.test_client(self)
        res = tester.get("/signup")
        status = res.status_code
        self.assertEqual(status,200)
    
    def test_admin(self):
        tester = app.test_client(self)
        res = tester.get("/admin")
        status = res.status_code
        self.assertEqual(status,200)
    
    # def test_employee(self):

    #     tester = app.test_client(self)
    #     res = tester.get("/employee")
    #     status = res.status_code
    #     self.assertEqual(status,200)
        


if __name__ == "__main__":
    unittest.main()