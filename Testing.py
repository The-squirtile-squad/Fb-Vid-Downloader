import pytest
import draft0
import re


# Testing for Link
def check_link(link):
    link_1 = re.compile(r'^(https:|)[/][/]www.([^/]+[.])*facebook.com')
    return re.search(link_1, link)


assert check_link(r'https://www.youtube.com/watch?v=dAHSJfWrENc')
assert check_link(r'https://fb.watch/7VOkuVaols/')
assert check_link(r'https://fb.watch/7VOm--dwgD/')


# def check_regis(name, lastname, uname, pw, email, ID):
#     name1 = draft0.regis()



# # Testing for login and password
# def test_tes():
#     pytest draft0.tes


# # Testing for registration
# def test_regis(self):
#     self.assertEqual('Rahul')
#     self.assertEqual('Shakya')
#     self.assertEqual('oopsie')
#     self.assertEqual(30090)
#     self.assertEqual('123456789')


# # Testing for browse path
# def test_browse(self):
#     self.assertEqual(draft0.new('C:/Videos/downloader project'), 'C:/Videos/downloader project')
#     self.assertEqual(draft0.new('C:/Videos/downloader project'), 'C:/Videos/downloader project')
#     self.assertEqual(draft0.new('C:/Videos/downloader project'), 'C:/Videos/downloader project')



# if __name__ == "__main__":
#     pytest.main()
