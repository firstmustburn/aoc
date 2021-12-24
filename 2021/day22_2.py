
# Strategy
#  - need a way to do SET operations on the regions
#  -  UNION the running state with each ON
#  -  SUBTRACT each OFF from the running state
#
# 3d region sets - CSG?  and measure the volume of the resulting solid?
#
# 3d region sets - the hard way
#  - when two regions intersect, break them up into smaller regions
#    - intersection types (see how many points of one region are in the other region)
#      - no points contained - no intersection, no split
#      - one point contained - split each region along the planes of the point of the other region inside it - both regions will have one point inside them
#      - 2 points contained 
#          - split the region along all the planes at the two points.  
#          - the other region will have no points, but use the planes that form the edge that intersects to split the other region
#      - 4 points contained 
#          - split the region along all the planes at the 4 points  
#          - the other region will have no points, but use the plane that intersects to split the other region into 2
#      - 8 points contained - one is completely contained in the other
#           - split the outer region along all the planes of the inner region (making 9 regions)
#           - do not split the inner region
#    - special cases - shared corner, shared edge, shared face -- see if any of these exist in the dataset 
#  - after breaking up, eliminate duplicates for unions, and remove the identical regions for subtracts
#  
# algo:
# start with first region, progressively UNION and SUBTRACT, keeping the final region (a collection of non-overlapping prisms) as the running state
# to count the number of cubes on, just use HxLxW for all the regions in the final set 

def debug(*args):
    # pass
    print(*args)

def pair_range(pair):
    return range(pair[0], pair[1]+1)

def pairwise(values):
    return zip(values[:-1],values[1:])

X_INDEX=0
Y_INDEX=1
Z_INDEX=2
ON_STR='on'
OFF_STR='off'
ORIENTATION_STR = {
    X_INDEX:"x",
    Y_INDEX:"y",
    Z_INDEX:"z",
}


