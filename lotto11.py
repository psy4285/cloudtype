import pandas as pd
import numpy as np
import itertools
import random
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from joblib import Parallel, delayed
import requests
import io

def calculate_pair_frequencies(numbers):
    pair_freq = {}
    for row in numbers:
        for pair in itertools.combinations(row, 2):
            pair = tuple(sorted(pair))
            if pair in pair_freq:
                pair_freq[pair] += 1
            else:
                pair_freq[pair] = 1
    return pair_freq

def calculate_recent_frequency(numbers, max_number):
    last_appearance = {num: -1 for num in range(1, max_number + 1)}
    recent_freq = {num: 0 for num in range(1, max_number + 1)}

    for idx, row in enumerate(numbers):
        for num in row:
            if last_appearance[num] != -1:
                recent_freq[num] = idx - last_appearance[num]
            last_appearance[num] = idx

    for num in range(1, max_number + 1):
        if last_appearance[num] != -1:
            recent_freq[num] = len(numbers) - last_appearance[num]

    return recent_freq

def is_combination_valid(combination):
    ranges = [(1, 10), (11, 19), (20, 29), (30, 39), (40, 45)]
    return all(sum(1 for num in combination if start <= num <= end) <= 2 for start, end in ranges)

def calculate_combined_score(combination, pair_freq, recent_freq, hot_numbers, cold_numbers):
    score = 0
    for pair in itertools.combinations(combination, 2):
        pair = tuple(sorted(pair))
        score += pair_freq.get(pair, 0)

    for num in combination:
        score += recent_freq[num]
        if num in hot_numbers:
            score += 1
        if num in cold_numbers:
            score -= 1
    return score

def generate_lotto_numbers(num_combinations):
    file_url = 'https://drive.google.com/uc?export=download&id=1uwBIZKqQCkbZnVHmnubgEw83wpw6Oq1c'
    response = requests.get(file_url)
    if response.status_code != 200:
        raise Exception("파일 다운로드 실패")

    file_data = io.BytesIO(response.content)
    lotto_data = pd.read_csv(file_data, encoding='utf-8', header=2)

    
    
    # 과거 당첨 번호 조합 추출
    past_winning_combinations = set(tuple(sorted(row)) for row in winning_numbers.values)

    # 당첨 번호와 보너스 번호 컬럼 추출
    winning_numbers = lotto_data.iloc[:, 13:19].apply(pd.to_numeric, errors='coerce')
    
    
    winning_numbers = lotto_data.iloc[:, 13:19].apply(pd.to_numeric, errors='coerce')
    pair_frequencies = calculate_pair_frequencies(winning_numbers.values)
    recent_freq = calculate_recent_frequency(winning_numbers.values, 45)

    # 여기에서 추가적인 데이터 처리 및 핫 & 콜드 넘버 계산을 진행합니다.
    # 예: hot_numbers, cold_numbers 계산 로직
    # 핫 & 콜드 넘버 계산
    N = 10  # 최근 10회 추첨 데이터를 기준으로 핫 & 콜드 넘버를 계산
    recent_draws = winning_numbers.iloc[-N:]
    hot_numbers = recent_draws.apply(lambda x: pd.Series(x).value_counts()).sum(axis=0).sort_values(ascending=False).index[:5]
    cold_numbers = recent_draws.apply(lambda x: pd.Series(x).value_counts()).sum(axis=0).sort_values(ascending=True).index[:5]
    
        
    

    all_possible_combinations = list(itertools.combinations(range(1, 46), 6))
    valid_combinations = [comb for comb in all_possible_combinations if is_combination_valid(comb)]
    sampled_combinations = random.sample(valid_combinations, min(10000, len(valid_combinations)))

    scored_combinations = [(calculate_combined_score(comb, pair_frequencies, recent_freq, hot_numbers, cold_numbers), comb) for comb in sampled_combinations]
    scored_combinations.sort(reverse=True, key=lambda x: x[0])

    return scored_combinations[:num_combinations]
