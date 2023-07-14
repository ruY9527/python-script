from rembg import remove

input_path = '/home/luohong/Pictures/2154676643.jpg'
output_path = '/home/luohong/Pictures/1.jpg'

# 来源: https://github.com/danielgatis/rembg
def removeBgroudBack():
    with open(input_path,'rb') as i:
        with open(output_path,'wb') as o:
            input = i.read()
            output = remove(input)
            o.write(output)    

if __name__ == '__main__':
    removeBgroudBack()