class Directions(object):
    '''
        Simple enumeration of the available directions
    '''
    Start, Forward, Back, Left, Right, End = range(1, 7)


class CameraMovement(object):
    '''
        Enumeration of camera directions
    '''
    Up, Down, Idle = [1, -1, 0]


class Throttle(object):
    '''
        Simple enumerations of the directions signs: up or down
    '''
    Up, Down = (1, -1)
