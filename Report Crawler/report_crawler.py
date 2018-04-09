# python version : 3.6.2
# selenium version : 3.11.0
# beautifulsoup version : 4.6.0


from selenium import webdriver
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
from time import sleep
import os
import shutil as st
# 다운로드 폴더, hwp 파일 저장 폴더 명, 그 외 파일 저장 폴더 명 설정 모듈
import config

# 셀레니움에서 웹 접근을 위한 드라이버
driver = None

# 사이트의 글 href(a태그의 href)를 저장하기 위한 리스트
hrefs = []
# 다운로드 파일 명을 저장하기 위한 리스트
filenames = []

# 이메일과 패스워드를 전달받아서 로그인하는 함수
def login_jwpark(uemail, password) :
    # 전역 변수로 선언된 드라이버 사용
    global driver

    # 크롬드라이버 경로, 드라이버에 연결된 웹 주소 경로
    chrome_dir = "./chromedriver"
    driver_url = "https://www.jwpark.kr/report_cse2018"
    # 크롬드라이버와 연결하고 해당 웹 주소로 연결
    driver = webdriver.Chrome(chrome_dir)
    driver.get(driver_url)

    # xpath를 사용하여 로그인 버튼 클릭
    login_xpath = """//*[@id="ly_btn"]"""
    # driver.find_element_by_xpath(xpath) : xpath를 사용하여 html 내부의 요소 찾음
    # click() : 요소 클릭
    driver.find_element_by_xpath(login_xpath).click()

    # 이메일과 비밀번호 입력
    # driver.find_element_by_id(id) : html 문서에서 태그에 주어진 id 값으로 요소 찾고 객체로 반환
    elem_login = driver.find_element_by_id("uemail")
    # clear() : 요소에 입력된 text 값 클리어
    elem_login.clear()
    # send_keys(keys) : 요소에 keys를 입력한다(보낸다).
    elem_login.send_keys(uemail)

    # 위와 동일
    elem_login = driver.find_element_by_id("upw")
    elem_login.clear()
    elem_login.send_keys(password)

    # xpath를 사용하여 로그인 시도
    login_btn_xpath = """/html/body/section/div[2]/div[2]/form/fieldset/div[2]/button"""
    driver.find_element_by_xpath(login_btn_xpath).click()

# 글의 시작번호, 끝 번호, 페이지 넘버를 전달받아 href를 세팅하는 함수
def set_hrefs(start, end, page_num) :
    # 전역 변수로 선언된 리스트 사용
    global hrefs
    # 레포트 게시판의 기본 url
    report_url = "https://www.jwpark.kr/index.php?mid=report_cse2018&page="

    # 기본주소+페이지넘버 에 해당하는 url로부터 html 문서를 bs 객체로 얻어옴
    html = urlopen(report_url + str(page_num))
    bsObj = bs(html, "html.parser")

    # html 문서에서 tbody 부분을 찾고 tr(학생들이 올린 글)을 찾는다. class : "" 를 통해 공지사항이 아닌 것만 가져오게 됨.
    tbody = bsObj.find("tbody")
    tbody_tr = tbody.find_all("tr", {"class": ""})

    # end부터 시작해서 start로 하향식으로 접근하게 됨.
    # last_no 가 start 와 같을 때 까지 반복.
    # 만약 현재 페이지 넘버에서 같아지지 않는다면 다음 페이지까지 읽어야 하는 경우이다.
    last_no = end

    # 모든 tr(게시글)에 대하여 반복
    for tr in tbody_tr :
        # 글번호(no)를 찾고 현재 last_no에 저장된 번호와 no 중 작은 번호로 갱신
        no = tr.find("td")
        no = int(no.get_text().strip())
        last_no = min(last_no, no)

        # no가 start보다 작다면 원하는 글 번호까지 읽어들인 것. 함수 종료
        if no < start : return

        # 그 외에는 a 태그에 있는 href를 얻어와 리스트에 저장.
        elif no >= start and no <= end :
            href = tr.find("a").get('href')
            hrefs.append(href)

    # 완료하지 못했다면 페이지 넘버를 하나 증가시키며 재귀호출
    # 첫 입력시 start와 end가 같을 경우 제대로 동작하지 않음.
    # start와 end가 같다는 건 하나만 내려받는 경우이므로 내버려 두기로 함..
    if last_no != start :
        set_hrefs(start, last_no, page_num+1)

