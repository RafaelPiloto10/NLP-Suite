start cmd.exe @cmd /k "conda activate NLP && cd %~dp0/src"
conda activate NLP && cd %~dp0 && python src/social_science_research_main.py && git pull origin