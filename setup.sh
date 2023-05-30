# Create a virtual environment
python3 -m venv topic_modelling_with_BERT_venv

# Activate the virtual environment
source ./topic_modelling_with_BERT_venv/bin/activate

# Install requirements
python3 -m pip install --upgrade pip
python3 -m pip install -r ./requirements.txt

# deactivate
deactivate

# To remove the environment run the following line from the terminal
#rm -rf topic_modelling_with_BERT_venv