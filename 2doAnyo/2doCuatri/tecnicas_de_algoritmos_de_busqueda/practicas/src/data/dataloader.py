import os
import pandas as pd

class DataLoader:
    def __init__(self, base_dir=None):
        """
        Initializes the DataLoader with the given base directory.
        If none is provided, it defaults to the 'data' folder located in the project root.
        """
        if base_dir is None:
            # Assume this file is at .../practicas/src/data/dataloader.py,
            # so go two levels up to reach the project root and then 'data'
            self.base_dir = "..//WILLOW-ObjectClass"

        self.dataframes = {}

        

    def load_data(self):
        """
        Loads data from folders under the base directory.
        Expects each category folder to contain .png and .mat files.
        Returns a dictionary of dataframes for each category.
        """
        self.dataframes = {}
        if not os.path.exists(self.base_dir):
            print(f"Data directory not found: {self.base_dir}")
            return self.dataframes

        for category in os.listdir(self.base_dir):
            # Evitar la carpeta __pycache__


            cat_path = os.path.join(self.base_dir, category)
            if os.path.isdir(cat_path):
                pairs = {}
                # Iterate over each file in the category
                for file in os.listdir(cat_path):
                    file_path = os.path.join(cat_path, file)
                    name, ext = os.path.splitext(file)
                    if ext.lower() == ".png":
                        pairs.setdefault(name, {})['img'] = file_path
                    elif ext.lower() == ".mat":
                        pairs.setdefault(name, {})['mat'] = file_path

                # Build a list of records containing both image and .mat file info.
                rows = []
                for base, data in pairs.items():
                    if 'img' in data and 'mat' in data:
                        # Adding category info can be useful later on.
                        data['category'] = category.lower()
                        rows.append(data)

                df = pd.DataFrame(rows)
                key = f"{category.lower()}_df"
                self.dataframes[key] = df

        if "__pycache__df" in self.dataframes:
            del self.dataframes["__pycache__df"]


        return self.dataframes

    def __str__(self):
        return f"DataLoader(base_dir={self.base_dir}, dataframes={list(self.dataframes.keys())})"