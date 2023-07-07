from enum import Enum
from enum import IntEnum,unique

class PEOPLE(Enum):
    YELLOW_RACE = '黄种人'
    WHITE_PERSON = '白种人'
    BLACK_RACE = '黑种人'
    DEFULT = 0
    
    
def forEnum():
    for item in PEOPLE:
        print(item.name, ' : ' , item.value)

if __name__ == '__main__':
    forEnum()