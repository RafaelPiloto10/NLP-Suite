source $HOME/anaconda/bin/activate
conda activate NLP
cd "$(dirname "$0")"
python src/social_science_research_main.py
git pull origin