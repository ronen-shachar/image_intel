from src.extractor import extract_all
import os

def test(path):

    print(f"DEBUG: Checking path: {os.path.abspath(path)}")
    if os.path.exists(path):
        print(f"DEBUG: Files found in folder: {os.listdir(path)}")
    else:
        print("DEBUG: PATH DOES NOT EXIST!")
    return extract_all(path)



if __name__ == "__main__":
    a = test("/Users/shilovaksler/Desktop/image_intel/images/sample_data")
    print(a)
    for d in a:
        print(d)