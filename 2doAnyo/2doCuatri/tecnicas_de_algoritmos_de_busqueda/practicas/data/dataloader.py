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
            self.base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data"))
        else:
            self.base_dir = base_dir
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
        return self.dataframes

    def get_dataframe(self, category_key):
        """
        Retrieves the dataframe associated with a specific category key.
        """
        if not self.dataframes:
            self.load_data()
        return self.dataframes.get(category_key, pd.DataFrame())

    def get_combined_dataframe(self):
        """
        Returns a single dataframe combining all category data.
        """
        if not self.dataframes:
            self.load_data()
        if self.dataframes:
            return pd.concat(list(self.dataframes.values()), ignore_index=True)
        return pd.DataFrame()

    def get_random_image_path(self, combined_df, category):
        """
        Retrieves a random image path from the combined dataframe for a given category.
        """
        if not combined_df.empty:
            df_cat = combined_df[combined_df['category'] == category.lower()]
            if not df_cat.empty:
                row = df_cat.sample(1).iloc[0]
                return row['img']
        return None
    
    def __str__(self):
        return f"DataLoader(base_dir={self.base_dir}, dataframes={list(self.dataframes.keys())})"