# 얻어온 href를 사용하여 파일들을 다운받는 함수
def download_files() :
    # 전역변수로 선언된 드라이버 사용
    global driver

    # 저장된 모든 href에 대하여 반복
    for href in hrefs :
        # 드라이버에 href를 연결한다.
        driver.get(href)
        # 파일 목록 오픈 버튼을 누른다.
        file_open_btn_xpath = """//*[@id="content"]/div/div[2]/div[3]/div[1]/button"""
        # 파일 등록이 안된 경우 예외가 발생한다. 무시하고 다음 href로 넘어간다.
        try :
            driver.find_element_by_xpath(file_open_btn_xpath).click()
        except :
            continue

        # 드라이버로부터 현재 페이지 소스를 읽고 bs 객체로 html 문서를 받아온다.
        html = driver.page_source
        # bs(html, parser)
        # html 문서를 html.parser 문서를 사용해서 파싱한 후 bs 오브젝트로 반환
        bsObj = bs(html, 'html.parser')
        # find_all(html 태그명), find(html 태그명)
        # 실질적으로 파일들은 ul 내부에 li 들에 있다.
        # ul 태그 중 클래스가 files인 것을 하나 찾고(find) 그 안에서 li 태그를 모두 찾음(find_all)
        lis = bsObj.find("ul", {"class":"files"}).find_all("li")
        # ul 태그 중 클래스가 files인 것을 하나 찾고(find) 그 안에서 a 태그를 모두 찾음(find_all)
        atags = bsObj.find("ul", {"class":"files"}).find_all("a")

        # a태그에서 텍스트를 뽑아서 파일명만 짤라서 filenames 에 저장
        for a in atags :
            # a태그에 대한 내용을 텍스트로 변환
            text = str(a)
            # 태그들은 <> 에 감싸져 있음.
            # '>' 문자를 기준으로 토큰화 시켜 tmp에 저장
            tmp = text.split('>')
            # 파일이름은 tmp[1]을 '<'로 토큰화 시키면 [0] 번째에 공백과 함께 들어있음.
            # strip() 함수로 왼쪽, 오른쪽 공백 제거
            filename = tmp[1].split('<')[0].strip()
            # filenames 리스트에 filename 추가
            filenames.append(filename)

        # 파일들의 기본적인 xpath는 아래와 같다.
        base_file_xpath = """//*[@id="content"]/div/div[2]/div[3]/div[1]/ul/li"""

        # 파일이 하나인 경우 뒤에 /a 만 붙여 클릭한다.
        if len(lis) == 1 :
            base_file_xpath += """/a"""
            driver.find_element_by_xpath(base_file_xpath).click()

        # 2개 이상이면 파일들은 [1], [2] 와 같이 첨자가 붙는다.
        # 규칙에 맞춰 파일 xpath를 만들고 클릭하게 한다.
        else :
            # //*[@id="content"]/div/div[2]/div[3]/div[1]/ul/li[1]/a
            # //*[@id="content"]/div/div[2]/div[3]/div[1]/ul/li[2]/a
            for i in range(1, len(lis)+1) :
                file_xpath = base_file_xpath + """[""" + str(i) + """]/a"""
                driver.find_element_by_xpath(file_xpath).click()

        # 잠깐 쉰다.
        sleep(1)

# 다운로드 받은 파일들을 repot_name 에 해당하는 폴더로 옮김
# .hwp 확장자가 아니면 다른 폴더에 넣음
def moveFiles(report_name) :
    # 폴더 경로 설정. 레포트 경로는 레포트 이름을 사용
    report_dir = report_name
    # 다운로드 폴더는 config에 저장된 경로 사용
    download_dir = config.download_dir
    # 다운로드 폴더로 chdir
    os.chdir(download_dir)
    # 한글파일 폴더명, 그 외 파일 폴더명을 config에 저장된 이름 사용
    report_dir_accept = config.report_dir_accept
    report_dir_except = config.report_dir_except

    # 예외가 발생할 수도 있기 때문에 try~ except 사용
    try :
        # 레포트 폴더 생성
        os.mkdir(report_dir)
        # 레포트 폴더로 이동
        os.chdir(report_dir)
        # 한글파일폴더, 그외파일폴더 생성
        os.mkdir(report_dir_accept)
        os.mkdir(report_dir_except)
    except :
        print("os.mkdir error.")

    # 모든 파일들에 대하여 반복
    # file은 파일명임
    for file in filenames :
        # 끝이 .hwp인 경우. 즉 한글파일 폴더로 옮김
        if file.endswith(".hwp") :
            # move(옮길 경로, 옮길 파일/폴더)
            st.move("../" + file, report_dir_accept)
        else :
            # 그외는 그외 폴더로 옮김
            st.move("../" + file, report_dir_except)

    print("************** moveFiles Complete **************")

# 이메일, 패스워드, 시작번호, 끝번호를 입력받아 위 함수들을 모두 실행시키는 함수.
def process(uemail, password, start, end, report_name) :
    login_jwpark(uemail, password)
    set_hrefs(start, end, 1) # 페이지넘버는 기본적으로 1번부터.
    download_files()
    moveFiles(report_name)

# 처리를 위해 필요한 입력들을 받고 process 함수를 호출하는 함수.
def init_process() :
    uemail = input("Input Email : ")
    password = input("Input Password : ")
    nums = list(map(int, input("Input Start, End Number : ").split()))
    report_name = input("Input report name : ")
    start = min(nums)
    end = max(nums)

    print()
    print("Run Process")
    process(uemail, password, start, end, report_name)

    # 프로세스가 정상적으로 끝나면 아래 Finish가 프롬프트에 떨어진다.
    # 크롬은 종료되지 않음.
    print("************** Finish **************")

# 함수 실행.
init_process()
