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
import os


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
a = []

for i in range(start, num + 1):
    a.append(
        "/html/body/div[3]/form/article/div[1]/div[1]/div/div/div/div[1]/ul/li["
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
    By.CSS_SELECTOR, "#modal > div > div.caching-set > button"
)
first_btn.click()


# 온라인 헬프데스크 화면 닫기
seconde_btn = driver.find_element(By.CSS_SELECTOR, "#wrap > div.popUp > div > button")
seconde_btn.click()

# 관리자 사이트 페이지로 이동
admin_btn = driver.find_element(
    By.CSS_SELECTOR,
    "#wrap_body > div > section > a:nth-child(3) > div > div > div.service-footer.float-menu",
)
admin_btn.click()


# 팝업창 화면 닫기
th_btn = driver.find_element(By.CSS_SELECTOR, "#NoticepopUpclose > button")
th_btn.click()

# 지원자 관리 클릭
first_user_btn = driver.find_element(
    By.CSS_SELECTOR, "#sidebar > ul > li:nth-child(2) > a"
)
first_user_btn.click()


# 공고별 지원자 관리 페이지 이동
user_btn = driver.find_element(
    By.CSS_SELECTOR, "#sidebar > ul > li:nth-child(2) > ul > li:nth-child(1) > a"
)
user_btn.click()

# 공고별 지원자 관리 > 공고명 클릭
recruitNoticeName_btn = driver.find_element(
    By.CSS_SELECTOR, "#recruitNoticeName > span"
)
recruitNoticeName_btn.click()


i = 0
while i < len(a):
    # xpath로 공고 클릭
    list_btn = driver.find_element(By.XPATH, a[i])

    # 공고가 화면에 보이지 않으면 스크롤을 내려서 보이게 함
    if not list_btn.is_displayed():
        actions = ActionChains(driver)
        actions.move_to_element(list_btn)
        actions.perform()

    list_btn.click()
    time.sleep(2)
    i += 1

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
        submit_btn = driver.find_element(
            By.CSS_SELECTOR, "#gridScrolledHeader > div > div:nth-child(2) > button"
        )
        submit_btn.click()
        time.sleep(2)

        # 지원서 제출완료 클릭
        finish_btn = driver.find_element(
            By.CSS_SELECTOR, "#gridSetThPanel > div > label:nth-child(5) > input"
        )
        finish_btn.click()
        time.sleep(2)

        # 조회 버튼 클릭
        inquiry_btn = driver.find_element(
            By.CSS_SELECTOR, "#gridSetThPanel > div > button:nth-child(7)"
        )
        inquiry_btn.click()
        time.sleep(2)
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
            allUuser_btn = driver.find_element(
                By.CSS_SELECTOR, "#gridFixedHeader > div > div.th.semiPadding > button"
            )
            allUuser_btn.click()
            time.sleep(5)

            # 검색결과 전체 선택 클릭
            allUuserSelect_btn = driver.find_element(
                By.CSS_SELECTOR, "#gridSetThPanel > div"
            )
            allUuserSelect_btn.click()
            time.sleep(5)

            # 문서 아이콘 클릭
            application_btn = driver.find_element(
                By.CSS_SELECTOR, "#gridUtil > div:nth-child(4) > button"
            )
            application_btn.click()
            time.sleep(2)

            # 지원서 엑셀 저장 클릭
            applicationStorage_btn = driver.find_element(
                By.CSS_SELECTOR,
                "#gridUtil > div:nth-child(4) > ul > li.divider.excelDowntop > a",
            )
            applicationStorage_btn.click()
            time.sleep(2)

            # 지원서 통합형 클릭
            integration_btn = driver.find_element(
                By.CSS_SELECTOR, "#modalBody > div:nth-child(3) > div.inbtnset > button"
            )
            integration_btn.click()
            time.sleep(2)

            # 엑셀저장 아이콘 클릭
            excel_btn = driver.find_element(By.CSS_SELECTOR, "#modalSubmit")
            excel_btn.click()
            time.sleep(2)

            # 대기 설정
            wait = WebDriverWait(driver, 10)

            try:
                # 대화 상자의 첫 번째 버튼 대기
                excel_btn_1 = wait.until(
                    EC.element_to_be_clickable(
                        (By.CSS_SELECTOR, "#Dialog > div > button:nth-child(1)")
                    )
                )
                excel_btn_1.click()
                time.sleep(2)

                # 다운로드 사유 입력
                reason_btn = driver.find_element(
                    By.CSS_SELECTOR, "#privacyDownloadReason"
                )
                reason_btn.click()

                reason_input = driver.find_element(
                    By.CSS_SELECTOR, "#privacyDownloadReason"
                )
                reason_input.send_keys("마이다스인 기술지원")

                # 대기 시간 설정
                max_wait_time = 3600  # 최대 대기 시간 설정 (3600초)
                wait = WebDriverWait(driver, max_wait_time)

                # 저장버튼 클릭
                excel_btn_2 = driver.find_element(
                    By.CSS_SELECTOR,
                    "#privacyDownloadDialog > div:nth-child(4) > button:nth-child(1)",
                )
                excel_btn_2.click()
                time.sleep(2)

                # 파일이 저장될 경로
                file_path = "C:\\Users\\midascs03\\Downloads"

                # 파일이 존재하는지 확인
                start_time = time.time()
                while not os.path.exists(file_path):
                    time.sleep(1)  # 1초 대기 후 다시 확인

                    # 최대 대기 시간을 초과하면 종료
                    if time.time() - start_time > max_wait_time:
                        raise TimeoutError("파일 다운로드 대기 시간이 초과되었습니다.")

                # 파일 확인 및 처리 작업 수행

                # 확인 버튼 클릭
                excel_btn_3 = wait.until(
                    EC.element_to_be_clickable(
                        (
                            By.CSS_SELECTOR,
                            "#Dialog > div > button:nth-child(1)",
                        )
                    )
                )
                excel_btn_3.click()
                time.sleep(2)
                # 이렇게 수정하면 최대 대기 시간을 3600초(1시간)로 설정하게 됩니다. 파일 다운로드가 완료되지 않았을 경우 1초씩 대기하며, 최대 대기 시간을 초과하면 TimeoutError가 발생합니다.

                recruitNoticeName = driver.find_element(
                    By.XPATH, '//*[@id="recruitNoticeName"]/span'
                ).text
                if i < len(b):
                    message = (
                        str(b[i])
                        + ". "
                        + recruitNoticeName
                        + ":"
                        + "다운로드되었습니다."
                    )
                    message_list.append(message)  # 메시지를 리스트에 추가
                    print(
                        str(b[i])
                        + ". "
                        + recruitNoticeName
                        + ":"
                        + "다운로드되었습니다."
                    )
                # 공고명 클릭
                recruitNoticeName_btn = driver.find_element(
                    By.CSS_SELECTOR, "#recruitNoticeName"
                )
                recruitNoticeName_btn.click()

            except NoSuchElementException as e:
                recruitNoticeName_btn = driver.find_element(
                    By.CSS_SELECTOR, "#recruitNoticeName"
                )
                recruitNoticeName_btn.click()
            recruitNoticeName_btn = driver.find_element(
                By.CSS_SELECTOR, "#recruitNoticeName"
            )
            recruitNoticeName_btn.click()

# 모든 메시지를 하나의 문자열로 결합하여 출력
message = "\n".join(message_list)
sg.Popup(message)
# 완료 메시지 출력
sg.Popup("자동화 프로그램 완료", "다운로드가 완료되었습니다.", "프로그램을 종료합니다.")
driver.quit()
