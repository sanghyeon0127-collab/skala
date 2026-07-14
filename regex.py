import re

PASSWORD_PATTERN = re.compile(
    r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^\w\s]).+$'
)


def is_valid_password(password: str) -> bool:
    """비밀번호가 조건을 만족하는지 검사합니다.

    조건:
    - 최소 하나의 영문 소문자
    - 최소 하나의 영문 대문자
    - 최소 하나의 숫자
    - 최소 하나의 기호
    """
    return bool(PASSWORD_PATTERN.match(password))


if __name__ == "__main__":
    sample_passwords = [
        "Password1!",
        "password1!",
        "PASSWORD1!",
        "Password!",
        "Password1",
    ]

    for pwd in sample_passwords:
        result = "유효" if is_valid_password(pwd) else "무효"
        print(f"{pwd}: {result}")
