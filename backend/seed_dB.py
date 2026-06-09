import os
import random
from datetime import datetime

import pandas as pd
from faker import Faker
from dotenv import load_dotenv
from sqlalchemy import create_engine,text

fake = Faker()

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)

print("Connected to Neon")