class Region:

    def __init__(self, xrange, yrange, zrange, ancestors=None):
        self._xrange = xrange
        self._yrange = yrange
        self._zrange = zrange
        if ancestors is None:
            ancestors = []
        self._ancestors = ancestors
        self._planes = None

    def copy(self):
        return Region(
            self._xrange,self._yrange,self._zrange,list(self._ancestors),
        )

    def get_range(self, range_ind):
        if range_ind == X_INDEX:
            return self._xrange
        elif range_ind == Y_INDEX:
            return self._yrange
        elif range_ind == Z_INDEX:
            return self._zrange
        else:
            raise IndexError(range_ind)

    def xrange(self):
        return self._xrange

    def yrange(self):
        return self._yrange

    def zrange(self):
        return self._zrange

    def xmin(self):
        return self._xrange[0]

    def xmax(self):
        return self._xrange[1]

    def ymin(self):
        return self._yrange[0]

    def ymax(self):
        return self._yrange[1]

    def zmin(self):
        return self._zrange[0]

    def zmax(self):
        return self._zrange[1]

    def xlen(self):
        return abs(self._xrange[1]-self._xrange[0])+1

    def ylen(self):
        return abs(self._yrange[1]-self._yrange[0])+1

    def zlen(self):
        return abs(self._zrange[1]-self._zrange[0])+1

    def get_planes(self):
        if self._planes is not None:
            return self._planes
        # create a plane for each face of the cube -- 
        # e.g. for the lower face, the plane is the x,y dimension of the region, and the z is the
        # [zmin-1, zmin].  The boundary between [zmin-1, zmin] is the cutting face that would
        # separate a region along the face of the cube.
        self._planes = []
        #X min plane
        self._planes.append(Plane(
            X_INDEX,
            (self.xmin()-1,self.xmin()),
            self._yrange,
            self._zrange,
            ancestors=[self],
        ))
        #X max plane
        self._planes.append(Plane(
            X_INDEX,
            (self.xmax(),self.xmax()+1),
            self._yrange,
            self._zrange,
            ancestors=[self],
        ))
        #y min plane
        self._planes.append(Plane(
            Y_INDEX,
            self._xrange,
            (self.ymin()-1,self.ymin()),
            self._zrange,
            ancestors=[self],
        ))
        #y max plane
        self._planes.append(Plane(
            Y_INDEX,
            self._xrange,
            (self.ymax(),self.ymax()+1),
            self._zrange,
            ancestors=[self],
        ))
        #Z min plane
        self._planes.append(Plane(
            Z_INDEX,
            self._xrange,
            self._yrange,
            (self.zmin()-1,self.zmin()),
            ancestors=[self],
        ))
        #Z max plane
        self._planes.append(Plane(
            Z_INDEX,
            self._xrange,
            self._yrange,
            (self.zmax(),self.zmax()+1),
            ancestors=[self],
        ))
        return self._planes

    def contains(self, point):
        return (point[0] >= self.xmin() and point[0] <= self.xmax()
            and point[1] >= self.ymin() and point[1] <= self.ymax()
            and point[2] >= self.zmin() and point[2] <= self.zmax())

    def _other_points_contained(self, other):
        #return true IFF the any vertex of other is in self
        for xi in other.xrange():
            for yi in other.yrange():
                for zi in other.zrange():
                    if self.contains((xi,yi,zi)):
                        return True
        return False

    def _region_region_intersects(self, other):
        return self._other_points_contained(other) or other._other_points_contained(self)

    def _region_plane_intersects(self_region, other_plane):
        #definitely not an intersection if the regions don't overlap
        if not self_region._region_region_intersects(other_plane):
            return False
        #if we are here, the regions overlap, but we need to check for planes coincident with faces
        if other_plane.orientation == X_INDEX:
            # coincident because the region min is the plane max (which means the other side of the
            # plane boundary is outside the region)
            if self_region.xmin() == other_plane.xmax():
                return False
            # coincident because the region max is the plane min (which means the other side of the
            # plane boundary is outside the region)
            if self_region.xmax() == other_plane.xmin():
                return False
        elif other_plane.orientation == Y_INDEX:
            #analogous to X
            if self_region.ymin() == other_plane.ymax():
                return False
            if self_region.ymax() == other_plane.ymin():
                return False
        elif other_plane.orientation == Z_INDEX:
            #analogous to X
            if self_region.zmin() == other_plane.zmax():
                return False
            if self_region.zmax() == other_plane.zmin():
                return False
        #else not coincident
        return True

    def intersects(self, other):
        if type(self) is Region and type(other) is Region:
            #intersect IFF any vertex of self is in other or any vertex of other is in self
            return self._region_region_intersects(other)
        elif type(self) is Region and type(other) is Plane:
            #intersect IFF any vertex of self is in other or any vertex of other is in self
            return self._region_plane_intersects(other)
        elif type(self) is Plane and type(other) is Region:
            #intersect IFF any vertex of self is in other or any vertex of other is in self
            return other._region_plane_intersects(self)
        else:
            raise NotImplemented(f"intersects for {self}, {other}")

    def divide_with_planes(self, planes):
        #start with a copy of ourself
        new_regions = [self.copy()]
        new_ancestors = self._ancestors + [self]

        def divide_with_plane(region_list, plane):
            new_regions_from_plane = []
            for reg in region_list: #iterate a copy since we are modifying in the loop
                if not plane.intersects(reg):
                    #keep the non-intersecting region in the output
                    new_regions_from_plane.append(reg)
                    continue
                # return two regions that are split at the boundary defined by the plane.  The original
                # region is unchanged
                if plane.orientation == X_INDEX:
                    # divide along X -- from the reg.xmin -> plane.xmin and plane.xmax -> reg.xmax
                    debug(f"X split {reg} at {plane.xrange()}")
                    new_xrange = (reg.xmin(),plane.xmin())
                    r1 = Region(new_xrange, reg.yrange(), reg.zrange(), new_ancestors)
                    new_xrange = (plane.xmax(),reg.xmax())
                    r2 = Region(new_xrange, reg.yrange(), reg.zrange(), new_ancestors)
                    debug(f"   into {r1} and {r2}")
                    new_regions_from_plane.append(r1)
                    new_regions_from_plane.append(r2)
                elif plane.orientation == Y_INDEX:
                    #analogous to x
                    debug(f"Y split {reg} at {plane.yrange()}")
                    new_yrange = (reg.ymin(),plane.ymin())
                    r1 = Region(reg.xrange(), new_yrange, reg.zrange(), new_ancestors)
                    new_yrange = (plane.ymax(),reg.ymax())
                    r2 = Region(reg.xrange(), new_yrange, reg.zrange(), new_ancestors)
                    debug(f"   into {r1} and {r2}")
                    new_regions_from_plane.append(r1)
                    new_regions_from_plane.append(r2)
                elif plane.orientation == Z_INDEX:
                    #analogous to x
                    debug(f"Z split {reg} at {plane.zrange()}")
                    new_zrange = (reg.zmin(),plane.zmin())
                    r1 = Region(reg.xrange(), reg.yrange(), new_zrange, new_ancestors)
                    new_zrange = (plane.zmax(),reg.zmax())
                    r2 = Region(reg.xrange(), reg.yrange(), new_zrange, new_ancestors)
                    debug(f"   into {r1} and {r2}")
                    new_regions_from_plane.append(r1)
                    new_regions_from_plane.append(r2)
            return new_regions_from_plane

        # starting with the initial region, divide by each plane
        # for each plane division, try to divide all the subregions 
        for plane in planes:
            new_regions = divide_with_plane(new_regions, plane)
        #sanity checks
        # intersect_fail = False
        # for r1, r2 in pairwise(new_regions):
        #     if r1.intersects(r2):
        #         debug("Unexpected intersection after dividing: ", r1, r2)
        #         intersect_fail = True
        # assert not intersect_fail
        return new_regions

    def __eq__(self, other):
        return self._xrange == other._xrange and self._yrange == other._yrange and self._zrange == other._zrange

    def __str__(self):
        return f"R(x={self._xrange}, y={self._yrange}, z={self._zrange})"

    def __repr__(self):
        return self.__str__()

