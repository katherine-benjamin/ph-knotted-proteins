# segs is a list of 1-simplices making up the chain
# we'd like to transform that into a list of successive 0-simplices
# so e.g. if segs is [[415,416], [253,252], [252,416], [253,415]]
# Then convert will output:
#     [415, 416, 252, 253, 415],
#     [[416, 252], [253, 415]]
def convert(segs):
    # rep will build up as a list of 0-simplices. we initialise it with just
    # the first segment
    rep = list(segs[0])
    x, y = rep
    # initialise list of bridges, possibly with the initial segment
    bridges = [rep] if y != x+1 and x != y+1 else []
    # we continue to build up rep until we've recovered everything
    while len(rep) < len(segs):
        i = 0
        # find the first segment which coincides with the last 0-simplex,
        # but isn't the segment we just added
        while rep[-1] not in segs[i] or rep[-2] in segs[i]:
            i += 1
        x, y = segs[i]
        # figure out which end of the segment we should add
        if rep[-1] == x:
            rep.append(y)
        else:
            rep.append(x)
        # update bridges
        if y != x+1 and x != y+1:
            bridges.append([x,y])
    # add the first 0-simplex back to complete the loop
    rep.append(rep[0])
    # check for one last bridge
    x, y = rep[-2], rep[-1]
    if y != x+1 and x != y+1:
        bridges.append([x,y])
    return rep, bridges