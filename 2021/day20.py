from bitarray import bitarray
from bitarray.util import ba2int


def line_to_bits(line):
    line = line.strip().replace('.','0').replace('#','1')
    result = bitarray(line)
    return result

def load(filename):
    with open(filename) as infile:
        lines = infile.readlines()


    enhancer = line_to_bits(lines[0])
    image = []
    for line in lines[1:]:
        if len(line.strip()) == 0:
            continue
        image.append(line_to_bits(line))

    lengths = [len(r) for r in image]
    assert min(lengths) == max(lengths)

    return enhancer, image

def crop(image, cropping):

    new_image = []
    for row in image[cropping:-cropping]:
        new_image.append(row[cropping:-cropping])

    return new_image


def pad(image, padding):

    rowlen = len(image[0])+2*padding
    new_image = []
    for i in range(padding):
        new_image.append(bitarray('0'*rowlen))
    for row in image:
        new_row = bitarray('0'*padding)
        new_row.extend(row)
        new_row.extend(bitarray('0'*padding))
        new_image.append(new_row)
    for i in range(padding):
        new_image.append(bitarray('0'*rowlen))

    return new_image    


def image_size(image):
    return len(image), len(image[0])


def enhance(enhancer, image):
    # oldrowcount, oldcolcount = image_size(image)

    image = pad(image,1)
    rowcount, colcount = image_size(image)
    # assert oldrowcount+2 == rowcount
    # assert oldcolcount+2 == colcount

    new_image = []

    #iterate while skipping the outer ring -- we have padded the image to offset this
    for r in range(rowcount):
        if r == 0 or r >= (rowcount-1):
            continue
        new_row = bitarray()
        for c in range(colcount):
            if c == 0 or c >= (colcount-1):
                continue
            offset = image[r-1][c-1:c+2] + image[r][c-1:c+2] + image[r+1][c-1:c+2]
            assert len(offset) == 9
            offset = ba2int(offset)
            new_row.append(enhancer[offset])
        #done with row
        new_image.append(new_row)

    #restore the lost ring and add one more because the enhancement makes the image bigger
    # new_image = pad(new_image,3)

    print("new image size: ", image_size(new_image))

    return new_image

def print_image(image):
    print("")
    print("")
    for row in image:
        print(row.to01().replace('0','.').replace('1','#'))
    print("")
    print("")

def pixel_count(image):
    count = 0
    for row in image:
        count += row.count()
    return count
    

if __name__ == "__main__":
    # enhancer, image = load('day20_test.txt')
    enhancer, image = load('day20.txt')

    original_rowcount, original_colcount = image_size(image)

    print_image(image)

    #make the file big so we can avoid artifacting at the boundaries
    #artifacts are a result of the canvas not actually being infinite
    #and the 0 enhancement being a 1 while the 511 enhangement is a 0
    #this makes the infinite grid "flash"
    # a better simulation would be to model the counts at the edges to account
    # for the infinite grid state alternating.  But this works okay
    image = pad(image,200)

    for i in range(50):
        print("Iteration", i+1)
        # print_image(image)
        image = enhance(enhancer, image)

    print_image(image)

    # crop in so we don't count the artifacting at the boundary
    image = crop(image, 50)

    print_image(image)

    print("# of pixels lit: ", pixel_count(image))

# Part 1
# # of pixels lit:  5081

# Part 2
# # of pixels lit:  15088