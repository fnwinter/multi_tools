"""모든 디스플레이를 복제(Clone) 모드로 전환합니다. (Win + P → '복제'와 동일)
전환 후 팝업으로 확장(Extend) 모드로 바꿀지 물어봅니다."""
import ctypes
import sys
import time

SDC_TOPOLOGY_CLONE = 0x00000002
SDC_TOPOLOGY_EXTEND = 0x00000004
SDC_APPLY = 0x00000080

MB_OKCANCEL = 0x00000001
MB_ICONQUESTION = 0x00000020
MB_SETFOREGROUND = 0x00010000
MB_TOPMOST = 0x00040000
IDOK = 1

ERROR_MESSAGES = {
    87: "ERROR_INVALID_PARAMETER",
    50: "ERROR_NOT_SUPPORTED",
    5: "ERROR_ACCESS_DENIED",
    31: "ERROR_GEN_FAILURE",
    1610: "ERROR_BAD_CONFIGURATION",
}


def set_topology(topology: int) -> int:
    user32 = ctypes.windll.user32
    return user32.SetDisplayConfig(0, None, 0, None, topology | SDC_APPLY)


def apply_with_retry(topology: int) -> int:
    # 로그인 직후에는 디스플레이 드라이버가 아직 준비 안 됐을 수 있어 몇 번 재시도
    for attempt in range(5):
        result = set_topology(topology)
        if result == 0:
            return 0
        time.sleep(2)
    print(f"SetDisplayConfig failed: {result} ({ERROR_MESSAGES.get(result, 'UNKNOWN')})",
          file=sys.stderr)
    return result


def ask_extend() -> bool:
    answer = ctypes.windll.user32.MessageBoxW(
        None,
        "디스플레이를 확장 모드로 변경하시겠습니까?",
        "DisplayClone",
        MB_OKCANCEL | MB_ICONQUESTION | MB_SETFOREGROUND | MB_TOPMOST,
    )
    return answer == IDOK


def main() -> int:
    result = apply_with_retry(SDC_TOPOLOGY_CLONE)
    if result != 0:
        return result
    if ask_extend():
        return apply_with_retry(SDC_TOPOLOGY_EXTEND)
    return 0


if __name__ == "__main__":
    sys.exit(main())
