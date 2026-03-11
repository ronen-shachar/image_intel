from map_view import *
from extractor import extract_all
from analyzer import *

if __name__ == "__main__":
    a= extract_all("C:/PythonProjects/FinalProject/image_intel/images/ready")
    b=sort_by_time(a)
    #c=create_map(b)
    print(total_analyzer(a))




