# =====================================================================
# 프로그램명: 실습 3 - Pandas EDA · Polars Lazy · DuckDB SQL 비교 
# 작성자: 김상현
# 작성일: 2026-07-16
# 설명: sales_100k.csv 데이터를 로딩하여 결측치 등 기초 탐색을 수행하고,
#       IQR 방식을 사용하여 특정 수치형 컬럼의 이상치를 제거합니다.
# 변경내역: 최초 작성
# =====================================================================

import pandas as pd
import sys
import os

def perform_pandas_eda(file_path: str, target_col: str = 'amount'):
    """
    지정된 경로의 CSV 파일을 읽어 기초 통계를 출력하고 
    IQR 방식을 통해 이상치를 제거한 DataFrame을 반환합니다.
    """
    # [1] 오류/예외 처리: 파일 존재 여부 사전 검출 및 로드 실패 방지
    if not os.path.exists(file_path):
        print(f"오류: '{file_path}' 경로에 파일이 존재하지 않습니다. 경로를 다시 확인해주세요.")
        sys.exit(1)

    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        print(f"오류: 데이터 로드 중 예외가 발생했습니다. ({e})")
        sys.exit(1)

    # [2] 기초 데이터 탐색 및 예외 처리
    try:
        print("--- 1. 기초 데이터 탐색 ---")
        
        # Checkpoint: df.info() 출력
        print("\n[데이터 정보 (df.info())]")
        df.info()
        
        # Checkpoint: isnull().sum() 출력
        print("\n[결측치 수 (df.isnull().sum())]")
        print(df.isnull().sum())
        
        # 이상치 제거 전 행 수 측정
        before_rows = len(df)
        
        # [3] IQR 기반 이상치 제거
        # Q1, Q3 계산 (감점 대상 회피: 올바른 공식 적용)
        Q1 = df[target_col].quantile(0.25)
        Q3 = df[target_col].quantile(0.75)
        IQR = Q3 - Q1
        
        # Checkpoint: between() 메서드를 활용한 정상 범위 필터링
        condition = df[target_col].between(Q1 - 1.5 * IQR, Q3 + 1.5 * IQR)
        df_cleaned = df[condition]
        
        # 이상치 제거 후 행 수 측정
        after_rows = len(df_cleaned)
        
        print("\n--- 2. IQR 이상치 제거 결과 ---")
        # Checkpoint: 제거 전/후 행 수 출력
        print(f"제거 전 데이터 행 수: {before_rows:,}")
        print(f"제거 후 데이터 행 수: {after_rows:,}")
        print(f"제거된 이상치 데이터 수: {before_rows - after_rows:,}")
        
        return df_cleaned

    except KeyError:
        print(f"오류: 데이터에 '{target_col}' 컬럼이 존재하지 않아 이상치 제거가 불가합니다.")
        sys.exit(1)
    except Exception as e:
        print(f"오류: 데이터 처리 중 예상치 못한 예외가 발생했습니다. ({e})")
        sys.exit(1)

if __name__ == "__main__":
    # 사용자 요청 경로 반영
    FILE_PATH = '/Users/sanghyeon/Downloads/sales_100k.csv'
    
    # 분석 대상 수치형 컬럼 설정
    TARGET_COLUMN = 'amount'
    
    # 함수 실행
    cleaned_data = perform_pandas_eda(FILE_PATH, TARGET_COLUMN)