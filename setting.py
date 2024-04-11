import os

# DEBUG = True
DEBUG = False

DEFAULT_LOG_LEVEL = "INFO"
# DEFAULT_LOG_LEVEL = "DEBUG"

# OFFLINE_CHATGPT = True
OFFLINE_CHATGPT = False

# DEFAULT_MODEL = 'gpt-3.5-turbo-0301'
# DEFAULT_MODEL = 'gpt-3.5-turbo'
# DEFAULT_MODEL = 'gpt-4'
DEFAULT_MODEL = 'gpt-4-1106-preview'

REQUEST_TIMEOUT_SECS = 60

SUBLIST = 1
# Number of words to generate for each word family
WORD_PER_FAMILY = 1
WORD_PER_FAMILY = None

DOMAIN = 'General Academic'
LEVEL_START = 'A2'
LEVEL_END = 'lower B2'
STUDENT_TYPE = 'Japanese university students without domain-specific English knowledge whose proficiency level is A2-B2'
# The number of times to retry when ChatGPT fails to generate a sentence for a word
RETRY_COUNT_FOR_SINGLE_WORD = 5

# The start position of keyword selection (count from 1, inclusive)
KEYWORD_START_POS = 1
# KEYWORD_START_POS = 11

# The number of keywords for generating sentences, -1 means all
KEYWORD_COUNT = -1
# KEYWORD_COUNT = 10

NEED_DISTRACTOR = True
# NEED_DISTRACTOR = False
TEST_DISTRACTOR_COUNT = 10 # The number of distractors to ask ChatGPT to test rationality in one trial
DISTRACTOR_COUNT = 3 # The number of distractors to output to result

# Fix the randomness, -1 means random
#   seems not working
RANDOM_SEED = 42
# RANDOM_SEED = -1


# Merriam-Webster API key
DICT_API_KEY = os.environ.get('MERRIAM_WEBSTER_API_KEY', None)
