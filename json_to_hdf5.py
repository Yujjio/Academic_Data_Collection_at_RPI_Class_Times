import h5py
import json


def convert_to_hdf5(data, filename):
    with h5py.File(filename, "w") as f:
        def recursive_conversion(group, data):
            if isinstance(data, dict):
                for key, value in data.items():
                    if isinstance(value, dict):
                        new_group = group.create_group(key)
                        recursive_conversion(new_group, value)
                    else:
                        group.create_dataset(key, data=value)
            elif isinstance(data, list):
                group.create_dataset("data", data=data)

        recursive_conversion(f, data)


if __name__ == "__main__":
  f = open("data.json", "r")
  data = json.load(f)
  convert_to_hdf5(data, "output.h5")