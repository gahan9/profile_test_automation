# coding=utf-8
import re
import os
import logging
from datetime import datetime

# set logger
logger = logging.getLogger('csv_merger')
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s: %(message)s',
                    # datefmt='[%Y-%d-%m_%X]',
                    datefmt='%X',
                    filename='csv_merger.log',
                    filemode='w')
ch = logging.StreamHandler()  # create console handler with a higher log level
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)


def csv_merger(directory, headers=None, new_name="merge.csv"):
    logger.info("Merging CSV from directory: {}".format(directory))
    if not os.path.exists(directory):
        logger.info("Invalid directory.. Directory does not exist")
        return False
    csv_collection = [i for i in os.listdir(directory) if os.path.splitext(i)[-1] == ".csv"]
    if not csv_collection:
        logger.info("No csv file in given location: {}".format(directory))
        return False

    new_name = new_name if headers else '{}.csv'.format(datetime.now().strftime('%Y-%d-%m_%H.%M.%S'))
    target_dir = os.path.join(directory, "merged")
    os.makedirs(target_dir, exist_ok=True)
    new_csv = os.path.join(target_dir, new_name)
    merge_csv = open(new_csv, "w", encoding="utf-8")
    count = 0
    for file_name in csv_collection:
        count += 1
        file = os.path.join(directory, file_name)
        logger.debug("processing file: {}\nlocated at: {}".format(file_name, file))
        f = open(file, encoding="utf-8")
        head_line = f.__next__()
        if count == 1:
            merge_csv.write(head_line)
            headers = head_line if not headers else headers
        if head_line == headers:
            for line in f:
                merge_csv.write("{}\n".format(line.replace("\n", "")))
        else:
            logger.info("headers not matched for file: {}".format(file))
        f.close()
    merge_csv.close()
    csv_fixer(new_csv)
    logger.info("Merged CSV stored at: {}".format(new_csv))


def csv_fixer(file_location):
    with open(file_location, encoding="utf-8") as fr:
        orig_content = fr.read()
        content = re.sub(r"[\n]{1,101}((?![A-Z]).*,)", r' \1', orig_content)
    print(len(orig_content), len(content))
    print(len(orig_content) - len(content))
    with open(file_location, 'w', encoding="utf-8") as fw:
        fw.write(content)


if __name__ == "__main__":
    # CSV_HEADER = ["DistrictName", "Sr.No", "TalukaName", "VillageName", "School Name", "Type of School", "No of standards", "No of Rooms", "Existing rooms", "Necessity of rooms", "Teachers", "No of Boys", "No of Girls", "No of students", "mid day meal centre", "Pure Drinking water Facility", "Toilet facility", "Electrification", "Separate Toilet facility for girls", "Compound wall", "Timeline"]
    CSV_HEADER = "DistrictName,Sr.No,TalukaName,VillageName,School Name,Type of School,No of standards,No of Rooms,Existing rooms,Necessity of rooms,Teachers,No of Boys,No of Girls,No of students,mid day meal centre,Pure Drinking water Facility,Toilet facility,Electrification,Separate Toilet facility for girls,Compound wall,Timeline"
    # CSV_DIR = r"C:\Users\swati\Desktop\Desktop\csv_merger"
    csv_merger(input("Enter Directory location: "))