class Plane(Region):

    def __init__(self, orientation, xrange, yrange, zrange, ancestors=None):
        super().__init__(xrange,yrange,zrange,ancestors)
        #in the orientation direction, the range needs to be length 1
        if orientation == X_INDEX:
            assert abs(xrange[0]-xrange[1])==1
        elif orientation == Y_INDEX:
            assert abs(yrange[0]-yrange[1])==1
        elif orientation == Z_INDEX:
            assert abs(zrange[0]-zrange[1])==1
        else:
            raise ValueError(f"unsupported orientation {orientation}")
        self.orientation = orientation

    def get_planes(self):
        return RuntimeError("not allowed for Plane")

    def __str__(self):
        return f"P(o={ORIENTATION_STR[self.orientation]}, x={self._xrange}, y={self._yrange}, z={self._zrange})"



def alignment_round(left_list_in, right_list_in):
    new_left = []
    new_right = []
    changed = False
    for right_reg in right_list_in:
        for left_reg in left_list_in:
            if left_reg.intersects(right_reg) and left_reg != right_reg:
                debug("Dividing intersecting regions:", left_reg, right_reg)
                #divide the intersecting regions and insert them back into the master list replacing the original regions
                new_left.extend(left_reg.divide_with_planes(right_reg.get_planes()))
                new_right.extend(right_reg.divide_with_planes(left_reg.get_planes()))
                changed = True
            else:
                debug("Keeping non-intersecting regions:", left_reg, right_reg)
                #no intersection, so just add them on
                new_left.append(left_reg)
                new_right.append(right_reg)
    return changed, new_right, new_left


def align_region_lists(left_list, right_list):
    while 1:
        has_changed, left_list, right_list = alignment_round(left_list, right_list)
        print(has_changed, left_list, right_list)
        if not has_changed:
            break


    sanity_check = True
    for right_reg in right_list:
        for left_reg in left_list:
            if left_reg.intersects(right_reg):
                print("alignment failure:  still intersects ", right_reg, left_reg)
                sanity_check = False
    assert sanity_check

    return left_list, right_list

    # regions_changed = False
    # def do_one_alignment():
    #     print("Aligning ",len(left_list), "/", len(right_list))
    #     for left_index, left_reg in enumerate(left_list):
    #         for right_index, right_reg in enumerate(right_list):
    #             if left_reg.intersects(right_reg) and left_reg != right_reg:
    #                 debug("Dividing intersecting regions:", left_reg, right_reg)
    #                 #divide the intersecting regions and insert them back into the master list replacing the original regions
    #                 left_list[left_index:left_index+1] = left_reg.divide_with_planes(right_reg.get_planes())
    #                 right_list[right_index:right_index+1] = right_reg.divide_with_planes(left_reg.get_planes())
    #                 debug("       ",left_list)
    #                 debug("       ",right_list)
    #                 return True
    #     #no alignments
    #     return False

    # while do_one_alignment():
    #     pass
                     
    # return regions_changed

