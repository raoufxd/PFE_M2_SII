from __future__ import print_function

from collections import defaultdict

import cubes
from cubes import Workspace, Cell, PointCut


class TweetCube:

    def __init__(self):
        self.createCube()

    def createCube(self):
        self.workspace = Workspace()
        self.workspace.register_default_store("sql",
                                         url="mysql://root:@localhost/tweetsdatawarehouse")

        model = cubes.read_model_metadata_bundle("../CubeModelisation/model/")

        self.workspace.import_model(model)
        self.browserTweet = self.workspace.browser("tweet")


    def getPieChartSource(self):
        cube = self.workspace.cube("tweet")
        cube.browser = self.browserTweet
        cell = Cell(cube)

        result = self.browserTweet.aggregate(cell, drilldown=["location","source"],aggregates=["numberOfTweets_sum"])

        output = []
        for row in result.table_rows("location"):
            #print(row.record)
            output.append(row.record)

        temp = defaultdict(lambda: defaultdict())
        for row in output:
            continent = row['location.continentName']
            source = row['source.sourceName']
            temp[continent][source] = row['numberOfTweets_sum']
        data = []
        for continent in temp:
            element = {'continentName': continent,
                       'iphoneNumber': temp[continent]['iPhone'],
                       'androidNumber': temp[continent]['Android'],
                       'webNumber': temp[continent]['Web'],
                       'otherSourceNumber': temp[continent]['Unknown']}
            data.append(element)
        #print(data)
        return data

    def getBarChartLanguage(self):
        cube = self.workspace.cube("tweet")
        cube.browser = self.browserTweet
        cell = Cell(cube)

        result = self.browserTweet.aggregate(cell, drilldown=["time:day", "language"],
                                             aggregates=["numberOfTweets_sum"])

        print("Record count : %8d" % result.summary["numberOfTweets_sum"])
        output = []
        for row in result.table_rows("time"):
            output.append(row.record)
            print(row.record)
        print(output)
        return output


    def getBarChartSentiment(self):
        cube = self.workspace.cube("tweet")
        cube.browser = self.browserTweet
        cell = Cell(cube)

        result = self.browserTweet.aggregate(cell, drilldown=["time:day","sentiment"], aggregates=["numberOfTweets_sum"])

        print("Record count : %8d" % result.summary["numberOfTweets_sum"])
        output = []
        for row in result.table_rows("time"):
            output.append(row.record)
            print(row.record)
        print(output)
        return output
