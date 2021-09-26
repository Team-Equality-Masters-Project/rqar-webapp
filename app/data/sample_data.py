import pandas as pd
import numpy as np

def sample_data(n=7):
    df = pd.DataFrame({"x": range(1, 11), "y": n})
    df['x*y'] = df.x * df.y
    return df