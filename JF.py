from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
import time
import pyautogui
import pyperclip
import PySimpleGUI as sg


# GUI 레이아웃 생성
layout = [
    [sg.Text("사이트 주소"), sg.InputText(key="_URL_")],
    [sg.Text("아이디"), sg.InputText(key="_ID_")],
    [sg.Text("비밀번호"), sg.InputText(key="_PW_", password_char="*")],
    [sg.Text("공고 시작 갯수"), sg.InputText(key="_START_")],
    [sg.Text("공고 끝 갯수"), sg.InputText(key="_NUM_")],
    [sg.Submit(), sg.Cancel()],
]

# GUI 생성
window = sg.Window("자동화 프로그램", layout)

# 사용자로부터 입력 받기
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == "Cancel":
        break
    elif event == "Submit":
        url = values["_URL_"]
        user_id = values["_ID_"]
        user_pw = values["_PW_"]
        start = int(values["_START_"])
        num = int(values["_NUM_"])
        break

start = int(values["_START_"])
num = int(values["_NUM_"])
a = []

for i in range(start, num + 1):
    a.append(
        "/html/body/div[4]/form/article/div[1]/div[1]/div/div/div/div[1]/ul/li["
        + str(i)
        + "]/button"
    )
print(a)

b = list(range(start, num + 1))
print(b)


# 팝업창을 띄우기 위한 함수
def show_popup(message):
    sg.popup(message, title="알림")


# 저장할 메시지 리스트
message_list = []

# Chrome WebDriver 옵션 설정
chrome_options = Options()
chrome_options.add_argument("--ignore-certificate-errors")
chrome_options.add_argument("--ignore-ssl-errors")

# 웹페이지 열기
driver = webdriver.Chrome(options=chrome_options)
driver.implicitly_wait(5)
driver.maximize_window()

# 브라우저 실행
driver.get(url)

# 아이디 입력
id = driver.find_element(By.CSS_SELECTOR, "#id")  # 아이디 입력창
id.click()
pyperclip.copy(user_id)
id.click()
pyautogui.hotkey("ctrl", "v")
time.sleep(2)

# 비밀번호 입력
pw = driver.find_element(By.CSS_SELECTOR, "#password")
pw.click()
pyperclip.copy(user_pw)
pw.click()
pyautogui.hotkey("ctrl", "v")
time.sleep(2)

# 로그인 버튼
login_btn = driver.find_element(By.CSS_SELECTOR, "#btn-login")
login_btn.click()
time.sleep(5)

# 이용서비스 선택 화면 닫기 클릭
first_btn = driver.find_element(
    By.CSS_SELECTOR, "#modal > div > div.caching-set > span > span > span > button"
)
first_btn.click()

# 온라인 헬프데스크 화면 닫기
seconde_btn = driver.find_element(By.CSS_SELECTOR, "#wrap > div.popUp > div > button")
seconde_btn.click()

# 관리자 사이트 페이지로 이동
admin_btn = driver.find_element(
    By.CSS_SELECTOR, "#wrap_body > div > section > a:nth-child(2) > div > div"
)
admin_btn.click()

# 지원자 관리 클릭
first_user_btn = driver.find_element(
    By.CSS_SELECTOR, "#sidebar > ul > li:nth-child(2) > a"
)
first_user_btn.click()


# 공고별 지원자 관리 페이지 이동
user_btn = driver.find_element(
    By.CSS_SELECTOR, "#sidebar > ul > li.facelift--open > ul > li:nth-child(2) > a"
)
user_btn.click()

# 공고별 지원자 관리 > 공고명 클릭
recruitNoticeName_btn = driver.find_element(By.CSS_SELECTOR, "#recruitNoticeName")
recruitNoticeName_btn.click()


# 스크롤 길이 알아내기
scroll_height = driver.execute_script("return document.body.scrollHeight")

# Wait for the modal to become invisible
wait = WebDriverWait(driver, 10)

