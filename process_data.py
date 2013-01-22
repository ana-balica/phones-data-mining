import json

class JsonFile():

    def __init__(self):
        self.file = 'items.json'
        self.data = ''

    def loadJson(self):
        contents = open(self.file, 'r').read()
        self.data = json.loads(contents)


class Smoothing():
    '''
    Performs smoothing by bin medians of the views
    '''

    def __init__(self):
        json_object = JsonFile()
        json_object.loadJson()
        self.data = json_object.data
        self.views = []
        self.means = []

    def smooth_views_data(self):

        for item in self.data:
            self.views.append(item['views'])

        self.views.sort()
        # split into chunks of 100
        chunks = []
        for i in xrange(0, len(self.views), 100):
            chunks.append(self.views[i:i+100])

        # compute the mean values
        for views_chunk in chunks:
            mean = reduce(lambda x, y: x + y, views_chunk) / len(views_chunk)
            self.means.append(mean)


class Clusterring():
    '''
    Performs the region clustering.
    Since we have little data, we are going to cluster regions
    by Chisinau and all other places
    '''
    def __init__(self):
        json_object = JsonFile()
        json_object.loadJson()
        self.data = json_object.data

        self.chisinau = 0
        self.others = 0

        self.orange = 0
        self.moldcell = 0
        self.other_providers = 0

    def cluster_regions(self):

        for item in self.data:
            if item['region'] == u"Chi\u015fin\u0103u mun.":
                self.chisinau += 1
            else:
                self.others += 1

    def cluster_telecommunication_providers(self):

        for item in self.data:
            if item['contacts'].startswith('3737'):
                self.moldcell += 1
            elif item['contacts'].startswith('3736'):
                self.orange += 1
            else:
                self.other_providers += 1


if __name__ == '__main__':

    smooth_object = Smoothing()
    smooth_object.smooth_views_data()
    print 'The mean views\n'
    print smooth_object.means

    cluster_object = Clusterring()
    cluster_object.cluster_regions()
    print 'Nr of adds in Chisinau - %s' % str(cluster_object.chisinau)
    print 'Nr of adds from other places - %s' % str(cluster_object.others)

    cluster_object.cluster_telecommunication_providers()
    print 'Orange\t\t%s' % str(cluster_object.orange)
    print 'Moldcell\t%s' % str(cluster_object.moldcell)
    print 'Other providers\t%s' % str(cluster_object.other_providers)