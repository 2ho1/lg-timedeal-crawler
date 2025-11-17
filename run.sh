#!/bin/bash

# LG Time Deal Crawler 실행 스크립트

# 가상환경 활성화 (있는 경우)
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# 스케줄러 실행
python main.py --mode schedule

