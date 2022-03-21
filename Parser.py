

import node

#because we know what to expect we are going to split each string into separate objects
# and then we can load them into objects after that
# but we won't load them as objects here this method is just for parser helper functions
def splitJson(jsonString):
    parsedList = jsonString.split(node.DELIMITER)
    return parsedList