i = 0
while i < len(a):
    try:
        # xpath로 공고 클릭
        list_btn = driver.find_element(By.XPATH, a[i])

        # 공고가 화면에 보이지 않으면 스크롤을 내려서 보이게 함
        if not list_btn.is_displayed():
            actions = ActionChains(driver)
            actions.move_to_element(list_btn)
            actions.perform()
            # 요소가 화면에 보이지 않으면 스크롤을 내려서 요소가 보이도록 함
            driver.execute_script("arguments[0].scrollIntoView();", list_btn)

        # 대기시간을 10초로 설정하고, 요소가 클릭 가능한 상태가 될 때까지 대기
        WebDriverWait(driver, 200000).until(
            EC.element_to_be_clickable((By.XPATH, a[i]))
        ).click()
        time.sleep(2)

        recruitNoticeName_btn = driver.find_element(
            By.CSS_SELECTOR, "#recruitNoticeName"
        )
        recruitNoticeName = driver.find_element(
            By.XPATH, '//*[@id="recruitNoticeName"]/span'
        ).text
        print(str(b[i]) + ". " + recruitNoticeName + ":" + "클릭하였습니다.")

        # 현재 설정된 검색조건에 해당되는 지원자가 없습니다. 확인
        no_result = driver.find_elements(
            By.CSS_SELECTOR, "#wrapGridScrolledBody.noSearchResult"
        )
        if no_result:
            recruitNoticeName_btn = driver.find_element(
                By.CSS_SELECTOR, "#recruitNoticeName"
            )
            recruitNoticeName = driver.find_element(
                By.XPATH, '//*[@id="recruitNoticeName"]/span'
            ).text
            if i < len(b):
                message = (
                    str(b[i])
                    + ". "
                    + recruitNoticeName
                    + ":"
                    + "공고에 지원한 지원자가 없습니다."
                )
                message_list.append(message)  # 메시지를 리스트에 추가
                print(
                    str(b[i])
                    + ". "
                    + recruitNoticeName
                    + ":"
                    + "공고에 지원한 지원자가 없습니다."
                )
            recruitNoticeName_btn.click()

        else:
            # 지원서 제출 클릭
            wait = WebDriverWait(driver, 5)
            submit_btn = wait.until(
                EC.element_to_be_clickable(
                    (
                        By.CSS_SELECTOR,
                        "#gridScrolledHeader > div > div:nth-child(2) > button",
                    )
                )
            )
            submit_btn.click()
            time.sleep(1)

            # 지원서 제출완료 클릭
            wait = WebDriverWait(driver, 2)
            finish_btn = wait.until(
                EC.element_to_be_clickable(
                    (
                        By.CSS_SELECTOR,
                        "#gridSetThPanel > div > label:nth-child(5) > span",
                    )
                )
            )
            finish_btn.click()
            time.sleep(1)

            # 조회 버튼 클릭
            wait = WebDriverWait(driver, 2)
            inquiry_btn = wait.until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, "#gridSetThPanel > div > button:nth-child(7)")
                )
            )
            inquiry_btn.click()
            time.sleep(1)

            # 현재 설정된 검색조건에 해당되는 지원자가 없습니다. 확인
            no_result = driver.find_elements(
                By.CSS_SELECTOR, "#wrapGridScrolledBody.noSearchResult"
            )
            if no_result:
                recruitNoticeName_btn = driver.find_element(
                    By.CSS_SELECTOR, "#recruitNoticeName"
                )
                recruitNoticeName = driver.find_element(
                    By.XPATH, '//*[@id="recruitNoticeName"]/span'
                ).text
                if i < len(b):
                    message = (
                        str(b[i])
                        + ". "
                        + recruitNoticeName
                        + "제출완료한 지원자가 없습니다."
                    )
                    message_list.append(message)  # 메시지를 리스트에 추가
                    print(
                        str(b[i])
                        + ". "
                        + recruitNoticeName
                        + ":"
                        + "제출완료한 지원자가 없습니다."
                    )
                recruitNoticeName_btn.click()
            else:
                # 지원자 전체 선택 버튼 클릭
                wait = WebDriverWait(driver, 5)
                allUuser_btn = wait.until(
                    EC.element_to_be_clickable(
                        (
                            By.CSS_SELECTOR,
                            "#gridFixedHeader > div > div.th.semiPadding > button",
                        )
                    )
                )
                allUuser_btn.click()
                time.sleep(2)

                # 검색결과 전체 선택 클릭
                wait = WebDriverWait(driver, 5)
                allUuserSelect_btn = wait.until(
                    EC.element_to_be_clickable(
                        (By.CSS_SELECTOR, "#gridSetThPanel > div")
                    )
                )
                allUuserSelect_btn.click()
                time.sleep(2)

                # 문서 아이콘 클릭
                wait = WebDriverWait(driver, 5)
                application_btn = wait.until(
                    EC.element_to_be_clickable(
                        (By.CSS_SELECTOR, "#gridUtil > div:nth-child(4) > button")
                    )
                )
                application_btn.click()
                time.sleep(2)

                # 지원서 엑셀 저장 클릭
                wait = WebDriverWait(driver, 5)
                applicationStorage_btn = wait.until(
                    EC.element_to_be_clickable(
                        (
                            By.CSS_SELECTOR,
                            "#gridUtil > div:nth-child(4) > ul > li.divider.excelDowntop > a",
                        )
                    )
                )
                applicationStorage_btn.click()
                time.sleep(2)

                # 지원서 통합형 클릭
                wait = WebDriverWait(driver, 5)
                integration_btn = wait.until(
                    EC.element_to_be_clickable(
                        (
                            By.CSS_SELECTOR,
                            "#modalBody > div > div > div:nth-child(1) > button",
                        )
                    )
                )
                integration_btn.click()
                time.sleep(2)

                # 엑셀저장 아이콘 클릭
                wait = WebDriverWait(driver, 5)
                excel_btn = wait.until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "#modalSubmit"))
                )
                excel_btn.click()
                time.sleep(2)

                # 확인 버튼 클릭
                wait = WebDriverWait(driver, 5)
                excel_btn_3 = wait.until(
                    EC.element_to_be_clickable(
                        (By.CSS_SELECTOR, "#Dialog > div > button:nth-child(1)")
                    )
                )
                excel_btn_3.click()
                time.sleep(2)

                # 취소 버튼 클릭
                wait = WebDriverWait(driver, 5)
                excelCancel_btn = wait.until(
                    EC.element_to_be_clickable(
                        (By.CSS_SELECTOR, "#Dialog > div > button:nth-child(2)")
                    )
                )
                excelCancel_btn.click()
                time.sleep(2)

                # 취소버튼2 클릭
                wait = WebDriverWait(driver, 5)
                cancel_btn = wait.until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "#modalCancel"))
                )
                cancel_btn.click()
                time.sleep(2)

                recruitNoticeName = driver.find_element(
                    By.XPATH, '//*[@id="recruitNoticeName"]/span'
                ).text
                if i < len(b):
                    message = (
                        str(b[i])
                        + ". "
                        + recruitNoticeName
                        + ":"
                        + "다운로드 완료되었습니다."
                    )
                    message_list.append(message)  # 메시지를 리스트에 추가
                    print(
                        str(b[i])
                        + ". "
                        + recruitNoticeName
                        + ":"
                        + "다운로드 완료되었습니다."
                    )

                # 공고명 클릭
                recruitNoticeName_btn = driver.find_element(
                    By.CSS_SELECTOR, "#recruitNoticeName"
                )
                recruitNoticeName_btn.click()

        # 공고명 +1 추가하여 다음 공고 클릭
        i += 1

        # 스크롤 다운
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
    except NoSuchElementException:
        print(
            str(b[i])
            + ". "
            + recruitNoticeName
            + ":"
            + "해당 공고는 존재하지 않습니다."
        )
        i += 1
        # 공고명 클릭
        recruitNoticeName_btn = driver.find_element(
            By.CSS_SELECTOR, "#recruitNoticeName"
        )
        recruitNoticeName_btn.click()
