# Dependencies

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
import numpy as np
import pandas as pd

# 1. import Flask
from flask import Flask

import datetime as dt

# Create engine
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
