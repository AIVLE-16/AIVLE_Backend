# config/text.py

# 회원 가입 이메일 인증 메세지
def message(domain, uidb64, token):
    return f"아래 링크를 클릭하면 회원가입 인증이 완료됩니다.\n\n 링크 : http://{domain}/account/activate/{uidb64}/{token}/\n\n감사합니다."
