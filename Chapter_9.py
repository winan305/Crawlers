import requests

# 폼 태그에 post로 보내기
params = {'firstname' : 'Jun', 'lastname' : 'DuYeong'}
request = requests.post("http://pythonscraping.com/files/processing.php", data=params)
print(request.text)

# 파일 보내기
'''files = {'uploadFile' : open('../files/Python-logo.png', 'rb')}
request = requests.post("http://pythonscraping.com/pages/processing2.php", files=files)
print(request.text)'''

# 로그인 폼에 로그인 매개변수 전송, 쿠키를 가져온 뒤 쿠키를 프로필 페이지에 보냄.
params = {'username' : 'DoDo', 'password' : 'password'}
request = requests.post("http://pythonscraping.com/pages/cookies/welcome.php", params)
print("Cookie is set to :")
print(request.cookies.get_dict())
print("------------")
print("Going to profile page...")
request = requests.get("http://pythonscraping.com/pages/cookies/profile.php", cookies=request.cookies)
print(request.text)

print()
# 세션으로 처리
session = requests.session()
params = {'username' : 'DoDo', 'password' : 'password'}
request = session.post("http://pythonscraping.com/pages/cookies/welcome.php", params)
print("Cookie is set to :")
print(request.cookies.get_dict())
print("------------")
print("Going to profile page...")
request = requests.get("http://pythonscraping.com/pages/cookies/profile.php", cookies=request.cookies)
print(request.text)