def region_list_union(left_list, right_list):
    if left_list == right_list:
        debug("Union equal regions:", left_list, right_list)
        return left_list
    debug("union:")
    debug("   ",left_list)
    debug("   ",right_list)

    print("aligning")
    left_list, right_list = align_region_lists(left_list, right_list)

    print("combining")
    combined_regions = []
    for region in left_list + right_list:
        if region not in combined_regions:
            combined_regions.append(region)
    assert len(combined_regions) <= len(left_list) + len(right_list)

    debug("   -->", combined_regions)
    debug("")
    return combined_regions

def region_list_difference(left_list, right_list):
    if left_list == right_list:
        debug("Difference equal regions:", left_list, right_list)
        return []

    debug("difference:")
    debug("   ",left_list)
    debug("   ",right_list)

    print("aligning")
    left_list, right_list = align_region_lists(left_list, right_list)

    print("differencing")
    remaining_regions = []
    for region in left_list:
        if region not in right_list:
            remaining_regions.append(region)
    assert len(remaining_regions) <= len(left_list)

    debug("   -->", remaining_regions)
    debug("")
    return remaining_regions



class Instruction:
    @classmethod
    def parse(cls, line):
        def parse_range(range_part, expected_name):
            name, numpart = range_part.split('=')
            assert name == expected_name
            numpart = tuple([ int(r) for r in numpart.split('..') ])
            assert len(numpart) == 2
            assert numpart[0] <= numpart[1]
            return numpart

        tokens = line.strip().split(' ')
        assert len(tokens)==2
        command = tokens[0]
        assert command in [ON_STR, OFF_STR]
        ranges = tokens[1].split(',')
        assert len(ranges) == 3
        x_range = parse_range(ranges[0], 'x')
        y_range = parse_range(ranges[1], 'y')
        z_range = parse_range(ranges[2], 'z')

        return Instruction(command, x_range, y_range, z_range)

    def __init__(self, command, x_range, y_range, z_range):
        self.command = command
        self.region = Region(x_range, y_range, z_range)

    def get_region(self):
        return self.region

    def __str__(self):
        return f"Instruction(cmd={self.command}, {self.region})"

    def __repr__(self):
        return self.__str__()


class InstructionSet:

    @classmethod
    def parse(self, lines):
        instructions = [ Instruction.parse(line) for line in lines]
        return InstructionSet(instructions)

    def __init__(self, instructions):
        self.instructions = instructions

    def process_regions(self):
        """Output a list of region objects representing the regions of space that are ON with the
        regions of space that are OFF removed in the sequence of the instruction set"""
        
        running_region = [self.instructions[0].get_region().copy()]
        for instruction in self.instructions[1:]:
            print("processing", instruction)
            if instruction.command == ON_STR:
                running_region = region_list_union(running_region, [instruction.get_region().copy()])
            elif instruction.command == OFF_STR:
                running_region = region_list_difference(running_region, [instruction.get_region().copy()])
            else:
                raise ValueError(f"Unhandled instruction command {instruction.command}")
            print("len of running region", len(running_region))

        self.regions = running_region
    
    def count_on_squares(self):
        total_on = 0
        debug("Counting squares")
        for region in self.regions:
            debug(f"Region {region}: {region.xlen()} x {region.ylen()} x {region.zlen()} = {(region.xlen() * region.ylen() * region.zlen())}")

            total_on += (region.xlen() * region.ylen() * region.zlen())

        return total_on




if __name__ == "__main__":
    
    with open('day22.txt') as infile:
        data = infile.read()

    iset = InstructionSet.parse(data.strip().split('\n'))
    iset.process_regions()
    print("Count in init region:", iset.count_on_squares())













